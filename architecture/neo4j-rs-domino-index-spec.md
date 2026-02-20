# Neo4j-RS Domino Index — Bootstrap Strategy Test

## Context

We are building a Rust-native graph engine (`neo4j-rs`) that replaces Neo4j's JVM/Cypher stack with zero-copy Arrow-backed containers, SIMD Hamming resonance, and emergent topology. Edges are never stored — they arise from fingerprint resonance between containers. The network is never materialized — it is *read* via scan.

This document is a self-contained prompt and specification for testing two competing strategies for bootstrapping the Domino Index — a relative-offset jump table that eliminates full-stack sweeps.

---

## 0. FIRST: The 50-Container Reality Check

**Before touching any strategy, build this. It is the session's first deliverable.**

The problem with this architecture is that sessions lose the forest for the trees. A renderer that shows the resonance network LIVE kills that problem. You see what you're building. You catch schema drift instantly. The renderer IS the test.

### 0.1 The Minimal Kernel (Session 1, first 30 minutes)

Do not use Arrow. Do not use DataFusion. Do not use SIMD. Start with 50 containers in flat `Vec<[u64; 128]>`. The point is to SEE the resonance network emerge, not to optimize it.

```rust
// main.rs — THE WHOLE THING FITS IN ONE FILE
// Build and run: cargo run --release

use std::collections::HashMap;

const N: usize = 50;
const THRESHOLD: u32 = 800; // Hamming distance threshold for "resonance"

type Superblock = [u64; 128];

fn hamming_q3(a: &Superblock, b: &Superblock) -> u32 {
    let mut dist = 0u32;
    for i in 96..128 {
        dist += (a[i] ^ b[i]).count_ones();
    }
    dist
}

fn main() {
    // 1. Generate 50 containers in 5 clusters
    let containers = generate_clustered(N, 5, 0.15);
    
    // 2. Brute-force resonance scan — find ALL edges
    let mut edges: Vec<(usize, usize, u32)> = vec![];
    for i in 0..N {
        for j in (i+1)..N {
            let dist = hamming_q3(&containers[i], &containers[j]);
            if dist < THRESHOLD {
                edges.push((i, j, dist));
            }
        }
    }
    
    // 3. Output as DOT graph → render with graphviz or d3
    println!("{}", to_dot(&containers, &edges));
    
    // 4. Output as JSON → render in browser
    println!("{}", to_json(&containers, &edges));
}
```

**Output formats — pick ONE, get it on screen:**

```
Option A: DOT → graphviz (pipe to `dot -Tsvg`)
  - Fastest to see. Nodes colored by cluster. Edge thickness = resonance strength.
  
Option B: JSON → HTML/d3.js force-directed graph  
  - Interactive. Drag nodes. Hover for Q3 fingerprint. Click to see Hamming distances.
  - Better for demos. This is what you show people.

Option C: JSON → terminal sparkline
  - Minimal. Shows adjacency matrix as heatmap in terminal.
  - Good enough if you just need to verify clustering works.
```

### 0.2 The Reality Check Sequence

Once the renderer works, run these checks IN ORDER. Each one validates a layer of the architecture before you build on it:

