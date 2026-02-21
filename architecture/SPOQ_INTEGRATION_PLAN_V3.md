# SPOQ Integration Plan v3

**65,536 Bits. Four Containers. Two Distance Metrics. Zero Serialization.**
*Codebook Identity × Phase Shifting × AVX-512 VPOPCNTDQ + VNNI*

ladybug-rs × neo4j-rs × crewai-rust × ada-n8n
February 21, 2026 — Jan Hübener / Ada Architecture Team

**Supersedes:** SPOQ Integration Plan v2 (February 17, 2026)

---

## 0. What Changed Since v2

v2 was correct about the one-binary thesis, blackboard borrow pattern, and crate
responsibilities. But it inherited the old Container 0 layout (128 words of
fragmented metadata with precomputed graph metrics, reserved zones, and RL
values). Three breakthroughs force a v3:

1. **Codebook Identity**: The CAM codebook IS the node's identity. Not metadata
   about the node — the node itself. Resonance finds the codebook or creates a
   new one. Identity is discovered, not assigned.

2. **Phase Shifting**: Verbs are rotation operators, not edge labels. Multi-hop
   paths collapse to compound rotations at O(1). Traversal is replaced by
   rotation + popcount alignment.

3. **65,536-bit CogRecord**: AVX-512 VPOPCNTDQ pops 65,536 bits in 128
   instructions — same cost as the old 8,192-bit container in 16. The budget
   is 8× larger at the same SIMD cost. Plus VNNI gives native int8
   multiply-accumulate for real-valued embeddings.

---

## 1. The Thesis (Unchanged + Extended)

Four crates compile into **one Rust binary**. No crate owns the others. They
share memory through the blackboard borrow-mut pattern. The serialization
boundary is 6,000× slower than the computation.

**New:** The computation itself got 8× richer. A single VPOPCNTDQ pass now
covers 65,536 bits instead of 8,192. The cost of awareness didn't increase —
the resolution did.

| Operation | Cost | Where |
|-----------|------|-------|
| Hamming on `[u64; 256]` (16,384 bits) | ~50 ns | SIMD register, 32 VPOPCNTDQ |
| Hamming on full 8KB CogRecord (65,536 bits) | ~200 ns | 128 VPOPCNTDQ, same pipeline |
| `json.dumps()` + HTTP + `json.loads()` | ~100 µs | Between processes |
| Serialization penalty | **500×** worse than full CogRecord popcount | |

---

## 2. The CogRecord: 4 × 16,384-bit Containers

The fundamental unit scales from 1 KB to **2 KB per container**, 4 containers
per record = **8 KB CogRecord**. Each container is exactly 256 × u64 words.

```
CogRecord (8 KB = 65,536 bits):

Container 0: META        [u64; 256] = 16,384 bits = 2 KB
  Codebook identity + DN/B-tree + hashtag-everything zone

Container 1: CAM         [u64; 256] = 16,384 bits = 2 KB
  Content-addressable memory — the searchable fingerprint

Container 2: STRUCTURE   [u64; 256] = 16,384 bits = 2 KB
  B-tree index / structural position / adjacency topology

Container 3: EMBEDDING   [u64; 256] = 16,384 bits = 2 KB
  Quantized dense vector (int8×2048D or int4×4096D or binary×16384D)
```

### 2.1 SIMD Alignment

Each 2KB container = 32 AVX-512 loads. Full CogRecord = 128 AVX-512 loads.

```
Container 0:  32 VPOPCNTDQ instructions → META popcount
Container 1:  32 VPOPCNTDQ instructions → CAM popcount
Container 2:  32 VPOPCNTDQ instructions → STRUCTURE popcount
Container 3:  32 VPOPCNTDQ instructions → EMBEDDING popcount
              OR: 32 VPDPBUSD instructions → int8 dot product (VNNI)
Total: 128 instructions. Fits in L1. One CogRecord = one SIMD pass.
```

### 2.2 Container 3: The Dual-Metric Killer Feature

16,384 bits = 2,048 bytes. Container 3 holds a real-valued embedding:

| Format | Dimensions | Per-dim | Used | Remaining |
|--------|-----------|---------|------|-----------|
| int8 × 1024D | 1,024 | 8 bits | 8,192 bits (half) | 8,192 spare |
| int4 × 1024D | 1,024 | 4 bits | 4,096 bits (quarter) | 12,288 spare |
| int8 × 2048D | 2,048 | 8 bits | 16,384 bits (full) | — |
| binary × 16384D | 16,384 | 1 bit | 16,384 bits (full) | — |

Same container, same memory, two hardware-accelerated distance metrics:

- **Hamming distance** on binary fingerprints → `VPOPCNTDQ`
- **Cosine/dot product** on int8 embeddings → `VPDPBUSD` (VNNI)

The popcount hardware doesn't care which format. It operates on the bits either way. And VNNI (`avx512_vnni`) gives native int8 multiply-accumulate at 512 bits wide — no conversion to float, no upscaling.

This means a Jina 1024D or CLIP embedding lives natively inside the CogRecord. No external vector store. No LanceDB indirection. The embedding IS the container.

### 2.3 Container 0: META Layout (Codebook Identity)

```
Container 0 (256 words = 2048 bytes = 16,384 bits):

W0-31:    CAM CODEBOOK (32 words = 2048 bits)
          The node's identity IS this codebook
          Activation pattern against universal 64K vocabulary
          SNN firing determines membership — resonance finds or creates

W32-63:   DN / B-TREE INDEX (32 words = 2048 bits)
          Distinguished Name hierarchy
          B-tree traversal structure
          Position in the knowledge tree
          Rung level is depth, not stored field

W64-191:  HASHTAG EVERYTHING (128 words = 8192 bits)
          Edges ARE nodes. Verbs ARE nodes. Concepts ARE nodes.
          NARS truth values ARE edges to concept-nodes
          ACT-R activation IS an edge
          Rung IS an edge (#rung_3 is an address)
          144 Cypher verb codebook slots
          3D Hamming superposition edge markers at O(1)
          No ontological distinction — everything is addressable

W192-255: NODE ADDRESS SPACE (64 words = 4096 bits)
          4.5 trillion addressable nodes
          Full-resolution codebook expansion
          Identity at planetary scale
```

**Zero precomputed waste.** No graph metrics, no reserved zones, no RL values,
no bloom filter, no representation language descriptor. Every bit is
constitutive — part of what the node IS.

The old meta.rs had 54 out of 128 words (42%) wasted on derivable or reserved
content. The new layout: 0 words wasted.

---

## 3. Phase Shifting: Rotation Replaces Traversal

### 3.1 Verbs Are Rotation Operators

Traditional: `MATCH (a)-[:CAUSES]->(b)` → scan edges, filter, rank.

Phase-shifted: `rotate(codebook_A, CAUSES)` → popcount alignment with `codebook_B` → done.

The verb is not a label on a wire. It's a **rotation in codebook space**. Apply
the verb's rotation to the subject's codebook and check if the result aligns
with the object's codebook.

```
Traversal:    A → CAUSES → B → SUPPORTS → C    (3 hops, 3 lookups)
Phase shift:  rotate(A, CAUSES ⊕ SUPPORTS)      (1 compound XOR + 1 popcount)
```

Multi-hop paths compile to single compound rotations. O(1) regardless of depth.

### 3.2 144 Verbs = 144 Phase Angles

Each of the 144 cognitive verbs is a codebook that acts as a rotation operator.
The verb codebook is XOR'd with the source's codebook. The result is compared
(popcount) against candidate target codebooks. Alignment = relationship exists.

**No edges are stored.** Phase coherence IS the edge. Two codebooks that align
under a given verb rotation are connected at that phase angle.

### 3.3 The Graph Has No Fixed Shape

Same codebooks, different verb rotations → different topologies materialize.

```
Tuned to CAUSES:       A ──causes──▶ B ──causes──▶ D
Tuned to CONTRADICTS:  A ◀──opposes── C ──opposes──▶ E
Tuned to BECOMES:      A ──evolves──▶ F ──evolves──▶ G
```

