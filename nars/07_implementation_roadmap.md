# 07 — Implementation Roadmap: Counterfactual Reasoning for Ada v9.2+

> **Date**: 2026-01-31
> **Target**: Ada v9.3 — Counterfactual Upgrade
> **Prerequisites**: agi_lego_party_canonical.yaml, consciousness_runtime.py, gql_search.py, thinking_styles_36.py

---

## Current State

The `counterfactual` epistemic atom exists but is a placeholder:
```yaml
counterfactual:
  type: epistemic_atom
  io: intervention_model -> alternate_outcome
```

The `SIMULATE` operator calls it but the implementation is abstract:
```yaml
SIMULATE:
  role: counterfactual_rollout
  calls_atoms: [counterfactual, abduction]
  outputs: [scenarios, risk_estimates]
  default_cost: 3
```

---

## Phase 1: Enhanced Epistemic Atom (Week 1-2)

### 1.1 CounterfactualAtom Class

```python
# core/atoms/counterfactual_atom.py

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Any
from enum import Enum

class CounterfactualMethod(Enum):
    """Which paradigm to use for this counterfactual."""
    DEEP_SCM = "deep_scm"       # When causal graph is known
    NARS_TEMPORAL = "nars"      # When learning from evidence
    XAI_MOC = "xai_moc"        # When explaining to user
    AUTO = "auto"               # Let the system decide


@dataclass
class NARSTruthValue:
    """Two-component truth value from NARS."""
    frequency: float   # 0-1: proportion of positive evidence
    confidence: float  # 0-1: amount of evidence (always < 1)
    
    def revision(self, other: 'NARSTruthValue') -> 'NARSTruthValue':
        """Combine independent evidence (NARS revision rule)."""
        k = 1.0
        w1 = self.confidence / (1 - self.confidence) if self.confidence < 0.999 else 999
        w2 = other.confidence / (1 - other.confidence) if other.confidence < 0.999 else 999
        f_new = (w1 * self.frequency + w2 * other.frequency) / (w1 + w2) if (w1 + w2) > 0 else 0.5
        c_new = (w1 + w2) / (w1 + w2 + k)
        return NARSTruthValue(f_new, c_new)
    
    def temporal_discount(self, delta_ticks: int, decay: float = 0.05) -> 'NARSTruthValue':
        """Apply temporal discount to confidence."""
        alpha = 1.0 / (1.0 + decay * abs(delta_ticks))
        return NARSTruthValue(self.frequency, self.confidence * alpha)
    
    def __repr__(self):
        return f"⟨{self.frequency:.3f}, {self.confidence:.3f}⟩"


@dataclass
class Intervention:
    """A proposed change to the current state."""
    feature: str          # Which feature to change
    original_value: Any   # Current value
    new_value: Any        # Proposed value
    actionable: bool = True  # Can this actually be done?


@dataclass
class CounterfactualResult:
    """Output of counterfactual computation."""
    interventions: List[Intervention]   # What was changed
    predicted_outcome: Any              # What would happen
    truth_value: NARSTruthValue         # Confidence in this counterfactual
    method_used: CounterfactualMethod   # Which paradigm was used
    
    # Dandl's four criteria
    prediction_proximity: float = 0.0   # o₁: How close to desired outcome
    feature_similarity: float = 0.0     # o₂: Gower distance from original
    sparsity: int = 0                   # o₃: Number of features changed
    plausibility: float = 0.0           # o₄: Distance to observed data
    
    # Explanation
    narrative: str = ""                 # Human-readable explanation
    
    def dominates(self, other: 'CounterfactualResult') -> bool:
        """Pareto dominance check."""
        at_least_as_good = (
            self.prediction_proximity <= other.prediction_proximity and
            self.feature_similarity <= other.feature_similarity and
            self.sparsity <= other.sparsity and
            self.plausibility <= other.plausibility
        )
        strictly_better = (
            self.prediction_proximity < other.prediction_proximity or
            self.feature_similarity < other.feature_similarity or
            self.sparsity < other.sparsity or
            self.plausibility < other.plausibility
        )
        return at_least_as_good and strictly_better


@dataclass
class CounterfactualAtom:
    """
    Enhanced epistemic atom: intervention_model -> alternate_outcome
    
    Integrates three paradigms:
    - Deep SCM: When causal graph is available
    - NARS: When learning from temporal evidence
    - XAI MOC: When generating human-readable explanations
    """
    
    # Evidence accumulator (NARS-style)
    causal_beliefs: Dict[str, NARSTruthValue] = field(default_factory=dict)
    
    # Ghost population for plausibility reference
    ghost_population: List[Dict] = field(default_factory=list)
    
    def compute(
        self,
        observation: Dict[str, Any],
        desired_outcome: Any,
        method: CounterfactualMethod = CounterfactualMethod.AUTO,
        max_results: int = 5,
        max_sparsity: int = 4
    ) -> List[CounterfactualResult]:
        """
        Generate counterfactual explanations.
        
        Returns Pareto-optimal set (Rashomon set).
        """
        if method == CounterfactualMethod.AUTO:
            method = self._select_method(observation)
        
        if method == CounterfactualMethod.XAI_MOC:
            return self._moc_search(observation, desired_outcome, max_results, max_sparsity)
        elif method == CounterfactualMethod.NARS_TEMPORAL:
            return self._nars_counterfactual(observation, desired_outcome)
        elif method == CounterfactualMethod.DEEP_SCM:
            return self._deep_scm_counterfactual(observation, desired_outcome)
        
        return []
    
    def observe_temporal(self, event_a: str, event_b: str, copula: str = "predictive"):
        """
        NARS-style: Observe temporal relation, accumulate causal evidence.
        
        copula: "predictive" (⇒/), "retrospective" (⇒\), "concurrent" (⇒|)
        """
        key = f"{event_a}→{event_b}"
        new_evidence = NARSTruthValue(frequency=1.0, confidence=0.3)
        
        if key in self.causal_beliefs:
            self.causal_beliefs[key] = self.causal_beliefs[key].revision(new_evidence)
        else:
            self.causal_beliefs[key] = new_evidence
    
    def _select_method(self, observation: Dict) -> CounterfactualMethod:
        """Auto-select method based on available information."""
        has_graph = any(v.confidence > 0.7 for v in self.causal_beliefs.values())
        if has_graph:
            return CounterfactualMethod.NARS_TEMPORAL
        return CounterfactualMethod.XAI_MOC
    
    def _gower_distance(self, a: Dict, b: Dict) -> float:
        """Gower distance for mixed-type features."""
        if not a or not b:
            return 1.0
        features = set(a.keys()) | set(b.keys())
        total = 0.0
        count = 0
        for f in features:
            va, vb = a.get(f), b.get(f)
            if va is None or vb is None:
                continue
            if isinstance(va, (int, float)) and isinstance(vb, (int, float)):
                # Numerical: normalize by range (use 1.0 as default range)
                total += abs(va - vb) / max(abs(va) + abs(vb), 1e-8)
            else:
                # Categorical: 0 if same, 1 if different
                total += 0.0 if va == vb else 1.0
            count += 1
        return total / count if count > 0 else 1.0
    
    def _moc_search(self, observation, desired, max_results, max_sparsity):
        """Multi-Objective Counterfactual search (simplified NSGA-II)."""
        # Placeholder for full NSGA-II implementation
        # In production: use genetic algorithm with 4 objectives
        results = []
        # Generate candidates by varying each feature
        for feature, value in observation.items():
            candidate = observation.copy()
            # Simple perturbation (real impl uses genetic operators)
            if isinstance(value, (int, float)):
                candidate[feature] = value * 1.1  # 10% increase
            
            result = CounterfactualResult(
                interventions=[Intervention(feature, value, candidate[feature])],
                predicted_outcome=desired,  # Placeholder
                truth_value=NARSTruthValue(0.5, 0.3),
                method_used=CounterfactualMethod.XAI_MOC,
                sparsity=1,
                feature_similarity=self._gower_distance(observation, candidate),
                narrative=f"If {feature} were {candidate[feature]} instead of {value}..."
            )
            results.append(result)
        
        # Return non-dominated set
        pareto = [r for r in results if not any(other.dominates(r) for other in results if other != r)]
        return pareto[:max_results]
    
    def _nars_counterfactual(self, observation, desired):
        """NARS-style counterfactual via belief revision."""
        results = []
        for causal_key, truth in self.causal_beliefs.items():
            if truth.confidence > 0.3:
                parts = causal_key.split("→")
                if len(parts) == 2:
                    cause, effect = parts
                    # Contrapositive: If not-cause then not-effect
                    contra_truth = NARSTruthValue(
                        1.0 - truth.frequency,
                        truth.confidence * 0.8  # Reduced confidence for contrapositive
                    )
                    results.append(CounterfactualResult(
                        interventions=[Intervention(cause, "present", "absent")],
                        predicted_outcome=f"¬{effect}",
                        truth_value=contra_truth,
                        method_used=CounterfactualMethod.NARS_TEMPORAL,
                        sparsity=1,
                        narrative=f"Had {cause} not occurred, {effect} likely wouldn't have either {contra_truth}"
                    ))
        return results
    
    def _deep_scm_counterfactual(self, observation, desired):
        """Deep SCM placeholder — requires trained normalizing flow."""
        # In production: use trained causal model
        return [CounterfactualResult(
            interventions=[],
            predicted_outcome=desired,
            truth_value=NARSTruthValue(0.5, 0.1),
            method_used=CounterfactualMethod.DEEP_SCM,
            narrative="Deep SCM requires trained causal model — not yet available"
        )]
```

