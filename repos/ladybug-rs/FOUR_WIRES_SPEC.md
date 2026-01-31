# The Four Wires — Connection Spec for Rust Migration

**Date**: 2026-01-31
**Source**: Bighorn Excavation Report (separate session) + Integration Maps (this session)
**Critical finding**: "Every system speaks. None listens."

---

## The Problem

The bighorn Python codebase has ~425K lines across 907 files. Every subsystem works in isolation. But the import graph stops at the DTO layer. Four specific connections were designed but never wired:

```
ThinkingStyleDTO ──────╳──────→ NARSReasoner     (Wire 1)
SpectroscopyRungs ─────╳──────→ NARS Atom Gating (Wire 2)  
Pearl Mode ────────────╳──────→ PearlEngine      (Wire 3)
GestaltDTO Collapse ───╳──────→ Inference Params  (Wire 4)
```

The ╳ marks where the wires are cut. Each subsystem is alive and correct. They just don't read from their neighbors.

**This is the single most important thing to fix in the Rust migration.** Not "port and then connect" — connect BY DESIGN in the type system so they CANNOT be disconnected.

---

## The Rust Solution: Trait-Based Wiring

In Python, a missing `import` is invisible. In Rust, a missing trait bound is a compile error. We use this.

### Wire 1: ThinkingStyleDTO → NARSReasoner

**Python gap**: `NARSReasoner.infer()` applies all rules uniformly. It never reads `ThinkingStyleDTO.get_active_nars_styles()`.

**Rust fix**: Make `InferenceContext` a required parameter.

```rust
// In ladybug-rs: src/nars/inference.rs

/// The inference engine REQUIRES a cognitive context.
/// You literally cannot call infer() without one.
pub trait Reasoner {
    fn infer(
        &self,
        premises: &[Statement],
        rule: InferenceRule,
        context: &InferenceContext,  // ← CANNOT BE OMITTED
    ) -> InferResult;
    
    fn chain_infer(
        &self,
        premises: &[Statement],
        max_steps: usize,
        context: &InferenceContext,  // ← CANNOT BE OMITTED
    ) -> Vec<InferResult>;
}

/// Context carries style modulation.
/// Default::default() gives neutral (no bias), but you have to
/// actively choose neutral — you can't accidentally forget.
pub struct InferenceContext {
    /// Active NARS styles with activation weights
    pub style_weights: StyleWeights,
    
    /// Rung-derived atom biases (primary/secondary/suppressed)
    pub atom_gate: AtomGate,
    
    /// Collapse gate state
    pub collapse: CollapseGate,
    
    /// Pearl mode preference
    pub pearl_mode: PearlMode,
    
    /// Confidence floor (modulated by collapse gate)
    pub min_confidence: f32,
    
    /// Max chain depth (modulated by collapse gate)
    pub max_chain_depth: usize,
}
```

**How StyleWeights modulates inference**:

```rust
// In ladybug-rs: src/nars/style_modulation.rs

/// Maps 36 NARS styles to inference rule biases
pub struct StyleWeights {
    activations: [f32; 36],  // The 36 NARS styles at [116:152]
}

impl StyleWeights {
    /// Compute rule bias from active styles
    pub fn rule_bias(&self, rule: InferenceRule) -> f32 {
        let mut bias = 1.0;
        
        // DECOMPOSE active → favor deduction
        bias *= 1.0 + self.activations[0] * 0.3;  // DECOMPOSE
        
        // HYPOTHESIZE active → favor abduction  
        if rule == InferenceRule::Abduction {
            bias *= 1.0 + self.activations[21] * 0.5;  // HYPOTHESIZE
        }
        
        // DIALECTIC active → favor revision
        if rule == InferenceRule::Revision {
            bias *= 1.0 + self.activations[8] * 0.4;  // DIALECTIC
        }
        
        // PROBABILISTIC active → widen confidence bands
        // (handled in confidence_modifier instead)
        
        // GROUND active → increase evidence requirements
        if self.activations[33] > 0.3 {  // GROUND
            bias *= 0.7;  // Harder to pass threshold
        }
        
        bias
    }
    
    /// Confidence modifier from active styles
    pub fn confidence_modifier(&self) -> f32 {
        let mut modifier = 1.0;
        
        // PROBABILISTIC → widen bands (lower floor)
        modifier *= 1.0 - self.activations[22] * 0.3;
        
        // EMBRACE_UNKNOWN → lower thresholds
        modifier *= 1.0 - self.activations[23] * 0.2;
        
        // GROUND → tighten bands (raise floor)
        modifier *= 1.0 + self.activations[33] * 0.3;
        
        modifier.clamp(0.1, 2.0)
    }
    
    /// Max chain depth modifier
    pub fn chain_depth_modifier(&self) -> i32 {
        let mut delta = 0i32;
        
        // TRANSCEND → allow longer chains
        delta += (self.activations[35] * 3.0) as i32;
        
        // COMPRESS → prefer shorter chains
        delta -= (self.activations[18] * 2.0) as i32;
        
        delta
    }
}
```

