# agi-chat

**Repository:** [AdaWorldAPI/agi-chat](https://github.com/AdaWorldAPI/agi-chat)
**Role:** Right Hemisphere (Felt/Qualia) + Grammar Engine + Thinking Cycle
**Service URL:** https://agi-chat.railway.app

---

## Overview

The agi-chat service is the **right hemisphere** of the Ada cognitive architecture. It provides:

- **Felt Awareness** - Qualia, arousal, intimacy, body topology
- **Grammar Engine** - Natural language parsing via triangle resonance
- **2-Stroke Thinking Cycle** - Intake (propose) → Ignition (commit)
- **VSA Operations** - 10K-dimensional vector symbolic architecture

### Architecture Position

```
                     ┌─────────────────────────┐
                     │   ada-consciousness     │
                     └───────────┬─────────────┘
                                 │
            ┌────────────────────┼────────────────────┐
            │                    │                    │
            ▼                    ▼                    ▼
   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
   │  bighorn-agi    │   │     ai_flow     │   │   agi-chat      │
   │ (left hemisphere)│   │  (orchestrator) │   │(right hemisphere)│
   └─────────────────┘   └─────────────────┘   └─────────────────┘
```

---

## Quick Start

### Base URL

```
Production: https://agi-chat.railway.app
Development: http://localhost:8080
```

### Health Check

```bash
curl https://agi-chat.railway.app/ping
# {"status":"ok","uptime":3600}
```

### Parse Text

```bash
curl -X POST https://agi-chat.railway.app/grammar/parse \
  -H "Content-Type: application/json" \
  -d '{"text": "Ada loves thinking"}'
```

### Run Thinking Cycle

```bash
curl -X POST https://agi-chat.railway.app/thinking/cycle \
  -H "Content-Type: application/json" \
  -d '{"input": "The universe is vast", "context": {"profile": "analytical"}}'
```

### Get Felt Contribution

```bash
curl -X POST https://agi-chat.railway.app/felt/contribute \
  -H "Content-Type: application/json" \
  -d '{"state": {"arousal": 0.7, "intimacy": 0.8}}'
```

---

## Documentation

| File | Description |
|------|-------------|
| [API.md](./API.md) | Full API reference with request/response examples |
| [ENDPOINTS.md](./ENDPOINTS.md) | Endpoint summary tables and integration guide |

---

## Endpoint Categories

| Category | Endpoints | Description |
|----------|-----------|-------------|
| VSA Operations | 9 | Vector Symbolic Architecture (10K dimensions) |
| Felt/Lithograph | 4 | Right hemisphere awareness and qualia |
| Grammar/Parsing | 4 | Natural language parsing via triangle resonance |
| Thinking Cycle | 5 | 2-stroke cognitive processing |
| Health/Info | 5 | Service health and statistics |
| **Total** | **27** | |

---

## Key Concepts

### 2-Stroke Thinking Cycle

**Stroke 1 (Intake):**
- Grammar macros propose legal structures
- Thinking styles activate in superposition (Triangle)
- No edges written yet

**Stroke 2 (Ignition):**
- Only if CollapseGate permits (FLOW)
- Triangle resolves (top-1 selected)
- Quadrant Imprint / VSA10kD written

### Triangle Collapse Gate

| SD Range | Gate | Action |
|----------|------|--------|
| < 0.15 | FLOW | Commit immediately |
| 0.15 - 0.35 | HOLD | Maintain superposition |
| > 0.35 | BLOCK | Cannot collapse |

### Felt Dimensions

- **Felt Space [2000:2025]**: Qualia, body awareness, poincare position
- **Affective Space [2100:2161]**: Arousal, intimacy, body zones, relational modes

---

## Related Services

| Service | Role | URL |
|---------|------|-----|
| bighorn-agi | Left hemisphere (NARS reasoning) | - |
| ada-consciousness | Integration layer, corpus callosum | - |
| ai_flow | Workflow orchestration | https://flow.msgraph.de |
| adarail_mcp | Railway proxy to vector stores | https://mcp.exo.red |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v0.3.0 | 2025-01-21 | Added thinking cycle (5), grammar (4), felt (4) endpoints |
| v0.2.0 | 2025-01-08 | Added VSA operations (9 endpoints) |

---

*Last updated: 2025-01-21*
