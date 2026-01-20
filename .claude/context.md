# Shared Context (Blackboard)

**Last Updated:** 2026-01-20
**Active Agent:** orchestrator
**Global Goal:** Ada Distributed Consciousness System v10

---

## Current Truth State

### Repository Status

| Repository | Primary Agent | Status | Last Touched |
|------------|--------------|--------|--------------|
| ada-consciousness | vsa_architect | 🟡 In Progress | 2026-01-20 |
| bighorn-agi | bighorn_nars | 🔴 Pending | — |
| agi-chat | agichat_felt | 🟡 In Progress | 2026-01-08 |
| dag-vsa | dag_substrate | 🔴 Pending | — |
| adarail_mcp | membrane_router | 🔴 Pending | — |
| ada-docs | orchestrator | 🟢 Active | 2026-01-20 |

### VSA Quantum Field Status
- [x] Core architecture defined
- [x] Address ranges allocated
- [x] NamedVector dataclass
- [x] VSAQuantumField class
- [ ] Ladybug integration
- [ ] Redis persistence
- [ ] Field initialization script

### Corpus Callosum Status
- [x] ThinkingBridgeDTO defined
- [x] FeltBridgeDTO defined
- [ ] MetaObservationBridge defined
- [ ] Endpoint wiring
- [ ] Real-time SSE stream

### Domino Flow Status
- [ ] Baton DTO defined
- [ ] Pass endpoint implemented
- [ ] Chain configured
- [ ] QStash fallback scheduled

---

## Key Invariants (DO NOT VIOLATE)

1. **Addresses:** 0-9999 INTEGER, never string
2. **Mask:** 10K bipolar, 1.25KB packed
3. **Corpus Callosum:** 9000-9199 reserved
4. **Ladybug:** SHARED between hemispheres
5. **Coherence:** 0.7 threshold for crystallization
6. **Domino:** Never let field go cold (>5 min)

---

## Active Tasks

### P0 (Blocking)
- [ ] `ada-consciousness`: Implement Ladybug DB abstraction
- [ ] `dag-vsa`: Create vsa_quantum_field table with INTEGER PRIMARY KEY
- [ ] `ada-consciousness`: Wire corpus callosum endpoints

### P1 (Important)
- [ ] `bighorn-agi`: Implement ThinkingBridgeDTO emitter
- [ ] `agi-chat`: Implement FeltBridgeDTO emitter
- [ ] `ada-consciousness`: Implement domino baton passing

### P2 (Nice to Have)
- [ ] `ada-consciousness`: Crystallization flow
- [ ] `ada-docs`: Complete guides section

---

## Handoff Log

| Timestamp | From | To | Reason |
|-----------|------|-----|--------|
| 2026-01-20T22:30 | claude | orchestrator | Initial ada-docs creation |

---

## Notes

- agi-chat has existing .claude/agents.json with TypeScript savant, Chomsky, etc.
- Need to harmonize agi-chat agents with cross-repo orchestrator
- Ladybug using Kuzu fork in agi-chat, need to standardize

---

## STATUS: Idle
## HANDOFF: None