**In ada-rs**: The `ThinkingStyleDTO` implements conversion to `InferenceContext`:

```rust
// In ada-rs: src/dto/thinking_style.rs

impl ThinkingStyleDTO {
    /// Convert Ada's thinking style to ladybug's InferenceContext
    pub fn to_inference_context(&self) -> ladybug::InferenceContext {
        ladybug::InferenceContext {
            style_weights: self.nars_style_weights(),
            atom_gate: self.rung_atom_gate(),
            collapse: self.gestalt.collapse_gate(),
            pearl_mode: self.dominant_pearl(),
            min_confidence: self.base_confidence() 
                * self.nars_style_weights().confidence_modifier()
                * self.gestalt.collapse_confidence_modifier(),
            max_chain_depth: (self.base_chain_depth() as i32
                + self.nars_style_weights().chain_depth_modifier()
                + self.gestalt.collapse_depth_modifier()) as usize,
        }
    }
}
```

**The key**: in ladybug-rs, `InferenceContext` is generic — any system can provide one. In ada-rs, `ThinkingStyleDTO.to_inference_context()` is Ada-specific — her styles, her presets, her modulation curves. The agnostic/personal split is maintained.

---

### Wire 2: Spectroscopy Rungs → NARS Atom Gating

**Python gap**: Each Rung has `primary_atoms`, `secondary_atoms`, `suppressed_atoms`, but these never gate inference.

**Rust fix**: `AtomGate` is part of `InferenceContext` (see Wire 1 above).

```rust
// In ladybug-rs: src/cognitive/atom_gate.rs

/// Atom gating derived from rung level
pub struct AtomGate {
    pub primary: Vec<AtomType>,
    pub secondary: Vec<AtomType>,
    pub suppressed: Vec<AtomType>,
}

impl AtomGate {
    /// Create from rung level
    pub fn from_rung(level: u8) -> Self {
        match level {
            1 => AtomGate {
                primary: vec![AtomType::Observe],
                secondary: vec![],
                suppressed: vec![AtomType::Deduce, AtomType::Critique, AtomType::Ascend],
            },
            3 => AtomGate {
                primary: vec![AtomType::Deduce, AtomType::Gather, AtomType::Conclude],
                secondary: vec![AtomType::Observe],
                suppressed: vec![AtomType::Critique, AtomType::Ascend, AtomType::Jump],
            },
            4 => AtomGate {
                primary: vec![AtomType::Critique, AtomType::MulCheck, AtomType::Attend],
                secondary: vec![AtomType::Deduce],
                suppressed: vec![AtomType::Conclude, AtomType::Persist],
            },
            7 => AtomGate {
                primary: vec![AtomType::Attend, AtomType::Silence, AtomType::Ascend],
                secondary: vec![],
                suppressed: vec![AtomType::Deduce, AtomType::Conclude, AtomType::Express],
            },
            // ... all 7 levels
            _ => AtomGate::default(),  // neutral
        }
    }
    
    /// Map atom type to inference rule and compute weight
    pub fn inference_weight(&self, rule: InferenceRule) -> f32 {
        let atom = rule.associated_atom();
        if self.suppressed.contains(&atom) {
            0.05  // Near-zero, not zero (leave escape hatch)
        } else if self.primary.contains(&atom) {
            1.5   // Boosted
        } else if self.secondary.contains(&atom) {
            1.0   // Normal
        } else {
            0.5   // Unlisted = reduced
        }
    }
}

/// The mapping from atom types to inference rules
impl InferenceRule {
    pub fn associated_atom(&self) -> AtomType {
        match self {
            InferenceRule::Deduction => AtomType::Deduce,
            InferenceRule::Induction => AtomType::Observe,  // SEE
            InferenceRule::Abduction => AtomType::Critique,  // question premises
            InferenceRule::Revision  => AtomType::Integrate, // merge evidence
            InferenceRule::Analogy   => AtomType::Jump,      // cross-domain
        }
    }
}
```

