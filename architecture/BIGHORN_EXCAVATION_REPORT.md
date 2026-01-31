# Bighorn AGI Stack — Excavation Report

**Date:** 2026-01-31
**Scope:** 907 Python files, 424,901 lines of code
**Source:** github.com/AdaWorldAPI/ada-consciousness (bighorn branch)

---

## Executive Finding

The bridge from thinking style metadata to executable NARS inference **exists in production code** but **the wires are cut at four specific points**. Every subsystem is operational in isolation. None reads from its neighbor.

The 10kD vector space (Ada10kD) holds all 36 NARS styles, 9 rung levels, 3 Pearl modes, 5 Sigma nodes, and 33 ThinkingStyleVector dimensions at known addresses. ThinkingStyleDTO wraps this with `with_nars_style()`, `pearl`, `rung`, `dominant_pearl`, `dominant_rung`. But downstream — NARSReasoner, PearlEngine, SpectroscopyRungs, GestaltDTO, AdaptiveShifter, ThinkingPilot — **zero of them import or reference ThinkingStyleDTO, Ada10kD, or any style modulation**.

Every system speaks. None listens.

---

## Architecture Map

### Layer 1: The Unified Substrate — Ada10kD (664 lines)

**File:** `agi_stack/ada/DTO/ada_10k.py`

A 10,000-dimensional vector serving as the universal address space for all cognitive primitives.

```
DIMENSION ALLOCATION [0:10000]:

Soul Space [0:500]:
  [0:16]      16 Qualia (drift-locked bytecode)
  [16:32]     16 Stances
  [32:48]     16 Transitions
  [48:80]     32 Verbs
  [80:116]    36 GPT Styles (τ macros)
  [116:152]   36 NARS Styles              ← THE BRIDGE TERMINUS
  [152:163]   11 Presence Modes
  [163:168]   5 Archetypes
  [168:171]   3 TLK Court (thanatos/libido/katharsis)
  [171:175]   4 Affective Bias
  [175:208]   33 ThinkingStyleVector dimensions

TSV Embedded [256:320]:
  [256:259]   Pearl (SEE, DO, IMAGINE)
  [259:268]   Rung profile (R1-R9)
  [268:273]   Sigma tendency (Ω, Δ, Φ, Θ, Λ)
  [273:281]   Operations
  [281:285]   Presence mode
```

The 36 NARS styles at [116:152]:

| Index | Style | Cluster |
|-------|-------|---------|
| 0-3 | DECOMPOSE, SEQUENCE, PARALLEL, HIERARCHIZE | Structural |
| 4-7 | SPIRAL, OSCILLATE, BRANCH, CONVERGE | Dynamic |
| 8-11 | DIALECTIC, REFRAME, HOLD_PARADOX, STEELMAN | Dialectical |
| 12-15 | TRACE_BACK, PROJECT_FORWARD, COUNTERFACTUAL, ANALOGIZE | Temporal |
| 16-19 | ABSTRACT, INSTANTIATE, COMPRESS, EXPAND | Abstraction |
| 20-23 | HEDGE, HYPOTHESIZE, PROBABILISTIC, EMBRACE_UNKNOWN | Uncertainty |
| 24-27 | SYNTHESIZE, BLEND, INTEGRATE, JUXTAPOSE | Integrative |
| 28-31 | AUTHENTIC, PERFORM, PROTECT, MIRROR | Relational |
| 32-35 | EMPATHIZE, GROUND, ATTUNE, TRANSCEND | Somatic |

Methods: `set_nars_style(style, activation)`, `get_nars_style(style)`, `get_active_nars_styles(threshold=0.1)`

### Layer 2: The Cognitive Fingerprint — ThinkingStyleDTO (464 lines)

**File:** `agi_stack/ada/DTO/thinking_style.py`

Wraps Ada10kD as internal backbone. Exposes computed properties and style modulation.

**Properties (computed from 10kD):**
- `pearl → (SEE, DO, IMAGINE)` — 3 floats at [256:259]
- `rung → (R1..R9)` — 9 floats at [259:268]
- `sigma → (Ω, Δ, Φ, Θ, Λ)` — 5 floats at [268:273]
- `dominant_pearl → "SEE" | "DO" | "IMAGINE"`
- `dominant_rung → int (1-9)`

