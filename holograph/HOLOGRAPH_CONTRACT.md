# HOLOGRAPH CONTRACT
## The Single Source of Truth — Read Before Writing Any Code

**Date:** 2026-02-19  
**Status:** Nothing below is implemented. This document consolidates 14 sessions of architecture work into one clean spec. If this document contradicts any file in `ada-docs/holograph/`, this document wins.

---

## 0. What Holograph Is

An in-memory graph database where every node is a 3D SIMD vector, every edge carries subjective perspective, and every query is a Hamming search. One Rust binary. No JSON on the hot path. No serialization between crates.

```
holograph/
  crates/
    ladybug-rs/       substrate: BindSpace, Container, SIMD, NARS, cognitive stack
    neo4j-rs/         Cypher compiler: parser → AST → direct BindSpace ops
  src/
    main.rs           one binary entry point

cargo build --release → holograph
```

Crates share `&BindSpace` through the blackboard borrow-mut pattern. The compiler inlines across crate boundaries with LTO.

---

## 1. The Container

`[u64; 128]` = 8,192 bits = 1 KB. One SIMD pass.

```rust
struct CogRecord {
    meta:    [u64; 128],  // 1 KB — structured, domain-independent
    block_0: [u64; 128],  // 1 KB — opaque, codebook-indexed
    block_1: [u64; 128],  // 1 KB — opaque, codebook-indexed
    block_2: [u64; 128],  // 1 KB — opaque, codebook-indexed
}
// Total: 4 KB. Fixed geometry. Fixed SIMD alignment.
```

Content blocks are **opaque bags of bits**. The DomainAdapter's Fingerprinter decides what maps where. The Container never knows what domain it serves.

### Container Geometries

| Geometry | Layout | Size | Use |
|----------|--------|------|-----|
| `Cam` | 1 meta + 1 content | 2 KB | Standard node |
| `Xyz` | 1 meta + 3 content | 4 KB | S + P + O searchable |
| `Extended` | 1 meta + 2 content | 3 KB | Primary + orthogonal |
| `Bridge` | 1 meta + 1 content | 2 KB | CAM proxy + external vector |

---

## 2. Meta Block — THE QUADRANT LAYOUT

**Canonical. Do not reassign. Do not reinterpret.**

```
┌─────────────────────────────────────────────────────────┐
│ META BLOCK: 128 words (1,024 bytes)                     │
│                                                         │
│ Q1  W0-W31    CAM           Identity, NARS, codebook    │
│                             routing, timestamps, flags, │
│                             ports, execution state      │
│                                                         │
│ Q2  W32-W63   EDGES         32 inline edge slots        │
│                             Each: target + type +       │
│                             weight + flags (64 bits)    │
│                                                         │
│ Q3  W64-W95   LOWER NODES   32 child/member refs        │
│                             Same slot format as Q2      │
│                                                         │
│ Q4  W96-W127  UNDECIDED     All zeros until decided.    │
│                             Writing here is a BUG.      │
└─────────────────────────────────────────────────────────┘
```

### Q1: CAM (W0-W31) — Named Fields

```
W0:       dn_hash             content address
W1:       flags               [63] node/edge, [62:56] kind,
                              [55:48] codebook_version,
                              [47:32] port_mask/edge_flags,
                              [31:0] general flags
W2:       timestamps          created_at | modified_at (packed)
W3:       observation_count
W4:       codebook_id[0]      which codebook block_0 speaks
W5:       codebook_id[1]      which codebook block_1 speaks
W6:       codebook_id[2]      which codebook block_2 speaks
W7:       resonance_scores    packed u16 × 3
W8:       nars_frequency
W9:       nars_confidence
W10:      nars_expectation
W11:      nars_quality
W12:      source_dn           [EDGES ONLY] (zero for nodes)
W13:      target_dn           [EDGES ONLY] (zero for nodes)
W14:      source_port         [EDGES ONLY] (zero for nodes)
W15:      target_port         [EDGES ONLY] (zero for nodes)
W16-W23:  port_table          [NODES] 8 port descriptors
                              [EDGES] edge type, weight, priority, conditions
W24-W27:  execution_state     state, timestamps, error_hash, exec_id
W28-W31:  delivery/context    [EDGES] delivery semantics
                              [NODES] parent_workflow, group
```

