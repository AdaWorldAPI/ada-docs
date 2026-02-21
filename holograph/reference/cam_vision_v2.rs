use std::f64::consts::PI;
use std::time::Instant;

const WORD_BITS: usize = 8192;
const WORD_LANES: usize = 128;
const NUM_ORI: usize = 8;
const PGRID: usize = 8;
const MAX_PATCHES: usize = PGRID * PGRID;

#[derive(Clone)]
#[repr(C, align(64))]
struct Word { lanes: [u64; WORD_LANES] }

impl Word {
    #[inline(always)] fn zero() -> Self { Word { lanes: [0u64; WORD_LANES] } }

    fn random(seed: u64) -> Self {
        let mut w = Self::zero();
        let mut s = seed;
        for i in 0..WORD_LANES { s ^= s << 13; s ^= s >> 7; s ^= s << 17; w.lanes[i] = s; }
        w
    }

    #[inline(always)]
    fn bind(a: &Word, b: &Word) -> Word {
        let mut o = Self::zero();
        for i in 0..WORD_LANES { o.lanes[i] = a.lanes[i] ^ b.lanes[i]; }
        o
    }

    #[inline(always)]
    fn distance(a: &Word, b: &Word) -> u32 {
        let mut d = 0u32;
        for i in 0..WORD_LANES { d += (a.lanes[i] ^ b.lanes[i]).count_ones(); }
        d
    }

    #[inline(always)]
    fn similarity(a: &Word, b: &Word) -> f64 {
        1.0 - (Self::distance(a, b) as f64 / WORD_BITS as f64)
    }

    /// BUNDLE: bit-parallel ripple-carry majority vote.
    ///
    /// For N input words, maintains ceil(log2(N+1)) counter lanes.
    /// Each counter[k][lane] holds the k-th bit of the per-position count.
    /// Adding a word = ripple-carry add of its bits into the counter.
    /// Final: parallel subtraction of threshold, check borrow.
    ///
    /// O(128 × N × log2(N)) u64 ops, zero branching in hot path.
    fn bundle(words: &[&Word]) -> Word {
        let n = words.len();
        if n == 0 { return Self::zero(); }
        if n == 1 { return words[0].clone(); }

        let threshold = (n / 2) + 1; // count > n/2  ⟺  count >= n/2 + 1
        let nbits = (64 - (n as u64).leading_zeros()) as usize;

        // counter[k] = array of WORD_LANES u64s, k-th bit of per-position count
        let mut counter: Vec<[u64; WORD_LANES]> = vec![[0u64; WORD_LANES]; nbits];

        // Accumulate: ripple-carry add each word
        for w in words {
            for lane in 0..WORD_LANES {
                let mut carry = w.lanes[lane];
                for k in 0..nbits {
                    let new_carry = counter[k][lane] & carry;
                    counter[k][lane] ^= carry;
                    carry = new_carry;
                    if carry == 0 { break; }
                }
            }
        }

        // Threshold: count >= threshold via parallel subtraction
        // Subtract threshold from each bit-position's count.
        // If no borrow → count >= threshold → set output bit.
        let mut out = Self::zero();
        let tv = threshold as u64;

        for lane in 0..WORD_LANES {
            let mut borrow = 0u64;
            for k in 0..nbits {
                let tbit = if (tv >> k) & 1 == 1 { !0u64 } else { 0u64 };
                let nb = (!counter[k][lane] & tbit)
                       | (!counter[k][lane] & borrow)
                       | (tbit & borrow);
                borrow = nb;
            }
            out.lanes[lane] = !borrow;
        }
        out
    }

    /// Naive bundle for correctness testing
    fn bundle_naive(words: &[&Word]) -> Word {
        let n = words.len();
        if n == 0 { return Self::zero(); }
        let threshold = n / 2;
        let mut out = Self::zero();
        for bit in 0..WORD_BITS {
            let lane = bit / 64;
            let pos = bit % 64;
            let mut count = 0usize;
            for w in words { if (w.lanes[lane] >> pos) & 1 == 1 { count += 1; } }
            if count > threshold { out.lanes[lane] |= 1u64 << pos; }
        }
        out
    }

