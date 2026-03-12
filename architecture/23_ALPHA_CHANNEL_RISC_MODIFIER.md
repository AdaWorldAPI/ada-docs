# 23_ALPHA_CHANNEL_RISC_MODIFIER.md

## The Alpha Channel: Structural Confidence for the RISC Brain

**Jan Hübener — Ada Architecture — March 2026**
**Extends**: 15_RISC_BRAIN_CONVERGENCE_VISION, hdr-popcnt-sweep (Belichtungsmesser)
**Grounded in**: Orangutan framework (Yong Xie, Alibaba, arXiv:2406.15488)
**Cross-repo**: ladybug-rs × lance-graph × holograph × ada-consciousness

---

## 0. The Problem

When you encode `Alice loves ???` — the unknown Object gets filled with hash noise
from `from_seed()` or `from_content("")`. That noise is INDISTINGUISHABLE from real
signal in Hamming distance. Every comparison pays for bits that mean nothing. The
system literally cannot tell "I know this" from "I made this up."

The pentary accumulator range -2..+2 has the same disease. Three states collapse
into the same representation:

```
Strong signal:  dimension got +3 from multiple agreeing sources → clean to +1
                HIGH CONFIDENCE. This bit is real.

Canceled signal: dimension got +1 and -1 from opposing sources → net 0
                 Forced to pick ±1 randomly. LOOKS LIKE SIGNAL BUT IS NOISE.

Undefined:      dimension was never written to → default value
                LOOKS IDENTICAL TO A CLEAN SIGNAL.
```

CAM retrieval fails because a fingerprint with many canceled dimensions sits at
~50% Hamming distance from everything. Not close enough to match, not far enough
to exclude. The dead zone between "this is something" and "this is noise."

---

## 1. The Neuroscience Grounding

The Orangutan framework (multiscale brain emulation, Alibaba 2024) solves an
identical problem in biological neural circuits. Three mechanisms translate directly:

### 1.1 Prediction Bias Circuit (Figure 5 in Orangutan)

When a prediction cell and an input cell have equal excitation, NEITHER the
positive nor negative prediction bias neuron fires. The brain doesn't see zero —
it explicitly represents ambiguity as a distinct state where both channels are
balanced and no decision is made.

**Translation**: Undefined dimensions are not zero. They are a third state that
should be excluded from comparison, not collapsed into a value.

### 1.2 All-or-None Critical State (the `all_or_none` attribute)

