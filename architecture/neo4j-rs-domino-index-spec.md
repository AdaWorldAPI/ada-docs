# Neo4j-RS Domino Index — Bootstrap Strategy Test

## Context

We are building a Rust-native graph engine (`neo4j-rs`) that replaces Neo4j's JVM/Cypher stack with zero-copy Arrow-backed containers, SIMD Hamming resonance, and emergent topology. Edges are never stored — they arise from fingerprint resonance between containers. The network is never materialized — it is *read* via scan.

This document is a self-contained prompt and specification for testing two competing strategies for bootstrapping the Domino Index — a relative-offset jump table that eliminates full-stack sweeps.

---

## 1. Architecture Contract (Non-Negotiable)

### 1.1 Container Layout — The Superblock

```
Total: 8192 bits = 4 × 32 × 64u = 1 AVX-512 superblock

Q0 [32 × u64] — Meta / Thinking Style
    Purpose: HOW this container thinks
    Content: Codebook class, inference mode, NARS truth-value template
    
Q1 [32 × u64] — Edges / NARS Relations  
    Purpose: WHAT logic this container carries
    Content: <S --> P>, <S <-> P>, inheritance, similarity, implication
    Encodes: Confidence × Frequency as bitpacked truth values
    
Q2 [32 × u64] — Nodes (Subjects/Objects)
    Purpose: WHO/WHAT this container represents
    Content: Entity fingerprints, concept embeddings (compressed)
    
Q3 [32 × u64] — CAM / Routing / Resonance Address
    Purpose: WHERE this container belongs in the network
    Content: Content-Addressable Memory index, DN-path accumulation
    Used for: Hamming resonance matching, Domino chain membership
```

### 1.2 Invariants

- **Zero-copy**: Containers live in Arrow RecordBatches. Never mutated in place.
- **WAL-only writes**: All state changes append to WAL. Containers fold pending commits on next read (self-healing on read).
- **No stored edges**: Edges emerge from `hamming(Q3_a, Q3_b) < threshold` + NARS negotiation in Q1.
- **Immutable batches + mutable WAL**: Borrow-mut conflict impossible by design.
- **SIMD-native**: All Hamming operations target AVX-512 (8192-bit) or AVX2 (4096-bit fallback).

### 1.3 Core Types

```rust
use arrow::array::FixedSizeBinaryArray;
use arrow::record_batch::RecordBatch;

/// One container = 1024 bytes = 8192 bits
pub const CONTAINER_BYTES: usize = 1024;
pub const QUADRANT_U64S: usize = 32;
pub const QUADRANTS: usize = 4;

/// The superblock as a flat array
pub type Superblock = [u64; 128]; // 4 × 32

/// Quadrant accessor (zero-copy slice into superblock)
#[inline]
pub fn q0(sb: &Superblock) -> &[u64; 32] { sb[0..32].try_into().unwrap() }
pub fn q1(sb: &Superblock) -> &[u64; 32] { sb[32..64].try_into().unwrap() }
pub fn q2(sb: &Superblock) -> &[u64; 32] { sb[64..96].try_into().unwrap() }
pub fn q3(sb: &Superblock) -> &[u64; 32] { sb[96..128].try_into().unwrap() }

/// Hamming distance on Q3 (resonance address) — SIMD target
#[inline]
pub fn hamming_q3(a: &Superblock, b: &Superblock) -> u32 {
    let mut dist = 0u32;
    for i in 96..128 {
        dist += (a[i] ^ b[i]).count_ones();
    }
    dist
}
```

### 1.4 Resonance Protocol

```
1. SCAN:      Container_A extracts Q3 fingerprint
2. RESONATE:  Hamming sweep (full or Domino-chained) finds candidates
3. NEGOTIATE: Compare Q1 (NARS logic) — do we agree on this relation?
              Agreement = confidence × frequency > threshold
4. BIND:      shared_commitment = hash(A.id, B.id, timestamp, relation)
              Append to WAL: (A.id, B.id, commitment)
5. FOLD:      On next read of A or B:
              Q3_new = Q3_old ⊕ commitment
              → Fingerprint now carries proof of binding
```

### 1.5 The Domino Index

```rust
/// Relative offset to next resonance partner in the Arrow batch
#[repr(C, packed)]
pub struct DominoEntry {
    /// Offset to next container in this chain (relative, not absolute)
    pub offset: u32,
    /// Hamming distance to that container's Q3
    pub hamming_dist: u16,
    /// Chain ID — which resonance neighborhood
    pub chain_id: u16,
}

/// Full Domino index = thin overlay, ~8 bytes per container
/// For 1M containers = 8MB — fits in L3 cache
pub struct DominoIndex {
    pub entries: Vec<DominoEntry>,
    /// Chain heads: chain_id → first container index
    pub chain_heads: HashMap<u16, u32>,
}
```