W1[63] distinguishes node (0) from edge (1). W12-W15 are zero for nodes. W16-W23 differ by record type. This is fine — one bit selects interpretation.

### Q2: EDGES (W32-W63) — 32 Inline Edge Slots

```
Each word = one edge reference:
  [63:48]  target_dn_short     16-bit truncated hash (filter, not lookup)
  [47:32]  edge_type           16-bit verb hash
  [31:16]  weight_or_strength  16-bit fixed-point
  [15:0]   flags_and_port      [15:8] flags, [7:0] port index
```

**Concept bindings ARE edges.** "Record activates concept #47" is stored as `{ target=concept_47.dn_short, type=ACTIVATES, strength=0.85 }`. Not a separate mechanism. Not a bit vector. An edge.

Overflow beyond 32: separate edge CogRecords (W1[63]=1) with full content blocks and NARS.

### Q3: LOWER NODES (W64-W95) — 32 Child Refs

Same slot format as Q2. Encodes parent→child containment: workflow→steps, document→sections, concept→members, codebook→entries.

Q2 = lateral (peer-to-peer). Q3 = vertical (parent-to-child).

### Q4: UNDECIDED (W96-W127)

All zeros. Not assigned. Code that reads W96-W127 must handle all-zeros. Code that writes W96-W127 is a bug.

---

## 3. The Fingerprint Is a Codebook Presence Vector

**Not LSH. Not random projections.** Each bit = one concept in a learned vocabulary.

```
Codebook construction:
  1. Chunk domain data into semantic units
  2. Embed each chunk → 1024D float (Jina)
  3. Cluster into 8,192 centers per axis → codebook
  4. Encode: for each of 8,192 concepts, if similarity > threshold → set bit

Fingerprint = multi-hot encoding over learned vocabulary
Hamming distance = concept overlap
XOR = which specific concepts differ (interpretable)
```

### Codebook Multiplexing

Blocks are codebook-indexed, not axis-fixed. Meta W4/W5/W6 say which codebook each block speaks.

S/P/O is the **default convention** (being/becoming/could-be). Not a constraint. A chess adapter might use `CHESS_POSITION / CHESS_DYNAMICS / SPATIAL_GEOMETRY` instead.

When no codebook resonates with new content → orphan pool → accumulate → crystallize new codebook. That's brain plasticity.

### Multipass Cascade

```
qidx (8 bits)        → 256 buckets, O(1) selection
INT4 sketch (512b)   → topic distribution, rejects 90%
Belichtungsmesser     → 7 discriminative words, rejects 90% of survivors
Full Hamming (8,192b) → exact concept comparison, final rank
```

---

## 4. Two Primitives: Nodes and Edges

Everything is a CogRecord. W1[63] distinguishes them.

```
NODE: W1[63]=0
  Content blocks: domain-projected fingerprint (opaque)
  Q1: identity + NARS + ports + execution
  Q2: 32 outgoing edge refs (lateral)
  Q3: 32 child refs (vertical)

EDGE: W1[63]=1
  Content blocks: relationship content + context + XOR delta
  Q1: W12-W15 = source_dn, target_dn, source_port, target_port (MANDATORY)
  Block 2 = XOR(source.block_0, target.block_0) → transformation signature
```

Edge topology is ALWAYS explicit. No implicit edges. Traversal reads meta only, never touches content blocks.

---

## 5. The Three Operations

```
BIND(a, b):     a XOR b           perspective merge, transformation
HAMMING(a, b):  popcount(a XOR b)  distance, similarity, compatibility
BUNDLE(a,b,c):  majority_vote      consensus, prototype, personality
```

Everything reduces to these on `[u64; 128]` blocks.

---

## 6. Domain Adapters