    #[inline(always)]
    fn permute(w: &Word, k: usize) -> Word {
        if k == 0 { return w.clone(); }
        let s = k % WORD_LANES;
        let mut o = Self::zero();
        for i in 0..WORD_LANES { o.lanes[(i + s) % WORD_LANES] = w.lanes[i]; }
        o
    }

    fn popcount(&self) -> u32 { self.lanes.iter().map(|l| l.count_ones()).sum() }
}

impl std::fmt::Debug for Word {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "Word(pop={} d={:.3})", self.popcount(), self.popcount() as f64 / WORD_BITS as f64)
    }
}

// ── Codebook ───────────────────────────────────────────────────────────────

struct Codebook {
    ori: [Word; NUM_ORI],
    pos: [Word; MAX_PATCHES],
}
impl Codebook {
    fn new() -> Self {
        Codebook {
            ori: std::array::from_fn(|i| Word::random(0xED6E_0000 + i as u64)),
            pos: std::array::from_fn(|i| Word::random(0xB050_0000 + i as u64)),
        }
    }
}

// ── Image + Sobel ──────────────────────────────────────────────────────────

struct Img { w: usize, h: usize, px: Vec<f64> }
impl Img {
    fn new(w: usize, h: usize) -> Self { Img { w, h, px: vec![0.0; w*h] } }
    #[inline] fn get(&self, x: usize, y: usize) -> f64 {
        if x < self.w && y < self.h { self.px[y*self.w+x] } else { 0.0 }
    }
    #[inline] fn set(&mut self, x: usize, y: usize, v: f64) {
        if x < self.w && y < self.h { self.px[y*self.w+x] = v; }
    }
    fn from_bmp(bmp: [u8; 8], sz: usize) -> Self {
        let mut img = Self::new(sz, sz);
        let sc = sz / 8;
        for cy in 0..8 { for cx in 0..8 {
            if bmp[cy] & (1 << (7-cx)) != 0 {
                for dy in 0..sc { for dx in 0..sc { img.set(cx*sc+dx, cy*sc+dy, 1.0); }}
            }
        }}
        img
    }
    fn x(s: usize) -> Self {
        let mut img = Self::new(s, s);
        for i in 0..s {
            let t = i as f64 / s as f64;
            let a = (t * s as f64) as usize;
            let b = ((1.0-t) * s as f64) as usize;
            img.set(a.min(s-1), i, 1.0); img.set(b.min(s-1), i, 1.0);
            if a+1<s { img.set(a+1, i, 0.7); }
            if b>0 { img.set(b-1, i, 0.7); }
        }
        img
    }
    fn t(s: usize) -> Self {
        let mut img = Self::new(s, s);
        for x in 0..s { img.set(x, s/4, 1.0); }
        for y in s/4..s { img.set(s/2, y, 1.0); }
        img
    }
    fn l(s: usize) -> Self {
        let mut img = Self::new(s, s);
        for y in 0..s { img.set(s/4, y, 1.0); }
        for x in s/4..s { img.set(x, s*3/4, 1.0); }
        img
    }
    fn o(s: usize) -> Self {
        let mut img = Self::new(s, s);
        let c = s as f64/2.0; let r = s as f64*0.35;
        for y in 0..s { for x in 0..s {
            let d = ((x as f64-c).powi(2)+(y as f64-c).powi(2)).sqrt();
            if (d-r).abs() < 1.5 { img.set(x, y, 1.0-(d-r).abs()/1.5); }
        }}
        img
    }
    fn plus(s: usize) -> Self {
        let mut img = Self::new(s, s);
        for x in s/4..s*3/4 { img.set(x, s/2, 1.0); }
        for y in s/4..s*3/4 { img.set(s/2, y, 1.0); }
        img
    }
}

