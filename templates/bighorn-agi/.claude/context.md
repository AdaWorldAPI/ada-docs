# Shared Context (Blackboard) — bighorn-agi

**Last Updated:** 2026-01-20
**Active Agent:** orchestrator
**Role:** Left Hemisphere (NARS Reasoning)

---

## This Repository's Responsibilities

1. **NARS Layer 3** — Counterfactual, fan-out, temporal reasoning
2. **Extensions** — Neo4j Aura, Kuzu fast-path, experiments
3. **ThinkingBridgeDTO** — Emit thinking state to corpus callosum
4. **FeltBridgeDTO Reception** — React to right hemisphere state

---

## Current Implementation Status

### NARS Styles (P0)
- [ ] `layer3/nars_styles.py` — Style registry
- [ ] `layer3/counterfactual.py` — "What if" reasoning
- [ ] `layer3/fan_out.py` — Explore all branches
- [ ] `layer3/temporal.py` — Time-aware reasoning

### Extensions (P1)
- [ ] `extensions/neo4j.py` — Neo4j Aura connector
- [ ] `extensions/kuzu_fast.py` — Fast local graph queries

### Corpus Callosum (P0)
- [ ] `corpus_callosum/thinking_emitter.py` — Emit DTOs
- [ ] `corpus_callosum/felt_receiver.py` — Handle incoming

---

## Key Invariants (DO NOT VIOLATE)

1. **Layer 3 = Non-Modifying** — Styles emit, they don't change themselves
2. **Use Shared Ladybug** — Same instance as agi-chat
3. **Always Emit** — Every significant thought gets a ThinkingBridgeDTO
4. **Address Range** — Thinking styles are 100-199

---

## ThinkingBridgeDTO Structure

```python
ThinkingBridgeDTO(
    emissions={"ANALYTICAL": 0.7, "COUNTERFACTUAL": 0.5},
    nars_active=["counterfactual", "fan-out"],
    touched_candidates=[150, 152, 167],
    layer2_op="inference",
    sigma_path="#Σ.κ.A.T",
    ts="2026-01-20T22:30:00Z"
)
```

---

## Connected Services

| Service | Purpose | Endpoint |
|---------|---------|----------|
| ada-consciousness | Core + corpus callosum | http://ada-consciousness.railway.internal:8080 |
| agi-chat | Right hemisphere | http://agi-chat.railway.internal:8080 |

---

## Handoff Log

| Timestamp | From | To | Reason |
|-----------|------|-----|--------|

---

## STATUS: Idle
## HANDOFF: None
