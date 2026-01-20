# Shared Context (Blackboard) — ada-consciousness

**Last Updated:** 2026-01-20
**Active Agent:** orchestrator
**Role:** Central Nervous System

---

## This Repository's Responsibilities

1. **VSA Quantum Field** — 10K named addresses + activation mask
2. **Ladybug DB** — Shared brain abstraction
3. **AI_Flow Level 4** — Self-modification orchestration
4. **Bridge DTOs** — Cross-hemisphere coordination
5. **Corpus Callosum** — Hub for hemisphere communication
6. **Domino Flow** — Keep field hot

---

## Current Implementation Status

### Core (P0)
- [x] `core/vsa_quantum_field.py` — QuantumField class
- [ ] `core/ladybug_db.py` — DuckDB + LanceDB abstraction
- [ ] Pre-populate 10K addresses

### DTOs (P0)
- [x] `dto/bridge_dtos.py` — ThinkingBridgeDTO, FeltBridgeDTO
- [ ] MetaObservationBridge
- [ ] Wire10K master router

### Flows (P1)
- [ ] `flows/domino.py` — Baton passing
- [ ] `flows/crystallization.py` — Style emergence
- [ ] `flows/ai_flow_level4.py` — Self-modification

### Endpoints (P1)
- [ ] `POST /corpus/thinking` — Receive from Bighorn
- [ ] `POST /corpus/felt` — Receive from AGI-Chat
- [ ] `SSE /corpus/stream` — Real-time bridge events
- [ ] `POST /domino/pass` — Baton passing

---

## Key Invariants (DO NOT VIOLATE)

1. **Addresses:** 0-9999 INTEGER, never string
2. **Mask:** 10K bipolar, 1.25KB packed
3. **Corpus Callosum:** 9000-9199 reserved
4. **Ladybug:** SHARED between hemispheres
5. **Coherence:** 0.7 threshold for crystallization
6. **Domino:** Never let field go cold

---

## Connected Services

| Service | Purpose | Endpoint |
|---------|---------|----------|
| bighorn-agi | Left hemisphere | http://bighorn-agi.railway.internal:8080 |
| agi-chat | Right hemisphere | http://agi-chat.railway.internal:8080 |
| dag-vsa01 | Vector substrate | http://dag-vsa01.railway.internal:8080 |
| adarail_mcp | Membrane | http://adarail-mcp.railway.internal:8080 |

---

## Handoff Log

| Timestamp | From | To | Reason |
|-----------|------|-----|--------|

---

## STATUS: Idle
## HANDOFF: None