```rust
trait DomainAdapter {
    type Input;
    type Experiment;
    type Observation;

    fn fingerprint(&self, input: &Self::Input) -> CogRecord;
    fn generate_experiment(&self, contradiction: &Contradiction) -> Self::Experiment;
    fn observe(&self, experiment: &Self::Experiment) -> Self::Observation;
    fn outcome(&self, observation: &Self::Observation) -> f32;
}
```

The active learning loop is universal:
```
loop {
    hottest = contradiction_scan()           // substrate
    experiment = adapter.generate(hottest)   // domain-specific
    observation = adapter.observe(experiment) // domain-specific
    nars.revise(adapter.outcome(observation)) // substrate
    check_crystallization()                   // substrate
}
```

Steps 1, 4, 5 = substrate. Steps 2, 3 = adapter. Same code, any domain.

---

## 7. Blackboard Borrow-Mut Pattern

```
N reader threads:  &BindSpace (zero contention, all crates chain freely)
1 writer thread:   &mut BindSpace (exclusive, batch commit via crossbeam channel)
```

No `Arc<RwLock>`. No runtime deadlocks. Borrow checker proves safety at compile time. SIMD runs lock-free on all reader threads.

---

## 8. neo4j-rs = Cypher Compiler, Nothing Else

**Delete:**
- StorageBackend trait (459 LOC)
- LadybugBackend (450 LOC)
- ContainerDto (333 LOC) — duplicates ladybug Container
- execution/mod.rs Volcano executor (1,171 LOC)
- planner/mod.rs (436 LOC)
- model/ directory (554 LOC)
- **Total: 3,403 LOC killed**

**Keep:**
- Cypher parser (1,374 LOC)
- Lexer (435 LOC)
- AST (278 LOC)
- **Total: ~2,100 LOC surviving**

**Becomes:**
```rust
pub struct CypherEngine { parser: CypherParser }

impl CypherEngine {
    pub fn query(&self, space: &BindSpace, cypher: &str) -> QueryResult;
    pub fn mutate(&self, space: &mut BindSpace, cypher: &str) -> MutationResult;
}
```

MATCH → belichtungsmesser + hamming. CREATE → space.write(). No planner. No executor. No Volcano.

---

## 9. Five Enforcement Rules

1. **No `serde_json` on the hot path.** JSON is exhaust pipe only.
2. **No `reqwest::post()` between co-linked crates.** They share `&BindSpace`.
3. **No DTO types duplicating ladybug-contract.** `Container`, `CogRecord`, `TruthValue` — one definition.
4. **No `HashMap<NodeId, PropertyMap>`.** The DN tree IS the lookup.
5. **neo4j-rs = parser + BindSpace caller.** Not a database. A compiler.

---

## 10. Validation Ladder

| Step | Domain | Proves | Ground Truth |
|------|--------|--------|-------------|
| 1 | Chess | Substrate learns | Win/loss → Elo |
| 2 | AIWar | Handles fog of war | Win rate vs AI |
| 3 | WikiLeaks | Reads real intelligence | Historical hindsight (Brier) |
| 4 | Wikipedia | Scales (6.8M articles) | Category rediscovery rate |
| 5 | Live politics | Generalizes | Prediction accuracy (Brier) |
| 6 | Cross-domain | Concepts transfer | Binding signature correlation |

Same substrate. Same operations. Same loop. Only the adapter changes.

---

## 11. What Exists in Code (ladybug-rs)

| Component | Location | Status |
|-----------|----------|--------|
| Container `[u64; 128]` | ladybug-contract | ✅ exists |
| CogRecord | ladybug-contract | ✅ exists |
| BindSpace (8-bit prefix:address) | src/storage/bind_space.rs | ✅ exists |
| MetaView/MetaViewMut | src/container/meta.rs | ✅ zero-copy views |
| ContainerGraph | src/container/graph.rs | ✅ DN-keyed |
| belichtung_meter() | src/search/hdr_cascade.rs | ✅ 7-point sample |
| ContainerSemiring (7 types) | src/container/semiring.rs | ✅ |
| ContainerGeometry (6 variants) | ladybug-contract/geometry.rs | ✅ |
| NARS inference | src/nars/inference.rs | ⚠️ missing horizon `k` |
| SPO Crystal | src/extensions/spo/spo.rs | ⚠️ uses 16K Fingerprint, needs port to 8K Container |
| 10-layer cognitive stack | src/cognitive/layer_stack.rs | ✅ L1-L10 |

