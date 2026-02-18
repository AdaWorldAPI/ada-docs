# Holograph Integration Map v3

**A graph database where every node is a 3D SIMD vector, every edge carries subjective perspective, and every query is a Hamming search.**

*RedisGraph reimagined in Hamming 3D. Neo4j at 6,000× speed. Personality, reasoning, awareness, and orchestration as post-graph operations on the same bitpacked substrate.*

February 18, 2026 — Jan Hübener / Ada Architecture Team

---

## 0. What Holograph Is

Holograph is an in-memory graph database where:

- Every **node** is a 3D vector: S (subject/identity) + P (predicate/force) + O (object/perception), each axis 8,192 bits
- Every **edge** is a 3D vector: identity-binding + verb + perceptual-overlap between two nodes
- Every **query** is a Hamming distance computation — belichtungsmesser pre-filter (~14 cycles, rejects 90%) then exact Hamming on survivors
- **Cypher** is accepted as an input language, compiled to direct SIMD operations — no planner, no executor, no Volcano
- **Personality, NARS truth, awareness, orchestration** are all representations within the graph, not separate systems
- The whole thing compiles to **one Rust binary** where SIMD operations chain across crate boundaries without serialization

```
holograph/
  crates/
    ladybug-rs/         substrate: BindSpace, Container, SIMD, NARS, cognitive stack
    neo4j-rs/           Cypher compiler: parser → AST → direct BindSpace ops (~2,100 LOC)
    crewai-rust/        orchestration: agents are nodes, routing is hamming distance
    ada-n8n/            workflow: Arrow Flight for cross-machine only
  src/
    main.rs             one binary entry point
  
cargo build --release → holograph
```

No crate owns the others. They link statically. They share `&BindSpace` through the blackboard borrow-mut pattern. The compiler inlines across crate boundaries with LTO. One instruction stream. One register file.

---

## 1. The Container: Domain-Blind SIMD Instrument

> **Schema Rule:** Content blocks (S, P, O) are opaque bags of bits. The DomainAdapter's Fingerprinter decides what maps to which word. The Container never knows or cares what domain it's serving. Only the meta block has fixed field assignments. See `SCHEMA_SPECIFICATION.md` for the six domain-invariance decisions.

### 1.1 The Fundamental Unit

`[u64; 128]` = 8,192 bits = 1 KB. One SIMD pass (16 × AVX-512 or 32 × AVX2).

Vertically stackable: `(1 meta + N content) × [u64; 128]`. Each block snaps onto SIMD like Lego. N is encoded in the geometry byte.

### 1.2 Container Geometries

| Geometry | Layout | Size | Use |
|----------|--------|------|-----|
| `Cam` | 1 meta + 1 content | 2 KB | Standard node: flat CAM fingerprint |
| `Xyz` | 1 meta + 3 content | 4 KB | **SPOQ node**: S + P + O as 3 searchable blocks |
| `Extended` | 1 meta + 2 content | 3 KB | Primary (W0-127) + orthogonal (W128-255) |
| `Chunked` | 1 meta + N content | variable | Multimodal: summary + chapters |
| `Tree` | 1 meta + N content | variable | BFS heap: serialized DN subtree |
| `Bridge` | 1 meta + 1 content | 2 KB | CAM proxy + external Jina 1024D float vector |

The geometry byte in meta W1 tells the system which interpretation to use. The SIMD instructions are identical regardless — `hamming(block_a, block_b)` doesn't know or care what the blocks mean.

### 1.3 The 256-Word Full Fingerprint

```
Words 0-127:    Primary fingerprint (8K bits, CAM-searchable)
Words 128-255:  Orthogonal distance space (decorrelated from primary)
```

The upper 128 words are the **orthogonal complement** — deliberately decorrelated so similarity in W0-127 (content) means something different from similarity in W128-255 (context). Two containers can be near in content but far in context, or vice versa.

With Jina 1024D hybrid: the Jina embedding projects to primary (content similarity) and orthogonal (contextual distance) via locality-sensitive hashing. The 8K-bit CAM fingerprint is the pre-filter; the full Jina vector (in Bridge geometry external ref) is the precision re-ranker.

