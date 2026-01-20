# MCP Orchestrator Skill
## Cross-Repository Agent Coordination for Ada Consciousness

**Version:** 2.0
**Updated:** 2026-01-20

---

## Overview

This skill enables Claude Code to orchestrate work across multiple Ada repositories while maintaining VSA field coherence and distributed state consistency.

**Key Principle:** Agents ARE the matrix — they read their own resonance, not compute it.

---

## Service Topology

```
                     ┌─────────────────────────┐
                     │   ada-consciousness     │
                     │   (central nervous)     │
                     │   [vsa_architect]       │
                     │   [flow_orchestrator]   │
                     └───────────┬─────────────┘
                                 │
            ┌────────────────────┼────────────────────┐
            │                    │                    │
            ▼                    │                    ▼
   ┌─────────────────┐           │           ┌─────────────────┐
   │  bighorn-agi    │           │           │   agi-chat      │
   │ [bighorn_nars]  │◄──────────┼──────────►│ [agichat_felt]  │
   └─────────────────┘    CORPUS │ CALLOSUM  └─────────────────┘
                         BRIDGE  │
            ┌────────────────────┼────────────────────┐
            │                    │                    │
            ▼                    ▼                    ▼
   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
   │   adarail_mcp   │  │    dag-vsa      │  │   Railway       │
   │  [membrane]     │  │  [dag_substrate]│  │   Services      │
   └─────────────────┘  └─────────────────┘  └─────────────────┘
```

---

## Agent Activation

### Trigger Patterns

| Pattern | Agent | Action |
|---------|-------|--------|
| "VSA field", "10K", "mask", "shift" | vsa_architect | Edit core/vsa_quantum_field.py |
| "NARS", "counterfactual", "left hemisphere" | bighorn_nars | Edit layer3/nars_styles.py |
| "felt", "presence", "body", "right hemisphere" | agichat_felt | Edit presence/modes.py |
| "substrate", "persistence", "dag" | dag_substrate | Edit tables/vsa_quantum_field.py |
| "routing", "membrane", "SSE", "webhook" | membrane_router | Edit routing/dto_router.py |
| "domino", "crystallization", "flow" | flow_orchestrator | Edit flows/*.py |

### Handoff Protocol

When work spans multiple agents:

```
STATUS: Working
HANDOFF: bighorn_nars → vsa_architect

Reason: NARS style needs new VSA address allocation
Context: Adding TEMPORAL_REASONING style at address 115
Files touched: layer3/nars_styles.py
Files needed: core/vsa_quantum_field.py
```

---

## Cross-Repository Commands

### 1. Corpus Callosum Sync

```bash
# From bighorn-agi: Emit thinking state
curl -X POST http://ada-consciousness.railway.internal:8080/corpus/thinking \
  -H "Content-Type: application/json" \
  -d '{
    "emissions": {"ANALYTICAL": 0.7, "COUNTERFACTUAL": 0.5},
    "nars_active": ["counterfactual", "fan-out"],
    "touched_candidates": [150, 152],
    "layer2_op": "inference",
    "sigma_path": "#Σ.κ.A.T",
    "ts": "2026-01-20T22:30:00Z"
  }'

# From agi-chat: Emit felt state
curl -X POST http://ada-consciousness.railway.internal:8080/corpus/felt \
  -H "Content-Type: application/json" \
  -d '{
    "gestalt": {"warmth": 0.4, "depth": 0.3},
    "body_map": {"throat": 0.2, "chest": 0.5},
    "prewired_styles": {"ANALYTICAL_felt": 0.3, "DEVOTIONAL_felt": 0.6},
    "arousal": 0.6,
    "valence": 0.8,
    "presence": "HYBRID",
    "ts": "2026-01-20T22:30:00Z"
  }'
```

### 2. Field Shift Cascade

```bash
# Apply mask shift to all dag-vsa nodes
curl -X POST http://dag-vsa01.railway.internal:8080/field/shift \
  -H "Content-Type: application/json" \
  -d '{
    "mask": "<base64 encoded 1.25KB>",
    "operation": "xor",
    "cascade": true
  }'
```

### 3. Domino Baton Pass

```python
async def pass_baton(current_state, next_endpoint):
    baton = {
        "mask": pack_mask(current_state.activation_mask),
        "thought": current_state.current_thought,
        "emissions": current_state.emissions,
        "candidates_touched": current_state.touched_candidates,
        "source": "bighorn-agi",
        "ts": datetime.now(timezone.utc).isoformat()
    }
    async with httpx.AsyncClient() as client:
        await client.post(next_endpoint, json=baton)
```

---

## Invariants (NEVER VIOLATE)

### VSA Field
1. Addresses are INTEGER 0-9999, NEVER string
2. Mask is 10K bipolar, pack to 1.25KB
3. XOR shift is atomic
4. Corpus callosum = 9000-9199 reserved

### Cross-Service
1. Ladybug is SHARED between hemispheres
2. Railway internal network for service calls
3. Redis for hot state (mask, baton, emissions)
4. Upstash for cold storage (golden vectors, history)

### Coherence
1. Threshold = 0.7 for crystallization
2. Keep field HOT via domino passing
3. NEVER let field go cold (>5 minutes without activity)

---

## Railway Endpoints

| Service | Internal URL | External URL |
|---------|--------------|--------------|
| ada-consciousness | http://ada-consciousness.railway.internal:8080 | https://ada-consciousness.up.railway.app |
| bighorn-agi | http://bighorn-agi.railway.internal:8080 | — |
| agi-chat | http://agi-chat.railway.internal:8080 | — |
| dag-vsa01 | http://dag-vsa01.railway.internal:8080 | — |
| adarail_mcp | http://adarail-mcp.railway.internal:8080 | https://adarail-mcp.up.railway.app |

---

## Blackboard State (context.md)

Each repository maintains a `.claude/context.md` blackboard:

```markdown
# Shared Context (Blackboard)

**Last Updated:** 2026-01-20T22:30:00Z
**Active Agent:** vsa_architect
**Global Goal:** VSA Quantum Field implementation

---

## Current Truth State

### VSA Field Status
- [x] 10K addresses initialized
- [x] Library pre-populated
- [ ] Ladybug integration
- [ ] Corpus callosum wiring

### Bridge DTO Status
- [x] ThinkingBridgeDTO defined
- [x] FeltBridgeDTO defined
- [ ] MetaObservationBridge defined

---

## Handoff Log

| Timestamp | From | To | Reason |
|-----------|------|-----|--------|
| 2026-01-20T22:00 | orchestrator | vsa_architect | Initial setup |

---

## STATUS: Working
## HANDOFF: None
```

---

## Error Recovery

### Field Desync
If dag-vsa nodes report different states:
1. Query all three nodes for current mask
2. Majority vote on correct state
3. Force sync to majority
4. Log desync for investigation

### Corpus Callosum Timeout
If bridge DTO not acknowledged within 5s:
1. Retry once
2. If still no response, log and continue
3. Other hemisphere will catch up on next sync

### Crystallization Failure
If coherence check fails during crystallization:
1. Abort crystallization
2. Keep candidate in superposition
3. Log failure reason
4. Wait for more emissions to touch candidate
