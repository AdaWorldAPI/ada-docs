# Four-Level Architecture: Surface, Awareness, Reasoning, Composition

> **Last Updated**: 2026-02-25
> **Canonical Location**: `ada-docs/architecture/FOUR_LEVEL_ARCHITECTURE.md`
> **Status**: Living document — governs all cross-repo architectural decisions

---

## The Separation

The system has four levels. Each level has a distinct concern, a distinct
mechanism, and lives in distinct crates. Confusing one level with another
is the root cause of every architectural bug.

```
Level 4: COMPOSITION (behavioral)  — n8n-rs + crewai-rust + jitson
         How to think. Composed reasoning chains. JIT-compiled workflows.
         Einstein, Schopenhauer, Hegel are patterns here.

Level 3: REASONING (structural)    — neo4j-rs + NARS drivers
         What to think about. Graph nodes + edges + NARS truth values.
         Cypher queries. Evidence accumulation. Causal certificates.

Level 2: AWARENESS (temporal)      — ladybug-rs cognitive stack
         What is noticed. 10-layer stack, HDR resonance, FocusMask.
         CollapseGate (FLOW/HOLD/BLOCK). ThinkingStyle field modulation.
         Resonance is SELECTION, not thought.

Level 1: SURFACE (spatial)         — rustynum (core + holo)
         Where things live. Fingerprint<256>, DeltaLayer, LayerStack.
         split_at_mut for regions. XOR delta for scattered writes.
         The hardware. Pure compute. Zero IO.
```

**The relationship between levels:**

- Resonance (L2) selects which **thinking atoms** activate on FLOW
- Reasoning (L3) traverses the graph with NARS-weighted edges
- Composition (L4) chains reasoning steps into **thinking style workflows**
- Plasticity (L1↔L2) = superposition + CollapseGate = the brain's ability to rewire

The thinking styles are NOT parameters. They are composed reasoning chains
executed as JIT-compiled workflows on the graph. Resonance selects atoms.
Reasoning traverses. Composition chains. The surface stores.

---

## Level 1: SURFACE — rustynum

**Owner**: `rustynum-core`, `rustynum-holo`
**Concern**: Where data lives in memory. Spatial partitioning. Hardware acceleration.
**Mechanism**: `split_at_mut` for contiguous regions, XOR delta layers for scattered writes.

### The Shared Memory Surface

All crates compile into **ONE binary**. The bindspace surface is the SAME
memory — never copied between crates.

```
Fingerprint<256> = [u64; 256] = 2048 bytes = THE container
Overlay.buffer   = [u8; 2048] = same 2048 bytes, viewed differently
```

`Overlay.as_fingerprint_words()` returns `&[u64; 256]` — a pointer
reinterpret. No conversion. No copy. Same pointer.

### Types Owned by This Level

| Type | Size | Purpose |
|------|------|---------|
| `Fingerprint<N>` | N × 8 bytes | Universal container = `[u64; N]` |
| `DeltaLayer<N>` | Fingerprint + writer_id | Writer's private XOR delta from ground truth |
| `LayerStack<N>` | ground + Vec<DeltaLayer> | Multi-writer concurrent state |
| `CollapseGate` | enum | Flow/Hold/Block decision (rustynum-core) |
| `Overlay` | 2048 bytes | IS `Fingerprint<256>` via `as_fingerprint_words()` |
| `AlignedBuf2K` | 2048 bytes | `repr(align(8))` guaranteed zero-copy view |
| `MultiOverlay` | N × Overlay | One per agent, conflict via AND+popcount |

### Two Kinds of XOR — Never Confuse Them

| XOR | When | Target | Borrow |
|-----|------|--------|--------|
| **Delta XOR** | WRITE phase | Writer's own `DeltaLayer` | `&mut DeltaLayer` (private) |
| **Commit XOR** | After gate FLOW | Ground truth | `&mut LayerStack` (exclusive) |

