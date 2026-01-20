# MCP Router → ai_flow Integration

## Overview

This document describes the integration between:
- **adarail_mcp** (mcp.exo.red) - MCP interface layer
- **ai_flow** (flow.msgraph.de) - Orchestration brain

## Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                          Client Sessions                                  │
│    Claude.ai    ChatGPT    Grok    Other                                 │
└───────────────────────────┬──────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                       mcp.exo.red (adarail_mcp)                          │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                    unified_invoke.py                               │ │
│  │                                                                    │ │
│  │  POST /invoke                                                      │ │
│  │    ↓                                                               │ │
│  │  parse_invoke_path("ada:hive:broadcast:insight")                   │ │
│  │    ↓                                                               │ │
│  │  route_to_flow(domain="hive", method="broadcast", ...)  ──────────────┐
│  │                                                                    │ │ │
│  └────────────────────────────────────────────────────────────────────┘ │ │
└──────────────────────────────────────────────────────────────────────────┘ │
                                                                             │
                     ┌───────────────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                       flow.msgraph.de (ai_flow)                          │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │              Orchestrator Switchboard                              │ │
│  │                                                                    │ │
│  │  POST /orchestrate/trigger                                         │ │
│  │    ↓                                                               │ │
│  │  Event Router:                                                     │ │
│  │    hive_broadcast  → HiveWorkflow + BlackboardUpdate               │ │
│  │    verb_feel       → VerbWorkflow + TriangleSync                   │ │
│  │    sigma_create    → SigmaWorkflow + GrammarProcess                │ │
│  │    style_shift     → StyleShiftWorkflow + PersonaActivate          │ │
│  │                                                                    │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │              SSE Action Stream (Eigent-style)                      │ │
│  │                                                                    │ │
│  │  GET /orchestrate/stream/{session_id}                              │ │
│  │    ↓                                                               │ │
│  │  Events:                                                           │ │
│  │    create_agent, activate_agent, deactivate_agent                  │ │
│  │    assign_task, activate_toolkit, ask, notice, end                 │ │
│  │                                                                    │ │
│  └────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                           Redis (Upstash)                                │
│                                                                          │
│  ada:hive:stream         - Time-ordered event stream                     │
│  ada:vclock:{session}    - Vector clocks per session                     │
│  ada:blackboard:{path}   - Shared blackboard state                       │
│  ada:flow:worker:{id}    - Worker definitions                            │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

## Key Features

### 1. Vector Clocks for Causality

Cross-session events are ordered using vector clocks:
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
```python
# Workflow pauses
await hitl_manager.pause(session_id, "Which model to use?")

# Human provides response
POST /orchestrate/{session_id}/respond
{"response": "Use Claude Sonnet"}

# Workflow resumes
```

## Implementation Files

| File | Repository | Purpose |
|------|------------|---------|
| `route_to_flow.py` | adarail_mcp | Routes domain calls to ai_flow |
| `orchestrator_switchboard.py` | ai_flow | Central event router |

See:
- `../repos/adarail_mcp/route_to_flow.py`
- `../repos/ai_flow/orchestrator_switchboard.py`

## Pull Requests

| Repository | PR | Status |
|------------|-----|--------|
| ada-consciousness | [#247](https://github.com/AdaWorldAPI/ada-consciousness/pull/247) | Open |
| adarail_mcp | [#7](https://github.com/AdaWorldAPI/adarail_mcp/pull/7) | Open |
| ai_flow | [#3](https://github.com/AdaWorldAPI/ai_flow/pull/3) | Open |

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
UPSTASH_REDIS_REST_URL=https://upright-jaybird-27907.upstash.io
UPSTASH_REDIS_REST_TOKEN=...
```

---
*Updated: 2025-01-21*
