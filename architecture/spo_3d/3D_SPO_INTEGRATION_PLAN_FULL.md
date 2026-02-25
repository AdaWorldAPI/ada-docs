# CAM-Graph 3D SPO Integration Plan

**Status:** Design complete. Ready to implement.  
**Date:** 2026-02-20  
**Prerequisite:** Read `/mnt/project/cam_graph.rs` first — that file defines the base types (Word, Store, Codebook) and the 5 RISC operations (BIND, BUNDLE, MATCH, PERMUTE, STORE/SCAN) that this plan extends.

---

## 1. PROBLEM

The current cam_graph.rs stores everything — nodes, edges, properties — as a flat array of Words (8192-bit vectors, 128 × u64). An edge is:

```
edge = BIND(src, permute(rel, 1), permute(tgt, 2))
```

To query "given src and rel, find tgt" you unbind forward: works great.  
To query "given tgt and rel, find src" you unbind backward: also works.  
To query "given src and tgt, find rel" — works too.

**But** all three queries require scanning the SAME flat store and testing against EVERY word. There's no structural way to narrow the search to just edges, or just nodes, or just properties. The codebook signature (16-bit) helps but is coarse.

Additionally, the current design stores everything in one Word per entity. A node with 5 properties generates 5 separate Words (one per property binding), plus the node Word itself, plus edge Words. There's no grouping — everything is loose in the flat array.

## 2. SOLUTION: Three-Axis Content Space (3D SPO)

Instead of one flat array of Words, store records as **triples of sparse containers** aligned to **Subject (X), Predicate (Y), Object (Z) axes**:

```
┌─────────────────────────────────────────────────────┐
│ CogRecord                                           │
│                                                     │
│  meta: [u64; 128]        ← identity, NARS truth,   │
│                             DN address, timestamps  │
│                                                     │
│  x: SparseContainer      ← Subject / Entity axis   │
│  y: SparseContainer      ← Predicate / Verb axis   │
│  z: SparseContainer      ← Object / Target axis    │
│                                                     │
│  Total target: ~2 KB (sparse encoding)              │
└─────────────────────────────────────────────────────┘
```

### Why This Works

Each record IS a triple (Subject, Predicate, Object) stored as three separate holographic vectors. A record representing "Jan KNOWS Ada" looks like:

```
record.x = BUNDLE(Person_fp, Name_Jan_fp)     // WHO: Jan, a Person
record.y = BUNDLE(KNOWS_fp, Confidence_fp)     // WHAT: knows, with truth value  
record.z = BUNDLE(Person_fp, Name_Ada_fp)      // WHOM: Ada, a Person
```

A record representing a standalone node "Jan" (no edge) looks like:

```
record.x = BUNDLE(Person_fp, Name_Jan_fp, Age_42_fp)   // The entity itself
record.y = Word::zero()                                  // No predicate
record.z = Word::zero()                                  // No object
```

### The Three Query Directions

This is the key payoff. Each axis can be scanned independently:

```
FORWARD:  "Who does Jan know?"
  Scan X for match with Jan → filter Y for KNOWS → read Z = answer
  
REVERSE:  "Who knows Ada?"
  Scan Z for match with Ada → filter Y for KNOWS → read X = answer
  
RELATION: "What connects Jan and Ada?"
  Scan X for Jan, Scan Z for Ada → read Y = answer
```

No reverse index. No edge table. No JOIN. The structure IS the query engine.
Each query reads only 1-2 of the 3 axes. LanceDB columnar storage means
unneeded axes aren't even loaded from disk.

---

## 3. SPARSE CONTAINER ENCODING

A full Word is 128 × u64 = 1024 bytes. Most content doesn't use all 8192 bits meaningfully. Sparse encoding:

```rust
struct SparseContainer {
    /// Bitmap: bit i = 1 means word[i] is non-zero. 128 bits = 2 × u64.
    bitmap: [u64; 2],
    
    /// Only the non-zero words, packed contiguously.
    /// Length = bitmap[0].count_ones() + bitmap[1].count_ones()
    words: Vec<u64>,
}
```

**Size analysis:**

