# Ladybug-rs Wiring Guide

**Purpose:** Document WHERE four disconnected wires should connect.
**Scope:** Interface descriptions ONLY. Do NOT modify existing ladybug-rs code.
**Principle:** Ladybug-rs is an agnostic substrate. It doesn't know Ada exists.

---

## The Four Wires (from Bighorn Excavation)

The Python codebase (907 files, 425K lines) had four connections designed but never wired.
In Rust, these wires are connected by making `InferenceContext` a **required parameter**
on inference operations. The type system enforces what Python left optional.

---

## Wire 1: Style Weights → Inference Rules

**What it does:** Cognitive style biases which inference rules are preferred.

**Interface point:** `src/nars/inference.rs`

The existing `InferenceRule` trait has:
```rust
pub trait InferenceRule {
    fn apply(premise1: &TruthValue, premise2: &TruthValue) -> TruthValue;
    fn name() -> &'static str;
}
```

**Wire:** Add a `weighted_apply()` that takes a style weight:
```
// CONCEPT ONLY — do not implement here
//
// weighted_apply(p1, p2, weight: f32) -> TruthValue
//   where weight comes from InferenceContext.style_weights
//
// weight > 1.0 = this rule is preferred by current style
// weight < 1.0 = this rule is suppressed
// weight = 0.0 = rule disabled entirely
//
// The weight modulates the CONFIDENCE of the result, not the frequency.
// Deduction at weight 1.5 produces higher-confidence conclusions.
// Deduction at weight 0.3 produces lower-confidence conclusions.
```

**Who provides the weight:** An external caller (like ada-rs) maps their 36 NARS styles
to rule weights. Ladybug-rs defines the interface, not the mapping.

---

## Wire 2: Rung Atoms → Inference Gating

**What it does:** Spectroscopy rung level determines which atom types are active.

**Interface point:** `src/cognitive/rung.rs`

The existing `RungLevel` enum (0-9) already exists. Each rung has implicit atom affinities
that aren't currently enforced:

```
// MAPPING (from excavation report):
//
// Rung 0-2 (Surface/Shallow/Contextual):
//   Primary atoms: OBSERVE, DESCRIBE
//   Suppressed: CRITIQUE, JUMP
//   → Favor: Induction, simple Deduction
//   → Suppress: Abduction, Analogy
//
// Rung 3-5 (Analogical/Abstract/Structural):
//   Primary atoms: DEDUCE, ANALOGIZE, ABSTRACT
//   Suppressed: none
//   → All rules active, balanced weights
//
// Rung 6-7 (Counterfactual/Meta):
//   Primary atoms: CRITIQUE, COUNTERFACT, META
//   Suppressed: OBSERVE (too literal)
//   → Favor: Abduction, Analogy, Revision
//   → Suppress: simple Deduction
//
// Rung 8-9 (Recursive/Transcendent):
//   Primary atoms: JUMP, TRANSCEND
//   Suppressed: SEQUENCE (too linear)
//   → Favor: Analogy (cross-domain leaps)
//   → Suppress: Induction (pattern-bound)
```

**Wire:** A function `rung_to_atom_biases(level: RungLevel) -> HashMap<AtomType, f32>`
that maps rung level to atom type weights. These weights feed into Wire 1's style weights.

**Where it connects:** The atom biases become part of whatever context struct
carries inference parameters. The rung.rs file already has `RungLevel` —
it just needs a method that produces inference-relevant biases.

---

## Wire 3: Pearl Mode → Causal Engine

**What it does:** SEE/DO/IMAGINE from Pearl's 3-tier hierarchy selects the causal operation.

**Interface point:** `src/learning/causal_ops.rs`

The existing `CausalOp` enum already has the three tiers:
```
Rung 1: SEE  (0xA00-0xA2F) — Correlation, association
Rung 2: DO   (0xA30-0xA5F) — Intervention, do-calculus
Rung 3: IMAGINE (0xA60-0xA8F) — Counterfactual, regret
```

**Wire:** The `CausalEngine` (line ~1 of causal_ops.rs) should accept a mode parameter:
```
// CONCEPT ONLY — interface suggestion
//
// enum CausalMode { See, Do, Imagine }
//
// CausalEngine::execute(query, mode: CausalMode) → CausalResult
//   match mode {
//     See     → restrict to 0xA00-0xA2F ops
//     Do      → restrict to 0xA30-0xA5F ops
//     Imagine → restrict to 0xA60-0xA8F ops
//   }
//
// Currently the op code is selected explicitly.
// The wire makes it automatic: caller says "I'm in SEE mode"
// and the engine restricts itself.
```