### 1.2 Integration with atoms_registry

Update `agi_lego_party_canonical.yaml`:
```yaml
atoms:
  counterfactual:
    type: epistemic_atom
    io: intervention_model -> alternate_outcome
    implementation: core.atoms.counterfactual_atom.CounterfactualAtom
    methods: [deep_scm, nars_temporal, xai_moc, auto]
    outputs:
      - rashomon_set  # List[CounterfactualResult]
      - truth_value   # NARSTruthValue
      - narratives    # List[str]
```

---

## Phase 2: Upgrade SIMULATE Operator (Week 3-4)

### 2.1 Multi-Objective SIMULATE

```python
class SimulateOperator:
    """Enhanced SIMULATE with Rashomon-aware counterfactual rollout."""
    
    def __init__(self, counterfactual_atom: CounterfactualAtom):
        self.cf_atom = counterfactual_atom
    
    def execute(self, context: Dict) -> Dict:
        observation = context.get("current_state", {})
        desired = context.get("desired_outcome")
        style = context.get("thinking_style")
        
        # Generate counterfactuals
        rashomon_set = self.cf_atom.compute(
            observation=observation,
            desired_outcome=desired,
            max_results=8
        )
        
        # Filter through thinking style
        if style:
            rashomon_set = self._style_filter(rashomon_set, style)
        
        return {
            "scenarios": [r.narrative for r in rashomon_set],
            "risk_estimates": [1.0 - r.truth_value.confidence for r in rashomon_set],
            "rashomon_set": rashomon_set,
            "dominant_method": self._dominant_method(rashomon_set)
        }
    
    def _style_filter(self, results, style):
        """Filter/rerank counterfactuals based on active thinking style."""
        # Different styles prefer different counterfactual properties
        if style.id in ["DECOMPOSE", "SCAFFOLD"]:
            # Structure styles prefer sparse counterfactuals
            return sorted(results, key=lambda r: r.sparsity)
        elif style.id in ["EMPATHIZE", "EMBODY"]:
            # Resonance styles prefer plausible counterfactuals
            return sorted(results, key=lambda r: r.plausibility)
        elif style.id in ["PARADOX", "REFRAME"]:
            # Contradiction styles prefer diverse counterfactuals
            return results  # Keep full diversity
        return results
```