fn bmp(ch: char) -> [u8; 8] {
    match ch {
        'X'=>[0x82,0x44,0x28,0x10,0x10,0x28,0x44,0x82],
        'T'=>[0xFE,0xFE,0x10,0x10,0x10,0x10,0x10,0x10],
        'L'=>[0x80,0x80,0x80,0x80,0x80,0x80,0xFE,0xFE],
        'O'=>[0x38,0x44,0x82,0x82,0x82,0x82,0x44,0x38],
        '+'=>[0x10,0x10,0x10,0xFE,0xFE,0x10,0x10,0x10],
        'V'=>[0x82,0x82,0x44,0x44,0x28,0x28,0x10,0x10],
        'A'=>[0x10,0x28,0x44,0x82,0xFE,0x82,0x82,0x82],
        'H'=>[0x82,0x82,0x82,0xFE,0xFE,0x82,0x82,0x82],
        'Y'=>[0x82,0x44,0x28,0x10,0x10,0x10,0x10,0x10],
        _=>[0;8],
    }
}

fn sobel(img: &Img) -> (Vec<f64>, Vec<f64>, usize) { // (mag, ori, w)
    let (w, h) = (img.w, img.h);
    let mut mag = vec![0.0f64; w*h];
    let mut ori = vec![0.0f64; w*h];
    for y in 1..h-1 { for x in 1..w-1 {
        let gx = -img.get(x-1,y-1)-2.0*img.get(x-1,y)-img.get(x-1,y+1)
                 +img.get(x+1,y-1)+2.0*img.get(x+1,y)+img.get(x+1,y+1);
        let gy = -img.get(x-1,y-1)-2.0*img.get(x,y-1)-img.get(x+1,y-1)
                 +img.get(x-1,y+1)+2.0*img.get(x,y+1)+img.get(x+1,y+1);
        let i = y*w+x;
        mag[i] = (gx*gx+gy*gy).sqrt();
        let mut a = gy.atan2(gx); if a<0.0{a+=PI;} if a>=PI{a-=PI;}
        ori[i] = a;
    }}
    (mag, ori, w)
}

fn img_to_word(img: &Img, cb: &Codebook, th: f64) -> Word {
    let (mag, ori, ew) = sobel(img);
    let (ph, pw) = (img.h/PGRID, img.w/PGRID);
    let mut pws: Vec<Word> = Vec::new();
    for py in 0..PGRID { for px in 0..PGRID {
        let (y0, x0) = (py*ph, px*pw);
        let mut hist = [0.0f64; NUM_ORI];
        let mut tot = 0.0;
        for dy in 0..ph { for dx in 0..pw {
            let m = mag[(y0+dy)*ew+(x0+dx)];
            if m > th {
                let b = ((ori[(y0+dy)*ew+(x0+dx)]/PI*NUM_ORI as f64) as usize).min(NUM_ORI-1);
                hist[b] += m; tot += m;
            }
        }}
        if tot < th*2.0 { continue; }
        let mut bs: Vec<(usize,f64)> = hist.iter().copied().enumerate().collect();
        bs.sort_by(|a,b| b.1.partial_cmp(&a.1).unwrap());
        if bs[0].1 < th { continue; }
        let ep = Word::bind(&cb.ori[bs[0].0], &cb.ori[bs[1].0]);
        let pos = Word::permute(&cb.pos[py*PGRID+px], 1);
        pws.push(Word::bind(&ep, &pos));
    }}
    if pws.is_empty() { return Word::zero(); }
    let refs: Vec<&Word> = pws.iter().collect();
    Word::bundle(&refs)
}

// ── Benchmarks ─────────────────────────────────────────────────────────────

