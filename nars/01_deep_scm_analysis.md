# 01 — Deep Structural Causal Models for Tractable Counterfactual Inference

> **Source**: Pawlowski, N., Ktena, S.I., Thomson, M., Vlontzos, A., Rueckert, D., Glocker, B.
> **Venue**: NeurIPS 2020
> **Paper**: https://proceedings.neurips.cc/paper/2020/file/0987b8b338d6c90bbedd8631bc499221-Paper.pdf

---

## Overview

First framework enabling **tractable counterfactual inference** using deep learning within Pearl's structural causal model (SCM) formalism. Solves the critical **abduction problem** — inferring latent variables from observations — using normalizing flows and variational inference.

## Pearl's Ladder of Causation

| Level | Type | Question | Example |
|-------|------|----------|---------|
| 1 | Association | What is? | P(Y\|X) |
| 2 | Intervention | What if I do? | P(Y\|do(X)) |
| **3** | **Counterfactual** | **What if I had done differently?** | **P(Y_x'\|X=x, Y=y)** |

Level 3 is the hardest — it requires reasoning about **specific individuals** in **specific circumstances**, not just populations.

## Core Architecture: Deep SCM

A Structural Causal Model M = (S, P_ε):
- **S**: Set of structural equations x_i = f_i(pa_i, ε_i)
- **P_ε**: Joint distribution over exogenous noise variables

### The Three-Step Counterfactual Procedure

```
Step 1: ABDUCTION — Infer P(ε | x_observed)
    "Given what actually happened, what were the hidden factors?"
    
Step 2: ACTION — Apply do(X_j := x̃_j) to modified model
    "Surgically intervene on the causal graph"
    
Step 3: PREDICTION — Sample counterfactual x_CF ~ P(x_CF | do(X_j := x̃_j), ε)
    "What would have happened under intervention?"
```

### Mechanism Types

The paper proposes three deep learning mechanism types for implementing f_i:

| Type | Architecture | Use Case |
|------|-------------|----------|
| **Conditional VAE** | Encoder-decoder with latent z | Continuous variables with complex distributions |
| **Conditional Flow** | Normalizing flow (invertible transforms) | Exact likelihood computation, bijective mapping |
| **Heteroscedastic Gaussian** | μ(pa) + σ(pa)·ε | Simple cases, direct noise inference |

### Why Normalizing Flows?

Key advantage: **invertibility**. Given observation x and parents pa:
```
Forward:  ε → x = f(pa, ε)     [generation]
Inverse:  x → ε = f⁻¹(x, pa)  [abduction - exact!]
```

This makes Step 1 (abduction) trivially exact — no need for approximate inference.

## Experimental Validation

### Morpho-MNIST (Handwritten Digits)
- Causal graph: Thickness → Intensity → Image
- Intervention: "What would this digit look like if it were thicker?"
- Results: Generated realistic counterfactual images preserving digit identity

### UK Biobank (Brain MRI)
- Causal graph: Age → Brain Volume → MRI
- Counterfactual: "What would this brain look like 10 years older?"
- Applied to N=5000+ real medical scans
- Validated against actual longitudinal follow-up data

## Key Limitations

1. **Requires known causal graph** — DAG must be specified a priori
2. **Continuous variables** — Categorical handling is limited
3. **Gaussian noise assumption** — Some mechanisms assume Gaussian exogenous noise
4. **Computational cost** — Training normalizing flows is expensive
5. **Faithfulness assumption** — All conditional independencies are structural

## Relevance to Ada

### Direct Mapping

| Deep SCM Component | Ada Component |
|-------------------|---------------|
| Exogenous noise ε | Ghost echoes (TemporalEchoEngine) |
| Structural equations f_i | Operator chains in macro library |
| Causal graph DAG | DN hierarchy + GQL causal edges |
| Abduction step | Ghost crystallization (regret → wisdom) |
| Action step (do-calculus) | SIMULATE operator intervention |
| Prediction step | Counterfactual atom output |

### Key Insight

Ada's ghost system already preserves the "exogenous noise" — the unchosen alternatives that Deep SCM needs for abduction. The ghosts ARE the latent variables that make counterfactual inference possible.