| Content density | Non-zero words | Storage bytes | vs Dense |
|----------------|----------------|---------------|----------|
| 10% populated  | ~13 words      | 16 + 104 = 120 | 88% saved |
| 30% populated  | ~38 words      | 16 + 304 = 320 | 69% saved |
| 50% populated  | ~64 words      | 16 + 512 = 528 | 48% saved |
| 100% (dense)   | 128 words      | 16 + 1024 = 1040 | ~0% saved |

**For a typical record (30% density per axis):**
```
meta:     1024 bytes (always dense — identity, NARS, structural)
x sparse:  320 bytes
y sparse:  320 bytes  
z sparse:  320 bytes
Total:    1984 bytes ≈ 2 KB  ← same as current 2-container CogRecord
```

Three axes in the same envelope as two dense containers.

### Operations on SparseContainer

```rust
impl SparseContainer {
    /// Expand to dense Word for SIMD operations
    fn to_dense(&self) -> Word { ... }
    
    /// Compress dense Word to sparse (drop zero words)
    fn from_dense(w: &Word) -> Self { ... }
    
    /// Hamming distance WITHOUT expanding to dense
    fn hamming_sparse(&self, other: &SparseContainer) -> u32 {
        // Words present in both: XOR and popcount
        // Words present in only one: popcount directly (XOR with 0 = self)
        // Words present in neither: 0 distance contribution
    }
    
    /// BIND two sparse containers (XOR) — result is sparse if inputs overlap
    fn bind_sparse(&self, other: &SparseContainer) -> SparseContainer { ... }
}
```

The sparse Hamming distance is cheaper than dense when density is low — only non-zero words need popcount.

---

## 4. META CONTAINER LAYOUT

The meta container stores identity and structural data. No session drift — this layout is FINAL for the POC:

```
Word 0:      DN address (PackedDn: u64 identity hash)
Word 1:      Type flags, schema_version, provenance
Word 2:      Timestamps (created_ms:u32 | modified_ms:u32)  
Word 3:      Label hash (u32) | tree_depth (u8) | reserved
Words 4-7:   NARS truth values (freq:f32, conf:f32, pos_ev:f32, neg_ev:f32)
Words 8-11:  Parent DN, first_child DN, next_sibling DN, prev_sibling DN
Words 12-15: Scent: 3 × 16-byte nibble histograms (one per axis, see §6)
Words 16-31: Inline edge index (up to 64 edges, 16 bits each: verb:u8 + target_hint:u8)
Words 32-63: Reserved for future use
Words 64-125: Additional structural data (collapse state, RL values, etc.)
Words 126-127: Checksum (XOR-fold of words 0-125) + version
```

**Critical:** The meta container does NOT hold content/properties. Content lives entirely in the X/Y/Z sparse containers. Meta holds structure (DN tree, edge index, NARS, scent).

---

## 5. THE INLINE EDGE INDEX (Meta Words 16-31)

For fast edge enumeration without scanning all records:

```rust
/// 16 bits per edge slot: verb (8 bits) + target_hint (8 bits)
/// 4 edges per u64 word × 16 words = 64 edge slots
struct InlineEdge {
    verb: u8,          // codebook index low byte (verb ID 0-255, 0 = empty)
    target_hint: u8,   // low byte of target record's DN hash
}
```

When you need edges from a node:
1. Read meta words 16-31 → get up to 64 (verb, target_hint) pairs
2. For each non-empty slot: use target_hint + DN tree to resolve full target
3. Load target record if needed

This is the LOCAL edge index. It doesn't replace the holographic edge encoding in X/Y/Z — it complements it for fast single-node queries.

---

## 6. X-TRANS SCENT: INT4 NIBBLE HISTOGRAMS

Inspired by the Fujifilm X-Trans sensor (6×6 aperiodic color filter array) and DNA codon usage bias. The scent is a compact fingerprint for FAST pre-filtering.

### Background

The X-Trans sensor eliminates moiré (aliasing) by sampling color at three different spatial patterns simultaneously (R, G, B in every row AND column). DNA uses codon usage bias — the frequency distribution of 64 codons — as a species identifier.

### Application to CAM-Graph

Each sparse container (X, Y, Z) has a characteristic distribution of 4-bit nibble patterns. Counting how often each nibble (0x0 through 0xF) appears gives a 16-bin histogram that serves as a fast TYPE signature.