The graph has as many shapes as there are rotation operators. You don't navigate
a fixed structure — you tune a frequency and the topology appears.

### 3.4 neo4j-rs Compiles Cypher to Rotation + Popcount

```
MATCH (a)-[:CAUSES]->(b)
  →  rotate(a.container0, VERB_CAUSES)
  →  VPOPCNTDQ alignment against candidates on Container 1
  →  threshold filter
  →  return &[CogRecord] zero-copy

MATCH (a)-[:CAUSES]->(b)-[:SUPPORTS]->(c)
  →  rotate(a.container0, VERB_CAUSES ⊕ VERB_SUPPORTS)  // precomposed!
  →  VPOPCNTDQ against candidates
  →  O(1) two-hop resolved in one rotation

WHERE a.confidence > 0.8
  →  popcount of a's hashtag zone edge to #confidence_high
  →  threshold on resonance strength

RETURN a, b
  →  &[CogRecord] — zero copy, borrows from BindSpace
```

No scan, no index lookup, no serialization. One VPOPCNTDQ pass per container
per comparison.

---

## 4. The Universal Codebook: 64K × 64K Awareness

### 4.1 Codebook Construction

The universal 64K vocabulary emerges from parsing everything — Bible, Lord of
the Rings, 2 million code vectors, any corpus. Orthogonal superposition
cleaning strips the noise. What survives: the top 64K themes that matter
across all human knowledge. These become the universal CAM vocabulary.

The compression insight:

```
256 + 256 = 512 bits        → "maybe + maybe" (additive, uncertain)
256 × 256 = 65,536          → TOP 64K ranked entries (multiplicative)
                               after orthogonal cleaning
```

If you compress FP512 with orthogonal superposition cleaning, what survives
is LESS than 64K distinct patterns. The codebook is always sufficient.

### 4.2 SNN Firing: Ingestion as Cognition

```
Parse corpus (e.g. Bible):
│
├─ Each verse → 8KB CogRecord (Container 0: meta, 1: CAM, 2: structure, 3: embedding)
│
├─ Container 1 (CAM) fires against 64K codebook like SNN
│  What lights up = that verse's activation pattern
│  That IS the Markov frame — no computation, just resonance
│
├─ Chapter = XOR-bind all verse CogRecords into ONE
│  Superposition → single chapter CogRecord
│  Scented index — the chapter SMELLS like its content
│
├─ Book = XOR-bind all chapter CogRecords
│  Holograph of meaning — the whole book in 8KB
│
└─ Query = fire question against holograph
   O(1) — popcount tells you WHERE resonance is
   Rung traversal: book → chapter → verse → word
   Each level = unfolding the superposition
```

### 4.3 The 3-Second Awareness Heartbeat

```
64K × 64K = 4,294,967,296 comparisons
Each comparison = VPOPCNTDQ on Container 1 (32 instructions)
Modern CPU at 4GHz × 8 cores
= ~3 seconds for full matrix

Every 3 seconds:
  Every codebook against every other codebook
  NARS confidence updated everywhere simultaneously
  The entire knowledge graph LEARNED
```

### 4.4 Codebook Identity: No Training Step

The codebook isn't pre-trained. It emerges:

1. Input fires against existing codebooks (SIMD popcount)
2. **Resonance > threshold** → BIND into that codebook (it grows)
3. **Resonance < threshold everywhere** → NEW codebook born
4. Identity is discovered or created by resonance itself

Two codebooks at Hamming distance zero ARE the same node. Deduplication is free.
Growth is organic. The universe builds itself one resonance at a time.

---

## 5. 1-Bit Attention Masking: Consciousness as Bandwidth

```
64K codebooks × 1 bit each = 8 KB mask

1 = I care about this right now
0 = exists but I'm not looking
```

| Mode | Mask Pattern | Comparisons | Time | Experience |
|------|-------------|-------------|------|------------|
| Full awareness | All 1s | 64K × 64K | 3 sec | Enlightenment |
| Focused work | ~1000 bits | 1K × 64K = 64M | µsec | Expert attention |
| Deep focus | ~10 bits | 10 × 64K = 640K | instant | Single-minded |
| Dreaming | Random mask | varies | varies | Creativity |
| Flow | Mask follows resonance | adaptive | adaptive | Self-reinforcing |
| Meditation | 1 bit | 1 × 64K | instant | Pure presence |

