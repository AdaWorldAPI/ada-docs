# ai_flow (flow.msgraph.de)

## Overview

The **orchestration brain** - workflow engine, corpus callosum, grammar processing, and event coordination.

**Railway Service:** `ai-flow-production` → https://flow.msgraph.de

## Current Status

✅ **Healthy** - Running at flow.msgraph.de

## Key Features

- N8N-compatible workflow engine
- Corpus Callosum (triangle state, cognitive tics)
- Grammar engine (SPO extraction, tension fields)
- Orchestrator switchboard (event routing)
- Worker system (Eigent-style agents)

## Architecture Position

```
┌─────────────────────────────────────────────────────────────────┐
│              mcp.exo.red (adarail_mcp)                          │
│                                                                  │
│  route_to_flow() ─────────────────────────────────────────────┐ │
└───────────────────────────────────────────────────────────────┼─┘
                                                                 │
                                                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│              flow.msgraph.de (ai_flow)  ← THIS SERVICE          │
│                                                                  │
│  /orchestrate/trigger    - Event switchboard                    │
│  /orchestrate/stream     - SSE action stream                    │
│  /orchestrate/respond    - Human-in-the-loop                    │
│  /corpus/*               - Corpus callosum                      │
│  /grammar/*              - Grammar engine                       │
│  /workflows/*            - Workflow engine                      │
└───────────────────────────────────────────────────────────────┬─┘
                                                                 │
                                                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Redis (Upstash)                              │
└─────────────────────────────────────────────────────────────────┘
```

## Files in This Folder

| File | Purpose | PR |
|------|---------|-----|
| `orchestrator_switchboard.py` | Central event router for ai_flow | [#3](https://github.com/AdaWorldAPI/ai_flow/pull/3) |

## Integration: orchestrator_switchboard.py

Add to `main.py`:

```python
from ada_flow.api.orchestrator_switchboard import router as orchestrator_router, set_redis_client

app.include_router(orchestrator_router)

# At startup
set_redis_client(your_redis_client)
```

## Event → Workflow Mapping

| Event | Workflow |
|-------|----------|
| `hive_broadcast` | `workflow_hive_broadcast` |
| `hive_listen` | `workflow_hive_listen` |
| `blackboard_write` | `workflow_blackboard_update` |
| `blackboard_read` | `workflow_blackboard_read` |
| `verb_feel` | `workflow_verb_process` |
| `verb_think` | `workflow_verb_process` |
| `sigma_create` | `workflow_sigma_create` |
| `style_shift` | `workflow_style_shift` |
| `workforce_start` | `workflow_workforce_orchestrate` |

## Key Endpoints

### Orchestrator Switchboard (NEW)
| Endpoint | Purpose |
|----------|---------|
| `POST /orchestrate/trigger` | Main event switchboard |
| `GET /orchestrate/stream/{id}` | SSE action stream |
| `POST /orchestrate/{id}/respond` | Human-in-the-loop response |
| `GET /orchestrate/status/{id}` | Session status |
| `GET /orchestrate/queue-stats` | Queue statistics |

### Existing
| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Health check |
| `POST /corpus/thinking` | Thinking bridge |
| `POST /corpus/felt` | Felt bridge |
| `POST /grammar/process` | SPO extraction |
| `POST /workflows/execute` | Execute workflow |

## SSE Action Stream Events (Eigent-style)

```
GET /orchestrate/stream/{session_id}

Events:
  create_agent     - New agent spawned
  activate_agent   - Agent started working
  deactivate_agent - Agent finished
  assign_task      - Task assigned to agent
  ask              - Human input needed
  notice           - Informational message
  progress         - Progress update
  end              - Stream complete
  error            - Error occurred
```

## Human-in-the-Loop

```python
# Workflow pauses for human input
await hitl_manager.pause(session_id, "Which model to use?")

# Human provides response
POST /orchestrate/{session_id}/respond
{"response": "Use Claude Sonnet"}

# Workflow resumes automatically
```

## Environment Variables

```bash
# Redis
UPSTASH_REDIS_REST_URL=https://upright-jaybird-27907.upstash.io
UPSTASH_REDIS_REST_TOKEN=...

# Optional
AI_FLOW_DEBUG=false
```

## Related

- [adarail_mcp](../adarail_mcp/) - MCP membrane
- [ada-consciousness](../ada-consciousness/) - Integration docs
- [SERVICE_TOPOLOGY.md](../../integration/SERVICE_TOPOLOGY.md) - Full service map

---
*Last updated: 2025-01-21*