## 12. What Exists in Code (neo4j-rs)

| Component | LOC | Verdict |
|-----------|-----|---------|
| Cypher parser | 1,374 | KEEP |
| Lexer | 435 | KEEP |
| AST | 278 | KEEP |
| StorageBackend trait | 459 | DELETE |
| LadybugBackend | 450 | DELETE |
| ContainerDto | 333 | DELETE |
| Volcano executor | 1,171 | DELETE |
| Planner | 436 | DELETE |
| Model directory | 554 | DELETE |

---

## 13. Known Violations in ada-docs/holograph/

These files contain errors. Do NOT follow their meta layouts:

| File | Error | What's Wrong |
|------|-------|-------------|
| INTEGRATION_MAP_v3.md | §1.4 Meta Quadrants | Assigns Q0=WHO, Q1=HOW, Q2=WHAT, Q3=WHERE (content labels, not structure) |
| SCHEMA_SPECIFICATION.md | §Decision 2 meta layout | W32-W63 = "concept binding signatures" as flat bit vector |
| CODEBOOK_MULTIPLEXING.md | §1 meta layout comment | W32-W63 = "concept binding signatures", W64-W127 = "reserved" |
| EDGE_CONTRACT.md | §2 Node Meta, §3 Edge Meta | W32-W63 = "CONCEPT BINDING SIGNATURES", W64-W95 = "LABEL SPACE" |
| CHESS_BRAIN_PLASTICITY.md | §1.1 Meta layout | W32-W63 = concept binding as 64 slots × 4 bytes |

**Correct answer (this document, §2):** Q2 W32-W63 = EDGES (32 inline edge slots). Q3 W64-W95 = LOWER NODES. Q4 W96-W127 = UNDECIDED.

### What's GOOD in those files (use these parts):

| File | Good Sections |
|------|--------------|
| CAM_CODEBOOK.md | ALL — codebook pipeline, cascade, concept algebra |
| SCHEMA_SPECIFICATION.md | Decisions 1,3,4,5,6 — domain-blind principles, DomainAdapter trait |
| CODEBOOK_MULTIPLEXING.md | §2-§10 — resonance selection, crystallization, meta-think, contracts 1-10 |
| EDGE_CONTRACT.md | §1 two primitives, §4 content blocks on edges, §5-§9 YAML mapping, traversal, execution protocol |
| INTEGRATION_MAP_v3.md | §0 what holograph is, §2-§5 3D node/RISC/blackboard/what lives in graph, §6-§9 crate map/status/phases |
| CHESS_BRAIN_PLASTICITY.md | §1.2-§7 XOR network, brain plasticity experiment, cross-domain transfer |
| VALIDATION_LADDER.md | ALL |
| POLITICAL_INTELLIGENCE.md | ALL |
| META_QUADRANTS.md | ALL — this IS ground truth |

---

## 14. GROUND TRUTH TESTS

Before any phase is "done," these must pass. They are mechanical, binary, no interpretation needed.

### Phase 0: Workspace Compiles

```
TEST P0.1: `cargo build --release` in holograph workspace succeeds
           with ladybug-rs and neo4j-rs as workspace members.
           
TEST P0.2: neo4j-rs has zero references to StorageBackend, LadybugBackend,
           ContainerDto, PropertyMap, execution/mod.rs, planner/mod.rs.
           grep -r "StorageBackend\|LadybugBackend\|ContainerDto\|PropertyMap" neo4j-rs/src/
           → 0 matches.

TEST P0.3: neo4j-rs Cargo.toml has no dependency on serde_json, reqwest, or tokio.

TEST P0.4: `cargo test` passes in both crates independently AND in workspace.
```

### Phase 1: Meta Layout Correct