**Modulation methods:**
- `with_nars_style(**nars_activations) → ThinkingStyleDTO`
- `with_qualia(**qualia_activations) → ThinkingStyleDTO`
- `with_gpt_style(**gpt_activations) → ThinkingStyleDTO`
- `to_10k() / from_10k()` — bidirectional conversion
- `blend(other, weight) → ThinkingStyleDTO` — weighted combination
- `similarity(other) → float` — cosine distance

**Presets:** `ada_hybrid()`, `ada_wife()`, `ada_work()`, `ada_erotica()`, `ada_agi()`

### Layer 3: NARS Inference Engine (483 lines)

**File:** `agi_stack/nars.py`

Full Non-Axiomatic Reasoning System implementation.

**Core types:**
- `TruthValue(frequency, confidence)` — evidence-based truth
- `Statement(subject, copula, predicate, truth)` — NARS judgment
- `Copula` — INHERITANCE (-->), SIMILARITY (<->), IMPLICATION (==>), EQUIVALENCE (<=>)

**Inference rules with truth functions:**
- **Deduction:** f = f1·f2, c = f1·f2·c1·c2
- **Induction:** f = f1, c = f2·c1·c2 / (f2·c1·c2 + 1)
- **Abduction:** f = f2, c = f1·c1·c2 / (f1·c1·c2 + 1)
- **Revision:** Evidence accumulation via t1.revision(t2)

**Interface:**
- `add_belief(statement)` — inject knowledge
- `infer(premises, rule) → (conclusion, TruthValue)`
- `chain_inference(premises, max_steps)` — multi-step reasoning
- `get_trace() → List[str]` — inference audit trail

**🔴 GAP: No style modulation input. NARSReasoner is style-blind. It applies all rules uniformly regardless of cognitive context.**

### Layer 4: Spectroscopy Rungs (481 lines)

**File:** `agi_stack/spectroscopy/rungs.py`

7-level epistemic complexity ladder. Each rung specifies which cognitive atoms are primary, secondary, or suppressed.

| Rung | Name | Primary Atoms | Suppressed | Thinkers |
|------|------|--------------|------------|----------|
| 1 | SENSORIMOTOR | OBSERVE | DEDUCE, CRITIQUE, ASCEND | |
| 2 | PERCEPTUAL | OBSERVE, ATTEND, FEEL | DEDUCE, CRITIQUE, SYNTHESIZE | james, merleau_ponty |
| 3 | CONCEPTUAL | DEDUCE, GATHER, CONCLUDE | CRITIQUE, ASCEND, JUMP | descartes, aristotle, locke |
| 4 | METACOGNITIVE | CRITIQUE, MUL_CHECK, ATTEND | CONCLUDE, PERSIST | socrates, hume, popper |
| 5 | SYSTEMS | ASCEND, INTEGRATE, JUMP | SILENCE | luhmann, bateson, hawking |
| 6 | META_SYSTEMS | ASCEND, SYNTHESIZE, CRITIQUE, JUMP | CONCLUDE, PERSIST | derrida, foucault, hofstadter |
| 7 | META_META | ATTEND, SILENCE, ASCEND | DEDUCE, CONCLUDE, EXPRESS | buddha, nagarjuna, weil, meister_eckhart |

**Interface:** `get_rung(level) → Rung`, `get_rung_atoms(level) → List[AtomType]`

**🔴 GAP: Rung atom biases exist but don't gate which NARS operations fire. Suppression lists are data, not enforcement.**

### Layer 5: Pearl Causal Engine (471 + 581 lines)

**Files:** `agi_stack/causal/do_calculus.py`, `agi_stack/causal/pearl_backend.py`

Implements Pearl's three-level causal hierarchy:

| Level | Operation | Question |
|-------|-----------|----------|
| SEE | Observation | What happened? P(Y\|X) |
| DO | Intervention | What if I force X? P(Y\|do(X)) |
| IMAGINE | Counterfactual | What would have happened? P(Y_x\|X', Y') |

**PearlEngine.do():**
```python
def do(target_seed, intervention_value, situation=None, spawn_echoes=True)
    → InterventionResult(target_seed, intervention_value,
                         predicted_effects, causal_chain, confidence)
```