fn bench(label: &str, n_words: usize, iters: usize) {
    let ws: Vec<Word> = (0..n_words).map(|i| Word::random(i as u64+1)).collect();
    let refs: Vec<&Word> = ws.iter().collect();

    // correctness
    let a = Word::bundle(&refs);
    let b = Word::bundle_naive(&refs);
    let err = Word::distance(&a, &b);

    // warm
    for _ in 0..3 { let _ = Word::bundle(&refs); let _ = Word::bundle_naive(&refs); }

    let t0 = Instant::now();
    for _ in 0..iters { let _ = Word::bundle(&refs); }
    let opt = t0.elapsed();

    let t1 = Instant::now();
    for _ in 0..iters { let _ = Word::bundle_naive(&refs); }
    let naive = t1.elapsed();

    println!("  {:>5} {} words × {:>6}: opt {:>8.1}µs  naive {:>8.1}µs  {:.1}×  err={}",
        label, n_words, iters,
        opt.as_micros() as f64 / iters as f64,
        naive.as_micros() as f64 / iters as f64,
        naive.as_nanos() as f64 / opt.as_nanos().max(1) as f64,
        err);
}

fn main() {
    println!("╔══════════════════════════════════════════════════════════╗");
    println!("║  CAM-VISION v2: ripple-carry SIMD bundle                ║");
    println!("╚══════════════════════════════════════════════════════════╝\n");

    println!("═══ OP BENCHMARKS (1M calls) ═══\n");
    let a = Word::random(42); let b = Word::random(43);

    let t = Instant::now();
    for _ in 0..1_000_000 { let _ = Word::bind(&a, &b); }
    println!("  bind:     {:.0} ns/call", t.elapsed().as_nanos() as f64 / 1e6);

    let t = Instant::now();
    for _ in 0..1_000_000 { let _ = Word::distance(&a, &b); }
    println!("  distance: {:.0} ns/call", t.elapsed().as_nanos() as f64 / 1e6);

    let t = Instant::now();
    for _ in 0..1_000_000 { let _ = Word::permute(&a, 7); }
    println!("  permute:  {:.0} ns/call", t.elapsed().as_nanos() as f64 / 1e6);

    println!("\n═══ BUNDLE BENCHMARK: optimized vs naive ═══\n");
    bench("small",   5,    10_000);
    bench("med",    16,    10_000);
    bench("med+",   32,     1_000);
    bench("large",  64,     1_000);
    bench("xlarge",128,       100);
    bench("huge", 1024,        10);

    println!("\n═══ RECOGNITION ═══\n");
    let cb = Codebook::new();
    let (sz, th) = (64, 0.15);

    let lib: Vec<(&str, Word)> = vec![
        ("X", img_to_word(&Img::x(sz), &cb, th)),
        ("T", img_to_word(&Img::t(sz), &cb, th)),
        ("L", img_to_word(&Img::l(sz), &cb, th)),
        ("O", img_to_word(&Img::o(sz), &cb, th)),
        ("+", img_to_word(&Img::plus(sz), &cb, th)),
    ];

    let mut ok = 0; let mut tot = 0;
    for c in ['X','T','L','O','+','V','A','H','Y'] {
        let w = img_to_word(&Img::from_bmp(bmp(c), sz), &cb, th);
        let mut best = ("?", 0.0f64);
        let mut s = String::new();
        for (n, lw) in &lib {
            let sim = Word::similarity(&w, lw);
            if sim > best.1 { best = (n, sim); }
            s.push_str(&format!(" {}:{:.3}", n, sim));
        }
        let exp = &c.to_string();
        let hit = best.0 == exp;
        if hit { ok += 1; }
        tot += 1;
        println!("{} {}_bmp → {} ({:.4}) |{}", if hit{"✓"}else{"✗"}, c, best.0, best.1, s);
    }
    println!("\nAccuracy: {}/{} ({:.0}%)\n═══ DONE ═══", ok, tot, ok as f64/tot as f64*100.0);
}