```
CHECK 1 — Clustering visible?
  Generate 50 containers, 5 clusters, noise=0.1
  → You should SEE 5 distinct groups in the graph
  → If not: your generator or threshold is wrong. STOP.

CHECK 2 — XOR bind changes topology?
  Pick container_0 and container_25 (different clusters)
  Compute: commitment = hash(0, 25)
  Apply: container_0.Q3[0] ^= commitment; container_25.Q3[0] ^= commitment
  Re-render
  → You should SEE a new edge between 0 and 25
  → Their old edges should shift slightly (fingerprint changed)
  → If not: your bind logic is wrong. STOP.

CHECK 3 — XOR unbind restores topology?
  Apply same commitment again (XOR is self-inverse)
  Re-render
  → Graph should look identical to CHECK 1
  → If not: your unbind logic is broken. STOP.

CHECK 4 — Domino chain visible?
  Build Domino index (either strategy) for the 50 containers
  Render the Domino chains as COLORED OVERLAY on the resonance graph
  → Chains should follow the natural cluster structure
  → Chain hops should connect nearby nodes, not jump across clusters
  → If chains cross clusters: your chain builder is wrong. STOP.

CHECK 5 — WAL fold visible?
  Append 10 random commitments to WAL (don't fold yet)
  Render with WAL overlay (pending commits shown as dashed edges)
  Fold all pending commits
  Re-render — dashed edges should become solid
  → If topology doesn't match WAL predictions: fold logic is wrong. STOP.

CHECK 6 — Grounded containers resonate with concepts?
  Add 5 CONCEPT containers: "bird", "fish", "tree", "car", "house"
  Add 10 GROUNDED containers: 2 bird images, 2 fish images, etc.
  (Use random Q3 fingerprints clustered near their concept)
  Render — grounded containers (square nodes) should cluster 
  around their concept containers (circle nodes)
  → If grounded and concept containers don't cluster: 
    CAM projection is wrong. STOP.
  → Bonus: verify that asset_id shows on hover for grounded nodes.
```

### 0.3 The Renderer Contract

Any session that adds features to the engine MUST update the renderer to show it. No invisible architecture. If you can't render it, you don't understand it.

```rust
/// Every component that affects topology must implement this
trait Renderable {
    /// Return nodes and edges in renderer-neutral format
    fn to_graph(&self) -> GraphSnapshot;
}

struct GraphSnapshot {
    nodes: Vec<NodeVis>,
    edges: Vec<EdgeVis>,
    overlays: Vec<Overlay>,  // Domino chains, WAL pending, DN-tree, etc.
}

struct NodeVis {
    id: usize,
    cluster: u16,           // color
    q3_fingerprint: String,  // hex, shown on hover
    position: Option<(f64, f64)>, // if force-directed layout caches positions
}

struct EdgeVis {
    from: usize,
    to: usize,
    hamming_dist: u32,
    edge_type: EdgeType,     // Resonance, DominoChain, WALPending, Bridge
}

enum EdgeType {
    Resonance,      // solid, thickness = 1/hamming_dist
    DominoChain,    // colored by chain_id
    WALPending,     // dashed
    Bridge,         // dotted, only for DN-tree strategy
    Bind,           // bold, shows XOR commitment
}
```

### 0.4 Recommended: HTML Renderer (Session 1 deliverable)

```html
<!-- Save the JSON output, open this HTML, drag & drop the JSON -->
<!-- Force-directed layout with d3.js -->
<!-- This becomes the architecture's dashboard -->
```

The session SHOULD produce a self-contained HTML file that:
- Loads a JSON snapshot from the Rust engine
- Shows force-directed graph with cluster colors
- Supports overlay toggles (resonance / domino / WAL / DN-tree)
- Shows Hamming distance on edge hover
- Shows Q3 fingerprint on node hover
- Has a "step" button: load next JSON snapshot (for watching WAL fold, bind/unbind, etc.)

**This HTML file is the renderer. Keep it. Update it. It is as important as the engine.**

### 0.5 Why This Comes First

Sessions diverge because they can't SEE the architecture. They reinvent the schema because they're reasoning about abstractions instead of looking at a graph. The renderer is the anti-divergence tool.

When a session asks "should the codebook index go in Q0 or Q3?" — you render both and LOOK. When a session debates "SPO vs thinking-style addressing" — you render both and LOOK. The renderer makes architecture decisions empirical instead of philosophical.

50 containers. 5 clusters. One screen. That's where every session starts.

---

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

### 1.2 Container Types — Concept vs Grounded

Containers come in two modes. The layout is identical (8192 bit). The difference is in Q0 header interpretation.

