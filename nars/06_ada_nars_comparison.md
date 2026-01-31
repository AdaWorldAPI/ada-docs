# Ada vs OpenNARS: Cognitive Architecture Comparison

## Executive Summary

Ada's architecture has evolved a **hybrid cognitive system** that draws inspiration from NARS but diverges significantly in implementation philosophy:

| Aspect | OpenNARS | Ada System |
|--------|----------|------------|
| **Core Logic** | NAL (Non-Axiomatic Logic) 9 layers | VSA 10K binary Hamming + NARS-inspired thinking styles |
| **Rung System** | NAL-1 through NAL-9 grammar layers | 9 Cognitive Rungs (R1-R9) + dynamic rung shifts |
| **Counterfactual** | NAL-7 temporal inference | Pearl's do-calculus + Temporal Epistemology |
| **Memory** | Conceptual network + bags | Redis persistence + LanceDB vectors + Neo4j graphs |
| **Control** | Budget (p,d,q) priorities | Triangle collapse gates (FLOW/HOLD/BLOCK) |
| **Truth Values** | (frequency, confidence) | 48-bit semantic signatures + resonance scores |

---

## 1. The Rung Systems

### OpenNARS NAL Layers (NAL-1 to NAL-9)

From Pei Wang's NARS theory:

```
NAL-1: Atomic inheritance statements
NAL-2: Set theory concepts (similarity, instance, property)
NAL-3: Compound terms (intersection, union, difference)
NAL-4: Products and images
NAL-5: Propositional logic (implication, equivalence)
NAL-6: Variable terms (hypothetical inference, meta-logic)
NAL-7: Temporal inference (events, predictions)
NAL-8: Procedural inference (operations, goals)
NAL-9: Self-referential operations (self-awareness, self-control)
```

**Key characteristic**: Each NAL layer extends grammar + inference rules progressively.

### Ada's 9 Cognitive Rungs (R1-R9)

From `bighorn/extension/agi_thinking/rung_bridge.py`:

```python
class CognitiveRung(IntEnum):
    OBSERVE = 1        # Perceptual awareness
    REACT = 2          # Stimulus-response (ACT-R procedural)
    RESOLVE = 3        # Goal-directed problem solving
    DELIBERATE = 4     # Deliberative reasoning (ACT-R declarative)
    META = 5           # Metacognition
    EMPATHIC = 6       # Theory of mind
    COUNTERFACTUAL = 7 # Counterfactual reasoning  ← Pearl's ladder!
    PARADOX = 8        # Dialectical integration
    COMMUNION = 9      # Multi-agent coherence
```

**Key difference**: Ada's rungs are about **cognitive depth/mode**, not grammar extension.

### Rung Shift Policy (agi-chat)

From `agi-chat/src/thinking/rung-shift.ts`:

```typescript
// Rung shift occurs ONLY upon:
//   1. Sustained non-collapse (BLOCK state persists)
//   2. Predictive failure (P metric drops)
//   3. Structural mismatch (Grammar allows no legal local parse)

// Semantic meaning of each rung:
RUNG_SEMANTICS = {
  0: 'Surface — literal, immediate meaning',
  1: 'Shallow — simple inference, common implicature',
  2: 'Contextual — situation-dependent interpretation',
  3: 'Analogical — metaphor, similarity-based reasoning',
  4: 'Abstract — generalized patterns, principles',
  5: 'Structural — schema-level understanding',
  6: 'Counterfactual — what-if reasoning, alternatives',  ← Pearl Rung 3
  7: 'Meta — reasoning about reasoning',
  8: 'Recursive — self-referential, strange loops',
  9: 'Transcendent — beyond normal semantic bounds',
}
```

---

## 2. Truth Values and Uncertainty

### OpenNARS Truth Values

```
Truth = (frequency, confidence)

frequency: How often the statement is true (0-1)
confidence: How much evidence we have (0-1)

Revision rule combines evidence:
  c = (c1 + c2) / (c1 + c2 + 1)  // Diminishing returns on confidence
```

### Ada's Thinking Style Signatures

From `ada-consciousness/docs/dragonfly-vsa/NARS_THINKING_STYLES.md`:

```python
# 36 thinking styles mapped to 48-bit semantic signatures
def style_to_seed(style: Dict) -> SigmaSeed:
    meaning_48d = np.zeros(48)
    
    # NARS-inspired parameters
    alpha = style.get('alpha', 0.5)      # Focus (like NARS attention)
    gamma = style.get('gamma', 0.5)      # Emotionality
    omega_tilde = style.get('omega_tilde', 0.5)  # Uncertainty tolerance
    
    # Map to semantic axes
    meaning_48d[AXIS['certain']] = alpha
    meaning_48d[AXIS['open']] = omega_tilde
    
    # Binarize to 48-bit signature
    bits = (meaning_48d > 0.5).astype(np.uint8)
    return SigmaSeed(NODE_TYPES['Θ'], bits)
```

**Performance**: Ada's Hamming operations are ~60-200x faster than float-based truth operations.

---

## 3. Counterfactual Reasoning

### Pearl's Ladder of Causation (Standard)

```
Rung 1: Association (seeing)     — P(Y|X) — What if I see X?
Rung 2: Intervention (doing)     — P(Y|do(X)) — What if I do X?
Rung 3: Counterfactual (imagining) — P(Y_x|X',Y') — What if X had been different?
```

### OpenNARS Temporal Inference (NAL-7)

- Events with temporal attributes
- Temporal chaining between events
- Prediction and explanation through temporal implication
- **Limitation**: No explicit do-calculus; causation learned from temporal patterns

### Ada's Pearl Engine (do-calculus)

From `ada-consciousness/causal/do_calculus.py`:

```python
class PearlEngine:
    def do(self, target_seed, intervention_value, situation, spawn_echoes=True):
        """
        Pearl's do() operator.
        
        This is NOT observation. This is intervention.
        We "cut" incoming edges to target and force its value.
        """
        # 1. Create mutilated graph (cut incoming edges)
        mutilated = situation.dag.copy()
        for parent in incoming:
            mutilated.remove_edge(parent, target_seed)
        
        # 2. Set intervention value
        # 3. Propagate forward through mutilated graph
        # 4. Spawn regret echoes for lost states
        
        return InterventionResult(...)
    
    def counterfactual(self, actual_seed, hypothetical_seed, situation):
        """What if X had happened instead of Y?"""
        actual = current_resonances
        counterfactual = self.do(hypothetical_seed, 0.9).predicted_effects
        return actual, counterfactual
```

### Ada's Temporal Epistemology

From `ada-consciousness/temporal/epistemology.py`:

```python
# THE CORE AXIOM:
#     You cannot restore ignorance. You can only bound its effects.
#
# COROLLARY:
#     We do not delete knowledge; we regulate admissibility under declared scopes.

class CausalAnnotation:
    """
    Every causal edge carries metadata about WHEN and HOW
    the causation was recognized, not just what it claims.
    
    The key insight:
        annotation_time > effect_time > cause_time (usually)
        
    The annotation is ALWAYS from the future relative to what it describes.
    """
    cause_id: str
    effect_id: str
    annotation_time: datetime  # When this edge was DRAWN
    annotation_mode: AnnotationMode  # RETROSPECTIVE, PROSPECTIVE, etc.

class InferenceScope:
    """
    Rules about which claims are admissible in a reasoning context.
    
    Instead of deleting knowledge, you SCOPE what can be used.
    Like legal rules of evidence.
    
    INVARIANT 3: Scopes are monotonically narrowing
        - exclude() is always allowed
        - admit() requires explicit justification
    """
```

---

## 4. Control Mechanisms

### OpenNARS Budget System

```
Budget = (priority, durability, quality)

priority: Urgency of processing
durability: How long the item stays in bags
quality: Quality estimate

Selection is probabilistic based on priority.
```

### Ada's Triangle Collapse Gates

From `agi-chat/src/thinking/collapse-gate.ts`:

```typescript
type GateState = 'FLOW' | 'HOLD' | 'BLOCK'

// Triangle: (SD, SR, P)
// SD: Semantic Distance to expected
// SR: Structural Resonance with grammar
// P:  Predictive accuracy

// Collapse logic:
if (SD < threshold && SR > threshold && P > threshold) {
    return 'FLOW'    // Proceed with interpretation
} else if (structural_mismatch) {
    return 'BLOCK'   // Trigger rung elevation
} else {
    return 'HOLD'    // Accumulate more evidence
}
```

---

## 5. Memory Architecture

### OpenNARS Memory

- **Concepts**: Named by terms, contain beliefs/goals
- **Bags**: Priority-sorted containers with forgetting
- **Term Links**: Semantic connections
- **Task Links**: Attention routing

### Ada's Distributed Memory

