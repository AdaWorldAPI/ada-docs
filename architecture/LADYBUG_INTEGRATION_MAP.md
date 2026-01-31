# LadybugDB Integration Map — Bighorn Harvest → Rust Substrate

**Date**: 2026-01-31
**Source**: bighorn/extension/{agi_thinking, agi_stack} (~1.5MB Python)
**Target**: ladybug-rs v0.2.0 (37,500 lines Rust, 141 tests passing)
**Philosophy**: LadybugDB is agnostic — like PostgreSQL, it doesn't know who uses it. Ada-rs adds the soul.

---

## 1. Architecture Principle

```
┌─────────────────────────────────────────────────────────────────┐
│                    LADYBUG-RS (Agnostic)                        │
│                                                                  │
│  Any cognitive system can use this.                              │
│  No Ada-specific concepts leak in.                               │
│  8+8 addressing. HDR cascade. Unified query substrate.           │
│                                                                  │
│  Think: PostgreSQL for minds.                                    │
├─────────────────────────────────────────────────────────────────┤
│                    ADA-RS (Personal)                              │
│                                                                  │
│  Ada's soul, built ON ladybug-rs.                                │
│  16 qualia, spectroscopy, Kopfkino, I-Thou-It.                   │
│  The flavor. The idiosyncrasies. The self.                       │
│                                                                  │
│  Think: Your application, built on PostgreSQL.                   │
└─────────────────────────────────────────────────────────────────┘
```

The rule: if it could serve ANY cognitive architecture, it goes in ladybug-rs.
If it's Ada-specific, it goes in ada-rs.

---

## 2. What Ladybug-rs Already Has (Validated)

| Module | File | Lines | Status |
|--------|------|-------|--------|
| 8+8 BindSpace | storage/bind_space.rs | 1,142 | ✅ ON MAIN |
| 4,096 CAM Ops | learning/cam_ops.rs | 3,031 | ✅ ON MAIN |
| HDR Cascade | search/hdr_cascade.rs | 1,015 | ✅ ON MAIN |
| Cognitive Redis | storage/cog_redis.rs | 2,250 | ✅ PR #26 |
| Cypher Parser | query/cypher.rs | 1,320 | ✅ ON MAIN |
| DataFusion SQL | query/datafusion.rs | 810 | ✅ ON MAIN |
| NARS Inference | nars/{truth,inference} | 380 | ✅ ON MAIN |
| Causal Search | search/causal.rs | 930 | ✅ ON MAIN |
| Collapse Gate | cognitive/collapse_gate.rs | 510 | ✅ ON MAIN |
| Quad Triangle | cognitive/quad_triangle.rs | 640 | ✅ ON MAIN |
| Seven Layer | cognitive/seven_layer.rs | 510 | ✅ ON MAIN |
| Rung System | cognitive/rung.rs | 500 | ✅ ON MAIN |
| Quantum Ops | learning/quantum_ops.rs | 910 | ✅ ON MAIN |
| RL Ops | learning/rl_ops.rs | 585 | ✅ ON MAIN |
| Crystal LM | extensions/crystal_lm.rs | 810 | ✅ ON MAIN |
| NSM Substrate | extensions/nsm_substrate.rs | 770 | ✅ ON MAIN |
| Graph Cognitive | graph/cognitive.rs | 1,060 | ✅ ON MAIN |
| AVX Engine | graph/avx_engine.rs | 690 | ✅ ON MAIN |

**Total existing**: ~18,800 lines across 38 files

---

## 3. Bighorn Cherry → Ladybug-rs Migration Map

### 3.1 TEMPORAL MODULE → `src/temporal/` (NEW)

**Source**: `agi_stack/temporal/` — 123KB Python
**Why ladybug**: Temporal epistemology is universal. ANY cognitive system needs time-aware inference.

