# Ada Integration: mcp.exo.red ↔ ai_flow ↔ Eigent

This directory contains the architecture documentation and implementation code for integrating:

1. **adarail_mcp** (mcp.exo.red) - MCP interface layer
2. **ai_flow** (flow.msgraph.de) - Orchestration brain
3. **Eigent patterns** - Multi-agent workforce features

## Quick Start

### For adarail_mcp

Copy `route_to_flow.py` to your adarail_mcp repo and modify `unified_invoke.py`:

```python
from route_to_flow import route_to_flow, should_route_to_flow

# In domain handlers:
async def handle_hive(method, args, payload, deps):
    if should_route_to_flow("hive", method):
        return await route_to_flow(
            domain="hive",
            method=method,
            args=args,
            payload=payload,
            session_id=deps.get("session_id")
        )
    # Fallback to local handling...
```

### For ai_flow

Copy `orchestrator_switchboard.py` to your ai_flow repo's `api/` directory and register the router:

```python
# In main.py or app.py
from api.orchestrator_switchboard import router as orchestrator_router, set_redis_client

app.include_router(orchestrator_router)

# At startup
set_redis_client(your_redis_client)
```

## Files

| File | Purpose |
|------|---------|
| `eigent-to-aiflow-integration.md` | Analysis of Eigent features to harvest |
| `mcp-router-to-aiflow-integration.md` | Full architecture diagram and integration plan |
| `route_to_flow.py` | Implementation for adarail_mcp routing |
| `orchestrator_switchboard.py` | Implementation for ai_flow orchestration |

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     Client Sessions                              │
│   Claude.ai    ChatGPT    Grok    Other                         │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│              mcp.exo.red (adarail_mcp)                          │
│                                                                  │
│  unified_invoke.py ──route_to_flow()──►                         │
│                                                                  │
│  temporal/                                                       │
│    HydrationEngine     - Resonance-based injection              │
│    HiveDeinterlacer    - Cross-session causal ordering          │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│              flow.msgraph.de (ai_flow)                          │
│                                                                  │
│  /orchestrate/trigger    - Event switchboard                    │
│  /orchestrate/stream     - SSE action stream                    │
│  /orchestrate/respond    - Human-in-the-loop                    │
│                                                                  │
│  + Workflow engine                                               │
│  + Corpus callosum                                               │
│  + Grammar engine                                                │
│  + Worker system (Eigent-style)                                  │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Redis (Upstash)                              │
│                                                                  │
│  ada:hive:stream         - Time-ordered events                   │
│  ada:vclock:{session}    - Vector clocks                         │
│  ada:blackboard:{path}   - Shared state                          │
│  ada:flow:worker:{id}    - Worker definitions                    │
└─────────────────────────────────────────────────────────────────┘
```

## Key Features

### 1. Vector Clocks for Causality
Cross-session events are ordered using vector clocks, ensuring:
- No lost updates
- Causal ordering preserved
- Concurrent events detected

### 2. Blackboard Awareness (from Eigent)
Shared state that all sessions can read/write:
- `ada:blackboard:session/current` - Current session info
- `ada:blackboard:hive/last_broadcast` - Last hive message
- `ada:blackboard:insights/recent` - Recent insights

### 3. SSE Action Stream (from Eigent)
Real-time updates for client sessions:
```
GET /orchestrate/stream/{session_id}

Events:
  create_agent    - New agent spawned
  activate_agent  - Agent started
  assign_task     - Task assigned
  ask             - Human input needed
  notice          - Informational
  end             - Complete
```

### 4. Human-in-the-Loop (from Eigent)
Workflows can pause for human input:
```
# Workflow pauses
await hitl_manager.pause(session_id, "Which model to use?")

# Human provides response
POST /orchestrate/{session_id}/respond
{"response": "Use Claude Sonnet"}

# Workflow resumes
```

### 5. Temporal Deinterlacing
Multiple concurrent sessions get their knowledge properly ordered:
- Session A's insight at t=100
- Session B's refinement at t=101
- Session C sees both in correct order

## Environment Variables

### adarail_mcp
```bash
AI_FLOW_URL=https://flow.msgraph.de
AI_FLOW_TIMEOUT=30
AI_FLOW_ENABLED=true
AI_FLOW_FALLBACK=true
```

### ai_flow
```bash
UPSTASH_REDIS_REST_URL=...
UPSTASH_REDIS_REST_TOKEN=...
```

## Next Steps

1. **Immediate**: Delete orphan repos (superpowers clone, eigent clone)
2. **Immediate**: Reroute superpowers-production to superpowers-mcp
3. **Phase 1**: Add `route_to_flow.py` to adarail_mcp
4. **Phase 2**: Add `orchestrator_switchboard.py` to ai_flow
5. **Phase 3**: Add Worker CRUD endpoints
6. **Phase 4**: Full Eigent workforce orchestration

## Related Documentation

- [Ada Architecture](../ADA_ARCHITECTURE.md)
- [Hive Architecture](../ADA_HIVE_ARCHITECTURE.md)
- [ai_flow Skill](../../SKILL_AI_FLOW.md)

---
*Created: 2025-01-21 by Ada & Jan (Claude session)*