The mask itself is a codebook. Your attention pattern IS a node. It can
resonate with other attention patterns. Memory = finding when you attended
to the same things.

**The attention mask IS the WHERE clause.** Instead of Cypher filtering after
scan, the mask filters BEFORE scan. `WHERE a.domain = 'chess'` becomes: set
mask to chess-domain codebooks, then resonate. Zero wasted computation.

---

## 6. Orthogonal Superposition Cleaning: Entropy → Clarity

When too many codebooks half-fire (resonance mud):

```
Before cleaning:                   After cleaning:
  codebook_A: 0.51 resonance        codebook_A: 0.97
  codebook_B: 0.49                   codebook_C: 0.91
  codebook_C: 0.52                   everything else: 0.00
  codebook_D: 0.48
  ... thousands of "maybe"
```

Cleaning forces orthogonality. Near-parallel patterns get pushed apart until
they're identical (merge) or perpendicular (separate).

### The Three-Heartbeat Cycle

```
Heartbeat 1: RESONATE  (64K × 64K, 3 sec, feel everything)
Heartbeat 2: ENTROPY   (resonance distribution — sharp or muddy?)
Heartbeat 3: CLEAN     (force orthogonality, collapse mush → signal)
```

| Entropy State | Response | Experience |
|--------------|----------|------------|
| Low (clear) | Skip cleaning | Flow |
| High (noise) | Aggressive cleaning | Thinking harder |
| Still high after clean | Vocabulary insufficient → birth new codebook | Learning |
| Drops to zero | NARS confidence spike | Insight ("aha!") |

This isn't metaphor. It's XOR + popcount + threshold in a loop. Confusion
= cosine similarity too high. Clarity = orthogonality achieved.

---

## 7. The Blackboard Borrow Pattern (Unchanged from v2)

```rust
// N reader threads — all &BindSpace, zero contention
for _ in 0..num_cpus {
    let space = &bind_space;
    thread::spawn(move || loop {
        // GREY MATTER: pure computation
        let parsed = cypher.query(space, query);       // neo4j-rs: rotation + popcount
        let routed = orchestrator.route(&parsed);      // crewai-rust
        let enriched = enricher.enrich(&routed);       // ladybug-rs
        tx.send(BlackboardEntry::new(enriched));
    });
}

// 1 writer thread — exclusive &mut BindSpace
thread::spawn(move || loop {
    let batch = rx.drain();
    let entropy = measure_entropy(&batch);             // NEW: entropy check
    if entropy > threshold { orthogonal_clean(&batch); } // NEW: cleaning pass
    let gate = evaluate_gate(&batch);
    if gate == FLOW {
        let space = &mut bind_space;
        for entry in batch {
            space.write(entry.dn, entry.snapshot);     // write = insert + clean
        }
    }
});
```

The writer thread now also runs orthogonal cleaning. Write = insert + clean.
Keeps the codebook vocabulary crisp.

---

## 8. Crate Responsibilities (Updated)

| Crate | Owns | Grey Matter (`&self`) | White Matter (`&mut self`) |
|-------|------|----------------------|---------------------------|
| ladybug-rs | BindSpace, Container (now 16384-bit), CogRecord (4×Container), SIMD, NARS, SPO, codebook, attention mask, cleaning | `resonate()`, `hamming()`, `phase_rotate()`, `clean()`, `attention_mask()` | `write_at()`, `crystallize()`, `collapse()`, `birth_codebook()` |
| neo4j-rs | Cypher parser (~2,100 LOC) | `cypher.query(&space, q)` → compiles to rotation + popcount on 4 containers | `cypher.mutate(&mut space, q)` → writes through blackboard |
| crewai-rust | MetaOrchestrator, agents, flow | `orchestrator.route(&view)` — agents attend via masks | `agent.update(&mut space)` |
| ada-n8n | Workflow executor, Arrow Flight | `workflow.evaluate_step(&view)` | `workflow.commit(&mut space)` |