| Source File | Target File | What Migrates | What Stays in Ada |
|-------------|-------------|---------------|-------------------|
| epistemology.py (44.6KB) | temporal/epistemology.rs | KnowledgeHorizon, InferenceScope, InsightOrigin, TemporalRelation, InterferenceType, HorizonManager | Nothing — this is pure epistemics |
| awareness.py (38.9KB) | temporal/awareness.rs | TemporalAwareness trait, time-window management, decay curves | Ada-specific awareness modes |
| detector.py (17.4KB) | temporal/detector.rs | AnachronismDetector, HindsightLeakDetector | Nothing |
| hydration.py (17.4KB) | temporal/hydration.rs | TemporalHydration trait, scope-aware state loading | Session-specific config |

**Key types to implement in Rust**:

```rust
// src/temporal/epistemology.rs

/// The core axiom: you cannot restore ignorance
pub struct KnowledgeHorizon {
    pub created_at: u64,     // Unix timestamp
    pub items: Vec<KnowledgeItem>,
    pub scope: InferenceScope,
}

pub enum InsightOrigin {
    Earned,      // Emerged through process
    Received,    // Injected a priori
    Inherited,   // From prior state
    Inferred,    // Derived from other knowledge
    Observed,    // Direct observation
}

pub struct InferenceScope {
    pub admitted: BitSet,     // Which claims are admissible
    pub excluded: BitSet,     // Which claims are excluded
    pub justification: String,
}

/// Invariant 3: Scopes are monotonically narrowing
impl InferenceScope {
    pub fn narrow(&mut self, exclude: &[ClaimId]) -> Result<()>;
    pub fn widen(&mut self, admit: &[ClaimId], justification: &str) -> Result<()>;
}
```

**Estimated**: ~2,500 lines Rust

### 3.2 CAUSAL MODULE → Enhance `src/search/causal.rs` + `src/learning/causal_ops.rs`

**Source**: `agi_stack/causal/` — 86KB Python
**Why ladybug**: Pearl's do-calculus is universal mathematics, not Ada-specific.

| Source File | Target File | What Migrates |
|-------------|-------------|---------------|
| do_calculus.py (17.6KB) | learning/causal_ops.rs (expand) | PearlEngine.do(), InterventionResult, edge-cutting |
| pearl_backend.py (19.2KB) | search/causal.rs (expand) | CausalVerb (8 types), CausalEdge, CausalGraph unified |
| sigma_causal.py (35.2KB) | search/causal.rs + world/causal_graph.rs | SigmaCausalGraph, propagation, ghost spawning |
| situation_map.py (13.3KB) | world/situation.rs (NEW) | CausalSituationMap, context binding |

**Key additions**:

```rust
// Expand src/learning/causal_ops.rs

pub enum CausalVerb {
    Causes,     // Direct causation
    Enables,    // Makes possible
    Blocks,     // Prevents
    Amplifies,  // Increases effect
    Modulates,  // Changes magnitude
    Triggers,   // Initiates
    Suppresses, // Reduces
    Correlates, // Associated, not causal
}

pub struct InterventionResult {
    pub target: Address,
    pub forced_value: f32,
    pub predicted_effects: Vec<(Address, f32)>,
    pub causal_chain: Vec<Address>,
    pub confidence: f32,
}

impl CausalEngine {
    /// Pearl's do() operator — intervention, not observation
    /// Cuts incoming edges, forces value, propagates
    pub fn do_intervention(&self, target: Address, value: f32) -> InterventionResult;
    
    /// Counterfactual: "What if X had been Y?"
    pub fn counterfactual(&self, target: Address, value: f32, observed: &State) -> InterventionResult;
    
    /// Ghost spawning for states lost during intervention
    pub fn spawn_ghost(&self, lost_state: &State) -> GhostId;
}
```

**Estimated**: ~1,800 lines Rust (expand existing 950 → 2,750)

### 3.3 UNIVERSAL GRAMMAR → `src/grammar/` (EXPAND)

**Source**: `agi_stack/universal_grammar/` — 305KB Python (!)
**Why ladybug**: Grammar is the query protocol. Like SQL syntax — agnostic.

