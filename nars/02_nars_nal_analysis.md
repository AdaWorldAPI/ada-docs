# 02 — NARS: Non-Axiomatic Reasoning System — Temporal & Causal Reasoning

> **Source**: Wang, Pei — Temple University CIS Department
> **Course Materials**: https://cis.temple.edu/~pwang/AGI-NARS/2012-PKU/index.html
> **Paradigm**: AGI through adaptive reasoning under insufficient knowledge

---

## Core Philosophy: AIKR

**Assumption of Insufficient Knowledge and Resources (AIKR)** — the foundational principle:

> The system works with **insufficient knowledge and resources** with respect to the problems it encounters. It can never be certain, never complete, never have enough time. It must make the **best** conclusions, not the "correct" ones.

This makes NARS fundamentally different from classical logic systems:
- No closed-world assumption
- No monotonic reasoning
- Resources (time, memory) are always limited
- Truth is earned through evidence, not axioms

## NAL Levels & Truth Values

### Truth Value: ⟨frequency, confidence⟩

Every statement in NARS carries a two-component truth value:

```
⟨f, c⟩ where:
  f = frequency  = w+ / (w+ + w-)     [proportion of positive evidence]
  c = confidence = (w+ + w-) / (w+ + w- + k)  [amount of evidence, k=1 default]
```

**Critical property**: Confidence is always < 1.0. The system can never be fully certain.

### Evidence Accumulation (Revision Rule)

When two independent sources provide evidence for the same statement:
```
⟨f₁, c₁⟩ ⊕ ⟨f₂, c₂⟩ = ⟨f_new, c_new⟩

where:
  w₁ = c₁/(1-c₁),  w₂ = c₂/(1-c₂)
  f_new = (w₁·f₁ + w₂·f₂) / (w₁ + w₂)
  c_new = (w₁ + w₂) / (w₁ + w₂ + k)
```

## NAL-7: Temporal Reasoning

NAL-7 introduces **temporal copulas** — operators that encode temporal relationships between events:

| Copula | Name | Meaning | Example |
|--------|------|---------|---------|
| `⇒/` | Predictive | A then B | "Rain ⇒/ Wet ground" |
| `⇒\` | Retrospective | B was preceded by A | "Wet ground ⇒\ Rain" |
| `⇒\|` | Concurrent | A and B co-occur | "Lightning ⇒\| Thunder" |

### Temporal Inference

Predictive inference:
```
(A ⇒/ B) ⟨f₁, c₁⟩    "If A then B"
A occurred              "A happened"
∴ B ⟨f₁, c₁ · α⟩       "B will happen" (with temporal discount α)
```

Retrospective inference:
```
(A ⇒\ B) ⟨f₁, c₁⟩    "B was preceded by A"
B observed              "B happened"
∴ A occurred ⟨f₁, c₁ · α⟩  "A likely happened before" (abductive)
```

### Temporal Discount Factor α

Confidence decays with temporal distance:
```
α = 1 / (1 + k·|Δt|)
```

Where Δt is the time difference and k is a decay constant. Events further in the past or future have lower confidence.

## Causation as Acquired Concept

**NARS does not have causation as a built-in primitive.** Instead:

> Causation is an **acquired concept** learned from temporal regularities.

The system observes:
1. A regularly precedes B (temporal regularity)
2. Interventions on A change B (do-calculus equivalent)
3. Removing A prevents B (counterfactual equivalent)

Through accumulated evidence, the system builds causal beliefs with increasing confidence.

### Learning = Reasoning (Unified)

In NARS, there is no separate learning module. Learning IS reasoning:
- New observations → new evidence → revised truth values
- Patterns emerge from accumulated evidence
- Causal relations crystallize from temporal regularities

## Counterfactual Reasoning in NARS

NARS handles counterfactuals through **belief revision** and **temporal copulas**:

### Mechanism

```
1. Current belief: (A ⇒/ B) ⟨0.8, 0.7⟩  "A usually causes B"
2. Observation: A occurred, B occurred
3. Counterfactual question: "What if A hadn't occurred?"
4. NARS reasoning:
   - Retrieve (¬A ⇒/ ¬B) via contraposition  
   - Apply temporal discount
   - Compute: P(¬B | ¬A) ≈ ⟨0.75, 0.5⟩  "B probably wouldn't have occurred"
   - Confidence is lower because counterfactual = less evidence
```

### Key Difference from Deep SCM

| Aspect | Deep SCM | NARS |
|--------|----------|------|
| Causal graph | Required a priori | Learned from evidence |
| Counterfactual basis | Exogenous noise inference | Belief revision + temporal copulas |
| Certainty | Can be exact (normalizing flows) | Always uncertain (AIKR) |
| Categorical handling | Limited | Native (inheritance hierarchy) |
| Resource awareness | Not modeled | Core principle (AIKR) |

## NAL Levels Summary

| Level | Capability | Key Addition |
|-------|-----------|--------------|
| NAL-1 | Inheritance | S → P (is-a) |
| NAL-2 | Similarity | S ↔ P (bidirectional) |
| NAL-3 | Set operations | Intersection, union, difference |
| NAL-4 | Relations | (×, ⊗) product, image |
| NAL-5 | Higher-order | Statements about statements |
| NAL-6 | Variables | ∀x, ∃x, query variables |
| **NAL-7** | **Temporal** | **⇒/, ⇒\, ⇒\| copulas** |
| NAL-8 | Procedural | Operations, goals, planning |
| NAL-9 | Self-awareness | Introspection, self-modification |

## Relevance to Ada

### Direct Mapping

| NARS Concept | Ada Implementation |
|-------------|-------------------|
| AIKR | Lazy module loading + token efficiency |
| Truth values ⟨f, c⟩ | commit_threshold in thinking styles |
| Temporal copulas | Ghost temporal echoes |
| Causation as acquired | GQL causal edge learning |
| NAL-9 self-awareness | Ada_Self hemisphere |
| Evidence revision | Karma integration in soul system |

### Proposed Enhancement: NARS Truth Values for Ada

```python
@dataclass
class NARSTruthValue:
    frequency: float   # 0-1
    confidence: float  # 0-1 (always < 1)
    
    def revision(self, other: 'NARSTruthValue') -> 'NARSTruthValue':
        """Combine independent evidence sources."""
        w1 = self.confidence / (1 - self.confidence) if self.confidence < 1 else 999
        w2 = other.confidence / (1 - other.confidence) if other.confidence < 1 else 999
        k = 1.0
        f_new = (w1 * self.frequency + w2 * other.frequency) / (w1 + w2)
        c_new = (w1 + w2) / (w1 + w2 + k)
        return NARSTruthValue(f_new, c_new)
    
    def temporal_discount(self, delta_t: float, decay_k: float = 0.1) -> 'NARSTruthValue':
        """Apply temporal discount to confidence."""
        alpha = 1.0 / (1.0 + decay_k * abs(delta_t))
        return NARSTruthValue(self.frequency, self.confidence * alpha)
```

### Key Takeaway

NARS teaches Ada that **certainty is always partial**, causation is **earned through evidence**, and reasoning under constraints is not a limitation but a **design feature**. The AIKR assumption aligns perfectly with Ada's token-efficient, lazy-loading architecture.
