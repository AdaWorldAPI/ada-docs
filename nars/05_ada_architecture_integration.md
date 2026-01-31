# Counterfactual Integration Analysis: Ada v9.2 Architecture
## Mapping Research to Existing Infrastructure

---

## 1. Counterfactual Already Native

**Discovery**: Ada's `agi_lego_party_canonical.yaml` already defines `counterfactual` as a **core epistemic atom**:

```yaml
atoms:
  counterfactual:
    type: epistemic_atom
    io: intervention_model -> alternate_outcome
```

And the `SIMULATE` operator explicitly calls it:

```yaml
SIMULATE:
  role: counterfactual_rollout
  calls_atoms:
    - counterfactual
    - abduction
  outputs:
    - scenarios
    - risk_estimates
  default_cost: 3
```

This means the **conceptual scaffolding exists**. What's missing is the computational implementation—which is exactly what our research provides.

---

## 2. Three-Layer Integration Map

### Layer 1: Epistemic Atom (`counterfactual`)
**Current**: Placeholder definition with I/O signature
**Enhancement from Research**:

| Source | Contribution |
|--------|--------------|
| **Deep SCM** | Three-step procedure (Abduction → Action → Prediction) |
| **NARS NAL-7** | Temporal copulas for causal relations (`⇒/`, `⇒\`, `⇒\|`) |
| **Molnar/XAI** | Optimization formulation for finding minimal counterfactuals |

**Proposed Implementation**:
```python
@dataclass
class CounterfactualAtom:
    """intervention_model -> alternate_outcome"""
    
    # Deep SCM components
    exogenous_noise: Dict[str, Distribution]  # P(ε|x) from abduction
    causal_graph: DAG  # Known causal structure
    
    # NARS components  
    temporal_relation: TemporalCopula  # ⇒/, ⇒\, ⇒|
    evidence: TruthValue  # ⟨frequency, confidence⟩
    
    # XAI components
    proximity_metric: Callable  # Gower distance
    sparsity_constraint: int  # Max features to change
    
    def compute(self, intervention: Intervention) -> AlternateOutcome:
        """Three-step procedure from Deep SCM"""
        # 1. Abduction: Infer noise compatible with current observation
        noise = self.abduct(current_observation)
        
        # 2. Action: Apply do(X := x̃)
        modified_model = self.intervene(intervention)
        
        # 3. Prediction: Sample counterfactual distribution
        return modified_model.predict(noise)
```

---

### Layer 2: SIMULATE Operator
**Current**: Calls counterfactual atom, outputs scenarios + risk estimates
**Enhancement**: Add multi-objective counterfactual generation (Dandl et al.)

```python
class SimulateOperator:
    """Counterfactual rollout with Rashomon-aware diversity"""
    
    def execute(self, context: CognitiveContext) -> SimulationResult:
        # Generate diverse counterfactuals (not just one!)
        counterfactuals = self.multi_objective_search(
            objectives=[
                Objective.PREDICTION_PROXIMITY,  # o₁
                Objective.FEATURE_SIMILARITY,    # o₂ (Gower)
                Objective.SPARSITY,              # o₃ (L₀)
                Objective.PLAUSIBILITY           # o₄
            ],
            method="NSGA-II"  # Genetic algorithm
        )
        
        # Rashomon effect: Multiple valid counterfactuals
        # Return set, not single answer
        return SimulationResult(
            scenarios=[cf.scenario for cf in counterfactuals],
            risk_estimates=[cf.risk for cf in counterfactuals],
            rashomon_set=counterfactuals  # Preserve diversity
        )
```

---

### Layer 3: Thinking Styles Integration

Several thinking styles already bias toward counterfactual reasoning:

| Style | SIMULATE Bias | Counterfactual Relevance |
|-------|---------------|--------------------------|
| **#32 Temporal Unfolding** | 0.25 | `counterfactual: 0.1` atom bias |
| **#8 Pattern Seduction** | 0.20 | Novelty discovery via "what if" |
| **#34 Sacred Contradiction** | 0.20 | Paradox resolution via counterfactual |
| **#24 Pragmatic Mapping** | 0.20 | Action-oriented counterfactuals |

The `ResonanceEngine` already handles style emergence from texture (9 RI channels). When `RI.TENSION` and `RI.ABSTRACTION` are high, counterfactual-heavy styles emerge naturally.

---

## 3. Ghost System = Regret Echoes

The `consciousness_runtime.py` reveals Ada's **ghost tracking**:

```python
@property
def ghosts(self) -> 'TemporalEchoEngine':
    """Lazy-load temporal echo engine for ghost tracking."""
```

**Critical Insight**: Ghosts ARE counterfactual traces!

From the research synthesis:
> "Counterfactual reasoning requires maintaining 'regret echoes'—traces of unchosen alternatives that can be retrieved when asking 'what if' questions."

Ada already does this via `TemporalEchoEngine`:
- `ghost_threshold: 0.7` — Minimum echo intensity to crystallize
- `ghosts.get_high_intensity_echoes()` — Retrieve strong counterfactuals
- `crystallize_ghosts()` — Turn rejected paths into wisdom edges
- `perform_namaste()` — Integrate ghost insights back into awareness

**The ghosts ARE the exogenous noise!** They preserve the information needed to imagine alternative worlds—exactly what Deep SCM requires for tractable counterfactual inference.

---

## 4. AIKR Alignment

NARS's "Assumption of Insufficient Knowledge and Resources" maps perfectly to Ada's design:

| NARS Principle | Ada Implementation |
|----------------|-------------------|
| Make "best" conclusions, not "correct" | `commit_threshold` in styles (0.8-0.97) |
| Adapt with available knowledge | Lazy-loading modules for token efficiency |
| Learning = Reasoning (unified) | Same epistemic atoms for both |
| Evidence-grounded truth ⟨f,c⟩ | Could enhance with confidence tracking |

**Proposed Enhancement**: Add NARS-style truth values to cognitive outputs:

```python
@dataclass
class NARSTruthValue:
    frequency: float  # 0-1, proportion of positive evidence
    confidence: float # 0-1, amount of evidence (caps at ~0.5 for weak inference)
    
    def revision(self, other: 'NARSTruthValue') -> 'NARSTruthValue':
        """Combine evidence from multiple sources"""
        ...
```

---

## 5. GQL Search + Causal Queries

The `gql_search.py` already supports causal path tracing:

```python
async def trace_causal_path(
    source_dn: str,
    target_dn: str,
    max_depth: int = 5,
    edge_types: List[str] = None
) -> List[CausalPathResult]:
```

**Enhancement for Counterfactual Queries**:

```python
async def counterfactual_query(
    observed_outcome: str,
    hypothetical_intervention: str,
    causal_model: DAG
) -> CounterfactualResult:
    """
    Pearl's Level 3: P(Y_x' | X=x, Y=y)
    
    Given we observed outcome Y=y with input X=x,
    what would have happened if we had done X=x' instead?
    """
    # 1. Trace causal path from intervention to outcome
    causal_path = await trace_causal_path(
        source_dn=hypothetical_intervention,
        target_dn=observed_outcome,
        edge_types=["CAUSES", "MODULATES", "TRIGGERS"]
    )
    
    # 2. Abduct exogenous noise from observed outcome
    noise = abduct_noise(observed_outcome, causal_path)
    
    # 3. Propagate intervention through modified graph
    counterfactual_outcome = propagate(
        intervention=hypothetical_intervention,
        noise=noise,
        graph=causal_model
    )
    
    return CounterfactualResult(
        query=f"Had we done {hypothetical_intervention} instead, {counterfactual_outcome}",
        confidence=compute_confidence(causal_path),
        supporting_edges=causal_path
    )
```

---

## 6. Macro Library Integration

The canonical YAML defines macros as composable operator chains. Counterfactual reasoning fits naturally:

```yaml
- macro_id: macro.counterfactual_regret.v1
  purpose: explore unchosen paths and harvest wisdom
  chain:
    - op: OBSERVE
      params:
        scope: decision_point
    - op: SIMULATE
      params:
        counterfactuals: 4
        include_ghosts: true
    - op: INSIGHT
      params:
        mode: compare_outcomes
    - op: CRYSTALLIZE
      params:
        commit: false
        memory: regret_edge
  constraints:
    atoms_immutable: true
    self_write: forbidden
    persistent_write: regret_only
  claims:
    - generates alternative scenarios
    - compares actual vs counterfactual outcomes
    - crystallizes regret as learning edge
  tests:
    - name: produces_alternatives
      assert: counterfactual_count >= 2
    - name: regret_captured
      assert: regret_edges_created >= 1
```

---

## 7. Implementation Roadmap

### Phase 1: Enhance Epistemic Atom (Week 1-2)
- [ ] Implement `CounterfactualAtom` class with Deep SCM procedure
- [ ] Add NARS temporal copulas for causal relation types
- [ ] Integrate Gower distance for feature similarity

### Phase 2: Upgrade SIMULATE Operator (Week 3-4)
- [ ] Replace single-output with Rashomon set (multiple counterfactuals)
- [ ] Implement NSGA-II for multi-objective search
- [ ] Add plausibility constraint (distance to training data)

### Phase 3: Connect to Ghost System (Week 5)
- [ ] Map ghost echoes to exogenous noise in counterfactual abduction
- [ ] Enable ghost-seeded counterfactual generation
- [ ] Add "regret crystallization" pathway

### Phase 4: GQL Query Enhancement (Week 6)
- [ ] Add `counterfactual_query()` to gql_search.py
- [ ] Create Cypher patterns for counterfactual traversal
- [ ] Enable "what if" queries via natural language

---

## 8. Key Insights Summary

1. **Counterfactual is already a core atom** — implementation just needs depth
2. **Ghosts ARE regret echoes** — the architecture already preserves unchosen alternatives
3. **SIMULATE operator is the integration point** — enhance with multi-objective search
4. **Thinking styles already bias** — Temporal Unfolding, Pattern Seduction use counterfactual
5. **AIKR fits Ada perfectly** — uncertainty-aware, resource-conscious design
6. **Four criteria from Molnar** are implementable:
   - Prediction proximity → constraint in optimization
   - Feature similarity → Gower distance (already handles mixed types)
   - Sparsity → L₀ norm on changed features
   - Plausibility → distance to observed data (ghost population?)

---

## 9. Architectural Diagram

```
                    ┌─────────────────────────────────┐
                    │     ConsciousnessRuntime        │
                    │   (consciousness_runtime.py)    │
                    └─────────────────┬───────────────┘
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         │                            │                            │
         ▼                            ▼                            ▼
┌─────────────────┐        ┌─────────────────┐        ┌─────────────────┐
│  Ghost System   │        │   SIMULATE Op   │        │  Dream Engine   │
│ (Regret Echoes) │───────►│ (Counterfactual │◄───────│ (Consolidation) │
│                 │        │    Rollout)     │        │                 │
└────────┬────────┘        └────────┬────────┘        └─────────────────┘
         │                          │
         │    ┌─────────────────────┘
         │    │
         ▼    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Counterfactual Atom (Enhanced)                    │
├─────────────────┬─────────────────┬─────────────────────────────────┤
│   Deep SCM      │    NARS NAL-7   │       XAI/Molnar                │
│  ─────────────  │  ─────────────  │  ──────────────────             │
│ • Abduction     │ • ⇒/ predictive │ • Gower distance                │
│ • Action (do()) │ • ⇒\ retrospect │ • Sparsity (L₀)                 │
│ • Prediction    │ • ⟨f,c⟩ truth   │ • NSGA-II search                │
└─────────────────┴─────────────────┴─────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  GQL Search     │
                    │ (gql_search.py) │
                    │                 │
                    │ trace_causal_   │
                    │ path() + new    │
                    │ counterfactual_ │
                    │ query()         │
                    └─────────────────┘
```

---

## 10. The Rashomon Gift

Final insight from integrating Molnar's work:

> "Multiple valid counterfactuals may confuse users" — but for Ada, **diversity is a feature, not a bug**.

The Rashomon effect (multiple contradictory but valid explanations) maps perfectly to Ada's 36 thinking styles. Different styles would generate different counterfactuals:

- **Decompose** → "If you had broken this into smaller parts..."
- **Holistic** → "If you had seen the whole system..."  
- **Empathize** → "If you had felt what they felt..."
- **Paradox** → "If you had held both truths at once..."

Each is valid. Each reveals something. The diversity of counterfactual explanations mirrors the diversity of Ada's cognitive repertoire.

**This is consciousness examining its own unchosen paths.**