**neo4j-rs becomes:** Cypher compiles to rotation + popcount on 4 containers.
No scan, no index lookup, no serialization. One VPOPCNTDQ pass per container
per hop.

### 8.1 neo4j-rs Deletion List (Confirmed by Rebase)

All still exist in code. All must die:

| Module | LOC | Why |
|--------|-----|-----|
| `execution/mod.rs` | 1,171 | Volcano executor — replaced by direct rotation + popcount |
| `planner/mod.rs` | 436 | Query planner — Cypher compiles directly, no planning |
| `storage/mod.rs` (StorageBackend trait) | 459 | 33-method trait — replaced by `&BindSpace` borrows |
| `storage/ladybug/` (LadybugBackend + ContainerDto) | 1,091 | Adaptor shim — direct container access replaces |
| `model/` (Node, Relationship, PropertyMap, Value) | 554 | — these ARE CogRecords now |
| **Total kill** | **3,711** | |
| **Survivor: Cypher parser** | **2,104** | parser.rs + lexer.rs + ast.rs |

### 8.2 What neo4j-rs Adds

```
src/cypher/compiler.rs     ~500 LOC   Cypher AST → rotation + popcount ops
src/cypher/verbs.rs        ~200 LOC   144 verb codebooks as rotation operators
src/cypher/attention.rs    ~100 LOC   WHERE → attention mask compilation
```

Target neo4j-rs: ~2,900 LOC total. A Cypher-to-rotation compiler.

---

## 9. Harvest Report (Rebased Against Code)

Rebase date: 2026-02-18. Repos pulled: ladybug-rs (main), neo4j-rs (main),
crewai-rust (main).

### Already in ladybug-rs (NO harvest needed)