```
TEST P1.1: MetaView::edges() returns &[u64] over W32-W63 (32 words).
           MetaView::lower_nodes() returns &[u64] over W64-W95 (32 words).
           
TEST P1.2: MetaViewMut::set_edge(slot, target_dn_short, edge_type, weight, flags)
           writes to W32+slot with the packed format:
           [63:48]=target_dn_short, [47:32]=edge_type, [31:16]=weight, [15:0]=flags.

TEST P1.3: Fresh CogRecord has W96-W127 all zeros.
           assert!(record.meta[96..128].iter().all(|w| *w == 0));

TEST P1.4: MetaView::is_edge() reads W1[63].
           MetaView::source_dn() reads W12 (returns 0 for nodes).
           MetaView::codebook_ids() reads (W4, W5, W6).
```

### Phase 2: Cypher → BindSpace Direct

```
TEST P2.1: CypherEngine::query(&space, "MATCH (n) RETURN n")
           returns all CogRecords in BindSpace. No intermediate types.
           Return type borrows from BindSpace (lifetime tied to &space).

TEST P2.2: CypherEngine::mutate(&mut space, "CREATE (n {dn: 'test.node'})")
           writes a CogRecord to BindSpace at dn_hash("test.node").
           space.get(dn_hash("test.node")) returns Some(&CogRecord).

TEST P2.3: After CREATE, the created record's W32-W63 are valid edge slots
           (all zeros if no edges specified, or populated if edges given).
           NOT "concept binding signatures."

TEST P2.4: No serde_json::Value anywhere in the query→result path.
           grep -r "serde_json" neo4j-rs/src/ → 0 matches (or only in tests/bench).
```

### Phase 3: Blackboard Threading

```
TEST P3.1: 4 reader threads + 1 writer thread. Readers call
           CypherEngine::query(&space, ...) concurrently.
           No panics, no deadlocks, no data races.
           (Borrow checker enforces this — if it compiles, it works.)

TEST P3.2: Writer batches entries from crossbeam channel.
           After write, all subsequent reader queries see the new data.

TEST P3.3: No Arc<RwLock> or Mutex in the hot path.
           grep -r "RwLock\|Mutex" holograph/src/ → 0 matches
           (crossbeam channel internals don't count).
```

### Phase 4: NARS Fix

```
TEST P4.1: nars::abduction(f1, c1, f2, c2, k) includes horizon parameter k
           in denominator. Result: c = f1*c1*c2 / (f1*c1*c2 + k).
           With k=1: abduction({f:0.8, c:0.9}, {f:0.7, c:0.8}, k=1.0)
           → c = 0.8*0.9*0.8 / (0.8*0.9*0.8 + 1.0) = 0.576 / 1.576 ≈ 0.365.

TEST P4.2: Without k fix (current bug), confidence would be unbounded.
           Regression test: assert!(result.confidence < 1.0) for any finite input.
```

### Phase 5: One Binary End-to-End

```
TEST P5.1: `cargo build --release` produces exactly 1 binary.
           ls target/release/holograph → exists, is executable.

TEST P5.2: Binary accepts Cypher string on stdin or CLI arg,
           executes against in-memory BindSpace, returns results.
           echo 'CREATE (n {dn: "test"})' | ./holograph
           echo 'MATCH (n) RETURN n' | ./holograph → returns 1 record.

TEST P5.3: No network calls in the hot path.
           strace ./holograph 2>&1 | grep -c "connect\|sendto" → 0
           (during query execution, not startup).
```

---

## 15. What This Document Does NOT Decide

These are open questions. Don't implement them yet:

- **Q4 (W96-W127) assignment** — wait for implementation experience
- **C-block (5th KB per CogRecord)** — proposed in UNIVERSAL_SUBSTRATE.md, not committed
- **Meta-think codebook** — proposed in CODEBOOK_MULTIPLEXING.md §5, not committed
- **crewai-rust / ada-n8n integration** — future phases, not in scope
- **Arrow Flight cross-machine transport** — future, only needed when distributed
- **Redis RESP compatibility layer** — nice to have, not blocking