---

## 2. The Two Strategies

### Strategy A: Full-Sweep Bootstrap → Incremental Domino

**Concept**: One-time O(N²) or O(N·K) initial sweep to build all chains, then maintain incrementally.

```
Phase 1 — BOOTSTRAP (offline, one-time)
  for each container_i in batch:
    scan ALL other containers
    find K nearest by hamming_q3
    assign chain_id by clustering (locality-sensitive hashing or K-means on Hamming)
    write DominoEntry { offset: nearest_in_chain - i, hamming_dist, chain_id }

Phase 2 — INCREMENTAL (runtime)
  on WAL fold (container fingerprint changes):
    old_chain = domino[container.idx].chain_id
    recompute hamming to old chain neighbors
    if still within threshold → patch offset only
    if drifted out → remove from old chain, scan chain_heads for new home
    patch 2-4 entries (old neighbors + new neighbors)
```

**Pros**: Globally optimal chains. Best query performance after bootstrap.  
**Cons**: O(N²) bootstrap for 1M containers = 10¹² comparisons. Even with SIMD at 5ms per 1M = still hours. Need LSH or approximate methods to cut bootstrap.

**Approximate Bootstrap** (realistic):

```
1. Compute LSH signature of Q3 for each container (e.g., SimHash, 64-bit)
2. Sort by LSH signature — similar containers now adjacent
3. Scan local windows (size W=100) to build initial chains  
4. O(N·W) = 10⁸ for 1M containers ≈ seconds with SIMD
5. Refine chains with a second pass over chain heads
```

### Strategy B: DN-Tree Bottom-Up Propagation

**Concept**: The Distinguished Name tree already encodes hierarchy. Use it as the scaffold — each DN node maintains the Domino chain for its children.

```
DN Tree:
  /cortex
    /vision
      /edge-detect    → chain of containers resonating here
      /color           → chain of containers resonating here
    /language
      /syntax          → chain of containers resonating here

Phase 1 — REGISTRATION
  Each container's Q3 is partially determined by its DN path
  Container registers with its DN leaf node
  Leaf node maintains a local Domino chain (sorted by Q3 hamming)

Phase 2 — CROSS-BRANCH RESONANCE  
  DN parent nodes maintain inter-chain links
  /cortex/vision knows that /edge-detect chain[7] resonates with /color chain[3]
  These are "bridge" DominoEntries with chain_id = BRIDGE

Phase 3 — INCREMENTAL
  WAL fold changes Q3 → container may drift to different DN leaf
  Only the old leaf and new leaf update their chains
  Parent updates bridge entries if cross-branch resonance changed
```

**Pros**: Naturally hierarchical. Incremental from the start — no cold bootstrap. Chain size bounded by DN leaf population. Bridge entries enable cross-domain discovery.  
**Cons**: Requires DN-tree to exist before Domino index. Cross-branch resonance discovery depends on how aggressively parents scan. Could miss resonance between distant branches.

---

## 3. Test Plan

### 3.1 Shared Infrastructure

Build this first — both strategies need it.

```rust
// === Step 1: Generate test data ===

/// Generate N random containers with controlled clustering
fn generate_test_batch(n: usize, num_clusters: usize, noise: f64) -> RecordBatch {
    // Create num_clusters centroid fingerprints (random Q3)
    // For each container:
    //   - Assign to random cluster
    //   - Q3 = centroid ⊕ random_noise(noise_level)
    //   - Q0, Q1, Q2 = random (irrelevant for Domino test)
    // Return as Arrow RecordBatch with FixedSizeBinary(1024) column
}

/// Brute-force Hamming scan — ground truth
fn brute_force_knn(batch: &RecordBatch, query_idx: usize, k: usize) -> Vec<(usize, u32)> {
    // Returns: Vec<(container_index, hamming_distance)> sorted ascending
}

// === Step 2: Implement both strategies ===

trait DominoBuilder {
    fn build(batch: &RecordBatch) -> DominoIndex;
    fn query(index: &DominoIndex, batch: &RecordBatch, query_idx: usize, threshold: u32) -> Vec<usize>;
    fn update(index: &mut DominoIndex, batch: &RecordBatch, changed_idx: usize, new_q3: &[u64; 32]);
}

struct FullSweepDomino;
struct DNTreeDomino;

impl DominoBuilder for FullSweepDomino { /* ... */ }
impl DominoBuilder for DNTreeDomino { /* ... */ }
```

### 3.2 Test Matrix