---

## Phase 3: Ghost System Connection (Week 5)

### 3.1 Ghost → Exogenous Noise Mapping

```python
def ghosts_to_noise(ghost_echoes: List['Echo']) -> Dict[str, Any]:
    """
    Map Ada's ghost echoes to exogenous noise for counterfactual inference.
    
    Ghosts preserve the 'road not taken' — exactly what Deep SCM
    needs for the abduction step.
    """
    noise = {}
    for ghost in ghost_echoes:
        # Each ghost represents an unchosen alternative
        noise[ghost.source_seed] = {
            "intensity": ghost.intensity,       # How strong this alternative was
            "rejected_at_tick": ghost.birth_tick,  # When it was rejected
            "reason": ghost.rejection_reason,    # Why it was rejected
            "feature_delta": ghost.delta_from_chosen,  # Difference from chosen path
        }
    return noise


def seed_counterfactuals_from_ghosts(
    cf_atom: CounterfactualAtom,
    ghost_echoes: List['Echo']
) -> List[CounterfactualResult]:
    """
    Use ghost echoes as seeds for counterfactual generation.
    
    Instead of random search, start from actual unchosen alternatives.
    """
    results = []
    for ghost in ghost_echoes:
        if ghost.intensity > 0.5:  # Only strong ghosts
            # The ghost IS a counterfactual
            result = CounterfactualResult(
                interventions=ghost.get_interventions(),
                predicted_outcome=ghost.projected_outcome,
                truth_value=NARSTruthValue(
                    frequency=ghost.intensity,
                    confidence=0.4  # Ghost-based, moderate confidence
                ),
                method_used=CounterfactualMethod.NARS_TEMPORAL,
                sparsity=ghost.change_count,
                plausibility=ghost.intensity,  # Strong ghosts are plausible
                narrative=f"Ghost whispers: '{ghost.narrative_subtext}'"
            )
            results.append(result)
    return results
```