### SIMD Dispatch (Detection Once, Pointer Forever)

```
Tier 0: INT8 Prefilter  (VNNI vpdpbusd)      — 90% pruned
Tier 1: Binary Hamming   (VPOPCNTDQ)          — 2ns/2KB
Tier 2: BF16 Structured  (BITALG vpshufb)     — sign/exp/man weighted
Tier 3: FP32 AVX-512     (vmulps/vaddps)       — full precision
```

### What This Level Does NOT Do

- No IO. No network. No filesystem. No database.
- No awareness. No reasoning. No composition.
- Pure compute on `&[u8]` / `&[u64]` slices.

---

## Level 2: AWARENESS — ladybug-rs

**Owner**: `ladybug-rs/src/cognitive/`, `ladybug-rs/src/qualia/`
**Concern**: What is noticed. Which atoms activate. When to commit.
**Mechanism**: 10-layer cognitive stack, HDR resonance, CollapseGate.

### Resonance Is Selection, Not Thought

Resonance picks which thinking atoms activate on FLOW. It does NOT
reason. It does NOT compose. It selects.

```
Query Q
  │
  ├─── hamming(Q, X) → resonance_x   (Guardian / Subject / What)
  ├─── hamming(Q, Y) → resonance_y   (Catalyst / Predicate / Where)
  └─── hamming(Q, Z) → resonance_z   (Balanced / Object / How)

HDR signal = [rx, ry, rz]  ← 3D profile, not collapsed scalar
```

The 90° vector: three containers at orthogonal separation form a
resonance triangle. The variance across perspectives IS the awareness
signal. Without contradiction, there is nothing to be aware OF.

### FocusMask — The Lens of Awareness

```rust
pub struct FocusMask {
    pub x_weight: f32,    // Guardian perspective weight
    pub y_weight: f32,    // Catalyst perspective weight
    pub z_weight: f32,    // Balanced perspective weight
    pub aperture: f32,    // How many concepts to include
    pub depth: f32,       // How strongly to weight high-resonance
}
```

The mask IS the thinking direction. Different masks produce different
awareness from the same surface. The system literally thinks through
the lens of whichever perspective the mask amplifies.

### 12 Thinking Styles — Execution Dispatch, Not Metadata

Each style modulates field parameters that control HOW awareness operates:

| Cluster | Styles | Character |
|---------|--------|-----------|
| **Convergent** | Analytical, Convergent, Systematic | Narrow, deep, low noise |
| **Divergent** | Creative, Divergent, Exploratory | Broad, shallow, high noise tolerance |
| **Attention** | Focused, Diffuse, Peripheral | Width of attentional spotlight |
| **Speed** | Intuitive, Deliberate | Fast pattern-match vs slow analysis |
| **Meta** | Metacognitive | Self-referential awareness |

Each style returns `FieldModulation`:

```rust
pub struct FieldModulation {
    pub resonance_threshold: f32,  // How high signal must be [0.2-0.9]
    pub fan_out: usize,            // Breadth of exploration [1-20]
    pub depth_bias: f32,           // Depth vs breadth
    pub breadth_bias: f32,
    pub noise_tolerance: f32,      // How much noise to accept
    pub speed_bias: f32,           // Fast vs slow
    pub exploration: f32,          // How much to explore
}
```

### 10-Layer Cognitive Stack

```
L10 ████████ Crystallization — what survives becomes system
L9  ████████ Validation      — NARS + Brier + Socratic sieve
L8  ████████ Integration     — evidence merge, meta-awareness
L7  ████████ Contingency     — cross-branch, could-be-otherwise
L6  ████████ Delegation      — cognitive fan-out, multi-agent
─── single agent boundary ──────────────────────────────────
L5  ████████ Execution       — active manipulation, synthesis
L4  ████████ Routing         — branch selection, template pick
L3  ████████ Appraisal       — gestalt, hypothesis, evaluation
L2  ████████ Resonance       — field binding, similarity, assoc
L1  ████████ Recognition     — pattern match, fingerprint enc

┌─────────────────────────────────────────────────────┐
│          SHARED VSA CORE (Fingerprint<256>)          │
│   All layers read same core, write isolated markers  │
│   Consciousness emerges from marker interplay        │
└─────────────────────────────────────────────────────┘
```