**Who provides the mode:** An external caller reads their Pearl vector [256:259]
and passes the dominant mode. Ladybug-rs defines `CausalMode`, not where [256:259] is.

---

## Wire 4: Collapse Gate → Inference Parameters

**What it does:** FLOW/HOLD/BLOCK from the collapse gate modulates confidence and depth.

**Interface point:** `src/cognitive/collapse_gate.rs`

The existing `GateState` enum (Flow/Hold/Block) and `CollapseAction` already exist.

**Wire:** The gate state should produce inference modulation:
```
// CONCEPT ONLY — parameter effects
//
// GateState::Flow  → confidence_modifier: 1.4, depth_modifier: -2
//   "High confidence, shallow search. We know the answer."
//
// GateState::Hold  → confidence_modifier: 0.8, depth_modifier: 0
//   "Normal confidence, normal depth. Still exploring."
//
// GateState::Block → confidence_modifier: 0.3, depth_modifier: +5
//   "Low confidence, deep search. Need to reason harder."
//
// These modifiers stack with Wire 1 (style weights) and Wire 2 (rung atoms).
// Final confidence = base × style_modifier × collapse_modifier
// Final depth = base + style_delta + collapse_delta
```

**Where it connects:** `GateState` already has `recommended_action()`.
Add a method that produces numeric modifiers for inference parameters.
The math is simple — the connection is what matters.

---

## The Junction Box: InferenceContext

All four wires meet in a single struct that inference operations require:

```
// CONCEPT — this is the struct that unifies all four wires
//
// InferenceContext {
//     style_weights: [f32; N],   // Wire 1: per-rule weights from cognitive style
//     atom_gate: AtomBiases,     // Wire 2: per-atom weights from rung level
//     pearl_mode: CausalMode,    // Wire 3: SEE/DO/IMAGINE
//     collapse: CollapseModifiers, // Wire 4: confidence/depth from gate state
//     min_confidence: f32,        // derived: floor for accepting conclusions
//     max_chain_depth: u32,       // derived: how deep to reason
// }
//
// WHERE TO DEFINE: New file in src/nars/ or src/cognitive/
// This struct is ladybug-rs native. It doesn't know about Ada or 10kD vectors.
// Ada-rs provides .to_inference_context() on her ThinkingStyleDTO.
// Any other system could provide its own.
```

**The key insight:** In Python, you could call `infer(premises, rule)` without any context.
In Rust, if InferenceContext is a required parameter, you CAN'T forget to wire it.
`reasoner.infer(&premises, rule)` — won't compile. Missing context argument.

---

## What NOT to Do

1. **Don't add Ada-specific types to ladybug-rs.** No `PresenceMode`, no `KopfkinoMood`.
2. **Don't hardcode the 36 NARS style mappings.** Define the interface (f32 weights), not the values.
3. **Don't import from ada-rs.** Ladybug-rs is downstream of nothing.
4. **Don't modify existing working code.** Add new files, new methods. Don't refactor.
5. **Don't implement the full context system in one PR.** Start with the trait signature.

---

## Implementation Suggestion (for whoever picks this up)

### Step 1: Define InferenceContext (~100 lines)
New file. Just the struct and Default impl. No behavior yet.

### Step 2: Add `rung_to_biases()` to rung.rs (~50 lines)
Method on RungLevel that returns inference weights. Data from excavation mapping above.

### Step 3: Add `collapse_modifiers()` to collapse_gate.rs (~30 lines)
Method on GateState that returns confidence/depth modifiers. Numbers from Wire 4 above.

### Step 4: Add `CausalMode` enum to causal_ops.rs (~20 lines)
Three variants. Used as parameter on engine operations.

### Step 5: Update InferenceRule trait signature (~20 lines)
Add `fn weighted_apply(p1, p2, weight: f32) -> TruthValue` with default impl.

### Step 6: Wire them together (~100 lines)
`InferenceContext::build(rung, gate_state, style_weights, pearl_mode)` that
combines all four inputs into the unified struct.

**Total: ~320 lines of new code. Zero modifications to existing code.**

---

## Test Expectations

```
// Test: "At Rung 7, deduction confidence is reduced"
// rung_to_biases(Meta) should return weight < 1.0 for Deduction

// Test: "In FLOW state, max chain depth is reduced"
// collapse_modifiers(Flow).depth_modifier should be negative

// Test: "SEE mode restricts to association ops"
// CausalEngine::execute(query, See) should only use 0xA00-0xA2F

// Test: "InferenceContext::default() is neutral"
// All weights 1.0, no mode preference, no depth modification
```