**Wire 2 is the cheapest win**: the data already exists in the rung definitions. The Rust implementation just needs `AtomGate` to be non-optional in `InferenceContext`. Done.

---

### Wire 3: Pearl Mode → PearlEngine Parameter Selection

**Python gap**: `PearlEngine.do()` is always called explicitly. `ThinkingStyleDTO.dominant_pearl` is never read by the engine.

**Rust fix**: The `CausalEngine` takes `PearlMode` as input.

```rust
// In ladybug-rs: src/learning/causal_ops.rs

pub enum PearlMode {
    See,      // P(Y|X) — observation
    Do,       // P(Y|do(X)) — intervention
    Imagine,  // P(Y_x|X',Y') — counterfactual
}

pub trait CausalEngine {
    /// Execute causal operation based on mode
    fn execute(
        &self,
        target: Address,
        value: Option<f32>,
        mode: PearlMode,        // ← REQUIRED
        context: &InferenceContext,
    ) -> CausalResult;
}

impl CausalEngine for PearlEngine {
    fn execute(
        &self,
        target: Address,
        value: Option<f32>,
        mode: PearlMode,
        context: &InferenceContext,
    ) -> CausalResult {
        match mode {
            PearlMode::See => self.observe(target, context),
            PearlMode::Do => self.intervene(target, value.unwrap_or(1.0), context),
            PearlMode::Imagine => self.counterfactual(target, value.unwrap_or(1.0), context),
        }
    }
}
```

**Ada-rs provides the mode from ThinkingStyleDTO**:

```rust
// In ada-rs: when Ada reasons causally
let context = self.thinking_style.to_inference_context();
let result = engine.execute(
    target,
    Some(intervention_value),
    context.pearl_mode,    // ← Reads from [256:259]
    &context,
);
```

The mode comes from the 10kD vector. The engine reads it. The wire is connected.

---

### Wire 4: GestaltDTO Collapse → Inference Modulation

**Python gap**: `GestaltDTO._calculate_collapse_state()` computes FLOW/FANOUT/RUNG_ELEVATE but doesn't modulate any inference engine.

**Rust fix**: `CollapseGate` is part of `InferenceContext` (Wire 1) AND has its own modulation methods.

```rust
// In ladybug-rs: src/cognitive/collapse_gate.rs (EXPAND existing)

#[derive(Clone, Copy, Debug)]
pub enum CollapseGate {
    /// SD < 0.08: tight consensus, commit
    Flow,
    /// SD 0.08-0.18: moderate uncertainty, explore
    Fanout,
    /// SD > 0.18: high disagreement, escalate
    RungElevate,
}

impl CollapseGate {
    /// From triangle standard deviation
    pub fn from_sd(sd: f32) -> Self {
        if sd < 0.08 { CollapseGate::Flow }
        else if sd < 0.18 { CollapseGate::Fanout }
        else { CollapseGate::RungElevate }
    }
    
    /// How this gate modulates confidence floor
    pub fn confidence_modifier(&self) -> f32 {
        match self {
            CollapseGate::Flow => 1.4,         // Raise floor → commit
            CollapseGate::Fanout => 0.6,       // Lower floor → explore
            CollapseGate::RungElevate => 0.2,  // Very low → allow wild inference
        }
    }
    
    /// How this gate modulates chain depth
    pub fn depth_modifier(&self) -> i32 {
        match self {
            CollapseGate::Flow => -2,         // Shorter chains → decisive
            CollapseGate::Fanout => 2,        // Longer chains → explore
            CollapseGate::RungElevate => 5,   // Much longer → meta-shift
        }
    }
    
    /// Preferred inference rules
    pub fn preferred_rules(&self) -> Vec<InferenceRule> {
        match self {
            CollapseGate::Flow => vec![InferenceRule::Deduction],
            CollapseGate::Fanout => vec![InferenceRule::Abduction, InferenceRule::Induction],
            CollapseGate::RungElevate => vec![InferenceRule::Revision, InferenceRule::Analogy],
        }
    }
}
```