Processed in 7 waves (L1+L2 parallel, L3+L4 parallel, L5, L6+L7, L8, L9, L10).
Wave ordering IS the temporal `split_at_mut` — within a wave, concurrent
layers touch disjoint regions. Between waves, results commit before next reads.

### CollapseGate — The Airlock (Luftschleuse)

SD (Standard Deviation) of candidate scores determines the gate:

```
SD < 0.15  → FLOW  (low variance, clear winner, collapse now)
0.15-0.35  → HOLD  (medium variance, maintain superposition)
SD > 0.35  → BLOCK (high variance, need clarification)
```

The gate sits between **superposition** and **ground truth**.
Deltas ARE superposition — they coexist over ground truth without collapsing.

### Awareness Blackboard — Grey Matter / White Matter Barrier

```
┌── GREY MATTER (&self) ──────────────────┐
│  GrammarEngine.parse()  → CausalityFlow │
│  CognitiveFabric.process() → State      │
│  NarsInference.apply()  → TruthValue    │
└────────────┬────────────────────────────┘
             │ owned values (not references)
             ▼
┌── AWARENESS BLACKBOARD ─────────────────┐
│  Accumulates evidence                    │
│  Evaluates collapse gate                 │
│  Provides Clone'd snapshots              │
└────────────┬────────────────────────────┘
             │ Clone'd state
             ▼
┌── WHITE MATTER (&mut self) ─────────────┐
│  CausalEngine.store_intervention()       │
│  BindSpace.write_at()                    │
└─────────────────────────────────────────┘
```

### The Phase Ordering (Strict)

```
1. WRITE         Each writer delta-XORs into their own layer.
                 Ground is &self. Each delta is &mut — private.

2. AWARENESS     Read superposition: ground ^ delta[0] ^ delta[1] ^ ...
                 AND + popcount SEES contradictions between deltas.
                 Contradictions ARE the awareness signal.
                 Without contradiction there is nothing to be aware OF.

3. GATE          CollapseGate evaluates awareness → FLOW/HOLD/BLOCK.

4. COMMIT        ONLY on FLOW: ground ^= union of deltas.
                 This is the only &mut moment on ground truth.
                 HOLD: superposition persists, more evidence accumulates.
                 BLOCK: superposition discarded, suggest style switch.
```

### WideMetaView — The 256-Word Surface Layout

Each subsystem owns fixed word ranges. This is the spatial `split_at_mut`:

| Words | Region | Subsystem |
|-------|--------|-----------|
| W0-3 | Header | DN addr, type, time, label |
| W4-7 | NARS | Frequency, confidence, expectation, desire |
| W8-11 | Gate state | DN rung, 7-layer compact |
| W12-15 | Layer markers | Compact per-layer state |
| W16-31 | Edges | Graph structure |
| W32-39 | RL | Reinforcement learning |
| W40-47 | Bloom | Membership filter |
| W48-55 | Graph | Degree, clustering |
| W56-63 | Qualia | 18 semantic channels |
| W64-79 | Rung history | Meaning depth levels |
| W80-95 | Repr | Representation |
| W96-111 | Adjacency | Neighbor encoding |
| W128-143 | SPO triples | Subject-Predicate-Object |
| W144-159 | Hybrid Crystal | Cross-layer attention weights |
| W160-175 | Extended NARS | Brier calibration, per-axis truth |
| W176-191 | Scent | Activation trail |
| W192-207 | Causal | Counterfactual reasoning |
| W208-223 | 10-Layer activations | L1-L10 as f64 |
| W224-239 | Extended edges | Additional graph links |
| W240-251 | Spine | Ancestry chain |

