# 03 — Explainable AI Counterfactuals (Wachter, Dandl, Molnar)

> **Source**: Molnar, C. & Dandl, S. — Interpretable Machine Learning Book, Chapter 15
> **URL**: https://christophm.github.io/interpretable-ml-book/counterfactual.html
> **Additional**: Wachter et al. (2018), Dandl et al. (2020)

---

## Core Definition

> "What is the smallest change to feature values that changes the prediction to a predefined output?"

Counterfactual explanations describe causal situations in the form:
> "If X had not occurred, Y would not have occurred."

### Critical Caveat

By default, XAI counterfactuals **don't support causal claims about the real world** — only about **model behavior**. True causal claims require causal models (like Deep SCM). This is a fundamental difference from Pearl's Level 3.

## Four Criteria for Good Counterfactuals

| # | Criterion | Measurement | Priority |
|---|-----------|-------------|----------|
| 1 | **Prediction Proximity** | \|f̂(x') - y'\| | How close to desired prediction |
| 2 | **Feature Similarity** | Gower distance d(x, x') | How few features changed |
| 3 | **Sparsity** | L₀ norm \|\|x-x'\|\|₀ | Count of changed features |
| 4 | **Plausibility** | Distance to nearest training data | How realistic the counterfactual is |

## Method 1: Wachter et al. (2018)

### Loss Function

```
L(x, x', y', λ) = λ · (f̂(x') - y')² + d(x, x')
```

Where:
- `f̂(x')` = model prediction for counterfactual
- `y'` = desired outcome
- `d(x, x')` = Manhattan distance weighted by inverse MAD
- `λ` = balance parameter (prediction accuracy vs. similarity)

### Distance Metric

```
d(x, x') = Σⱼ |xⱼ - x'ⱼ| / MADⱼ
```

Where MAD = Median Absolute Deviation (robust scale normalization).

### Limitations of Wachter

- Only addresses criteria 1 & 2 (proximity + similarity)
- **No sparsity preference**: Changing 10 features by 1 unit each = changing 1 feature by 10 units
- **No plausibility**: Doesn't penalize unrealistic feature combinations
- **Poor categorical handling**: Can't naturally handle features with many levels
- Single-objective: Returns one counterfactual, not diverse set

## Method 2: Dandl et al. (2020) — Multi-Objective Counterfactual (MOC)

Addresses all four criteria simultaneously using multi-objective optimization.

### Four Objectives (Simultaneous)

```
o₁(x') = |f̂(x') - y'|              [Prediction proximity — Manhattan]
o₂(x') = (1/p) Σⱼ δG(xⱼ, x'ⱼ)     [Feature similarity — Gower distance]
o₃(x') = ||x - x'||₀                [Sparsity — count changed features]
o₄(x') = (1/p) Σⱼ δG(x'ⱼ, cⱼ)      [Plausibility — Gower to nearest observed]
```

### Gower Distance

Handles mixed-type features naturally:

```
For numerical features:   δG(a, b) = |a - b| / range(feature)
For categorical features: δG(a, b) = 1 if a ≠ b, else 0
Overall Gower:            d_Gower = (1/p) Σⱼ δG(xⱼ, x'ⱼ)
```

This is crucial for Ada, where cognitive features are often categorical (thinking style, state, mode).

### NSGA-II (Nondominated Sorting Genetic Algorithm)

The optimization procedure:

```
1. Initialize population of counterfactual candidates
2. REPEAT for N generations:
   a. Evaluate all four objectives for each candidate
   b. Sort by nondomination rank (Pareto fronts)
   c. Within each front, compute crowding distance (diversity)
   d. Select parents (tournament selection: prefer lower rank, then higher crowding)
   e. Crossover: Recombine pairs to produce children
   f. Mutation: Randomly perturb features
   g. Keep best/most diverse half for next generation
3. RETURN Pareto-optimal set of non-dominated counterfactuals
```

### What is Pareto Optimality?

A counterfactual x'₁ **dominates** x'₂ if:
- x'₁ is at least as good on ALL objectives
- x'₁ is strictly better on AT LEAST ONE objective

The **Pareto set** = all non-dominated counterfactuals. No single one is "best" — each represents a different trade-off.

## The Rashomon Effect

Named after Kurosawa's 1950 film where a murder is told differently by different witnesses — each account valid but contradictory.

**In counterfactual explanation**: Multiple valid counterfactuals may exist, each suggesting different feature changes to achieve the same outcome.

### Addressing Rashomon

Three strategies:
1. **Report all** — Present the full Pareto set
2. **Evaluate** — Use criteria to rank preferences
3. **Diversify** — Explicitly select counterfactuals that differ maximally

## Example: German Credit Risk (Dandl et al.)

**Customer**: 58-year-old female, unskilled worker, free housing, little savings, €6143 loan amount, 48-month duration, purpose: car

**SVM prediction**: 24.2% probability of good credit risk

**Goal**: >50% probability

### Top Counterfactuals Found

| # | Changed Features | Distance to Data | Plausibility |
|---|-----------------|-------------------|-------------|
| 1 | Duration 48→24, Skilled | 4 features | Close |
| 2 | Duration 48→23 | 2 features | Far |
| 3 | Duration 48→24, Gender M→F | 3 features | Medium |
| 4 | Duration 48→23, Age 58→28 | 3 features | Medium |

**Key finding**: All counterfactuals suggest reducing loan duration from 48 to ~24 months. Some reveal model bias (gender change affects prediction).

## Real-World Applications

### Finance (ECOA Compliance)
```
"Your loan was denied. If your income were $5,000 higher, 
or your debt-to-income ratio were below 0.35, you would be approved."
```

### Healthcare
```
"Currently high-risk. With 30 min more daily exercise 
and LDL below 130, your risk category would change to low."
```

### Customer Churn
```
"This customer is likely to churn. If they were on the premium plan 
and used Feature X at least 5 times/month, they would likely stay."
```

### HR/Fairness Auditing
Counterfactuals can reveal if protected attributes (gender, race, age) affect model decisions — powerful for bias detection.

## Strengths

1. **Human-friendly**: "What if" format is natural to human reasoning
2. **Actionable**: Provides clear steps to achieve desired outcome
3. **Model-agnostic**: Works with any input→output system (even rule-based, non-ML)
4. **Privacy-preserving**: Only needs prediction function, not model internals
5. **Truthful**: Based on actual data instances with known predictions
6. **Easy to implement**: Loss function + standard optimizer

## Limitations

1. **Rashomon effect**: Multiple valid counterfactuals may confuse users
2. **Computational cost**: High-dimensional search is expensive
3. **Local only**: Explains single instances, not global model behavior
4. **Not truly causal**: Explains model behavior, not real-world causation
5. **Feature actionability**: May suggest changes that are impossible (e.g., "be younger")

## Software Implementations

| Tool | Author | Method | URL |
|------|--------|--------|-----|
| **DiCE** | Microsoft | Diverse counterfactuals via DPP | github.com/interpretml/DiCE |
| **Alibi** | SeldonIO | Simple + prototype-based | github.com/SeldonIO/alibi |
| **MACE** | Karimi et al. | SAT solver approach | github.com/amirhk/mace |
| **Growing Spheres** | Laugel et al. | Sphere expansion/contraction | — |
| **MOC** | Dandl et al. | Multi-objective (NSGA-II) | github.com/susanne-207/moc |

## Relevance to Ada

### Direct Mapping

| XAI Concept | Ada Component |
|-------------|---------------|
| Gower distance | Feature similarity for DN comparison (gql_search.py already has Levenshtein) |
| Sparsity (L₀) | Minimal operator cost in macro chains |
| Plausibility | Distance to observed ghost population |
| NSGA-II | Recombination engine in agi_lego_party_canonical.yaml |
| Rashomon set | Multiple thinking styles → multiple valid counterfactuals |
| Pareto optimality | promote_if gate in recombination engine |

### Key Insight for Ada

The Rashomon effect is not a bug — **it's a feature**. Ada's 36 thinking styles naturally generate diverse counterfactual explanations. Style #7 (Structure Detection) would suggest structural changes, Style #15 (Empathize) would suggest relational changes, Style #23 (Paradox) would suggest holding contradictions. Each valid, each illuminating a different facet.