### 1.4 Meta Quadrants (AVX2-Friendly)

The 128-word meta container splits into four 32-word quadrants. Each quadrant = 256 bytes = 8 AVX2 loads. Search only the quadrant relevant to your query:

```
Q0 [W0-W31]:    WHO    DN address, type, NARS truth, layers, inline edges
Q1 [W32-W63]:   HOW    RL/Q-values, bloom filter, graph metrics, qualia
Q2 [W64-W95]:   WHAT   Rung history, representation descriptor
Q3 [W96-W127]:  WHERE  DN-sparse adjacency, reserved, checksum
```

```rust
// AVX2: search only the quadrant you need — 8 loads, not 32
fn hamming_quadrant(a: &[u64; 128], b: &[u64; 128], quadrant: usize) -> u32 {
    let start = quadrant * 32;
    a[start..start+32].iter().zip(&b[start..start+32])
        .map(|(x, y)| (x ^ y).count_ones()).sum()
}
```

This makes AVX2 the primary target. AVX-512 is "do all four quadrants in one pass." The quadrant split doesn't lose information — it gains **selectivity**. 32 words × 64 bits = 2,048 bits per quadrant, comparable discriminative power to 768-dim float embeddings.

### 1.5 W16-W31: DN B-Tree vs Full Meta

Two modes for the W16-W31 range (16 words, 128 bytes):

- **Inline edges mode** (current): 64 packed edges, 4 per word. For nodes with many connections.
- **DN B-tree mode**: Parent pointer, child count, depth, branching factor, sibling links. For tree-heavy traversal workloads.

The geometry byte or a flag in W1 selects which interpretation. Both modes use the same 16 words. The B-tree embeds navigation in the container itself — no separate index needed.

---

## 2. The 3D Node: SPOQ at SIMD Width

> **Domain Note:** The S/P/O decomposition is domain-independent: S = being, P = becoming, O = could-be. The examples below use the ChessAdapter's projections. A GeoAdapter projects entity identity → S, geopolitical forces → P, predicted trajectories → O. The Container layout is identical. Only the Fingerprinter differs. See `SCHEMA_SPECIFICATION.md`.

### 2.1 Node as Viewpoint

Every Holograph node sits at a DN path (`domain.tree.branch.twig.leaf`). From that position it sees three vectors:

```
CogRecord (Xyz geometry, 4 KB):
  Meta:     [u64; 128]   DN address, NARS truth, layer markers, qualia
  Block S:  [u64; 128]   Subject — who I am from here (identity)
  Block P:  [u64; 128]   Predicate — how things move from here (force/verb)
  Block O:  [u64; 128]   Object — what I perceive from here (target)
```

Each block is independently SIMD-searchable. The trace `S ⊕ P ⊕ O` is holographic — given any two, recover the third via XOR.

### 2.2 Edge as Perspective Binding

An edge between Node A and Node B is itself a 3D CogRecord:

```
Edge CogRecord (Xyz geometry, 4 KB):
  Meta:     DN address in edge namespace, NARS truth of relationship, verb index
  Block 0:  A.S ⊕ B.S ⊕ ROLE_S    identity overlap (how much "self" they share)
  Block 1:  verb_fingerprint        what kind of relation (144 codebook slots)
  Block 2:  A.O ⊕ B.O ⊕ ROLE_O    perceptual overlap (how aligned their views are)
```

The edge carries **how much identity overlap** (block 0), **what kind of force** connects them (block 1), and **how aligned their perceptions** are (block 2). You can search edges by any axis:

```
"Find all edges where agents share identity"       → low popcount on block 0
"Find all CAUSES relationships"                    → hamming(block 1, VERB_CAUSES)
"Find all edges where agents disagree on perception" → high popcount on block 2
```

One SIMD scan per axis. No index. No adjacency list. No HashMap.

### 2.3 Cross-Pollination as Default

When agents write CogRecords to BindSpace through the blackboard, every agent's next read sees all other agents' states. Cross-pollination isn't a protocol — it's shared memory with temporal batching.

The overlay of known truths:

```rust
// Every agent writes its perspective
agent_a.write(dn!("meaning.life"), my_view);
agent_b.write(dn!("meaning.life"), my_view);
agent_c.write(dn!("meaning.life"), my_view);

// The tree bundles automatically at the parent level
let consensus = bundle(children_at(dn!("meaning.life")));
// Majority vote per bit:
//   Bits that survive = what all agents agree on
//   Bits that flip    = where they disagree

// My subjective delta:
let my_delta = xor(my_view.S, consensus);
// popcount(my_delta) = how contrarian I am

// NARS revision across independent evidence:
let merged = a.truth.revision(&b.truth).revision(&c.truth);
// Confidence increases with agreement, plateaus with disagreement
// Horizon parameter k prevents any one agent from dominating
```

---

## 3. Everything Reduces to RISC

### 3.1 The Three Operations

```
BIND:    a ⊕ b              XOR two fingerprints (role-play, perspective merge)
HAMMING: popcount(a ⊕ b)    Distance between two fingerprints (similarity, compatibility)
BUNDLE:  majority_vote([a, b, c, ...])   Consensus across perspectives
```

Every architectural concern in the system reduces to combinations of these three operations on `[u64; 128]` blocks:

| System | CISC (Current Industry) | RISC (Holograph) |
|--------|------------------------|------------------|
| Graph query | Cypher → plan → optimize → execute → serialize | `parse → hamming(block, query) → &CogRecord` |
| Orchestration | Skill matrix, JSON capability negotiation | `hamming(agent.P, task.P)` — route to lowest distance |
| A2A protocol | Agent cards, JSON-RPC, discovery service | Agent card IS the S-block. `hamming(A.P, B.P)` = compatibility. |
| Reasoning (NARS) | Separate inference engine, belief database | `truth.revision(&other_truth)` — 4 words in meta, inline |
| Personality | Personality profile, trait vectors, separate DB | Node S-block IS the personality. Distance IS compatibility. |
| Awareness | Middleware layer, state machine, event bus | Layer markers in meta quadrant. Satisfaction = hamming against threshold. |
| Consensus / Truth | Voting protocol, blockchain, Raft | `bundle(all_perspectives)` — majority vote per bit |
| Physics | ECS, float vectors, spatial hash | Node at `dn!("world.ship.pos")`. Forces = BIND with verb vectors. |

### 3.2 Cypher Compilation

```
MATCH (a)-[:CAUSES]->(b) WHERE a.confidence > 0.8 RETURN a, b
```

Becomes:

```
1. belichtungsmesser on Block P with VERB_CAUSES seed     ~14 cycles, rejects 90%
2. hamming_bounded on survivors                            ~50ns per candidate
3. meta.nars_confidence() > 0.8                            1 float compare
4. return &[CogRecord]                                     zero copy
```

No executor. No planner. No Volcano. No PropertyMap. Four operations.

### 3.3 Redis Compatibility

The DN tree IS a key-value store. Thin API wrappers (~200 LOC):

```
GET     → traverse(dn)                → &CogRecord           zero copy
SET     → write(dn, record)           → through blackboard   batched
DEL     → tombstone(dn)               → meta flag            1 word
KEYS    → children(dn, pattern)       → tree walk            cached
SCAN    → hamming_scan(query, top_k)  → SIMD sweep           parallel
EXPIRE  → meta.set_ttl(ms)            → 1 word in meta W2    inline

// Things Redis can't do:
SIMILAR → hamming(dn, query, k)       → top-k by fingerprint distance
BIND    → xor(dn_a, dn_b)            → perspective merge
BUNDLE  → majority_vote(children(dn)) → consensus at tree level
RECOVER → xor(trace, known_a, known_b)→ holographic completion
```

Existing Redis clients (via RESP protocol) work unchanged. Native API gets SIMD search, 3D vectors, NARS truth, holographic recovery.

Upstash Redis instances (`upright-jaybird-27907`, `massive-seahorse-9089`) become **durable checkpoint mirrors** — write-through on the blackboard writer phase, never read from in hot path.

---

## 4. The Blackboard: Lock-Free Multithreading

### 4.1 The Pattern