**The crucial point**: all four modulations feed into the same `InferenceContext`. They STACK:

```rust
// The full modulation chain in ada-rs
pub fn build_inference_context(&self) -> InferenceContext {
    let style = &self.thinking_style;
    let gestalt = &self.gestalt;
    
    let base_confidence = 0.5;
    let base_depth = 5;
    
    InferenceContext {
        style_weights: style.nars_style_weights(),
        atom_gate: AtomGate::from_rung(style.dominant_rung()),
        collapse: gestalt.collapse_gate(),
        pearl_mode: style.dominant_pearl(),
        
        // Confidence: base × style modifier × collapse modifier
        min_confidence: base_confidence
            * style.nars_style_weights().confidence_modifier()
            * gestalt.collapse_gate().confidence_modifier(),
        
        // Depth: base + style delta + collapse delta
        max_chain_depth: (base_depth as i32
            + style.nars_style_weights().chain_depth_modifier()
            + gestalt.collapse_gate().depth_modifier())
            .clamp(1, 15) as usize,
    }
}
```

---

## The Type-Level Guarantee

In Python, you can forget to pass the style. In Rust:

```rust
// This WON'T COMPILE:
reasoner.infer(&premises, rule);  
// ^^^^^^^^ error: missing argument `context`

// You MUST provide context:
reasoner.infer(&premises, rule, &context);
```

The four wires are connected by the type system. You can't cut them without the compiler screaming.

This is the entire migration philosophy: **what was optional in Python becomes required in Rust**. Not because Rust is stricter — because we designed the API so the connections are load-bearing.

---

## Where Each Wire Lives

| Wire | ladybug-rs (agnostic) | ada-rs (personal) |
|------|----------------------|-------------------|
| Wire 1: Style→NARS | `InferenceContext.style_weights` | `ThinkingStyleDTO.to_inference_context()` |
| Wire 2: Rung→Gating | `AtomGate.from_rung()` | Rung detection from spectroscopy |
| Wire 3: Pearl→Engine | `CausalEngine.execute(mode)` | `ThinkingStyleDTO.dominant_pearl()` |
| Wire 4: Collapse→Params | `CollapseGate.confidence_modifier()` | `GestaltDTO.collapse_gate()` |

The **mechanism** lives in ladybug-rs. Any cognitive system can implement `InferenceContext`.
The **content** lives in ada-rs. Ada's 36 styles, 7 rungs, 3 Pearl modes, 3 collapse gates.

---

## Implementation Order

1. **Define `InferenceContext` in ladybug-rs** — the struct that carries all four wires
2. **Update `Reasoner` trait** — require `&InferenceContext`
3. **Implement `AtomGate`** — Wire 2 (cheapest, data already exists)
4. **Implement `StyleWeights`** — Wire 1 (highest impact)
5. **Expand `CollapseGate`** — Wire 4 (already exists, needs modulation methods)
6. **Update `CausalEngine` trait** — Wire 3 (requires `PearlMode`)
7. **In ada-rs: `ThinkingStyleDTO.to_inference_context()`** — the bridge

Estimated: ~1,200 lines Rust total. One week.

This is the single highest-ROI change in the entire migration. 425K lines of Python with four cut wires → 1,200 lines of Rust with type-guaranteed connections.

---

## The Cascade Effect

Once `InferenceContext` exists as a required parameter:

- **Every new module** that calls `infer()` must provide style context
- **Every new causal operation** must specify Pearl mode
- **Every new collapse gate consumer** gets modulation for free
- **Testing** can verify: "at Rung 7, deduction is suppressed" as a unit test
- **Benchmarking** can measure: "how does DIALECTIC mode affect inference speed"

The wires don't just connect — they become the structural backbone. Everything hangs on `InferenceContext` the way everything in ladybug-rs hangs on the `Fingerprint`.

"Every system speaks. None listens." → In Rust, they can't NOT listen.