| Test | What it measures | N | Clusters | Noise |
|------|-----------------|---|----------|-------|
| T1 — Build Time | Bootstrap latency | 10K, 100K, 1M | 64 | 0.1 |
| T2 — Query Recall | % of true KNN found via Domino | 100K | 64 | 0.1, 0.3, 0.5 |
| T3 — Query Latency | Time per resonance query | 100K, 1M | 64 | 0.1 |
| T4 — Update Cost | Time to patch index after WAL fold | 100K | 64 | 0.1 |
| T5 — Drift Stability | Recall after N% of containers update Q3 | 100K | 64 | 0.1 |
| T6 — Scaling | All metrics at 10K → 1M | varied | 64 | 0.1 |

### 3.3 Specific Tests

#### T1: Build Time

```rust
#[bench]
fn bench_build_full_sweep(b: &mut Bencher) {
    let batch = generate_test_batch(100_000, 64, 0.1);
    b.iter(|| FullSweepDomino::build(&batch));
}

#[bench]  
fn bench_build_dn_tree(b: &mut Bencher) {
    let batch = generate_test_batch(100_000, 64, 0.1);
    let dn_tree = build_mock_dn_tree(64); // 64 leaves matching clusters
    b.iter(|| DNTreeDomino::build_with_tree(&batch, &dn_tree));
}
```

**Expected outcome**: DN-Tree builds faster because it's O(N·K_local) where K_local = containers per leaf. Full-Sweep with LSH should be comparable but with higher constant factor.

#### T2: Query Recall

```rust
fn test_recall(strategy: &impl DominoBuilder, batch: &RecordBatch, sample_size: usize) -> f64 {
    let index = strategy.build(batch);
    let mut total_recall = 0.0;
    
    for query_idx in random_sample(batch.num_rows(), sample_size) {
        let ground_truth = brute_force_knn(batch, query_idx, 20);
        let domino_result = strategy.query(&index, batch, query_idx, ground_truth[19].1);
        
        let found = domino_result.iter()
            .filter(|idx| ground_truth.iter().any(|(gt_idx, _)| gt_idx == *idx))
            .count();
        
        total_recall += found as f64 / ground_truth.len() as f64;
    }
    
    total_recall / sample_size as f64
}
```

**Success criteria**: Recall > 0.95 for noise=0.1, > 0.85 for noise=0.3. Below that the Domino chains are too fragmented.

**Key question answered**: Does DN-Tree miss cross-branch resonance? If recall drops significantly vs Full-Sweep at high noise, we need more aggressive bridge scanning.

#### T4: Update Cost (the million-hashtable question)

```rust
fn test_update_storm(strategy: &impl DominoBuilder, batch: &RecordBatch) {
    let mut index = strategy.build(batch);
    let n = batch.num_rows();
    
    // Simulate: 10% of containers fold WAL commits (new Q3)
    let changed: Vec<(usize, [u64; 32])> = (0..n/10)
        .map(|_| {
            let idx = rand::random::<usize>() % n;
            let mut new_q3 = extract_q3(batch, idx);
            // XOR with a random commitment (simulating bind)
            let commitment: u64 = rand::random();
            new_q3[0] ^= commitment;
            (idx, new_q3)
        })
        .collect();
    
    let start = Instant::now();
    for (idx, new_q3) in &changed {
        strategy.update(&mut index, batch, *idx, new_q3);
    }
    let elapsed = start.elapsed();
    
    println!("Updated {}% containers in {:?}", 10, elapsed);
    println!("Per update: {:?}", elapsed / changed.len() as u32);
    
    // Verify recall didn't collapse
    let recall = test_recall(strategy, batch /* with updates applied */, 100);
    println!("Post-update recall: {:.3}", recall);
}
```

**This is the critical test.** If 100K updates in a million-container index take >100ms, the real-time resonance network won't work. Target: <1μs per update.

#### T5: Drift Stability

```rust
fn test_progressive_drift(strategy: &impl DominoBuilder, batch: &RecordBatch) {
    let mut index = strategy.build(batch);
    
    // Progressively drift containers and measure recall decay
    for drift_pct in [1, 5, 10, 20, 50] {
        apply_random_drift(&mut index, batch, drift_pct);
        let recall = test_recall(strategy, batch, 100);
        println!("After {}% drift: recall={:.3}", drift_pct, recall);
    }
    
    // Question: at what drift % do we need a full rebuild?
    // DN-Tree hypothesis: never (local repairs suffice)
    // Full-Sweep hypothesis: at ~30% drift, chains degrade
}
```

---

## 4. Implementation Roadmap

### Phase 0: Scaffolding (do this first)

```
□ Cargo workspace: neo4j-rs-domino/
  ├── core/          — Superblock type, quadrant accessors, Hamming SIMD
  ├── gen/           — Test data generator (clustered containers)
  ├── domino-full/   — Strategy A implementation
  ├── domino-dn/     — Strategy B implementation  
  └── bench/         — Criterion benchmarks + recall tests
```