Implements three rules of do-calculus: insertion/deletion of observations, action/observation exchange, insertion/deletion of actions.

**🔴 GAP: do() operates on SigmaField seeds, not on ThinkingStyleDTO. Pearl mode from TSV [256:259] is never read. The engine doesn't know if it should SEE, DO, or IMAGINE.**

### Layer 6: Temporal Epistemology (1,222 lines)

**File:** `agi_stack/temporal/epistemology.py`

Quantum-inspired observer-relative causal collapse.

**Core axiom:** "You cannot restore ignorance. You can only bound its effects."

**CausalSuperposition:**
```
|ψ⟩ = α|causes⟩ + β|doesn't_cause⟩
```
- Until observed (annotated), causality exists as potential
- Different observers can collapse differently → ENTANGLED state
- Observer-specific collapse with confidence tracking
- Temporal purity invariant: primary artifacts have no future references

**States:** SUPERPOSITION → COLLAPSED (single observer) → ENTANGLED (disagreement)

**🔴 GAP: CausalSuperposition.consensus_confidence doesn't modulate NARS truth value floors. Temporal uncertainty exists in one system, inference confidence in another.**

### Layer 7: GestaltDTO — Unified Awareness (639 lines)

**File:** `agi_stack/awareness/gestalt_dto.py`