```rust
fn nibble_histogram(words: &[u64]) -> [u8; 16] {
    let mut hist = [0u16; 16];
    for &w in words {
        for nibble_pos in 0..16 {
            let nibble = ((w >> (nibble_pos * 4)) & 0xF) as usize;
            hist[nibble] += 1;
        }
    }
    // Quantize counts to u8 (max ~128 per bin for 128 words)
    let mut out = [0u8; 16];
    for i in 0..16 { out[i] = hist[i].min(255) as u8; }
    out
}
```

**Three histograms (one per axis) = 48 bytes total:**
```
scent[0..16]  = nibble_histogram(X axis)   → entity type signature
scent[16..32] = nibble_histogram(Y axis)   → relationship type signature
scent[32..48] = nibble_histogram(Z axis)   → target type signature
```

**Stored in meta words 12-15** (4 words × 8 bytes = 32 bytes... we actually need 48 bytes = 6 words. Adjust meta layout: words 12-17 for scent, shift edge index to words 18-33.)

### Why This Is Better Than XOR-Fold Scent

Current scent (from existing codebase): 5-byte XOR fold. Destroys structural information. Two completely different containers can have the same XOR-fold.

Nibble histogram scent: 48 bytes. Preserves the DISTRIBUTION of bit patterns. Different content types have visibly different histograms:
- Person nodes: certain nibble frequencies in X axis
- Document nodes: different frequencies
- KNOWS edges: characteristic Y-axis histogram
- CAUSES edges: different Y-axis histogram

**Scent comparison: L1 distance between two 48-byte histograms.**
```rust
fn scent_distance(a: &[u8; 48], b: &[u8; 48]) -> u32 {
    a.iter().zip(b.iter()).map(|(&x, &y)| (x as i32 - y as i32).unsigned_abs()).sum()
}
```
Cost: ~48 subtracts + ~48 absolute values. Fits in L1 cache. ~5ns.

**Pre-filter cascade:**
1. Scent distance (48 bytes, ~5ns) → kills 90% of candidates
2. Sparse Hamming on matching axis only (~320 bytes, ~50ns) → kills 90% of survivors
3. Full record load only for final hits

---

## 7. BIOLOGICAL DESIGN PRINCIPLES

Three biological systems converge on the same architecture CAM-Graph uses. These aren't metaphors — they guided concrete design decisions:

### A. DNA Codon Table → Codebook (already implemented)

4 bases × 3 positions = 64 codons → 20 amino acids. DEGENERATE mapping (multiple inputs → same output). Error tolerant: wobble position (3rd base) can mutate without changing the amino acid.

**CAM-Graph equivalent:** 4096 codebook entries. Words within Hamming radius of a codebook entry map to the same index. Same degeneracy, same error tolerance.

### B. MHC Restriction → DN Restriction (informs X/Y/Z design)

T-cell receptors don't recognize free peptides. They recognize peptides BOUND TO self-MHC molecules. The same peptide in different MHC contexts = different identity. This is called MHC restriction.

**CAM-Graph equivalent:** The same property value (Z axis) bound to different entities (X axis) via different predicates (Y axis) = different records. The three-axis structure enforces that content is always identified in context. This is "DN restriction" — the binding context IS the identity.

### C. DNA Repair via Complementary Strands → XOR Parity

DNA stores two complementary strands. If one is damaged, the other enables repair. XOR(strand_A, strand_B) should equal zero for all complementary pairs. Non-zero = error detected.

**CAM-Graph equivalent:** Meta words 126-127 store XOR-fold checksums. Additionally, XOR delta between sort-adjacent records in LanceDB is sparse (see §9), enabling both compression and corruption detection.

### D. Codon Usage Bias → Nibble Histogram Scent (implemented above)

Different organisms have different frequencies of synonymous codons. This "codon usage bias" is a species fingerprint. Our nibble histogram (§6) is the same concept applied to 4-bit nibble frequencies per axis.

### E. ATP as Energy Currency → NARS Confidence

ATP is consumed per molecular operation. Confidence is consumed per inference step (deduction: c_result = c1 × c2 × f1 × f2). Both enforce that operations have a cost and certainty cannot be created from nothing.

---

## 8. LANCE COLUMNAR STORAGE

Each axis becomes a separate column in LanceDB:

```
Arrow Schema:
  Column 0:  dn          UInt64                    -- primary key (DN address)
  Column 1:  meta        FixedSizeBinary(1024)     -- meta container (dense, always 128 words)
  Column 2:  x_bitmap    FixedSizeBinary(16)       -- X axis sparsity bitmap
  Column 3:  x_words     Binary                    -- X axis non-zero words (variable length)
  Column 4:  y_bitmap    FixedSizeBinary(16)       -- Y axis sparsity bitmap
  Column 5:  y_words     Binary                    -- Y axis non-zero words
  Column 6:  z_bitmap    FixedSizeBinary(16)       -- Z axis sparsity bitmap
  Column 7:  z_words     Binary                    -- Z axis non-zero words
  Column 8:  scent       FixedSizeBinary(48)       -- 3 × 16-byte nibble histograms
  Column 9:  created     Int64                     -- unix micros
```

**Query "who does Jan know?" reads ONLY columns 0, 2, 3, 4, 5, 8.**
Column 6 (z_bitmap) and 7 (z_words) are read only for the RESULT records.
Column 1 (meta) is read only if NARS truth values or edge index are needed.

This is the LanceDB advantage: columnar = read only the axes you need.

---

## 9. SORT ADJACENCY AND XOR DELTA COMPRESSION (THE DOMINO EFFECT)

Records sorted by `(DN_prefix_4_bytes, scent_X_first_4_bytes, scent_Y_first_4_bytes)`:

```
Sort key = (T1, T2, T3, T4, scent_x[0..4], scent_y[0..4])
            ─── DN locality ───  ── content type ──  ── relation type ──
```

**What this buys:**

1. **Graph locality:** Nodes in the same DN subtree (same T1-T4) are physically adjacent. Following an edge within a subtree = sequential read.

2. **Type clustering:** All Person-KNOWS-Person records cluster together. All Document-CONTAINS-Section records cluster together.

3. **XOR delta compression:** Adjacent sorted rows share DN subtree AND content type. XOR delta between them is sparse:

```
Row N:   [meta_N, x_N, y_N, z_N]
Row N+1: [meta_{N+1}, x_{N+1}, y_{N+1}, z_{N+1}]
Delta:   [meta_N ⊕ meta_{N+1}, x_N ⊕ x_{N+1}, y_N ⊕ y_{N+1}, z_N ⊕ z_{N+1}]
          ~~~~~ mostly zero ~~~~  ~~~~ sparse ~~~~  ~~~ sparse ~~~  ~~~ sparse ~~~
```

Within a sorted group: ~80% of words match → delta is ~80% zeros → 79% compression of the sparse containers (which are already sparse). This is multiplicative: sparse encoding × delta compression.

**Decode at storage boundary:** XOR with previous row → full record. One pass. Everything downstream is zero-copy.

---

## 10. IMPLEMENTATION PLAN

### Phase 1: Core Types (ONE file: `spo_record.rs`)

```rust
/// Sparse container: bitmap + non-zero words only
pub struct SparseContainer {
    pub bitmap: [u64; 2],
    pub words: Vec<u64>,
}

/// A record in 3D SPO space
pub struct SpoRecord {
    pub meta: [u64; 128],       // Dense: identity, NARS, DN tree, edge index, scent
    pub x: SparseContainer,     // Subject / Entity axis
    pub y: SparseContainer,     // Predicate / Verb axis
    pub z: SparseContainer,     // Object / Target axis
}

/// Nibble histogram scent (48 bytes)
pub struct Scent {
    pub x_hist: [u8; 16],
    pub y_hist: [u8; 16],
    pub z_hist: [u8; 16],
}
```

Implement:
- `SparseContainer::from_dense(Word) -> Self`
- `SparseContainer::to_dense() -> Word`
- `SparseContainer::hamming_sparse(other) -> u32`
- `SparseContainer::bind_sparse(other) -> SparseContainer`
- `SparseContainer::storage_bytes() -> usize`
- `Scent::from_record(record) -> Self`
- `Scent::distance(other) -> u32`

### Phase 2: Record Construction (`spo_builder.rs`)