Orangutan's inhibitory synapses have three modes:
- `0` = analog (continuous inhibition)
- `1` = weak threshold (fire only when |E'| > |E|)
- `2` = strong threshold (fire when |E'| ≥ |E|)

The critical state where excitations are equal represents two independent states,
not a single zero. The system tracks WHICH kind of ambiguity it is.

**Translation**: `canceled` (evidence for both sides) ≠ `undefined` (no evidence).
Both are non-signal, but they carry different epistemic status.

### 1.3 Penalty Circuit (Figure 11b in Orangutan)

Every orientation cell is paired with an autaptic inhibitory neuron that CONSTANTLY
sends inhibition to the vector cell. The orientation cell cancels this inhibition
only when it's active. The missing signal is ACTIVELY PENALIZED, not passively
absent.

**Translation**: Undefined dimensions should not merely fail to contribute to
similarity — they should actively reduce the score. Absence of evidence is weak
evidence of absence at the substrate level.

---

## 2. The Alpha Channel

One extra bitvector per node. Same dimensionality as the data vector. Each bit:

```
alpha = 1  →  this dimension carries real signal (defined)
alpha = 0  →  this dimension is undefined (transparent, skip)
```

The vector carries its own confidence mask. No external metadata needed.

### 2.1 Storage Schema Update

```
LanceDB: spo_nodes

    merkle_root     Binary(6)       ← content address
    clam_path       Binary(3)       ← DN tree position
    vector          Binary(2048)    ← THE NODE. 16384 bits.
    alpha           Binary(2048)    ← CONFIDENCE MASK. 16384 bits. (NEW)
    nars_packed     Binary(8)       ← truth/confidence/evidence
    spine_hash      Binary(32)      ← Blake3 seal
    spine_dirty     u8              ← dirty flag
    pentary         Binary(512)     ← signed accumulators
```

Double the vector storage per node (2KB → 4KB). But computation is CHEAPER
because early exit skips undefined regions. Net: more bytes stored, fewer
cycles computed.

### 2.2 The Core Hamming Operation

```rust
// WITHOUT alpha (current, noisy):
fn hamming(a: &[u64], b: &[u64]) -> u32 {
    a.iter().zip(b).map(|(x, y)| (x ^ y).count_ones()).sum()
}

// WITH alpha (signal only):
fn hamming_alpha(
    a: &[u64], b: &[u64],
    a_alpha: &[u64], b_alpha: &[u64]
) -> f32 {
    let mut disagreements: u32 = 0;
    let mut shared_defined: u32 = 0;

    for i in 0..a.len() {
        let mask = a_alpha[i] & b_alpha[i];        // both must be defined
        disagreements += ((a[i] ^ b[i]) & mask).count_ones();
        shared_defined += mask.count_ones();
    }

    if shared_defined == 0 { return f32::NAN; }     // incomparable
    disagreements as f32 / shared_defined as f32     // normalized
}
```

One extra AND per cache line. One cycle. Eliminates ALL noise from undefined
dimensions. The NaN return for zero shared alpha is the substrate saying
"these vectors have nothing in common to compare."

---

## 3. Alpha Propagation Rules

**CRITICAL**: The alpha propagation for BIND was initially proposed as OR.
That is wrong. If Alice has alpha=1 at dimension k and ??? has alpha=0,
then `Alice XOR ??? = real_bit XOR noise_bit = noise`. Result is undefined.

### 3.1 Corrected Propagation

```
BIND (XOR):
    result_data  = a_data XOR b_data
    result_alpha = a_alpha AND b_alpha
    
    Both inputs must be defined for the binding to carry signal.
    Role vectors (from BLAKE3) are always fully defined (alpha = all-ones),
    so: S ⊕ ROLE_S → result_alpha = s_alpha AND 1...1 = s_alpha
    Role binding preserves entity alpha perfectly.

BUNDLE (MAJORITY):
    result_data  = MAJORITY(input_data, weighted by alpha)
    result_alpha = MAJORITY(input_alphas)
    
    Dimension is defined if enough voters were defined.
    3/5 inputs have alpha=1 at bit k → vote is meaningful → alpha=1
    1/5 inputs have alpha=1 at bit k → noise dominates → alpha=0

UNBIND (XOR):
    result_data  = bound_data XOR key_data
    result_alpha = bound_alpha AND key_alpha
    
    Same as BIND. Can only recover signal where both are defined.

AND/NOT (Factorization):
    result_data  = a_data AND (NOT b_data)
    result_alpha = a_alpha AND b_alpha
    
    Both must be defined for the factorization to mean anything.

BLAKE3 (Seal):
    input_data   = data AND alpha  (hash only defined bits)
    Hash changes when defined bits change. Undefined bits are invisible.
    A node with 50% alpha and one with 80% alpha produce different hashes
    even if their defined bits are identical — because BLAKE3 sees the
    alpha-masked input length.

THRESHOLD (Gating):
    Compare against alpha-normalized distance.
    ADDITIONAL GUARD: if shared_alpha < min_overlap → incomparable → skip
    Two early-exit conditions instead of one.

POPCOUNT (Distance):
    popcount_signal  = POPCOUNT(data AND alpha)       // defined set bits
    popcount_defined = POPCOUNT(alpha)                 // total defined
    popcount_noise   = POPCOUNT(data AND NOT alpha)    // noise (ignore)
    
    Normalized activation = popcount_signal / popcount_defined
```

### 3.2 The SPO Triple with Alpha

```
Full triple (all known):
    data  = (Alice ⊕ ROLE_S) ⊕ (loves ⊕ ROLE_P) ⊕ (Bob ⊕ ROLE_O)
    alpha = alice_α AND 1..1 AND loves_α AND 1..1 AND bob_α AND 1..1
          = alice_α AND loves_α AND bob_α
          = 1...1 (all entities fully known → full alpha)

Partial triple (unknown object):
    data  = (Alice ⊕ ROLE_S) ⊕ (loves ⊕ ROLE_P) ⊕ (??? ⊕ ROLE_O)
    alpha = 1..1 AND 1..1 AND 0..0
          = 0...0 (all alpha is zero → Belichtungsmesser reads zero → SKIP)
```

This means you DON'T STORE triples with unknowns as full SPO vectors.
The alpha channel enforces this structurally. Instead, you store the
partial projection:

```
SP_ projection:
    data  = (Alice ⊕ ROLE_S) ⊕ (loves ⊕ ROLE_P)
    alpha = 1...1 (fully defined — it only claims to encode S and P)
```

The 2^3 factorization produces 8 SEPARATE vectors, each with its own alpha,
stored independently. The `SP_` projection is a first-class citizen with full
alpha — it encodes less information, not uncertain information.

**Partial knowledge ≠ uncertain knowledge.**

- Partial: "I know Alice loves, haven't encoded who" → full alpha, less content
- Uncertain: "I think Alice loves Bob, not sure" → partial alpha, contested bits

---

## 4. Alpha-Aware Belichtungsmesser

The 7-point Belichtungsmesser reads exposure per chunk. Add alpha awareness:

```rust
fn belichtungsmesser_alpha(
    data: &[u64; 256],      // 16384 bits
    alpha: &[u64; 256],     // 16384 bits
) -> ExposureReading {
    // 7 sample points, evenly spaced across the vector
    let stride = 256 / 7;
    let mut exposures = [0u32; 7];
    let mut alpha_counts = [0u32; 7];

    for point in 0..7 {
        let idx = point * stride;
        exposures[point] = (data[idx] & alpha[idx]).count_ones();
        alpha_counts[point] = alpha[idx].count_ones();
    }

    // EARLY EXIT: if majority of sample points have alpha ≈ 0
    let defined_points = alpha_counts.iter().filter(|&&c| c > 8).count();
    if defined_points < 3 {
        return ExposureReading::Transparent;
        // "Not enough light to expose. Skip this frame."
        // Cost: 7 POPCNT + 7 AND = O(7) instead of O(16384)
    }

    // Normal exposure reading on defined bits only
    let total_signal: u32 = exposures.iter().sum();
    let total_defined: u32 = alpha_counts.iter().sum();
    let density = total_signal as f32 / total_defined as f32;

    ExposureReading::Exposed { density, defined_points }
}
```

### 4.1 HDR Cascade with Dual Early Exit

```
Stage 1: 1-bit Hamming on 1/16 sample (alpha-masked)
    → only sample bits where BOTH vectors have alpha=1
    → if shared_alpha < threshold → "not enough overlap" → SKIP (NEW)
    → if distance > reject_band → "not similar" → SKIP (existing)

Stage 2: 1-bit Hamming on 1/4 sample (alpha-masked)
    → same dual exit

Stage 3: 4-bit INT8 full precision (alpha-masked)
    → pentary accumulators only on defined dimensions

Stage 4: BF16/FP32 foveal (alpha-masked)
    → full precision where it matters

Early exit at EACH stage has TWO independent reasons:
    (a) Hamming distance too high → not similar → skip
    (b) Shared alpha too low → not enough overlap → incomparable → skip
```

### 4.2 Information Metrics from Alpha

```rust
fn vector_metrics(data: &[u64], alpha: &[u64]) -> VectorMetrics {
    let total_bits = data.len() * 64;
    let defined = alpha.iter().map(|x| x.count_ones()).sum::<u32>();
    let signal = data.iter().zip(alpha).map(|(d, a)| (d & a).count_ones()).sum::<u32>();

    VectorMetrics {
        // How much of this vector carries real information?
        information_density: defined as f32 / total_bits as f32,

        // Of the defined bits, what fraction is set?
        signal_ratio: signal as f32 / defined.max(1) as f32,

        // NARS confidence — STRUCTURAL, NOT METADATA
        nars_confidence: defined as f32 / total_bits as f32,
    }
}
```

NARS confidence is the alpha density. Not a separate float. Not external metadata.
The confidence IS the proportion of defined dimensions. As evidence accumulates:

```
New triple arrives → XOR into vector → alpha bits flip 0→1
More evidence → more alpha bits defined → confidence increases
Contradictory evidence → accumulator magnitudes drop → alpha bits flip 1→0
Confidence decreases structurally.
```

---

## 5. Alpha-Aware Mexican Hat with Penalty Circuit

Direct translation of Orangutan's autaptic inhibitory neuron (Figure 11b):

```rust
fn mexican_hat_alpha(
    center: &[u64],
    surround: &[u64],
    center_alpha: &[u64],
    surround_alpha: &[u64],
    total_bits: u32,
) -> i32 {
    let mut excitation: u32 = 0;
    let mut inhibition: u32 = 0;
    let mut undefined_center: u32 = 0;

    for i in 0..center.len() {
        // Excitation: only from defined center bits
        excitation += (center[i] & center_alpha[i]).count_ones();

        // Inhibition: only from defined surround bits
        inhibition += (surround[i] & surround_alpha[i]).count_ones();

        // Orangutan penalty: every UNDEFINED center bit is actively penalized
        // The autaptic neuron constantly fires; only active input cancels it
        undefined_center += (!center_alpha[i]).count_ones();
    }

    // Penalty proportional to undefined fraction
    let penalty = undefined_center / 4;  // tunable divisor

    excitation as i32 - inhibition as i32 - penalty as i32

    // A vector with 80% alpha pays 20% penalty
    // A vector with 20% alpha pays 80% penalty
    // A vector with  0% alpha is ALL penalty → maximally suppressed
    // Undefined vectors can't false-match — they're penalized below noise floor
}
```

The penalty circuit ensures that:
- **Active input**: excitation minus canceled inhibition = net positive
- **Missing input**: no excitation, full penalty = net negative
- **This is not the same as zero input**

The missing signal is actively penalized. Undefined dimensions don't just fail
to contribute — they hurt the score. This pushes undefined vectors OUT of the
resonance entirely.

---

## 6. The Six RISC Instructions with Alpha Modifier

Not a seventh instruction. Alpha is a MODIFIER on the existing six. Like condition
flags on ARM instructions. Every instruction optionally respects the alpha channel.
Same 6 instructions. Richer semantics. One extra AND per operation.

```
INSTRUCTION     WITHOUT .α                  WITH .α MODIFIER
─────────────────────────────────────────────────────────────────────────
XOR             a ^ b                       data: a ^ b
                                            alpha: a_α AND b_α

POPCOUNT        popcount(a ^ b)             popcount((a ^ b) AND a_α AND b_α)
                                            / popcount(a_α AND b_α)

MAJORITY        majority(inputs)            majority on α=1 bits only
                                            result_α = majority(input_αs)

AND/NOT         a AND NOT b                 (a AND NOT b), α = a_α AND b_α

BLAKE3          blake3(data)                blake3(data AND α)

THRESHOLD       dist < σ_band               dist < σ_band
                                            AND shared_α > min_overlap
─────────────────────────────────────────────────────────────────────────

Assembly-level notation (ARM-style condition suffix):

    XOR.α   r0, r1, r2          ; bind with alpha propagation
    PCNT.α  r3, r0, r4          ; alpha-normalized popcount
    MAJ.α   r5, {r0..r4}        ; majority vote, alpha-aware
    ANDN.α  r6, r0, r1          ; factorize with alpha intersection
    B3.α    r7, r0              ; seal only defined bits
    THR.α   r8, r3, σ, min_α    ; threshold with overlap guard
```

---

## 7. Alpha Accumulation from Pentary

The pentary column already stores signed accumulators (-2..+2). Alpha can be
derived from accumulator magnitude at any time:

```rust
fn pentary_to_alpha(pentary: &[i8], threshold: i8) -> Vec<u64> {
    // Each accumulator value maps to alpha:
    //   |acc| >= threshold  →  alpha = 1 (confident)
    //   |acc| <  threshold  →  alpha = 0 (uncertain/canceled)
    //
    // Default threshold = 1:
    //   +2, -2  →  alpha = 1 (strong evidence)
    //   +1, -1  →  alpha = 1 (some evidence)
    //    0      →  alpha = 0 (canceled or never written)

    let mut alpha = vec![0u64; pentary.len() / 64 + 1];
    for (i, &acc) in pentary.iter().enumerate() {
        if acc.abs() >= threshold {
            alpha[i / 64] |= 1u64 << (i % 64);
        }
    }
    alpha
}
```

For BUNDLE operations, the accumulator magnitude at each dimension directly
encodes confidence. The alpha channel is a binarized snapshot of this
continuous confidence signal, taken at a threshold that can shift:

- **Strict threshold (2)**: Only dimensions with strong multi-source agreement.
  High precision, low recall. For CAM exact-match retrieval.

- **Relaxed threshold (1)**: Any non-zero evidence counts.
  Lower precision, full recall. For exploratory search.

- **Dynamic threshold**: Adapts to the vector's information density.
  Dense vectors (many bundles) need higher thresholds.
  Sparse vectors (few bundles) can use lower thresholds.
  This IS Orangutan's STP/STD dynamics: freshness decays toward NaN.

---

## 8. Connection to NARS

### 8.1 Confidence as Alpha Density

```
NARS truth value: <frequency, confidence>

frequency  = popcount(data AND alpha) / popcount(alpha)
             "Of the things I know, how many are true?"

confidence = popcount(alpha) / total_bits
             "How much do I actually know?"

Both are O(1) POPCOUNT operations on the stored vectors.
Neither requires external metadata.
The NARS truth value is EMBEDDED IN THE SUBSTRATE.
```

### 8.2 Evidence Accumulation

```
Positive evidence:  dimension k gets +1 → accumulator increases → alpha stays 1
Negative evidence:  dimension k gets -1 → accumulator decreases
                    If acc crosses zero → alpha flips 1→0 (confidence drops)
                    If acc goes strongly negative → alpha returns to 1, data flips

No evidence:        dimension k untouched → acc stays at 0 → alpha = 0

The confidence trajectory:
    First observation:   few alpha bits set  → low confidence
    Repeated agreement:  more alpha bits     → confidence rises
    Contradiction:       some alpha bits drop → confidence decreases
    Convergence:         surviving alpha bits → stable high confidence
```

### 8.3 Revision and Choice

NARS revision combines two judgments. With alpha:

```rust
fn nars_revise(
    a_data: &[u64], a_alpha: &[u64],  // judgment 1
    b_data: &[u64], b_alpha: &[u64],  // judgment 2
) -> (Vec<u64>, Vec<u64>) {            // revised (data, alpha)
    let mut result_data = vec![0u64; a_data.len()];
    let mut result_alpha = vec![0u64; a_alpha.len()];

    for i in 0..a_data.len() {
        let both_defined = a_alpha[i] & b_alpha[i];
        let only_a = a_alpha[i] & !b_alpha[i];
        let only_b = b_alpha[i] & !a_alpha[i];

        // Where both defined: use majority (this IS NARS revision)
        let agree = !(a_data[i] ^ b_data[i]) & both_defined;
        let disagree = (a_data[i] ^ b_data[i]) & both_defined;
        // Agreement → keep value, alpha = 1
        // Disagreement → contested, alpha = 0 (need more evidence)

        result_data[i] = (a_data[i] & (agree | only_a))
                       | (b_data[i] & only_b);
        result_alpha[i] = agree | only_a | only_b;
        // Note: disagree bits get alpha = 0 (contested → undefined)
    }

    (result_data, result_alpha)
}
```

Where both judgments agree → high confidence (alpha = 1).
Where they disagree → uncertainty (alpha = 0, excluded from future comparisons).
Where only one has evidence → accept it (alpha = 1, but weaker total confidence).

---

## 9. Implementation Priority

### Phase 1: Storage (immediate)
- Add `alpha Binary(2048)` column to LanceDB spo_nodes
- Default: all-ones for existing nodes (backward compatible)
- BLAKE3 seal recomputed over `data AND alpha`

### Phase 2: Hamming (next)
- Modify all POPCOUNT paths to use `hamming_alpha()`
- Add `shared_alpha < min_overlap` guard to THRESHOLD
- One extra AND per comparison — minimal perf cost

### Phase 3: Belichtungsmesser (then)
- Alpha-aware 7-point sampling
- Dual early exit (distance + overlap)
- Transparent reading for mostly-undefined vectors

### Phase 4: Mexican Hat (then)
- Penalty circuit for undefined dimensions
- Alpha-weighted excitation/inhibition
- Prevents false-match on low-alpha vectors

### Phase 5: Pentary Integration (finally)
- Derive alpha from accumulator magnitudes
- Dynamic threshold based on bundle count
- STP/STD-like temporal decay of alpha

---

## 10. Summary

| Aspect | Before | After |
|--------|--------|-------|
| Unknown dimensions | Noise (indistinguishable from signal) | Transparent (excluded from comparison) |
| Canceled dimensions | ~50% Hamming from everything (dead zone) | Alpha = 0, penalized in Mexican hat |
| NARS confidence | External float, separate metadata | Alpha density, structural, O(1) POPCOUNT |
| Comparison cost | O(16384) always | O(defined) with early exit on low overlap |
| Storage per node | 2KB (vector only) | 4KB (vector + alpha) |
| False match rate | High for sparse/partial vectors | Near zero (penalty circuit + overlap guard) |
| Partial triples | Encoded with noise, pollute search | Separate projections, each fully defined |
| Epistemic status | "I don't know" = "I made this up" | "I don't know" ≠ "I made this up" |

The alpha channel is one extra bitvector. One extra AND per operation.
It gives the substrate the ability to distinguish knowledge from noise —
the single most important property a cognitive system can have.

---

*Inspired by the Orangutan framework's prediction bias circuit, all-or-none
critical state handling, and autaptic penalty neurons. The biological brain
never forces a decision at the synapse level when evidence is balanced — it
propagates the ambiguity upward and lets higher-level circuits resolve it
with context. The alpha channel does the same for the RISC brain.*