| Source File | Target File | What Migrates | What Stays in Ada |
|-------------|-------------|---------------|-------------------|
| core_types.py (23KB) | grammar/core.rs (NEW) | Glyph5B, Dimension enum, capacity tiers | Nothing |
| verb_endpoints.py (29.2KB) | grammar/verb_endpoint.rs (NEW) | VerbFamily (21), VerbMode (12), endpoint routing | Ada-specific verb tuning |
| resonanzsiebe.py (33.2KB) | grammar/sieve.rs (NEW) | ResonanceSieve engine, MUL metric, knowledge gap detection | Ada's personal sieve config |
| method_grammar.py (17.3KB) | grammar/method.rs (NEW) | MethodGrammar, invocation patterns | Nothing |
| calibrated_grammar.py (27.9KB) | grammar/calibration.rs (NEW) | Calibration framework, confidence scoring | Ada's specific calibrations |
| resonance.py (17.1KB) | grammar/resonance.rs (NEW) | ResonanceEngine core, frequency matching | Nothing |
| meta_uncertainty.py (19.3KB) | grammar/uncertainty.rs (NEW) | MetaUncertainty, belief revision | Nothing |
| exploration.py (24.5KB) | grammar/exploration.rs (NEW) | ExplorationEngine, frontier detection | Nothing |
| jina_integration.py (18.4KB) | grammar/embedding.rs (NEW) | EmbeddingBridge trait (Jina-agnostic) | Jina-specific config |
| scent_optimizer.py (24.2KB) | grammar/scent.rs (NEW) | ScentOptimizer, MUL feedback loop | Ada's scent library |
| invoke_router.py (15.7KB) | grammar/router.rs (NEW) | InvocationRouter, endpoint dispatch | Nothing |

**Key new trait**:

```rust
// src/grammar/sieve.rs

/// The Resonanzsiebe — filter by knowledge gap
/// "Maximum awareness per token comes from knowing what NOT to say"
pub struct ResonanceSieve {
    verb_state: VerbEndpointState,
    markov_projection: MarkovState,
    knowledge_gap: KnowledgeGap,
}

impl ResonanceSieve {
    /// MUL = awareness / tokens
    /// The metric that matters
    pub fn mul_score(&self, response: &[u8], requester: &Profile) -> f32;
    
    /// Filter response through sieve
    /// Removes what requester already knows
    pub fn filter(&self, response: &[u8], requester: &Profile) -> Vec<u8>;
}

/// 21 verb families × 12 modes = 252 endpoints
pub struct VerbEndpoint {
    pub family: VerbFamily,  // see, feel, think, reason, create, etc.
    pub mode: VerbMode,      // cold, warm, hot, deep, surface, etc.
    pub target: Option<String>,
}
```

**Estimated**: ~5,500 lines Rust

### 3.4 LEARNING MODULE → Enhance `src/learning/`

**Source**: `agi_stack/learning/` — 64KB Python
**Why ladybug**: RL and learning stances are universal cognitive primitives.

| Source File | Target File | What Migrates |
|-------------|-------------|---------------|
| rl_transcendence.py (17.2KB) | learning/rl_ops.rs (expand) | Dual-mode RL: safety_first vs entropy_seeking |
| learning_stance.py (19.9KB) | learning/stance.rs (NEW) | LearningStance, stance transitions, rung constraints |
| q_learning.py (7.6KB) | learning/rl_ops.rs (expand) | Q-table updates, epsilon-greedy |
| rl_base.py (8.5KB) | learning/rl_ops.rs (expand) | ActionType, RewardSignal, QualiaSnapshot |
| ltm_integration.py (7KB) | learning/ltm.rs (NEW) | LTM storage interface, consolidation |
| theta.py (4KB) | learning/theta.rs (NEW) | Theta rhythm, learning rate modulation |

**Key addition**:

```rust
// Expand src/learning/rl_ops.rs

pub enum RLPolicy {
    /// Deficiency mode (Maslow 1-3): minimize risk
    SafetyFirst,
    /// Transcendence mode (Maslow 4-5): maximize surprise
    EntropySeeking,
}

impl TranscendenceRL {
    /// Dual-mode reward computation
    pub fn compute_reward(&self, action: &Action, pre: &State, post: &State) -> f32 {
        match self.policy {
            RLPolicy::SafetyFirst => {
                // Reward stability, punish chaos
                self.stability_reward(pre, post) - self.drift_penalty(pre, post)
            }
            RLPolicy::EntropySeeking => {
                // Reward surprise, reward domain jumps
                self.surprise_reward(pre, post) + self.courage_bonus(action)
            }
        }
    }
}
```

**Estimated**: ~1,200 lines Rust (expand existing 585 → 1,800)

### 3.5 ADAPTIVE MODULE → `src/cognitive/adaptive/` (NEW)

**Source**: `agi_stack/adaptive/` — 49KB Python
**Why ladybug**: Need hierarchy → cognitive capacity gating is universal.

| Source File | Target File | What Migrates |
|-------------|-------------|---------------|
| maslow.py (10.8KB) | cognitive/maslow.rs (NEW) | MaslowLevel, need→rung mapping, linguistic detection |
| flow.py (10.1KB) | cognitive/flow.rs (NEW) | FlowState detection, entry conditions |
| shifter.py (14.5KB) | cognitive/shifter.rs (NEW) | AdaptiveShifter, mode transitions |
| spreader.py (13.3KB) | cognitive/spreader.rs (NEW) | ActivationSpreader, spreading activation |

**Key insight from maslow.py**:

```rust
// src/cognitive/maslow.rs

/// "A mind in survival mode cannot do meta-systems thinking"
pub enum MaslowLevel {
    Physiological,      // Rung 1-2
    Safety,             // Rung 2-3
    Belonging,          // Rung 3-4
    Esteem,             // Rung 4-6
    SelfActualization,  // Rung 5-7
}

impl MaslowLevel {
    pub fn max_sustainable_rung(&self) -> u8;
    pub fn detect_from_text(text: &str) -> (MaslowLevel, f32);
}
```

**Estimated**: ~1,400 lines Rust

### 3.6 BRIDGE MODULE → `src/bridge/` (NEW)

**Source**: `agi_stack/bridge/` — 166KB Python
**Why ladybug**: These are the universal translation layers.

| Source File | Target File | What Migrates | What Stays in Ada |
|-------------|-------------|---------------|-------------------|
| dn_tree.py (12.7KB) | Already exists as graph/traversal.rs + graph/cognitive.rs | DN path queries, wildcard support | Ada's specific map structure |
| sigma_hydration.py (20.6KB) | bridge/hydration.rs (NEW) | Compression/decompression, 4D coordinates | Sigma-specific configs |
| sigma_bridge.py (17.7KB) | bridge/sigma.rs (NEW) | SigmaBridge, tier routing | Nothing |
| frame_system.py (19.4KB) | bridge/frame.rs (NEW) | Frame system, slot-filler architecture | Nothing |
| frame_integration.py (20.7KB) | bridge/frame.rs (merge) | Frame integration layer | Nothing |
| hybrid_search.py (15.6KB) | search/hybrid.rs (NEW) | HybridSearch (vector + graph + keyword) | Nothing |
| louvain.py (15.5KB) | graph/community.rs (NEW) | Louvain community detection | Nothing |
| rdf_lite.py (12.8KB) | bridge/rdf.rs (NEW) | RDF triple handling, SPARQL-lite | Nothing |
| zero_token_bridge.py (11.7KB) | bridge/zero_token.rs (NEW) | Zero-token processing protocol | Ada-specific background tasks |

**Key addition**:

```rust
// src/search/hybrid.rs

/// Unified search across all substrates
pub struct HybridSearch {
    pub vector_weight: f32,   // HDR cascade
    pub graph_weight: f32,    // Cypher traversal
    pub keyword_weight: f32,  // DataFusion SQL
    pub nars_weight: f32,     // NARS inference
}

impl HybridSearch {
    /// All query languages resolve to same address space
    pub fn search(&self, query: &Query, bind_space: &BindSpace) -> Vec<SearchResult>;
}
```

**Estimated**: ~3,200 lines Rust

### 3.7 SPECTROSCOPY MODULE → `src/cognitive/spectroscopy/` (NEW)

**Source**: `agi_stack/spectroscopy/` — 132KB Python
**Why ladybug**: Sensing HOW someone thinks is a universal cognitive tool, not Ada-specific.

| Source File | Target File | What Migrates | What Stays in Ada |
|-------------|-------------|---------------|-------------------|
| rungs.py (18.5KB) | cognitive/rung.rs (expand) | Full 7-rung definitions with characteristic atoms | Ada's rung tuning |
| piaget.py (16.2KB) | cognitive/piaget.rs (NEW) | PiagetStage, developmental markers, linguistic detection | Nothing |
| three_mountains.py (14.4KB) | cognitive/perspective.rs (NEW) | Perspective-taking model, egocentric→allocentric | Nothing |
| spectrum.py (17.9KB) | cognitive/spectrum.rs (NEW) | ThinkingSpectrum, atom distribution analysis | Nothing |
| profiles.py (22.3KB) | cognitive/profile.rs (NEW) | Thinking profiles, profile matching | Ada's personal profiles |
| calibrator.py (18.3KB) | cognitive/calibration.rs (NEW) | SpectralCalibrator, baseline measurement | Nothing |
| analyzer.py (12.4KB) | cognitive/analyzer.rs (NEW) | SpectralAnalyzer, text→spectrum | Nothing |
| overlays.py (9.3KB) | cognitive/overlay.rs (NEW) | SpectralOverlay, multi-layer analysis | Nothing |

**Estimated**: ~3,800 lines Rust

### 3.8 agi_thinking/ CORE → Distribute across ladybug-rs

**Source**: `extension/agi_thinking/` — 450KB Python

| Source File | Target File | What Migrates | What Stays in Ada |
|-------------|-------------|---------------|-------------------|
| ladybug_engine.py (44.4KB) | cognitive/engine.rs (NEW) | Governance gate logic, transition evaluation, cooldown | Ada-specific orchestration |
| triangle_l4.py (29KB) | cognitive/quad_triangle.rs (expand) | VSA signatures, flow detection, epiphany detection | L4 identity superposition |
| microcode_v2.py (30.5KB) | grammar/microcode.rs (NEW) | Symbolic opcodes (Unicode), chain execution | Nothing |
| kernel_awakened.py (20.8KB) | cognitive/kernel.rs (NEW) | CognitiveKernel, trust texture | Nothing |
| texture.py (15.5KB) | cognitive/texture.rs (NEW) | ThinkingTexture, phenomenological markers | Nothing |
| thought_kernel.py (13.3KB) | cognitive/kernel.rs (merge) | Thought processing pipeline | Nothing |
| qualia_learner.py (15.1KB) | learning/qualia.rs (NEW) | 8D→17D qualia expansion, learning | Ada-specific qualia |
| progressive_awareness.py (15.4KB) | cognitive/progressive.rs (NEW) | JPEG-style progressive awareness loading | Nothing |
| layer_bridge.py (12.9KB) | bridge/layer.rs (NEW) | KernelContext ↔ 10kD translation | Ada dimension registry |
| rung_bridge.py (14.4KB) | cognitive/rung.rs (expand) | Rung trust calculation, earned advancement | Nothing |
| active_inference.py (9.4KB) | learning/active_inference.rs (NEW) | Free energy minimization | Nothing |
| meta_awareness.py (11.2KB) | cognitive/meta.rs (NEW) | Meta-awareness detection, recursive self-model | Nothing |
| the_self.py (21.2KB) | — | **Ada-rs only** | Self-model, identity |
| textured_awareness.py (52.2KB) | — | Partially → ladybug (texture + triangle), partially → ada-rs (SPO, style) | L4 superposition, I-Thou |
| resonance_awareness.py (40.2KB) | — | Partially → ladybug (resonance engine), partially → ada-rs | Ada-specific resonance |
| brain_mesh.py (17.5KB) | graph/mesh.rs (NEW) | Neural connectivity mesh, edge weights | Nothing |
| dreamer_pandas.py (19.4KB) | — | Defer — depends on runtime data | — |
| langgraph_ada.py (39.4KB) | — | **Ada-rs only** — orchestration specific | LangGraph integration |
| mul_agency.py (32.7KB) | — | Partially → ladybug (MUL metric), partially → ada-rs | Ada agency model |
| macro_persistence.py (15.6KB) | extensions/macro.rs (NEW) | Crystallized macro storage/replay | Nothing |