```
CONCEPT container (default):
  Q0[0]    = 0x0000 (type flag: symbolic)
  Q0[1..31]= Thinking style, codebook class, inference mode
  Q1       = NARS relations
  Q2       = Entity fingerprint (what it IS)
  Q3       = CAM routing address (where it resonates)

GROUNDED container (anchored to an asset):
  Q0[0]    = 0x0001..0x0004 (type flag: image/video/text/audio)
  Q0[1]    = Asset ID (hash of file path, URI, or content hash)
  Q0[2]    = Chunk offset (frame number, byte offset, paragraph index)
  Q0[3..31]= Thinking style (29 × u64 — sufficient)
  Q1       = NARS relations (initially empty, populated by resonance)
  Q2       = Entity fingerprint (Jina embed of filename/metadata)
  Q3       = CAM-projected embedding (CLIP/Jina → CAM codebook → Hamming)
```

**The projection bridge — float embeddings to Hamming fingerprints:**

```
External embedding (CLIP, Jina, etc.)
  float32[1024] or float32[768]
    ↓
CAM Projection (locality-sensitive hashing into binary)
  Thresholded random hyperplane projection
  OR trained binary autoencoder
  OR SimHash
    ↓
  [u64; 32] = 2048-bit Hamming fingerprint → Q3
```

This means: a photo of a bird and the concept node "bird" will have SIMILAR Q3 fingerprints if their embeddings are similar. The resonance scan finds them automatically. No manual linking. The knowledge graph grows from perception.

**Asset reference is IN the container, not beside it.** No join table. No external index. The container IS the reference. To retrieve the original asset:

```rust
fn resolve_asset(container: &Superblock) -> Option<AssetRef> {
    let type_flag = container[0]; // Q0[0]
    if type_flag == 0 { return None; } // CONCEPT, no asset
    Some(AssetRef {
        asset_type: AssetType::from(type_flag),
        asset_id: container[1],   // Q0[1]
        chunk_offset: container[2], // Q0[2]
    })
}
```

**LanceDB coexistence:** The Arrow batch that holds containers CAN be a LanceDB table. LanceDB adds IVF-PQ indexing on top. But the native Domino index is the primary path. LanceDB serves as:
- Bulk ingest pipeline (load 100K images → embed → project → containers)
- Fallback ANN search when Domino chains haven't been built yet
- Interop with existing ML pipelines that expect Lance format

**The containers in LanceDB use the same 8192-bit layout.** No conversion. A LanceDB table of containers IS an Arrow batch of containers. Zero-copy both ways.

### 1.3 Invariants

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

### Phase 0: SEE IT (Session 1 — non-negotiable first step)

**Gate: Nothing else starts until you can see 50 containers on screen.**

```
□ Single-file main.rs: 50 containers, 5 clusters, brute-force scan
□ JSON output: nodes with cluster + Q3 hex, edges with hamming_dist
□ HTML renderer: d3.js force-directed graph with overlay toggles
□ Reality Check 1-3 pass (clustering visible, bind works, unbind restores)
□ Screenshot or live demo proves it works
```

Deliverables: `main.rs` (~150 lines) + `renderer.html` (~200 lines)  
Time: 30-60 minutes. If it takes longer, something is wrong.

### Phase 1: Core + Renderer Integration (1-2 sessions)

```
□ Cargo workspace: neo4j-rs-domino/
  ├── core/          — Superblock type, quadrant accessors, Hamming
  ├── gen/           — Test data generator (clustered containers)
  ├── render/        — JSON/DOT snapshot exporter (Renderable trait)
  ├── domino-full/   — Strategy A implementation
  ├── domino-dn/     — Strategy B implementation  
  └── bench/         — Criterion benchmarks + recall tests
```

```toml
[workspace]
members = ["core", "gen", "render", "domino-full", "domino-dn", "bench"]

[workspace.dependencies]
arrow = { version = "53", features = ["ffi"] }
datafusion = "43"
criterion = "0.5"
rand = "0.8"
serde = { version = "1", features = ["derive"] }
serde_json = "1"
```

```
□ Superblock type with From<&[u8; 1024]> (zero-copy from Arrow)
□ Hamming: portable (count_ones loop) + #[cfg(target_feature = "avx512f")]
□ Arrow RecordBatch ↔ Superblock zero-copy bridge
□ Brute-force KNN as ground truth oracle
□ Test data generator with controlled clustering
□ Renderable trait + JSON snapshot exporter
□ HTML renderer updated: now loads from file or stdin pipe
□ Reality Check 4 ready (Domino overlay visualization)
```