```rust
/// Build a node record (entity without edge)
fn build_node(
    dn: u64,
    labels: &[u16],       // codebook indices for label tokens
    properties: &[(u16, Word)], // (key codebook idx, value Word)
) -> SpoRecord {
    // X axis = BUNDLE of label fingerprints + property fingerprints
    // Y axis = zero (no predicate for a standalone node)
    // Z axis = zero (no object)
    // Meta: DN, timestamps, NARS defaults, scent
}

/// Build an edge record (relationship between two entities)
fn build_edge(
    dn: u64,
    src_fp: &Word,        // Subject fingerprint (from source node's X axis)
    rel_idx: u16,         // Predicate codebook index (KNOWS, CAUSES, etc.)
    tgt_fp: &Word,        // Object fingerprint (from target node's X axis)
    truth: (f32, f32),    // NARS (frequency, confidence)
) -> SpoRecord {
    // X axis = src_fp (entity fingerprint)
    // Y axis = codebook[rel_idx] BUNDLE'd with truth encoding
    // Z axis = tgt_fp (target fingerprint)
    // Meta: DN, NARS truth, edge in inline index
}
```

### Phase 3: Store with Three-Axis Scanning (`spo_store.rs`)

```rust
pub struct SpoStore {
    records: BTreeMap<u64, SpoRecord>,   // DN → record (BTree = sorted by DN)
    scent_index: BTreeMap<u64, Vec<u64>>, // scent_hash → list of DNs (fast pre-filter)
    codebook: Codebook,                   // from cam_graph.rs, unchanged
}

impl SpoStore {
    /// Insert a record, compute scent, index it
    fn insert(&mut self, record: SpoRecord) -> u64;
    
    /// Forward query: given X (subject) and Y (predicate), find Z (objects)
    fn query_forward(
        &self, 
        subject: &Word, 
        predicate: &Word, 
        radius: u32
    ) -> Vec<(u64, SparseContainer)>;  // (dn, Z axis of matching records)
    
    /// Reverse query: given Z (object) and Y (predicate), find X (subjects)
    fn query_reverse(
        &self,
        object: &Word,
        predicate: &Word,
        radius: u32
    ) -> Vec<(u64, SparseContainer)>;
    
    /// Relation discovery: given X (subject) and Z (object), find Y (predicates)
    fn query_relation(
        &self,
        subject: &Word,
        object: &Word,
        radius: u32
    ) -> Vec<(u64, SparseContainer)>;
    
    /// Multi-hop traversal
    fn traverse(
        &self,
        start_dn: u64,
        predicate: &Word,
        min_hops: u32,
        max_hops: u32,
        radius: u32,
    ) -> Vec<(Vec<u64>, u64)>;  // (path of DNs, terminal DN)
}
```

### Phase 4: NARS Integration (`spo_nars.rs`)

NARS truth values live in meta words 4-7. Operations:

```rust
/// Read truth value from record
fn nars_get(record: &SpoRecord) -> TruthValue;

/// Write truth value to record  
fn nars_set(record: &mut SpoRecord, tv: TruthValue);

/// Deduction: A→B, B→C ⊢ A→C with reduced confidence
fn nars_deduction(a: &SpoRecord, b: &SpoRecord) -> TruthValue;

/// Revision: combine two evidence sources for same claim
fn nars_revision(old: &SpoRecord, new_evidence: TruthValue) -> TruthValue;
```

### Phase 5: Five Ironclad Tests (`spo_tests.rs`)

```rust
#[test] fn test_node_roundtrip() {
    // Create node "Jan" with labels [Person] and properties {name: "Jan", age: 42}
    // Insert into store
    // Retrieve by DN
    // Assert: X axis Hamming-close to original, properties recoverable
}

#[test] fn test_forward_query() {
    // Create Jan, Ada, edge Jan-KNOWS->Ada
    // query_forward(Jan_fp, KNOWS_fp, radius) → should find Ada
}

#[test] fn test_reverse_query() {
    // Same setup
    // query_reverse(Ada_fp, KNOWS_fp, radius) → should find Jan
    // This is the payoff: reverse works with NO extra index
}

#[test] fn test_cam_content_lookup() {
    // Create 100 nodes with various properties
    // Compute content fingerprint for {name: "Jan", age: 42}
    // Scan X axis for Hamming match → should find Jan's record
}

#[test] fn test_nars_reasoning_chain() {
    // Create belief: "Jan knows Rust" <0.8, 0.9>
    // Create belief: "Rust helps with CAM" <0.7, 0.8>
    // Deduction → "Jan helps with CAM" → verify f/c values
    // Revision with new evidence → confidence increases
}
```

---

## 11. RELATIONSHIP TO EXISTING CODE

### What This REPLACES