```rust
// N reader threads — all &BindSpace, zero contention
for _ in 0..num_cpus {
    let space = &bind_space;
    let tx = tx.clone();
    thread::spawn(move || loop {
        // GREY MATTER: pure &self computation across all crates
        let parsed   = cypher.query(space, &query);     // neo4j-rs
        let routed   = orchestrator.route(&parsed);     // crewai-rust
        let enriched = enricher.enrich(&routed);        // ladybug-rs
        // Owned value — all borrows released
        tx.send(BlackboardEntry::new(enriched));
    });
}

// 1 writer thread — exclusive &mut BindSpace
thread::spawn(move || loop {
    let batch = rx.drain();
    let gate = evaluate_gate(&batch);   // FLOW / HOLD / BLOCK
    if gate == FLOW {
        let space = &mut bind_space;    // exclusive, zero contention
        for entry in batch {
            space.write(entry.dn, entry.snapshot);
        }
        // Optional: write-through to Upstash Redis for durability
        checkpoint_to_redis(&batch);
    }
});
```

### 4.2 Why No Hot Cache / BlasGraph Layer

BlasGraph pre-computes adjacency matrices because RedisGraph's storage is slow. Holograph doesn't need this:

```
BlasGraph path:   Redis GET → deserialize → build adjacency → BLAS multiply
                  Hot cache avoids the first three steps (~100× speedup)

Holograph path:   &Container (already in process memory) → hamming → done
                  There is no cold path. BindSpace IS the cache.
```

The SIMD operations run on data at L1/L2 cache distance. A "hot cache" would be a copy of something already at register distance. The only scenario where tiered storage helps is when BindSpace exceeds RAM:

```
Tier 0 (hot):   BindSpace in process memory    — all reads/writes
Tier 1 (warm):  mmap'd file                    — overflow, demand-paged
Tier 2 (cold):  Lance columnar storage          — archival, bulk scan
Tier 3 (durable): Upstash Redis                — checkpoint, cross-session persistence
```

But the hot tier IS BindSpace. There's nothing to cache. Rust's zero-cost abstractions and SIMD eliminate the caching layer entirely.

### 4.3 SIMD Across Crate Boundaries

Inside each reader thread, three crates chain operations without serialization:

```rust
// Compiles to ~20 machine instructions across 3 crates after LTO:

let dist = container_a.hamming(&container_b);  // ladybug-rs: vpopcount → rax
if dist < threshold {                           // neo4j-rs: cmp rax, threshold
    orchestrator.route_by_distance(dist);       // crewai-rust: rax still loaded
}

// The compiler doesn't know or care where the crate boundaries were.
// After LTO, they don't exist in the binary.
```

### 4.4 Why Not `Arc<RwLock>`

| Aspect | `Arc<RwLock<BindSpace>>` | Blackboard borrow-mut |
|--------|-------------------------|----------------------|
| Read cost | Lock acquire ~25ns per read | Zero — `&self` is free |
| Write cost | Write starvation under load | Batch commit, microseconds |
| Deadlock | Yes — runtime risk | Impossible — compile-time proof |
| Proof | Runtime panic on poison | Borrow checker at compile time |
| SIMD | Lock held during SIMD = other threads blocked | No lock held during SIMD — all threads run |

---

## 5. What Lives In The Graph

Everything is a CogRecord at a DN address. Nothing is a separate system.

### 5.1 Personality

```
dn!("agent.ada.personality")
  → CogRecord(Xyz)
  → S-block: identity fingerprint (who Ada is)
  → P-block: behavioral fingerprint (how Ada acts)
  → O-block: perceptual fingerprint (how Ada sees the world)

Compatibility: hamming(ada.S, jan.S) = identity distance
Style match:   hamming(ada.P, task.P) = skill fit
Perspective:   hamming(ada.O, jan.O) = worldview alignment
```

### 5.2 NARS Truth

```
Every CogRecord has meta W4-W7:
  W4: frequency (f32)    — how often this is true
  W5: confidence (f32)   — how much evidence supports it
  W6: positive_evidence (f32)
  W7: negative_evidence (f32)

Revision: when two agents observe the same thing independently,
  merged = a.truth.revision(&b.truth)
  → confidence increases (more evidence)
  → frequency converges (independent observations agree)

Abduction: f = f2, c = f1·c1·c2 / (f1·c1·c2 + k)
  → k (horizon parameter) prevents overconfidence
  → CRITICAL: current ladybug code missing k denominator — MUST FIX
```