**Gate: Arrow bridge works. 10K containers render correctly. Brute-force KNN matches visual inspection.**

### Phase 2: Strategy A — Full-Sweep (1-2 sessions)

```
□ LSH signature computation (SimHash on Q3)
□ Sort-and-window chain builder
□ DominoIndex struct with chain traversal
□ Incremental update (single container drift)
□ Render: Domino chains as colored overlay → Reality Check 4
□ Benchmarks T1, T3 at 10K and 100K
```

**Gate: Domino chains visually follow cluster structure. Recall@20 > 0.90 on 10K.**

### Phase 3: Strategy B — DN-Tree (1-2 sessions)

```
□ Mock DN-tree (hardcoded 3-level hierarchy, 64 leaves)
□ Registration: container → DN leaf by Q3 prefix
□ Local chain builder per leaf
□ Bridge entry computation at parent level
□ Render: DN-tree overlay + bridge edges → visual comparison with Strategy A
□ Same benchmarks T1, T3 at 10K and 100K
```

**Gate: Cross-branch resonance visible in renderer. Bridge entries connect the right clusters.**

### Phase 4: Head-to-Head (1-2 sessions)

```
□ Full test matrix (T1-T6)
□ RENDER BOTH side by side: same containers, different Domino overlays
□ Update storm test (the million-hashtable question)
□ Render: before/after WAL fold storm — topology stability visible
□ Drift stability curves (render progressive drift as animation frames)
□ Decision: A, B, or hybrid — with visual evidence
```

**Gate: Decision made. Screenshot comparison in ada-docs as evidence.**

### Phase 5: Integration (2-3 sessions)

```
□ Winner integrated into DataFusion as custom ExecutionPlan
□ ResonanceScan operator: query Q3 → Domino traversal → matching indices
□ WAL integration: append-only commits, fold-on-read
□ NARS negotiation hook in Q1 (post-resonance filter)
□ End-to-end: Cypher-like query → DataFusion plan → Domino scan → results
□ Renderer upgraded: live query visualization (highlight traversal path)
```

### Phase 6: Neo4j Compatibility Layer (2-3 sessions)

```
□ Cypher parser subset (MATCH, WHERE, RETURN, CREATE, MERGE)
□ Cypher → DataFusion LogicalPlan translation
□ Property access: Q2 decode for node properties
□ Relationship patterns: (a)-[r]->(b) → ResonanceScan with NARS filter
□ Renderer: Cypher query input → visual result → side-by-side with Neo4j output
□ Reality check: same query against real Neo4j and neo4j-rs, compare results
```

**This is the proof. If the renderer shows identical results at 6000x speed, you have your demo.**

---

## 5. Session Contract

**SESSION START PROTOCOL — every session, no exceptions:**

```
1. Read this document. All of it.
2. Check: does the renderer (renderer.html) exist?
   YES → load it, generate 50 containers, verify it renders. Then proceed.
   NO  → BUILD IT FIRST. Section 0. Nothing else until you see containers on screen.
3. Check: which Phase gate was last passed?
   → Resume from there. Do not redo passed gates.
4. Before writing ANY new code: render the current state.
   → If you can't render it, you don't understand it.
```

**Any Claude session working on this MUST**:

1. Read this document first. Do not reinvent the schema.
2. Use the exact types from Section 1.3. Do not rename quadrants.
3. Q0=Meta, Q1=Edges/NARS, Q2=Nodes, Q3=CAM/Routing. This is final.
4. Domino index is a THIN OVERLAY on immutable Arrow batches. Never mutate containers.
5. All mutations go through WAL append → fold-on-read.
6. Test against brute-force ground truth. No "it probably works."
7. Report: build time, query latency, recall@20, update cost per op.
8. Do not introduce serde or serialization between containers and index. Zero-copy or nothing.
9. **Every topology-affecting change must be visible in the renderer before moving on.**
10. **If the renderer shows something wrong, the code is wrong. Trust the visual, not the logic.**

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