```toml
# Cargo.toml workspace
[workspace]
members = ["core", "gen", "domino-full", "domino-dn", "bench"]

[workspace.dependencies]
arrow = { version = "53", features = ["ffi"] }
datafusion = "43"
criterion = "0.5"
rand = "0.8"
```

### Phase 1: Core (2-3 sessions)

```
□ Superblock type with From<&[u8; 1024]> (zero-copy from Arrow)
□ SIMD Hamming: portable (count_ones loop) + #[cfg(target_feature = "avx512f")]
□ Arrow RecordBatch ↔ Superblock zero-copy bridge
□ Brute-force KNN as ground truth oracle
□ Test data generator with controlled clustering
```

### Phase 2: Strategy A — Full-Sweep (2-3 sessions)

```
□ LSH signature computation (SimHash on Q3)
□ Sort-and-window chain builder
□ DominoIndex struct with chain traversal
□ Incremental update (single container drift)
□ Benchmarks T1, T3 at 10K and 100K
```

### Phase 3: Strategy B — DN-Tree (2-3 sessions)

```
□ Mock DN-tree (hardcoded 3-level hierarchy, 64 leaves)
□ Registration: container → DN leaf by Q3 prefix
□ Local chain builder per leaf
□ Bridge entry computation at parent level
□ Same benchmarks T1, T3 at 10K and 100K
```

### Phase 4: Head-to-Head (1-2 sessions)

```
□ Full test matrix (T1-T6)
□ Recall comparison at varying noise levels
□ Update storm test (the million-hashtable question)
□ Drift stability curves
□ Decision: A, B, or hybrid
```

### Phase 5: Integration (2-3 sessions)

```
□ Winner integrated into DataFusion as custom ExecutionPlan
□ ResonanceScan operator: query Q3 → Domino traversal → matching indices
□ WAL integration: append-only commits, fold-on-read
□ NARS negotiation hook in Q1 (post-resonance filter)
□ End-to-end: Cypher-like query → DataFusion plan → Domino scan → results
```

---

## 5. Session Contract

**Any Claude session working on this MUST**:

1. Read this document first. Do not reinvent the schema.
2. Use the exact types from Section 1.3. Do not rename quadrants.
3. Q0=Meta, Q1=Edges/NARS, Q2=Nodes, Q3=CAM/Routing. This is final.
4. Domino index is a THIN OVERLAY on immutable Arrow batches. Never mutate containers.
5. All mutations go through WAL append → fold-on-read.
6. Test against brute-force ground truth. No "it probably works."
7. Report: build time, query latency, recall@20, update cost per op.
8. Do not introduce serde or serialization between containers and index. Zero-copy or nothing.

**Architecture decisions already made** (do not reopen):

- Edges are emergent (Hamming resonance), not stored
- Containers are immutable Arrow FixedSizeBinary(1024)
- XOR bind for commitment, XOR unbind for plasticity
- WAL is append-only, fold-on-read for self-healing
- SIMD Hamming is the distance metric, not cosine, not L2
- Domino chains use relative offsets, not absolute pointers
- DataFusion is the query engine, Arrow is the memory format
- LanceDB integration via shared Arrow batches (not through Lance API)

**Open decisions** (these are what we're testing):

- Full-sweep bootstrap vs DN-tree bottom-up (THIS TEST)
- Optimal chain length (too short = many hops, too long = linear scan)
- Bridge entry density for DN-tree strategy
- LSH function choice for full-sweep (SimHash vs MinHash on binary)
- Rebuild threshold: at what drift % is a full rebuild cheaper than patching
- Q3 prefix allocation for DN-tree registration (how many bits = DN address vs free resonance)

---

## 6. Decision Framework

After running T1-T6, score each strategy:

| Criterion | Weight | A wins if... | B wins if... |
|-----------|--------|-------------|-------------|
| Build time | 15% | LSH bootstrap < 10s for 1M | Always faster (no cold start) |
| Query recall | 30% | > 0.95 at noise=0.3 | > 0.90 at noise=0.3 AND no cross-branch blind spots |
| Query latency | 20% | < 100μs per resonance query at 1M | Same or better |
| Update cost | 25% | < 1μs per WAL fold update | < 1μs AND bounded by leaf size |
| Drift stability | 10% | Recall > 0.90 after 20% drift | Same or better without rebuild |

**Hybrid option**: Use DN-tree for initial structure + full-sweep refinement passes on bridge entries. This is likely the actual answer but we need the data to prove it.

---

*This document is the single source of truth for the neo4j-rs Domino index work. Save it. Reference it. Do not diverge from it.*