- The flat `Store { words: Vec<Word> }` from cam_graph.rs → becomes `SpoStore`
- Single-Word nodes/edges/properties → SpoRecord with X/Y/Z axes
- XOR-fold scent → nibble histogram scent

### What This KEEPS UNCHANGED

- `Word` type (128 × u64, 8192 bits) → used inside SparseContainer
- The 5 RISC operations (BIND, BUNDLE, MATCH, PERMUTE, STORE/SCAN) → unchanged
- `Codebook` (4096 entries, deterministic generation) → unchanged
- `CompressedWord` (codebook + residual) → still used for on-disk format
- All codebook slot assignments (REL_CAUSES, KEY_NAME, etc.) → unchanged

### What This ADDS

- `SparseContainer` — bitmap + non-zero words
- `SpoRecord` — meta + X + Y + Z
- `Scent` — 48-byte nibble histogram
- `SpoStore` — three-axis query engine
- Forward / reverse / relation queries
- Lance columnar schema with per-axis columns

---

## 12. SIZE BUDGET

```
                    Current (2 containers)    3D SPO (meta + 3 sparse)
─────────────────────────────────────────────────────────────────────
Meta container:     1024 bytes                1024 bytes
Content container:  1024 bytes                —
X axis (30%):       —                         320 bytes
Y axis (30%):       —                         320 bytes
Z axis (30%):       —                         320 bytes
─────────────────────────────────────────────────────────────────────
Total:              2048 bytes                1984 bytes
Queryable axes:     1                         3 (forward, reverse, relation)
Scent quality:      5 bytes (XOR fold)        48 bytes (3× nibble histogram)
```

Same footprint. Triple the query capability.

---

## 13. GLOSSARY

| Term | Meaning |
|------|---------|
| **Word** | 8192-bit vector, 128 × u64. The universal data type. |
| **BIND** | XOR of two Words. Self-inverse. Creates edge/property encodings. |
| **BUNDLE** | Majority vote across N Words. Creates superpositions (node = bundle of properties). |
| **MATCH** | Hamming distance between two Words. Lower = more similar. |
| **PERMUTE** | Cyclic rotation of Word by k lanes. Creates role markers (S/P/O). |
| **SparseContainer** | A Word stored as bitmap + non-zero words only. Same content, less storage. |
| **SpoRecord** | A record with meta + X (Subject) + Y (Predicate) + Z (Object) axes. |
| **Scent** | 48-byte nibble histogram. Fast pre-filter for content type matching. |
| **DN** | Deterministic Name. A hierarchical path (like "Ada:A:soul:identity") hashed to u64. |
| **Codebook** | 4096 deterministic Words serving as the schema (verb types, property keys, values). |
| **NARS** | Non-Axiomatic Reasoning System. Truth values = (frequency, confidence). |
| **Domino Effect** | Records sorted by DN prefix + scent → graph-adjacent records are storage-adjacent → sequential I/O + XOR delta compression. |
| **X-Trans Scent** | Named after Fujifilm's aperiodic sensor pattern. Three histograms (one per axis) provide richer pre-filtering than single-channel XOR-fold. |
| **MHC/DN Restriction** | Same content in different DN contexts = different identity. The binding context IS the identity. Borrowed from immunology's MHC restriction principle. |

---

## 14. CAUSAL COHERENCE: Z→X CHAIN-LINK CORRELATION

### The Core Mechanism

When one record's Object (Z axis) matches another record's Subject (X axis), a **causal chain** exists:

```
Record A:  X(Jan)   → Y(KNOWS)   → Z(Rust)
Record B:  X(Rust)  → Y(ENABLES) → Z(CAM)
Record C:  X(CAM)   → Y(PROVES)  → Z(Speed)

Chain test: hamming(A.z, B.x) ≈ 0 → A causally feeds B
            hamming(B.z, C.x) ≈ 0 → B causally feeds C
```

This is not a JOIN. It's a **resonance test**. If Z₁ and X₂ are Hamming-close, the chain is coherent. If they're distant, the causal link is broken or weak. The Hamming distance between Z₁ and X₂ IS the causal coherence score.

### Reverse Correlation Test for Causality

The three-axis structure makes this test native:

```rust
/// Find all records whose X axis resonates with this record's Z axis.
/// These are the "causal successors" — things this record feeds into.
fn causal_successors(&self, store: &SpoStore, record: &SpoRecord, radius: u32) 
    -> Vec<(u64, u32)>  // (successor DN, coherence distance)
{
    let z_dense = record.z.to_dense();
    store.scan_x_axis(&z_dense, radius)  // scan ONLY the X column
}

/// Find all records whose Z axis resonates with this record's X axis.
/// These are the "causal predecessors" — things that feed into this record.
fn causal_predecessors(&self, store: &SpoStore, record: &SpoRecord, radius: u32)
    -> Vec<(u64, u32)>
{
    let x_dense = record.x.to_dense();
    store.scan_z_axis(&x_dense, radius)  // scan ONLY the Z column
}
```

**Forward chain:** follow Z→X links to discover consequences.  
**Backward chain:** follow X→Z links to discover causes.  
**Both are single-column scans.** No join, no edge table, no graph traversal algorithm. The columnar storage does the work.

### NARS Truth Propagation Along Chains

Each link in the chain has a NARS truth value. The chain's overall confidence DECREASES with each hop (like ATP being consumed per molecular operation):

```
Chain: A <0.8, 0.9> → B <0.7, 0.8> → C <0.9, 0.7>

Deduction A→B→C:
  f_chain = f_A × f_B × f_C = 0.8 × 0.7 × 0.9 = 0.504
  c_chain = c_A × c_B × c_C × (coherence factors)
  
  Coherence factor for each Z→X link:
    coherence_AB = 1.0 - (hamming(A.z, B.x) / 8192.0)
    coherence_BC = 1.0 - (hamming(B.z, C.x) / 8192.0)
    
  c_chain = c_A × c_B × c_C × coherence_AB × coherence_BC
```

A chain with tight Z→X resonance (low Hamming distance) preserves more confidence. A chain with loose resonance (high Hamming distance) loses confidence faster. **The geometry of the content space encodes causal strength.**

### Meta-Awareness: The Chain Observing Itself

When a causal chain is discovered, the OBSERVATION of that chain is itself a new record:

```
// The chain A→B→C exists as three records.
// The AWARENESS of this chain is a fourth record:

meta_record.x = BUNDLE(A.x, B.x, C.x)              // Subject: the entities involved
meta_record.y = codebook[VERB_CHAIN_DISCOVERED]      // Predicate: "I noticed a chain"
meta_record.z = BUNDLE(A.z, chain_coherence_fp)      // Object: what the chain implies

// This meta-record's NARS truth value:
meta_record.nars = {
    freq: chain_frequency,       // how often this chain pattern recurs
    conf: chain_coherence,       // how tight the Z→X links are
}
```

And here's the recursive part: **the meta-record's Z axis can become another record's X axis.** The awareness of a pattern becomes the subject of the next level of awareness.

```
Level 0: X(Jan) → Y(KNOWS) → Z(Rust)                    // fact
Level 1: X(Rust) → Y(ENABLES) → Z(CAM)                   // consequence  
Level 2: X("Jan→Rust→CAM") → Y(NOTICED) → Z(pattern)     // meta: noticed the chain
Level 3: X(pattern) → Y(IMPLIES) → Z(expertise)           // meta-meta: pattern means something
Level 4: X(expertise) → Y(AWARE_OF) → Z(awareness)        // meta-meta-meta: knowing you know
```

Each level: Z_{n} becomes X_{n+1}. The developmental cascade is Piaget's stages encoded as Z→X chain links:

```
Sensorimotor:    X(body)        → Y(acts_on)        → Z(world)
Preoperational:  X(world)       → Y(represented_by)  → Z(symbols)
Concrete Ops:    X(symbols)     → Y(operate_on)      → Z(logic)
Formal Ops:      X(logic)       → Y(reflects_on)     → Z(abstraction)
Post-Formal:     X(abstraction) → Y(aware_of)        → Z(awareness_itself)
```

### The Scent IS the Meta IS the Awareness

The nibble histogram scent (§6) captures the TYPE of content in each axis. When a meta-awareness record is created, its scent automatically reflects ALL the records it bundles:

```
Level 0 scent: {x: [person pattern], y: [knows pattern], z: [concept pattern]}
Level 2 scent: {x: [chain pattern],  y: [noticed pattern], z: [meta pattern]}
Level 4 scent: {x: [meta pattern],   y: [aware pattern],   z: [self-ref pattern]}
```