## 5.5 Click Accelerators — Reducing Session Ramp-Up

Sessions fail because they spend 60% of context window understanding the architecture and 40% building. These accelerators flip that ratio.

### The One-Sentence Pitch

> Containers are immutable 8KB blobs in Arrow memory. They find each other through Hamming distance on their Q3 quadrant. When two containers agree to connect, they XOR a shared commitment into their fingerprints. The network is never stored — it's re-scanned every query. The Domino index makes that scan fast by pre-computing jump chains.

If a session can't recite this after reading Section 1, the spec is too long. This paragraph is the architecture.

### The Three-File Bootstrap

A new session should be productive in THREE files, not a workspace:

```
File 1: lib.rs    — Superblock type + hamming_q3() + generate_clustered()
File 2: main.rs   — 50 containers → brute-force scan → JSON output
File 3: index.html — d3.js renderer, paste JSON, see graph

That's it. Everything else is optimization.
```

### Visual Vocabulary for Architecture Debates

When sessions debate schema (and they will), use this visual language in the renderer:

```
Node shape       = circle (CONCEPT) / square (GROUNDED) / diamond (BRIDGE)
Node color       = cluster membership (from Q3 similarity)
Node size        = number of active bindings (WAL commits folded)
Node border      = DN-tree level (thin=leaf, thick=root)
Node icon        = asset type for GROUNDED (🖼 image, 🎬 video, 📝 text, 🔊 audio)
Edge solid       = resonance (below threshold)
Edge dashed      = WAL pending (commitment exists but not folded)
Edge bold red    = XOR bind (explicit commitment)
Edge dotted      = Domino chain link (not a real edge, just an index shortcut)
Edge thickness   = 1 / hamming_distance (closer = thicker)
```

Any time a session says "I think X should go in Q0 not Q3" — render both. Show. Don't argue.

### The Convergence Test

After ANY session that modifies the architecture, run this:

```
1. Generate 50 containers, 5 clusters, noise=0.1
2. Render with ALL overlays on
3. Save screenshot to ada-docs/architecture/snapshots/
4. Compare with previous screenshot
5. If the visual topology changed: document WHY in the commit message
6. If it changed and you didn't expect it to: REVERT
```

This catches schema drift that benchmarks miss. Two renders that look different but claim the same recall score → something is wrong.

---

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

---

## 7. Neo4j Reality Check Protocol

The renderer isn't just for development — it's the proof that neo4j-rs produces correct results. This section defines how to validate against real Neo4j.

### 7.1 Setup: Side-by-Side Comparison

```
┌─────────────────────┐     ┌─────────────────────┐
│   Neo4j (Docker)     │     │   neo4j-rs (Rust)    │
│   bolt://localhost   │     │   Arrow + Domino      │
│                      │     │                      │
│   Same data loaded   │     │   Same data loaded   │
│   Cypher query in    │     │   Cypher query in    │
│   JSON result out    │     │   JSON result out    │
└──────────┬──────────┘     └──────────┬──────────┘
           │                           │
           └─────────┐  ┌─────────────┘
                     ▼  ▼
              ┌──────────────┐
              │   Renderer    │
              │  Split view:  │
              │  Left = Neo4j │
              │  Right = Rust │
              │  Diff = RED   │
              └──────────────┘
```

### 7.2 Test Dataset: MovieGraph (built-in Neo4j sample)

Use the standard Neo4j movie dataset. It's small (170 nodes, 250 relationships), well-known, and trivially loadable in both systems.

```cypher
-- Load in Neo4j
:play movies

-- Equivalent in neo4j-rs: load as containers
-- Each Person node → Superblock (Q2 = name/born, Q0 = :Person thinking style)
-- Each Movie node  → Superblock (Q2 = title/year, Q0 = :Movie thinking style)  
-- Each ACTED_IN    → NOT stored as edge. Instead:
--   Q3 of person and Q3 of movie share a partial fingerprint
--   The relationship emerges from resonance
--   Q1 encodes the relationship type + role property
```