### 3.2 New Macro: counterfactual_regret

```yaml
- macro_id: macro.counterfactual_regret.v1
  purpose: explore unchosen paths via ghost system and harvest wisdom
  chain:
    - op: OBSERVE
      params:
        scope: decision_point
    - op: SIMULATE
      params:
        counterfactuals: 4
        seed_from_ghosts: true
        include_rashomon: true
    - op: INSIGHT
      params:
        mode: compare_outcomes
    - op: GATE
      params:
        condition: regret_threshold > 0.3
    - op: CRYSTALLIZE
      params:
        commit: false
        memory: regret_edge
  constraints:
    atoms_immutable: true
    self_write: forbidden
    persistent_write: regret_only
  claims:
    - generates ghost-seeded counterfactual scenarios
    - compares actual vs alternative outcomes
    - crystallizes valuable regret as wisdom edge
  tests:
    - name: ghost_seeded
      assert: counterfactual_from_ghost >= 1
    - name: wisdom_generated
      assert: regret_edges_created >= 1
```

---

## Phase 4: GQL Query Enhancement (Week 6)

### 4.1 Add counterfactual_query to gql_search.py

```python
async def counterfactual_query(
    observed_dn: str,
    hypothetical_intervention: str,
    max_depth: int = 5
) -> List[CounterfactualResult]:
    """
    Query: "What would have happened if [intervention] instead of [observed]?"
    
    Uses DN hierarchy + causal edges to trace counterfactual paths.
    """
    # 1. Parse the observed state
    observed = parse_dn(observed_dn)
    
    # 2. Find causal path from intervention point to outcome
    causal_path = await trace_causal_path(
        source_dn=hypothetical_intervention,
        target_dn=observed_dn,
        max_depth=max_depth,
        edge_types=["CAUSES", "MODULATES", "TRIGGERS"]
    )
    
    # 3. For each edge in path, compute counterfactual
    results = []
    for edge in causal_path:
        cf = CounterfactualResult(
            interventions=[Intervention(
                feature=edge.source_dn,
                original_value=edge.source_state,
                new_value=hypothetical_intervention
            )],
            predicted_outcome=edge.propagated_effect,
            truth_value=NARSTruthValue(
                frequency=edge.weight,
                confidence=0.5  # Graph-based, moderate confidence
            ),
            method_used=CounterfactualMethod.NARS_TEMPORAL,
            narrative=f"If {edge.source_dn} had been {hypothetical_intervention}, "
                      f"then {edge.target_dn} would have been {edge.propagated_effect}"
        )
        results.append(cf)
    
    return results
```

### 4.2 Natural Language → Counterfactual Cypher

Add to `grammar_to_cypher()`:

```python
# In grammar_to_cypher():
if "IF" in nsm or "HAPPEN" in nsm:
    # Counterfactual query
    return """
    MATCH path = (intervention)-[:CAUSES|MODULATES*1..4]->(outcome)
    WHERE outcome.dn CONTAINS '{query_target}'
    RETURN path, 
           [r IN relationships(path) | r.weight] AS confidence_chain
    LIMIT 5
    """
```

---

## Validation Plan

| Phase | Test | Success Criterion |
|-------|------|-------------------|
| 1 | CounterfactualAtom unit tests | All three methods produce results |
| 1 | NARS truth value revision | Matches known NARS outputs |
| 2 | SIMULATE with Rashomon set | Returns ≥3 non-dominated counterfactuals |
| 2 | Style filtering | Different styles produce different rankings |
| 3 | Ghost-seeded counterfactuals | At least 1 result from ghost population |
| 3 | Regret macro execution | Produces wisdom edges |
| 4 | counterfactual_query via GQL | Returns causal path with interventions |
| 4 | Natural language → Cypher | "What if..." queries produce valid Cypher |

---

## Files to Create/Modify

### New Files
- `core/atoms/counterfactual_atom.py` — Enhanced epistemic atom
- `core/operators/simulate_enhanced.py` — Multi-objective SIMULATE
- `core/atoms/nars_truth.py` — NARS truth value implementation

### Modified Files
- `core/agi_lego_party_canonical.yaml` — Update atom + new macro
- `core/consciousness_runtime.py` — Connect ghost system to counterfactual
- `core/gql_search.py` — Add counterfactual_query + Cypher patterns