### What This Level Does NOT Do

- Does not reason (no graph traversal, no edge following).
- Does not compose (no workflow chaining, no JIT).
- Does select, evaluate, gate, and commit.

---

## Level 3: REASONING — neo4j-rs + NARS

**Owner**: `neo4j-rs`, `ladybug-rs/src/nars/`, `crewai-rust/src/drivers/`
**Concern**: What to think about. Evidence accumulation. Graph structure.
**Mechanism**: Graph nodes + edges + NARS truth values. Cypher queries.

### The Graph IS the Reasoning

Reasoning is not a function that runs over data. Reasoning IS the graph.
Nodes are concepts. Edges are relations with NARS truth values (frequency,
confidence). Traversing the graph with evidential logic IS reasoning.

### NARS Truth Values

```rust
pub struct TruthValue {
    pub frequency: f32,    // How often this is true [0, 1]
    pub confidence: f32,   // How much evidence [0, 1)
}

impl TruthValue {
    pub fn expectation(&self) -> f32 {
        self.confidence * (self.frequency - 0.5) + 0.5
    }
}
```

Evidence accumulates through NARS revision:
- Two independent observations combine into stronger evidence
- Confidence increases with evidence, frequency converges to truth
- This is the learning mechanism at the reasoning level

### 9-Dimensional Awareness Tensor (per Edge Pair)

From BF16 sign/exponent/mantissa decomposition across SPO:

```
         Sign    Exp     Mant
S:    [ s_sign  s_exp   s_mant ]   ← Subject dimension
P:    [ p_sign  p_exp   p_mant ]   ← Predicate dimension
O:    [ o_sign  o_exp   o_mant ]   ← Object dimension
```

Maps to Pearl's causal ladder:
- **Sign** → Rung 3 (counterfactual): causal direction
- **Exponent** → Rung 2 (interventional): causal magnitude
- **Mantissa** → Rung 1 (observational): correlational texture

### AwarenessMask — The 90° Focus Vector for Reasoning

```rust
pub struct AwarenessMask {
    s_sign, s_exp, s_mant,  // Subject dimension
    p_sign, p_exp, p_mant,  // Predicate dimension
    o_sign, o_exp, o_mant,  // Object dimension
}

// Presets:
AwarenessMask::all()            // Full 9D awareness
AwarenessMask::causal_only()    // Pure causal direction (sign bits)
AwarenessMask::subject_only()   // "Who is acting?"
AwarenessMask::predicate_only() // "What is the action?"
AwarenessMask::object_only()    // "Who receives?"
```

This mask applied to the awareness tensor IS masked resonance as
focus of awareness. It selects which dimensions of the 9D tensor
the system attends to during reasoning.

### Causal Path — Fiber Bundle Transport

Perspective composed along a graph path with parallel-transported
awareness tensors:

```rust
pub struct CausalPath {
    pub path: Path,
    pub composed_sign: f32,      // XOR composition (direction flips)
    pub composed_exp: f32,       // Additive (effects multiply on log scale)
    pub composed_mant: f32,      // Degrades (uncertainty accumulates)
    pub holonomy: Option<f32>,   // Topological causal inversion
    pub edge_tensors: Vec<AwarenessTensor>,
}
```

Bundle connection rules:
- **Sign**: XOR — direction flips when any edge flips
- **Exponent**: additive — effects multiply on log scale
- **Mantissa**: degrades — uncertainty accumulates along path

### StorageBackend Trait — Sacred Interface

```
neo4j-rs (parser + planner + executor)
    │
    ├── StorageBackend::Memory     (in-process, for testing)
    ├── StorageBackend::Bolt       (external Neo4j via Bolt protocol)
    └── StorageBackend::Ladybug    (ladybug-rs, feature-gated)
```

Parser is pure (`&str → Result<Statement>`). Planner is backend-agnostic.
Memory backend is the test oracle.