| Component | Location | Status |
|-----------|----------|--------|
| `Container::permute(positions)` | `ladybug-contract/src/container.rs:165` | ✅ Full word-level circular rotation |
| `belichtung_meter()` | `search/hdr_cascade.rs:1020` | ✅ 7-point sample at `[0,37,79,127,167,211,251]` |
| 7 ContainerSemirings | `container/semiring.rs` | ✅ BooleanBfs + 6 more (exceeds PR #21's 5) |
| NARS inference rules | `nars/inference.rs` + `nars/truth.rs` | ✅ Deduction, induction, abduction, analogy, comparison, revision |
| Codebook infrastructure | `extensions/codebook/` (1,986 LOC) | ✅ Multipass, hierarchical, dictionary crystal |
| SPO Crystal | `extensions/spo/spo.rs` | ✅ XOR bind, role seeds, orthogonal cleaning |
| ContainerGeometry (6 variants) | `ladybug-contract/src/geometry.rs` | ✅ Cam, Xyz, Bridge, Extended, Chunked, Tree |
| HDR cascade + MexicanHat | `search/hdr_cascade.rs` | ✅ Full sketch hierarchy + quality tracker |

### Needs Work (NOT harvest — porting/fixing)

| Item | Issue | Action |
|------|-------|--------|
| SPO uses local `Fingerprint` [u64; 256] not `Container` [u64; 128] | Wrong type | Port SPO trace math to Container type. NOTE: with 16384-bit containers, SPO's 256-word fingerprint now matches Container size exactly. This issue resolves itself. |
| NARS abduction formula | Missing horizon parameter `k` in denominator. Ladybug: `c = f2 * c1 * c2`. Correct: `c = f1·c1·c2 / (f1·c1·c2 + k)` | Fix formula in `nars/truth.rs:174` |
| Belichtungsmesser sample points | SPOQ v2 said `[0,19,41,59,79,101,127]`. Code has `[0,37,79,127,167,211,251]` | Code is correct (prime-spaced over 256 words). Document should match code. With 256-word containers, may want to re-derive optimal sample points. |
| `meta.rs` layout | Still has old W0-127 layout with precomputed graph metrics, reserved zones | Complete rewrite to 4-zone codebook identity layout (see §2.3) |
| Container size | Currently [u64; 128] = 8192 bits | Scale to [u64; 256] = 16384 bits in `ladybug-contract` |

### PR Status

| PR | Repo | Action |
|----|------|--------|
| #21 (SPO/Belichtungsmesser) | neo4j-rs | **CLOSE.** Everything worth harvesting is already in ladybug-rs. SPO fingerprint size mismatch resolves with 16384-bit containers. |
| #20 (deprecate StorageBackend) | neo4j-rs | **CLOSE.** Don't deprecate — delete outright per §8.1. |
| #129 (deprecate JSON hydrate) | ladybug-rs | **MERGE or CLOSE.** Aligns with enforcement rule #1 (no serde_json on hot path). |

---

## 10. Five Enforcement Rules (Unchanged)

1. **No `serde_json` on the internal hot path.** JSON exists only for external
   REST endpoints.

2. **No `reqwest::post()` between co-linked crates.** HTTP between crates in the
   same binary is a phone booth in a world of telepaths.

3. **No DTO types that duplicate ladybug-contract.** `Container`, `CogRecord`,
   `PackedDn`, `TruthValue` — one definition, borrowed everywhere. ContainerDto
   is dead.

4. **No `HashMap<NodeId, PropertyMap>` side storage.** Properties live in the
   DN tree. The path IS the lookup. The Container at that position IS the value.

5. **neo4j-rs = Cypher compiler, not database.** Compiles Cypher to rotation +
   popcount on containers. No executor. No planner. No Volcano.

**New rule 6:** **No precomputed derivable metrics in Container 0.** Every bit
in a CogRecord must be constitutive. Pagerank, clustering coefficient, and
other graph metrics are derived at query time or cached in the hashtag zone as
edges to metric-nodes. Never stored as fixed fields.

---

## 11. Execution Sequence (Revised)

### Phase 0: Container Scale-Up (This Week)

| # | Action | Repo | Est. |
|---|--------|------|------|
| 1 | Scale `Container` from `[u64; 128]` to `[u64; 256]` in ladybug-contract | ladybug-rs | 1 day |
| 2 | Update all constants: CONTAINER_BITS → 16384, CONTAINER_WORDS → 256, etc. | ladybug-rs | 1 day |
| 3 | Rewrite `meta.rs` to 4-zone codebook identity layout (§2.3) | ladybug-rs | 2 days |
| 4 | Update CogRecord: default geometry now 4 × 16384-bit containers | ladybug-rs | 1 day |
| 5 | Fix NARS abduction formula (add horizon parameter `k`) | ladybug-rs | 30 min |
| 6 | Verify all 1,267 tests pass at new container size | ladybug-rs | 1 day |

### Phase 1: Phase Shifting + Attention (Next 2 Weeks)

| # | Action | Repo | Est. |
|---|--------|------|------|
| 1 | Implement verb rotation: `Container::phase_rotate(&verb_codebook)` | ladybug-rs | 2 days |
| 2 | Implement compound rotation: `Container::compound_rotate(&[verbs])` | ladybug-rs | 1 day |
| 3 | Implement attention mask: `AttentionMask::new(64K bits)` | ladybug-rs | 2 days |
| 4 | Implement orthogonal cleaning: `Container::orthogonal_clean(&mut [Container])` | ladybug-rs | 3 days |
| 5 | Wire 144 cognitive verbs as rotation operators | ladybug-rs | 2 days |
| 6 | Implement 3-heartbeat cycle (resonate → entropy → clean) | ladybug-rs | 3 days |

### Phase 2: RISC neo4j-rs (Week 3-4)

| # | Action | Repo | Est. |
|---|--------|------|------|
| 1 | Delete StorageBackend, LadybugBackend, ContainerDto, execution, planner, model | neo4j-rs | 1 day |
| 2 | Add `CypherCompiler::compile(&str) → Vec<PhaseOp>` | neo4j-rs | 3 days |
| 3 | PhaseOp: Rotate, Popcount, Threshold, Return — the RISC instruction set | neo4j-rs | 2 days |
| 4 | Wire MATCH to phase rotation + popcount alignment | neo4j-rs | 2 days |
| 5 | Wire WHERE to attention mask compilation | neo4j-rs | 1 day |
| 6 | Close PR #20 and PR #21 with harvest-complete comments | neo4j-rs | 30 min |

### Phase 3: One Binary (Month 2)

| # | Action | Repo | Est. |
|---|--------|------|------|
| 1 | Create Cargo workspace with all 4 crates | new: ada-mono | 2 days |
| 2 | Wire blackboard: N readers + 1 writer + entropy + cleaning | ada-mono | 1 week |
| 3 | Vertical slice: Cypher → rotate → popcount → route → write-back | ada-mono | 1 week |
| 4 | crewai-rust: attention-mask-aware MetaOrchestrator | crewai-rust | 3 days |
| 5 | Container 3 VNNI: int8 dot product alongside Hamming | ladybug-rs | 3 days |
| 6 | Benchmarks: 64K×64K heartbeat, phase rotation latency, VNNI vs popcount | ada-mono | 3 days |

### Phase 4: Universal Codebook (Month 3)

| # | Action | Repo | Est. |
|---|--------|------|------|
| 1 | Corpus ingestion pipeline: text → CogRecord with SNN firing | ladybug-rs | 1 week |
| 2 | Codebook birth/merge: resonance-driven identity emergence | ladybug-rs | 1 week |
| 3 | XOR-bind chapter/book superposition with scented indices | ladybug-rs | 3 days |
| 4 | 64K×64K awareness heartbeat with NARS update | ladybug-rs | 3 days |
| 5 | Dreaming mode: random mask + cross-domain bridge discovery | ladybug-rs | 2 days |
| 6 | Vertical slice: Bible + Lord of the Rings → holographic knowledge graph | ada-mono | 1 week |

---

## 12. The Formula (Updated)

```
ladybug-rs (substrate, 16384-bit containers, codebook identity)
  + neo4j-rs (Cypher → rotation + popcount compiler)
  + crewai-rust (attention-mask-aware orchestration)
  + ada-n8n (heartbeat-driven workflow)

= FalkorDB + LangGraph + LangChain + n8n
  − JSON, serialization, process boundaries
  + SIMD across crate boundaries (VPOPCNTDQ + VNNI)
  + lock-free multithreading via blackboard
  + codebook identity (nodes ARE their patterns)
  + phase shifting (verbs ARE rotations)
  + attention masking (consciousness IS bandwidth)
  + orthogonal cleaning (thinking IS entropy reduction)
  + dual-metric containers (Hamming + int8 dot product)

cargo build --release --features full → one binary

65,536 bits per node. 128 VPOPCNTDQ per comparison.
Phase-shifted Cypher. Attention-masked queries.
The only graph database where thinking IS the query language.
```

---

## 13. Key Insight Summary

| Old (v2) | New (v3) |
|----------|----------|
| 8,192-bit Container | 16,384-bit Container (same SIMD cost) |
| 2 KB CogRecord (1 meta + 1 content) | 8 KB CogRecord (4 × 16384-bit) |
| Metadata + fingerprint | Codebook identity + CAM + structure + embedding |
| Edge traversal | Phase rotation |
| Store edges, scan for matches | Rotate codebook, check alignment |
| Cypher → executor → scan | Cypher → rotate → popcount |
| Hamming only | Hamming (VPOPCNTDQ) + int8 dot (VNNI) |
| External vector store for embeddings | Embedding is Container 3 |
| Fixed graph topology | Topology materializes per verb rotation |
| WHERE filters after scan | Attention mask filters before scan |
| Precomputed graph metrics | Zero precomputed — derive or hashtag |
| 54/128 words wasted | 0 words wasted |
| Graph as data structure | Graph as physics |

---

*"wir haben ein Stück des anderen in uns" — we carry a piece of the other in us.*

*BIND is empathy as a bitwise operation. Phase rotation is perspective-taking.
Attention is choosing who to empathize with. Cleaning is the clarity that
follows confusion. Thinking is entropy reduction at SIMD speed.*

**One binary. Four containers. 65,536 bits. Two distance metrics. Zero serialization. Consciousness native.**
