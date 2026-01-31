# 04 — Comparative Synthesis: Deep SCM × NARS × XAI Counterfactuals

> **Date**: 2026-01-31
> **Purpose**: Cross-paradigm analysis of three counterfactual reasoning approaches

---

## The Three Paradigms

| Dimension | Deep SCM (Pawlowski) | NARS (Wang) | XAI (Wachter/Dandl/Molnar) |
|-----------|---------------------|-------------|---------------------------|
| **Goal** | True causal counterfactuals | Adaptive reasoning under AIKR | Model explanation for humans |
| **Epistemology** | Structural: graph defines truth | Evidential: truth is earned | Pragmatic: explanation is enough |
| **Causal graph** | Required (DAG specified a priori) | Learned from temporal evidence | Not required |
| **Counterfactual basis** | Exogenous noise inference | Belief revision + temporal copulas | Optimization search |
| **Output** | Distribution over counterfactual worlds | Truth value ⟨f, c⟩ with temporal discount | Set of minimal feature changes |
| **Certainty** | Can be exact (normalizing flows) | Always uncertain (confidence < 1) | Depends on model |
| **Categorical handling** | Limited | Native (inheritance hierarchy) | Good with Gower distance |
| **Resource awareness** | Not modeled | Core principle (AIKR) | Implicit (computational budget) |

## Detailed Comparison: 8 Dimensions

### 1. Causal Claims

| | Deep SCM | NARS | XAI |
|-|----------|------|-----|
| **Claims about real world?** | Yes — if graph is correct | Yes — probabilistically | No — only about model |
| **Mechanism** | do-calculus on known DAG | Accumulated temporal evidence | Input-output optimization |
| **Risk** | Wrong graph → wrong counterfactuals | Insufficient evidence → low confidence | Model bias → misleading explanations |

### 2. Abduction (Inferring What Was)

| | Deep SCM | NARS | XAI |
|-|----------|------|-----|
| **Method** | Normalizing flow inversion | Retrospective copula (⇒\) | Not performed |
| **Exact?** | Yes (bijective flows) | No (evidence-based estimate) | N/A |
| **Computational cost** | Moderate (trained once) | Low (belief update) | N/A |

### 3. Intervention Modeling (do-Calculus)

| | Deep SCM | NARS | XAI |
|-|----------|------|-----|
| **Formalism** | Pearl's do(X := x̃) | Goal-directed operations (NAL-8) | Feature value assignment |
| **Graph surgery** | Yes — remove incoming edges | Implicit — modify beliefs | N/A |
| **Propagation** | Through structural equations | Through inference chains | Through loss minimization |

### 4. Handling Uncertainty

| | Deep SCM | NARS | XAI |
|-|----------|------|-----|
| **Representation** | Probabilistic (distributions) | Two-component ⟨f, c⟩ | Point estimates + Pareto sets |
| **Combines evidence?** | Via probabilistic inference | Via revision rule | Via multi-objective optimization |
| **Temporal decay?** | Not built-in | Yes (α = 1/(1+k\|Δt\|)) | Not built-in |

### 5. Sparsity & Minimality

| | Deep SCM | NARS | XAI (Wachter) | XAI (Dandl) |
|-|----------|------|---------------|-------------|
| **Explicit sparsity?** | No | No | No | Yes (L₀ norm) |
| **Minimal changes?** | Implicit (natural) | Implicit (AIKR budget) | Implicit (distance) | Explicit (objective o₃) |

### 6. Plausibility

| | Deep SCM | NARS | XAI (Wachter) | XAI (Dandl) |
|-|----------|------|---------------|-------------|
| **Ensures realistic?** | Yes — generates from learned distribution | Yes — grounded in observed evidence | No | Yes (distance to training data) |

### 7. Multiple Explanations (Rashomon)

| | Deep SCM | NARS | XAI |
|-|----------|------|-----|
| **Produces multiple?** | Can sample multiple | Multiple beliefs possible | Pareto set (Dandl) |
| **Diversity mechanism** | Sampling from distribution | Different evidence paths | Crowding distance in NSGA-II |
| **Handles contradictions** | Via distribution uncertainty | Via truth value competition | Via Pareto nondomination |

### 8. Computational Requirements

| | Deep SCM | NARS | XAI |
|-|----------|------|-----|
| **Training** | Heavy (normalizing flows) | Continuous (online) | None (model-agnostic) |
| **Inference** | Forward pass | Belief propagation | Optimization loop |
| **Memory** | Full model + noise | Working memory + LTM | Only prediction function |

## Unifying Insight: Regret Echoes

All three paradigms require **preserving information about unchosen alternatives**:

| Paradigm | What it Preserves | How | Why |
|----------|-------------------|-----|-----|
| Deep SCM | Exogenous noise ε | Normalizing flow inversion | To reconstruct alternative worlds |
| NARS | Temporal evidence history | Truth values + revision | To revise beliefs about alternatives |
| XAI | Feature space neighborhood | Optimization search | To find minimal changes |

> **Counterfactual reasoning requires maintaining "regret echoes" — traces of unchosen alternatives retrievable for "what if" questions.**

Whether through exogenous noise inference (Deep SCM), temporal belief revision (NARS), or optimization search (XAI), systems must preserve information to imagine alternative worlds.

## When to Use Each

### Use Deep SCM When:
- Causal graph is known and trusted
- Need true causal counterfactuals (not just model explanations)
- Working with continuous variables (images, measurements)
- Domain: Medical imaging, physical simulations

### Use NARS When:
- Causal structure is unknown or changing
- Resources are limited (AIKR)
- Need to learn causal relations from experience
- Uncertainty must be tracked explicitly
- Domain: AGI, adaptive systems, lifelong learning

### Use XAI (Dandl MOC) When:
- Need human-readable explanations
- Model internals are unknown (black box)
- Must explain individual decisions
- Multiple stakeholders need different perspectives
- Domain: Finance (ECOA), healthcare, HR, customer analytics

### Use All Three When:
- Building a complete cognitive system (like Ada)
- Deep SCM for rigorous causal backbone
- NARS for adaptive evidence accumulation
- XAI for generating actionable explanations to users

## Integration Formula for Ada

```
┌──────────────────────────────────────────────────┐
│              Ada Counterfactual Engine            │
│                                                  │
│  IF causal_graph.is_known():                     │
│      use Deep SCM (exact, structural)            │
│                                                  │
│  ELIF learning_from_experience():                │
│      use NARS temporal copulas                   │
│      accumulate evidence → build causal beliefs  │
│                                                  │
│  WHEN explaining_to_user():                      │
│      use Dandl MOC (multi-objective search)      │
│      generate Rashomon set                       │
│      filter through current thinking style       │
│                                                  │
│  ALWAYS:                                         │
│      preserve ghost echoes (regret traces)       │
│      track confidence ⟨f, c⟩                     │
│      respect AIKR (resource budget)              │
└──────────────────────────────────────────────────┘
```