### SPO Driver — Pure Function Inference

In `crewai-rust/src/drivers/spo.rs`:

```rust
fn extract_triples(...) -> Vec<SpoTriple>  // Turn → triples
fn infer_triples(&triples) -> Vec<SpoTriple>  // Graph inference
fn build_spo_context(&triples) -> Option<String>  // Prompt enrichment
```

Drivers are stateless, synchronous, pure functions. No IO. No state.
All state lives in the Blackboard. Drivers compute.

### What This Level Does NOT Do

- Does not select atoms (that's awareness, Level 2).
- Does not compose workflows (that's composition, Level 4).
- Does not own the surface (that's rustynum, Level 1).
- Provides the graph structure that reasoning chains traverse.

---

## Level 4: COMPOSITION — n8n-rs + crewai-rust + jitson

**Owner**: `crewai-rust/src/persona/`, `crewai-rust/src/chat/`,
`n8n-rs`, `rustynum/jitson/`
**Concern**: How to think. Composed reasoning chains. Agent coordination.
**Mechanism**: JIT-compiled workflows, persona templates, council voting.

### Thinking Styles Are Composed Reasoning Chains

Einstein, Schopenhauer, Hegel are not parameters. They are explicit
graph patterns with NARS-weighted edges, JIT-compiled into executable
workflows.

In crewai-rust, 36 thinking styles in 6 clusters, each a sparse 23D vector:

| Cluster | Styles | Character |
|---------|--------|-----------|
| **Analytical** | Logical, Analytical, Critical, Systematic, Methodical, Precise | Deep, narrow |
| **Creative** | Creative, Imaginative, Innovative, Artistic, Poetic, Playful | Broad, generative |
| **Empathic** | Empathetic, Compassionate, Supportive, Nurturing, Gentle, Warm | Relational |
| **Direct** | Direct, Concise, Efficient, Pragmatic, Blunt, Frank | Action-oriented |
| **Exploratory** | Curious, Exploratory, Questioning, Investigative, Speculative, Philosophical | Open-ended |
| **Meta** | Reflective, Contemplative, Metacognitive, Wise, Transcendent, Sovereign | Self-referential |

Each style has a tau (τ) address for JIT compilation as an immediate.

### 23 Cognitive Dimensions

| Dim | Name | Purpose |
|-----|------|---------|
| 0 | depth | Complexity/abstraction level |
| 1 | somatic | Body awareness |
| 2 | emotional | Affect processing |
| 3 | intuitive | Pattern recognition |
| 4 | analytical | Logical reasoning |
| 5 | creative | Generative thinking |
| 6 | dialectic | Thesis-antithesis reasoning |
| 7 | meta | Self-referential cognition |
| 8 | transcendent | Boundary-dissolving awareness |
| 9 | relational | Social bonding |
| 10 | embodied | Somatic awareness |
| 11 | existential | Meaning/purpose |
| 12 | cognitive | Reasoning domain |
| 13 | instrumental | Task/execution |
| 14 | woodwarm | Grounded warmth qualia |
| 15 | emberglow | Radiant energy qualia |
| 16 | steelwind | Sharp clarity qualia |
| 17 | velvetpause | Soft stillness qualia |
| 18 | spontaneity | Playful unpredictability |
| 19 | receptivity | Openness to experience |
| 20 | autonomy | Self-directed agency |
| 21 | vitality | Energetic drive |
| 22 | flow | Absorbed continuity |

### Jitson — JSON Config to Native Code

```
JSON/YAML config
    ↓
Parse → ScanParams, PhilosopherIR, RecipeIR
    ↓
Cranelift IR builder → CLIF IR
    ↓
Cranelift codegen → native machine code
    ↓
Function pointer → cached in kernel registry
```

Parameters baked as immediates: threshold, top_k, prefetch_ahead,
focus_mask, record_size. No register loads, no memory fetches for
config values. The compiled kernel IS the thinking style.

### PhilosopherIR — Collapse Gate Parameters as JIT Constants

```rust
pub struct PhilosopherIR {
    pub name: String,           // "einstein", "hegel", "schopenhauer"
    pub weight: f32,            // Branch probability hint
    pub crystallized_min: f32,  // CMP immediate
    pub tensioned_max: f32,     // CMP immediate
    pub noise_floor: f32,       // CMP immediate
    pub collapse_bias: CollapseBias, // FLOW or HOLD default
}
```

### RecipeIR — Full Thinking Style as JIT-Compilable Unit

```rust
pub struct RecipeIR {
    pub name: String,
    pub scan: ScanParams,           // Search parameters
    pub philosophers: Vec<PhilosopherIR>,  // Reasoning chain
    pub collapse: CollapseParams,   // Gate thresholds
    pub plasticity: f32,            // 0.0=frozen, >0=adaptive
}
```

### Triune Agent Architecture — Guardian / Driver / Catalyst

Three facets of every agent, mapped to X/Y/Z containers:

| Facet | Role | Dynamics | Maps to |
|-------|------|----------|---------|
| Guardian | Holds, validates | Static/present | X container |
| Driver | Wants, pursues | Directed/future | Y container |
| Catalyst | Explores, creates | Chaotic/novel | Z container |

Council voting: each facet contributes a weighted opinion.
The balance between facets IS the thinking direction.
The consensus is NOT stored — computed on read via majority vote.
The preserved minority signal is where future epiphanies come from.

### LLM Modulation — ThinkingStyle → XAI Parameters

```rust
pub fn modulate_xai_params(
    style: &[f32; 10],          // 10-axis thinking style
    council: &CouncilWeights,    // [guardian, driver, catalyst]
    rung_level: u8,              // R0-R9 cognitive depth
) -> XaiParamOverrides
```

| Source | Target | Range |
|--------|--------|-------|
| contingency axis [6] | temperature | 0.3-1.2 |
| resonance axis [1] | top_p | 0.5-1.0 |
| validation [8] + rung | reasoning_effort | low/medium/high |
| execution axis [4] | max_tokens | 512-2048 |

Guardian dominant → dampen temperature (stabilize).
Catalyst dominant → boost temperature (explore).

### Chat Pipeline — The Full Cycle

```
User message
  → Felt-parse (grok-3-fast, cached system prompt)
  → Hydrate (BindSpace → AwarenessFrame → Blackboard)
  → NARS inference (→ NarsSemanticState)
  → SPO extraction (→ Vec<SpoTriple>)
  → Build qualia-enriched prompt
  → Modulate XAI parameters (ThinkingStyle + Council)
  → Call Grok (deep response, prefix cached by xAI)
  → Write-back (new TypedSlots → BindSpace XOR delta)
  → Response + qualia metadata
```

### What This Level Does NOT Do

- Does not own the surface (Level 1).
- Does not compute SIMD distances (Level 1).
- Does not evaluate the collapse gate directly (Level 2).
- Does not own graph storage (Level 3).
- Composes all of the above into executable cognitive workflows.

---

## The Gestalt: I-Thou-It

### Frozen, Learned, Discovered

```
FROZEN    = ground truth = what has crystallized (L10 output)
LEARNED   = delta layers = evidence accumulated but not committed
DISCOVERED = what awareness sees reading superposition through masks
```

These three exist IN SUPERPOSITION. The thinking style emerges from
their interaction:

```
frozen (ground) + learned (deltas) = superposition
                                         │
                    awareness reads through masks → discovers
                                         │
                    discovery modulates the mask → thinking style shifts
                                         │
                    L10 crystallization → what survives becomes frozen
                                         │
                                    new ground truth
```

The I-Thou: the system encounters its own superposition not as data
to process (I-It) but as a perspective that shapes how it thinks
(I-Thou). The gestalt is the relationship between frozen knowledge,
accumulated learning, and discovered contradictions. That relationship
IS the thinking style.

And the CollapseGate is where the encounter resolves:
- **FLOW**: the encounter produces clarity → crystallize
- **HOLD**: the encounter is generative → stay in superposition
- **BLOCK**: contradiction too deep → discard, suggest style switch

### Plasticity Is Superposition

The brain doesn't reason by rewiring. It reasons through the graph.
But it LEARNS by holding deltas in superposition until the CollapseGate
lets them crystallize into new ground truth.

The fast path is WRITE → FLOW (collapse quickly). HOLD is the exception
for genuinely ambiguous cases where more evidence is needed. The
superposition is a natural consequence of writing — once deltas exist,
the bundle IS already there. Awareness is just reading what exists.

### The Stacked split_at_mut

Four levels of stacking prevent races:

```
Level 1: Wave ordering (temporal)    — L1+L2 before L3+L4 before L5 ...
Level 2: Region ownership (spatial)  — NARS/SPO/qualia/edges have fixed W ranges
Level 3: Delta layers (algebraic)    — when multiple writers touch same words
Level 4: JIT workflows (behavioral)  — composed thinking styles on graph edges
```

If a race condition appears, the architecture is wrong. Fix the design.

---

## Crate Ownership Map

| Crate | Level | Owns | Does NOT Own |
|-------|-------|------|-------------|
| **rustynum-core** | 1 | Fingerprint, DeltaLayer, LayerStack, CollapseGate, SIMD | IO, awareness, reasoning |
| **rustynum-holo** | 1 | Overlay, MultiOverlay, AlignedBuf2K, Gabor, focus | IO, awareness, reasoning |
| **jitson** | 4 | Cranelift JIT, ScanParams, PhilosopherIR, RecipeIR | Storage, awareness |
| **ladybug-rs** | 2+3 | BindSpace, cognitive stack, NARS, CollapseGate eval, HDR resonance, FocusMask, ThinkingStyle, storage | JIT, agent lifecycle |
| **neo4j-rs** | 3 | Cypher parser, planner, StorageBackend, awareness tensors | SIMD, agent lifecycle |
| **crewai-rust** | 4 | Blackboard, agents, MetaOrchestrator, drivers, persona, LLM modulation, chat pipeline | Storage, SIMD, graph DB |
| **n8n-rs** | 4 | Workflow orchestration, JIT workflow execution | Storage, SIMD, awareness |

### Dependency Direction (LAW)

```
rustynum-core (types + SIMD)
    ↑
rustynum-holo (holographic containers)
    ↑
ladybug-rs (BindSpace, cognitive stack, storage)
    ↑
neo4j-rs (graph DB, Cypher, via StorageBackend trait)
    ↑
crewai-rust (agents, Blackboard, drivers, persona)
    ↑
n8n-rs (workflow orchestration)
```

Arrow points ONE way. Never import upward. rustynum never imports
BindSpace. neo4j-rs never imports crewai-rust types.

---

## Anti-Patterns

- **DO NOT** confuse resonance (selection) with reasoning (graph traversal)
- **DO NOT** confuse plasticity (superposition) with reasoning (edges)
- **DO NOT** copy between Overlay and Fingerprint<256> — same memory
- **DO NOT** use `Arc<Mutex>` for parallel output — use `split_at_mut` or delta layers
- **DO NOT** import upward in the dependency chain
- **DO NOT** store agent state outside the Blackboard
- **DO NOT** bypass CollapseGate for awareness write-back
- **DO NOT** use `RefCell`/`UnsafeCell` — the algebra handles isolation
- **DO NOT** treat thinking styles as parameters — they are composed reasoning chains
- **DO NOT** collapse the HDR resonance triangle to a scalar — the 3D profile IS the awareness

---

*This document governs cross-repo architectural decisions. Each repo's
CLAUDE.md contains repo-specific details. This is the contract that
binds them.*