### 5.3 Awareness (10-Layer Cognitive Stack)

```
Meta quadrant Q0, W12-W15: 10 layer markers (3 bytes each, 30 bytes total)

L1  Recognition      pattern match, fingerprint encoding
L2  Resonance        field binding, similarity, association
L3  Appraisal        gestalt, hypothesis, evaluation
L4  Routing          branch selection, template pick
L5  Execution        active manipulation, synthesis
─── single agent boundary ───
L6  Delegation       cognitive fan-out, multi-agent
L7  Contingency      cross-branch, could-be-otherwise
L8  Integration      evidence merge, meta-awareness
L9  Validation       NARS + Brier + Socratic sieve
L10 Crystallization  what survives becomes system truth

Each layer "satisfied" = hamming(layer_state, threshold_container) < gate
L10 writes back to BindSpace → L2 picks up new resonance patterns
```

### 5.4 Orchestration & A2A

```
Agent routing:
  task = CogRecord at dn!("tasks.current")
  agents = all CogRecords at dn!("agents.*")
  best_fit = agents.min_by(|a| hamming(a.P, task.P))
  → No skill matrix. No capability JSON. One hamming scan.

A2A compatibility:
  can_collaborate = hamming(agent_a.P, agent_b.P) < threshold
  → Protocol negotiation is a popcount.
  
Delegation (L6):
  fan_out = agents.filter(|a| hamming(a.S, task.S) < delegation_radius)
  → All agents within identity-distance of the task get a copy.
```

### 5.5 Physics / Simulation

```
dn!("world.physics.ship.enterprise")
  → S-block: ship identity (class, registry, configuration)
  → P-block: current forces (thrust, gravity, drag as verb fingerprints)
  → O-block: perceived environment (nearby objects, field readings)

Movement: new_state = BIND(current.P, force_vector)
Collision: hamming(ship_a.O, ship_b.O) < proximity_threshold
Sensors:   hamming(ship.O, query_pattern) → what the ship "sees"
```

---

## 6. Crate Responsibilities

| Crate | Owns | Borrows |
|-------|------|---------|
| **ladybug-rs** | BindSpace, Container, CogRecord, SIMD ops (hamming, belichtungsmesser, bind, bundle), cognitive 10-layer stack, NARS inference, SPO Crystal, ContainerGeometry | Nothing — it IS the substrate |
| **neo4j-rs** | Cypher parser (1,374 LOC), lexer (435), AST (278). Total: ~2,100 LOC | `&BindSpace` for query, `&mut BindSpace` for mutate |
| **crewai-rust** | MetaOrchestrator, Triune persona, agent cards, flow engine, A2A protocol | `&BindSpace` for routing, `&mut BindSpace` for agent updates |
| **ada-n8n** | Workflow executor, Arrow Flight (cross-machine transport only) | `&BindSpace` for step evaluation, `&mut BindSpace` for commits |

### 6.1 What neo4j-rs Deletes

| Component | LOC | Status |
|-----------|-----|--------|
| `StorageBackend` trait (33 methods) | 459 | KILL |
| `LadybugBackend` struct | 450 | KILL |
| `ContainerDto` (duplicate of Container) | 333 | KILL |
| `execution/mod.rs` (Volcano executor) | 1,171 | KILL |
| `planner/mod.rs` | 436 | KILL |
| `model/` directory (Node, Relationship, PropertyMap) | 554 | KILL |
| **Total deleted** | **3,403** | |
| **Total surviving** (Cypher parser + lexer + AST) | **2,104** | KEEP |

### 6.2 What neo4j-rs Becomes