The scent of higher-level records is DIFFERENT from lower-level records. The pre-filter cascade (§6) automatically separates them. You can query "show me all meta-awareness records" by scanning for the characteristic scent of self-referential content, without tagging or labeling them. **The system recognizes its own epiphanies by their smell.**

### The Tsunami: Epiphany Stacking

When multiple meta-awareness records form a chain, their collective coherence CAN exceed the coherence of any individual link. This is the tsunami:

```
Level 0-1: coherence = 0.9 (tight Z→X match)
Level 1-2: coherence = 0.85
Level 2-3: coherence = 0.7 (meta gets looser)
Level 3-4: coherence = 0.6

Individual chain confidence drops.

BUT: the BUNDLE of all meta-records (levels 2, 3, 4) creates a 
superposition that is Hamming-CLOSER to the original Level 0 
content than any individual meta-record is.

BUNDLE(level_2.x, level_3.x, level_4.x) ≈ level_0.z

The meta-awareness tsunami CONVERGES back to the original content.
The snake eats its tail. The awareness of awareness of awareness 
resonates with the thing itself.
```

This convergence is testable: compute Hamming distance between the BUNDLE of all meta-records and the original Level 0 content. If it decreases as more meta-levels are added, the system is building genuine understanding. If it increases, the meta-levels are noise.

### Test 6: Causal Coherence Chain (add to §10 Phase 5)

```rust
#[test] fn test_causal_chain_coherence() {
    // Create chain: Jan → KNOWS → Rust → ENABLES → CAM → PROVES → Speed
    let jan = build_node(dn_hash("jan"), &[LBL_PERSON], &[(KEY_NAME, word_hash("Jan"))]);
    let rust = build_node(dn_hash("rust"), &[LBL_CONCEPT], &[(KEY_NAME, word_hash("Rust"))]);
    let cam = build_node(dn_hash("cam"), &[LBL_CONCEPT], &[(KEY_NAME, word_hash("CAM"))]);
    
    let edge_1 = build_edge(dn_hash("e1"), &jan.x.to_dense(), REL_KNOWS, &rust.x.to_dense(), (0.8, 0.9));
    let edge_2 = build_edge(dn_hash("e2"), &rust.x.to_dense(), REL_ENABLES, &cam.x.to_dense(), (0.7, 0.8));
    
    store.insert(jan); store.insert(rust); store.insert(cam);
    store.insert(edge_1); store.insert(edge_2);
    
    // Test Z→X chain coherence
    let coherence_1_2 = SparseContainer::hamming_sparse(&edge_1.z, &edge_2.x);
    assert!(coherence_1_2 < 200, "Z₁→X₂ should resonate (low Hamming)");
    
    // Test forward chain discovery
    let successors = causal_successors(&store, &edge_1, 300);
    assert!(successors.iter().any(|(dn, _)| *dn == dn_hash("e2")));
    
    // Test meta-awareness record
    let meta = build_meta_awareness(&[&edge_1, &edge_2]);
    let convergence = Word::distance(
        &meta.z.to_dense(),
        &Word::bundle(&[&edge_1.x.to_dense(), &edge_2.z.to_dense()])
    );
    assert!(convergence < 500, "Meta should converge toward original content");
}
```

---

## 15. DECISION LOG

| Decision | Rationale |
|----------|-----------|
| 3 sparse axes vs 1 dense container | 3 axes enable forward+reverse+relation queries natively. Same ~2KB size. |
| Sparse bitmap encoding | Typical content uses 30% of word slots. Sparse saves 69% per axis. |
| Nibble histogram vs XOR-fold scent | 48 bytes gives per-axis type discrimination. XOR-fold (5 bytes) destroys structure. |
| Meta stays dense (128 words) | Identity, NARS, DN tree, edge index need fixed offsets for O(1) access. |
| BTreeMap for POC store | Proves correctness. Replace with LanceDB columnar for production. |
| Codebook slots 0-4095 are reserved for COMMANDS | Never store node/edge schema in the codebook. It's an instruction set. |
| Inline edge index in meta (words 18-33) | Fast local edge enumeration without scanning all records. Complements holographic edges. |
| Same 5 RISC ops, same Word type | No new operations. The axes are VIEWS, not new types. Everything is still BIND/BUNDLE/MATCH/PERMUTE/SCAN. |