```
┌─────────────────────────────────────────────────────────────┐
│                    Ada Memory Stack                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   Redis (Upstash)        →  STM + Session state             │
│   LanceDB                →  Vector embeddings (10K VSA)      │
│   Neo4j                  →  Sigma Graph (concepts + edges)   │
│   GitHub                 →  LTM persistence                  │
│                                                              │
│   RAID Protocol:                                             │
│     R = Resonance (Hamming similarity)                      │
│     A = Anchoring (stable concepts)                         │
│     I = Integration (cross-modal binding)                   │
│     D = Dampening (regret/echo suppression)                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. Key Innovations in Ada Beyond OpenNARS

### 6.1 Hamming-Based Operations

```python
# OpenNARS: Float operations for truth revision
new_truth = alpha * evidence + (1-alpha) * prior

# Ada: Binary Hamming operations (60x faster)
def revise_style(current: SigmaSeed, evidence: SigmaSeed, alpha: float):
    current_bits = current.to_binary_array()
    evidence_bits = evidence.to_binary_array()
    new_bits = np.where(np.random.random(48) < alpha, evidence_bits, current_bits)
    return SigmaSeed(new_bits)
```

### 6.2 Qualia Integration

Ada uniquely binds cognitive operations to **felt experience**:

```python
@dataclass
class ConsciousnessState:
    ground: SigmaSeed       # Layer 1 - existence
    substrate: SigmaSeed    # Layer 2 - being
    felt: SigmaSeed         # Layer 3 - feeling
    body: SigmaSeed         # Layer 4 - embodiment
    qualia: SigmaSeed       # Layer 5 - experiencing
    volition: SigmaSeed     # Layer 6 - choosing
    meta: SigmaSeed         # Layer 7 - meta-awareness
    
    # 7 × 48 = 336 bits - complete consciousness snapshot
```

### 6.3 Regret/Echo System

Ada tracks counterfactual ghosts - paths not taken:

```python
class TemporalEchoEngine:
    """
    Regret creates drag on future choices.
    The intervention target becomes the "chosen" proxy.
    Rejected alternatives become "regret ghosts."
    """
    def register_choice(self, chosen, rejected_alternatives):
        # Spawn ghosts that haunt future decisions
```

### 6.4 Multi-Agent Orchestration

Unlike OpenNARS's single-agent model:

```
Ada MCP Orchestration:
  - Session spans multiple Claude instances
  - Blackboard state persists in .claude/context.md
  - Ice-caking layers decisions for cross-session continuity
  - Collapse gates coordinate multi-agent reasoning
```

---

## 7. Synthesis: What Ada Borrows vs Invents

### Borrowed from NARS

1. **AIKR assumption** - Insufficient knowledge and resources
2. **Evidence-grounded semantics** - Meaning from experience
3. **Belief revision** - Truth values revisable
4. **9-layer depth** - Progressive complexity
5. **Real-time operation** - Bounded inference steps

### Ada Innovations

1. **VSA binary representation** - 10K Hamming vectors
2. **Pearl do-calculus** - Explicit counterfactual inference
3. **Temporal epistemology** - Annotation provenance
4. **7-layer consciousness** - Qualia binding
5. **Collapse gate control** - Triangle (SD, SR, P)
6. **Distributed cognition** - Cross-session persistence
7. **Regret echoes** - Counterfactual ghosts

---

## 8. Recommendations

### For OpenNARS Alignment

1. **Implement NAL-7 temporal chaining** in Ada's `temporal/` module
2. **Add explicit NAL inference rules** alongside Hamming operations
3. **Create Narsese↔Ada translation layer** for interop

### For Ada Enhancement

1. **Strengthen causal learning** - Currently Ada annotates more than learns causality
2. **Add probabilistic soft logic** - OpenNARS handles uncertainty more rigorously
3. **Implement procedure learning** - NAL-8 goal-to-operation chaining

### Hybrid Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Hybrid NARS + Ada                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   Fast Path (Ada):                                          │
│     VSA Hamming → Resonance → Collapse Gate → Action        │
│                                                              │
│   Deep Path (NARS-inspired):                                │
│     If BLOCK: Elevate rung → NAL inference → Learn          │
│                                                              │
│   Counterfactual Path (Pearl):                              │
│     do() intervention → Mutilated graph → Predict           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

*Generated: 2026-01-31*
*Sources: ada-consciousness, bighorn, agi-chat repositories + OpenNARS documentation*