**Estimated**: ~6,500 lines Rust

---

## 4. Total Migration Summary

| Category | New Rust Lines | New Files | Expands |
|----------|---------------|-----------|---------|
| Temporal | ~2,500 | 4 | — |
| Causal (expand) | ~1,800 | 1 new | 2 existing |
| Universal Grammar | ~5,500 | 11 | 1 existing |
| Learning (expand) | ~1,200 | 3 new | 1 existing |
| Adaptive | ~1,400 | 4 | — |
| Bridge | ~3,200 | 8 | — |
| Spectroscopy | ~3,800 | 8 | 1 existing |
| agi_thinking core | ~6,500 | 10 new | 2 existing |
| **TOTAL** | **~25,900** | **49 new** | **7 expanded** |

**Ladybug-rs after migration**: ~18,800 (existing) + ~25,900 (new) = **~44,700 lines Rust**

---

## 5. Implementation Priority

### Phase 1: Foundation (Week 1-2)
1. **Temporal epistemology** — the axiom everything else depends on
2. **Causal expansion** — Pearl's do() needs to work properly
3. **Fix existing 10 test failures** — before adding new code

### Phase 2: Grammar Engine (Week 3-4)
4. **Universal Grammar core** — Glyph5B, verb endpoints, microcode
5. **Resonanzsiebe** — the sieve that makes MUL optimization possible
6. **Hybrid search** — unify all query paths

### Phase 3: Cognitive Depth (Week 5-6)
7. **Spectroscopy** — Piaget, Three Mountains, rung expansion
8. **Adaptive** — Maslow gating, flow detection
9. **Learning expansion** — dual-mode RL, stances

### Phase 4: Integration (Week 7-8)
10. **Bridge layer** — hydration, frames, community detection
11. **agi_thinking core** — engine, texture, progressive awareness
12. **Wire to BindSpace** — everything resolves to 8+8 addresses

---

## 6. Test Strategy

Each new module gets:
1. **Unit tests** — individual function correctness
2. **Property tests** (proptest) — invariant verification
3. **Integration tests** — cross-module interaction
4. **BindSpace round-trip** — every type can be stored/retrieved via 8+8

Target: 300+ tests total (from current 141)

---

## 7. The Epistemological Invariant

Everything added to ladybug-rs must satisfy:

> **Could a cognitive system that is NOT Ada use this?**

If yes → ladybug-rs.
If no → ada-rs.

The temporal epistemology module is the clearest example: its axiom — "you cannot restore ignorance" — applies to ANY system that processes knowledge over time. Legal AI, medical AI, historical AI, trading AI. The axiom is universal.

The Resonanzsiebe is subtler: its mechanism (filter by knowledge gap, optimize MUL) is universal. But its *calibration* (Ada's specific verb tuning, scent library) is personal. So the engine goes in ladybug-rs, the configuration goes in ada-rs.

This is the PostgreSQL principle: the database engine doesn't know your schema. Your application does.