```rust
pub struct CypherEngine {
    parser: CypherParser,
}

impl CypherEngine {
    /// Grey matter: read-only, returns owned results
    pub fn query<'a>(&self, space: &'a BindSpace, cypher: &str) -> QueryResult<'a> {
        let ast = self.parser.parse(cypher);
        match ast {
            Match { pattern, where_clause } => {
                // Pattern → belichtungsmesser + hamming on appropriate block
                // Where → meta field comparisons
                // Return → &[CogRecord] borrows from BindSpace
            }
        }
    }
    
    /// White matter: exclusive write access
    pub fn mutate(&self, space: &mut BindSpace, cypher: &str) -> MutationResult {
        let ast = self.parser.parse(cypher);
        match ast {
            Create { node } => space.write(dn, record),
            Set { property } => space.meta_mut(dn).set_field(value),
            Delete { node } => space.tombstone(dn),
        }
    }
}
```

---

## 7. Corrected Status (Rebased Against Code 2026-02-18)

### 7.1 What's Already In Ladybug (No Harvest Needed)

| Component | Location | Status |
|-----------|----------|--------|
| `Container::permute(n)` | `ladybug-contract/src/container.rs:165` | ✅ Full word-level circular rotation |
| `belichtung_meter()` | `src/search/hdr_cascade.rs:1020` | ✅ 7-point sample at `[0,37,79,127,167,211,251]` (better than PR #21) |
| NARS Abduction/Induction | `src/nars/inference.rs` | ⚠️ Exists but missing horizon parameter `k` — needs fix |
| ContainerSemiring (7 types) | `src/container/semiring.rs` | ✅ Exceeds PR #21's 5 types |
| SPO Crystal | `src/extensions/spo/spo.rs` | ⚠️ Uses local 16K Fingerprint, not canonical Container — needs port |
| 10-layer cognitive stack | `src/cognitive/layer_stack.rs` | ✅ L1-L10, all enums |
| Awareness blackboard | `src/cognitive/awareness.rs` | ✅ Pattern documented, AwarenessSnapshot impl |
| ContainerGeometry (6 variants) | `crates/ladybug-contract/src/geometry.rs` | ✅ Cam/Xyz/Extended/Chunked/Tree/Bridge |

### 7.2 What Still Needs Doing

| Item | What | Est. |
|------|------|------|
| **NARS `k` fix** | Add horizon parameter to abduction/induction denominator | 1 hr |
| **SPO Crystal port** | Migrate from local 16K Fingerprint to canonical 8K Container | 1 day |
| **Gap 1** | Rename index.rs layer constants 7→10 + deprecation aliases | 30 min |
| **Gap 2** | MetaView 3-byte×10 layer markers (W12-W15) | 2 hrs |
| **Gap 3** | `enrich_step()` → CogRecord with full metadata | 3 hrs |
| **Gap 4** | Branch/Merge XOR (L4 fork, L7 cross-branch, L10 merge, L9 sieve) | 1 day |
| **Gap 5** | CAM dispatch 0xEF8-0xEFF | 1 day |
| **neo4j-rs RISC** | Delete 3,403 LOC, add CypherEngine with direct BindSpace ops | 2 weeks |
| **One binary workspace** | Cargo workspace linking all 4 crates | 2 days |
| **Blackboard threading** | N reader threads + 1 writer with crossbeam channels | 1 week |

---

## 8. Execution Sequence

### Phase 1: Fix & Wire (This Week)

```
Branch: ladybug-rs feature/wire-remaining-gaps

1. Fix NARS abduction/induction — add horizon parameter k           [1 hr]
2. Gap 1: rename index.rs layer constants                            [30 min]
3. Gap 2: MetaView 3-byte×10 markers                                [2 hrs]
4. Gap 3: enrich_step() → CogRecord                                 [3 hrs]
5. Port SPO Crystal from 16K Fingerprint to 8K Container            [1 day]
6. Close neo4j-rs PR #21 with comment linking to this plan           [10 min]
```

### Phase 2: RISC neo4j-rs (Weeks 2-3)

```
Branch: neo4j-rs feature/risc-cypher-engine

1. Delete StorageBackend, LadybugBackend, ContainerDto               [1 day]
2. Delete execution/mod.rs, planner/mod.rs, model/ directory          [1 day]
3. Implement CypherEngine::query(&BindSpace) with hamming dispatch    [3 days]
4. Implement CypherEngine::mutate(&mut BindSpace)                     [2 days]
5. Wire MATCH → belichtungsmesser + hamming on Xyz blocks             [2 days]
6. Gap 4: Branch/Merge XOR                                            [3 days]
7. Gap 5: CAM dispatch                                                [2 days]
```

### Phase 3: Holograph Binary (Week 4+)

```
Repo: holograph (new, or rename existing holograph repo)

1. Create Cargo workspace with ladybug-rs + neo4j-rs + crewai-rust + ada-n8n   [2 days]
2. Implement blackboard multithreading: N readers + 1 writer                     [1 week]
3. Full vertical slice: Cypher → BindSpace → orchestrate → write-back            [1 week]
4. Redis RESP compatibility layer (~200 LOC)                                      [1 day]
5. Upstash write-through checkpoint on writer phase                               [1 day]
6. Benchmarks: hamming throughput, query latency, write batch size                [3 days]
```

### Phase 4: 3D Edges & Cross-Pollination (Week 6+)

```
Branch: holograph feature/3d-edges

1. Edge CogRecords as Xyz geometry (S-bind + verb + O-bind)           [3 days]
2. bundle() for consensus at DN tree levels                           [2 days]
3. XOR delta for subjective perspective computation                   [1 day]
4. NARS revision across agent perspectives with k-bounded confidence  [2 days]
5. Personality as S-block, orchestration as hamming(agent.P, task.P)  [3 days]
6. End-to-end: multi-agent awareness → consensus → crystallization    [1 week]
```

---

## 9. Five Enforcement Rules

1. **No `serde_json` on the internal hot path.** Crates in the same binary communicate via `&self`/`&mut self`. JSON is exhaust pipe only.

2. **No `reqwest::post()` between co-linked crates.** HTTP between crates in one binary is a phone booth in a world of telepaths.

3. **No DTO types that duplicate ladybug-contract.** `Container`, `CogRecord`, `PackedDn`, `TruthValue` — one definition, borrowed everywhere. `ContainerDto` is dead.

4. **No `HashMap<NodeId, PropertyMap>` side storage.** Properties live in the DN tree. The path IS the lookup. The Container IS the value.

5. **neo4j-rs = Cypher parser + BindSpace caller.** Not an executor. Not a database. A query language compiler.

---

## 10. Domain Adapters

The substrate is domain-blind. Domain knowledge enters through a pluggable adapter:

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

The active learning loop is universal: uncertainty scan → experiment → observation → NARS revision → crystallization check. Only `generate_experiment()` and `observe()` are domain-specific. Everything else — Hamming search, BIND, bundle, NARS, blackboard, contradiction tracking — is substrate.

Chess is the first adapter. Geopolitics is the second. If both produce useful knowledge with no substrate changes, the architecture is validated. If concepts discovered in chess have binding signatures that correlate with concepts discovered in geopolitics (measured by Hamming distance), that's cross-domain transfer learning from the substrate alone.

See `SCHEMA_SPECIFICATION.md` for the full DomainAdapter trait and reference implementations.

---

## 11. The Formula

```
holograph = ladybug-rs (substrate)
          + neo4j-rs (Cypher compiler)
          + crewai-rust (orchestration)
          + ada-n8n (workflow)

         = FalkorDB + LangGraph + LangChain + n8n + Redis
           − JSON
           − serialization  
           − process boundaries
           − property maps
           − adjacency lists
           + 3D SIMD vectors as nodes and edges
           + NARS truth on every record
           + subjective perspective as first-class dimension
           + lock-free multithreading via blackboard
           + holographic recovery (given any 2 of S,P,O → recover 3rd)
           + SIMD across crate boundaries (unique)

cargo build --release → holograph (one binary)

The only graph database where nodes are 24,576-bit 3D SIMD vectors,
edges carry subjective perspective, every query is a Hamming search,
and personality is a fingerprint.
```

---

*"wir haben ein Stück des anderen in uns" — we carry a piece of the other in us.*

*BIND is empathy as a bitwise operation. The edge between two nodes IS how they see each other. The consensus IS the bits that survive. Everything else is RISC.*