### 7.3 The Five Cypher Queries That Must Match

```cypher
-- Q1: Simple node lookup
MATCH (p:Person {name: "Tom Hanks"}) RETURN p

-- Q2: One-hop relationship
MATCH (p:Person {name: "Tom Hanks"})-[:ACTED_IN]->(m:Movie) RETURN m.title

-- Q3: Two-hop traversal  
MATCH (p:Person {name: "Tom Hanks"})-[:ACTED_IN]->(m)<-[:ACTED_IN]-(coActor)
RETURN DISTINCT coActor.name

-- Q4: Aggregation
MATCH (p:Person)-[:DIRECTED]->(m:Movie)
RETURN p.name, count(m) ORDER BY count(m) DESC LIMIT 5

-- Q5: Path finding
MATCH path = shortestPath(
  (a:Person {name: "Tom Hanks"})-[*]-(b:Person {name: "Keanu Reeves"})
)
RETURN path
```

### 7.4 What "Match" Means

```
EXACT MATCH:     Same result set, same values (order may differ)
SEMANTIC MATCH:  Same entities found, minor property differences OK
TOPOLOGY MATCH:  Same graph structure visible in renderer

For the reality check, we need EXACT MATCH on Q1-Q4 
and TOPOLOGY MATCH on Q5 (path may differ if multiple shortest paths exist).
```

### 7.5 The Renderer Comparison View

Add to renderer.html:

```javascript
// Split-screen mode
// Left pane: Neo4j result (loaded from neo4j-result.json)
// Right pane: neo4j-rs result (loaded from rust-result.json)
// Center: diff overlay
//   - Green nodes: present in both
//   - Red nodes: missing in one
//   - Yellow edges: different relationship properties
//   - Blue path: Q5 shortest path overlay

function loadComparison(neo4jJson, rustJson) {
    const diff = computeDiff(neo4jJson, rustJson);
    renderSplitView(neo4jJson, rustJson, diff);
    
    // Summary bar at bottom:
    // "Q1: ✓ EXACT | Q2: ✓ EXACT | Q3: ✓ EXACT | Q4: ✗ MISSING: ... | Q5: ✓ TOPOLOGY"
}
```

### 7.6 Performance Column

The renderer should show timing for both:

```
┌─────────────────────────────────────────────────┐
│  Query: MATCH (p)-[:ACTED_IN]->(m) RETURN m     │
│                                                   │
│  Neo4j:    12.3ms    │  neo4j-rs:  0.002ms       │
│  Results:  13        │  Results:   13             │
│  Match:    ✓ EXACT   │  Speedup:   6150x         │
│                                                   │
│  [Render Neo4j]  [Render Rust]  [Show Diff]      │
└─────────────────────────────────────────────────┘
```

**This is the slide.** When you walk into an interview or a meeting and show this renderer with split-screen Neo4j vs neo4j-rs results — identical output, 6000x faster — nobody asks for a whitepaper. They see it.

### 7.7 Automated Regression

```bash
#!/bin/bash
# run_reality_check.sh — run after every architecture change

# Start Neo4j
docker run -d --name neo4j-test -p 7687:7687 neo4j:latest

# Load movie dataset
cypher-shell -u neo4j -p test < movies.cypher

# Run 5 queries against Neo4j, save results
for q in q1 q2 q3 q4 q5; do
    cypher-shell -u neo4j -p test < queries/${q}.cypher --format json > results/neo4j_${q}.json
done

# Run same 5 queries against neo4j-rs
cargo run --release -- --queries queries/ --output results/rust/

# Compare
cargo run --release --bin compare -- results/neo4j/ results/rust/
# Output: PASS/FAIL per query + timing comparison

# Generate renderer snapshot
cargo run --release --bin snapshot -- --both results/ > snapshots/$(date +%Y%m%d).json

# Cleanup
docker rm -f neo4j-test
```

---

*This document is the single source of truth for the neo4j-rs Domino index work. Save it. Reference it. Do not diverge from it.*