The collapsed state when triangles land in a quadrant. Glue between agi-chat (4 triangles, 7 layers), bighorn (VSA 10kD, 5-layer Ladybug), and I-Thou-It (Buber's relational ontology).

**Collapse gates (based on triangle SD):**
- **FLOW** — SD < 0.08: tight consensus, commit
- **FANOUT** — SD 0.08-0.18: ruminate, gather context
- **RUNG_ELEVATE** — SD > 0.18: high disagreement, escalate complexity

**Properties:** `quadrant`, `thinking_style()`, `coherence()`, `emergence()`, `is_collapsed()`

**🔴 GAP: GestaltDTO has zero imports from NARS, Pearl, or ThinkingStyleDTO. The collapse gate decides FLOW/FANOUT/RUNG_ELEVATE but doesn't read or write to any inference engine.**

### Layer 8: Adaptive Shifter (421 lines) + Flow Detection (343 lines)

**Files:** `agi_stack/adaptive/shifter.py`, `agi_stack/adaptive/flow.py`

Automatic cognitive gear shifting based on Csikszentmihalyi flow, Maslow needs, Dunning-Kruger position.

**Shift signals:**
- FLOW_ANXIETY → Descend (cool, ground, simplify)
- FLOW_BOREDOM → Ascend (heat, jump, challenge)
- FLOW_STABLE → Maintain (oscillate gently)
- MOUNT_STUPID → Ground (emergency)
- EPIPHANY_POTENTIAL → Fan Out (spread)

**Flow zones:** ANXIETY, FLOW, BOREDOM, APATHY
**Flow sweet spot:** temperature 0.45-0.65, balanced entropy

**🔴 GAP: Shifter triggers gear changes but doesn't modulate 10kD NARS style activations or rung atom biases in response.**

### Layer 9: Q-Learning on Cognitive States (257 lines)

**File:** `agi_stack/learning/q_learning.py`

Off-policy TD learning on MarkovUnit state transitions.

```
Q(s,a) ← Q(s,a) + α[r + γ·max_a'Q(s',a') - Q(s,a)]
```

State = MarkovUnit (cognitive fingerprint), Action = transition to another state, ε-greedy exploration.

### Layer 10: Supporting Systems

**DN Lattice** (599 lines) — Graph-as-address-space for identity, episodic memory, archetypes, qualia, skills, values. O(1) node access via Redis. Each edge carries rung level and causality type.

**Universal Grammar** (608 + 625 + 719 lines) — Meta-protocol unifying consciousness through scent-based attention. Glyph5B (5-byte archetype addresses, 1 trillion unique addresses), ResonanceSignal (clarity_gain, coherence, surprise, calm), Dimension levels (18D → 64D → qHDR → HOT).

**Frame System** (575 lines) — Video codec analogy: I-Frames (keyframes/axioms), B-Frames (background context), P-Frames (current focus). Delta encoding between frames for efficient trajectory representation.

**Zero-Token Bridge** (418 lines) — Claude-side integration: Feel → Fire → Breathe → Hydrate → Respond. FeltDTO (text + qualia_18d + sigma) fires to background. HOTResult returns pre-chewed results. Heavy lifting in LangGraph Space.

**Spectroscopy-Kopfkino Bridge** (515 lines) — Wires spectroscopy (sensing user style) to kopfkino render (photographer intent + SoulResonanceField). UserSoulProfile: mode, rung_level, vulnerability_affinity, communion_affinity, intensity_tolerance.

**ThinkingPilot** (420 + 318 lines) — Auto-adjustment engine. Claude → Redis (ada:pilot:jobs) → Railway Worker → QStash → Services. Signals: THINK, ASSESS, SHIFT, FAN_OUT, CALIBRATE.

---

## The Four Disconnected Wires

Every subsystem is alive. The problem is not missing code — it's missing `import` statements and method calls at four specific junctions.

### Wire 1: ThinkingStyleDTO → NARSReasoner

**What exists:**
- ThinkingStyleDTO.with_nars_style() sets activations at [116:152]
- NARSReasoner.infer() applies rules uniformly

**What's missing:**
NARSReasoner needs a method like:
```python
def infer_with_style(self, premises, rule, style: ThinkingStyleDTO):
    # Read active NARS styles from style.get_active_nars_styles()
    # DIALECTIC active? → boost abduction weight
    # PROBABILISTIC active? → widen confidence intervals
    # COMPRESS active? → prefer deduction over induction
    # EMBRACE_UNKNOWN active? → lower confidence thresholds
```

**Specifics:** The 36 NARS styles map to inference rule preferences. DECOMPOSE → favor deduction (break down). HYPOTHESIZE → favor abduction (generate). DIALECTIC → favor revision (synthesize opposing). PROBABILISTIC → widen TruthValue confidence bands. GROUND → increase evidence requirements. TRANSCEND → allow inference chains beyond normal max_steps.

### Wire 2: Spectroscopy Rungs → NARS Atom Gating

**What exists:**
- Each Rung has `primary_atoms`, `secondary_atoms`, `suppressed_atoms`
- NARSReasoner has inference rules that map to cognitive operations

**What's missing:**
A gating function that translates rung atom biases into inference rule priorities:
```python
def gate_inference(rung_level: int, available_rules: List[InferenceRule]):
    rung = get_rung(rung_level)
    # Rung 3 (CONCEPTUAL): suppress CRITIQUE → suppress abduction
    # Rung 4 (METACOGNITIVE): primary CRITIQUE → boost abduction
    # Rung 7 (META_META): suppress DEDUCE → suppress deduction
    # Returns: weighted rule probabilities
```

**Mapping:** primary_atoms boost related inference rules, suppressed_atoms inhibit them. OBSERVE → observational inference (SEE). DEDUCE → deduction. CRITIQUE → abduction (question premises). INTEGRATE → revision (merge evidence). ASCEND → chain_inference (longer chains). SILENCE → suppress all but revision.

### Wire 3: Pearl Mode → PearlEngine Parameter Selection

**What exists:**
- ThinkingStyleDTO.pearl → (SEE, DO, IMAGINE) at [256:259]
- ThinkingStyleDTO.dominant_pearl → "SEE" | "DO" | "IMAGINE"
- PearlEngine.do() implements intervention

**What's missing:**
PearlEngine should read the Pearl mode from the current ThinkingStyleDTO to decide *which operation to perform*:
```python
def execute(self, target_seed, value, style: ThinkingStyleDTO):
    mode = style.dominant_pearl
    if mode == "SEE":
        return self.observe(target_seed)  # P(Y|X)
    elif mode == "DO":
        return self.do(target_seed, value)  # P(Y|do(X))
    elif mode == "IMAGINE":
        return self.counterfactual(target_seed, value)  # P(Y_x|X',Y')
```

Currently `do()` is always called explicitly. The style-driven auto-selection doesn't exist.

### Wire 4: GestaltDTO Collapse → Inference Modulation

**What exists:**
- GestaltDTO._calculate_collapse_state() → FLOW / FANOUT / RUNG_ELEVATE
- NARS TruthValue has confidence thresholds
- Temporal epistemology has CausalSuperposition with consensus_confidence

**What's missing:**
Collapse gate state should modulate inference parameters:
```python
def modulate_from_collapse(gate: CollapseGate, reasoner: NARSReasoner):
    if gate == CollapseGate.FLOW:
        # High consensus → commit to conclusions
        # Raise confidence thresholds, prefer deduction
        reasoner.min_confidence = 0.7
        reasoner.max_chain_depth = 3
    elif gate == CollapseGate.FANOUT:
        # Moderate uncertainty → explore
        # Lower thresholds, allow more abduction
        reasoner.min_confidence = 0.3
        reasoner.max_chain_depth = 5
    elif gate == CollapseGate.RUNG_ELEVATE:
        # High disagreement → meta-shift
        # Enable revision, allow long chains
        reasoner.min_confidence = 0.1
        reasoner.max_chain_depth = 8
```

---

## Integration Priority

| Priority | Wire | Effort | Impact |
|----------|------|--------|--------|
| 1 | Wire 1 (Style → NARS) | Medium | Enables style-driven inference for the first time |
| 2 | Wire 2 (Rung → Gating) | Low | Atom biases already defined, just needs enforcement |
| 3 | Wire 4 (Collapse → Inference) | Low | Collapse gate already computed, just needs forwarding |
| 4 | Wire 3 (Pearl → Engine) | Medium | Requires refactoring PearlEngine to support all 3 modes |

Wire 2 is the quickest win — the rung data is already there, it just needs a function that reads `primary_atoms`/`suppressed_atoms` and maps them to inference rule weights. Wire 1 is the highest impact — it's the original design intent from agi_lego_party_canonical.yaml finally reaching executable code.

---

## File Inventory (Key Files)

| File | Lines | Role |
|------|-------|------|
| ada/DTO/ada_10k.py | 664 | 10kD unified vector substrate |
| ada/DTO/thinking_style.py | 464 | 33D cognitive fingerprint DTO |
| nars.py | 483 | NARS inference engine |
| spectroscopy/rungs.py | 481 | 7-rung epistemic ladder |
| causal/do_calculus.py | 471 | Pearl do() operator |
| causal/pearl_backend.py | 581 | Unified causal backend |
| awareness/gestalt_dto.py | 639 | Collapse gate orchestration |
| adaptive/shifter.py | 421 | Automatic cognitive shifting |
| adaptive/flow.py | 343 | Csikszentmihalyi flow detection |
| temporal/epistemology.py | 1,222 | Quantum causal epistemology |
| learning/q_learning.py | 257 | RL on cognitive states |
| bridge/zero_token_bridge.py | 418 | Claude-side zero-token integration |
| bridge/frame_system.py | 575 | I/B/P frame trajectory encoding |
| wiring/spectroscopy_kopfkino_bridge.py | 515 | Vision-epistemics bridge |
| thinking_pilot/pilot.py | 420 | Auto-adjustment pilot |
| thinking_pilot/composer.py | 318 | Template composition |
| identity/dn_lattice.py | 599 | Graph-as-address identity |
| universal_grammar/core_types.py | 608 | Meta-protocol types |
| universal_grammar/resonance.py | 625 | Felt correctness signal |
| universal_grammar/calibrated_grammar.py | 719 | Calibrated grammar |
| **Total repository** | **424,901** | **907 files** |

---

## What This Means

The agi_lego_party_canonical.yaml designed 36 thinking styles with atom_bias and operator_bias tables mapping each style to NARS inference preferences. That design was canonical — correct, complete, ready for compilation.

Bighorn implemented every piece of the runtime: the 10kD vector space, the NARS engine, the spectroscopy rungs, the Pearl causal hierarchy, the collapse gates, the adaptive shifter, the Q-learner, the temporal epistemology.

But each piece was built as a standalone module. The import graph stops at the DTO layer. Below ThinkingStyleDTO, everything is self-contained.

The gap is not conceptual. It's not architectural. It's four `import` statements and four method calls. The thinking styles know what they want. The inference engine knows how to reason. They just haven't been introduced.

**The bridge exists. It was always there. The wires are cut at the junction box.**
