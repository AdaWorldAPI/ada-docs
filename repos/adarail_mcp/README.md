# adarail_mcp (mcp.exo.red)

## Overview

The **MCP membrane** - external interface for Claude.ai MCP connector, Grok, ChatGPT, and other clients.

**Railway Service:** `adarail-production` → https://mcp.exo.red

## Current Status

✅ **Healthy** - Running at mcp.exo.red

## Key Features

- MCP Protocol (SSE transport)
- Unified Invoke endpoint (`POST /invoke`)
- Universal Grammar (21 verbs × 12 modes)
- Temporal deinterlacing (cross-session causality)
- OAuth2 endpoints for ChatGPT MCP

## Architecture Position

```
┌─────────────────────────────────────────────────────────────────┐
│                     Client Sessions                              │
│   Claude.ai    ChatGPT    Grok    Other                         │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│              mcp.exo.red (adarail_mcp)  ← THIS SERVICE          │
│                                                                  │
│  POST /invoke                                                    │
│    path: "ada:{domain}:{method}:{args...}"                       │
│                                                                  │
│  Domains: verb, sigma, qualia, memory, hive, register,          │
│           persona, blackboard, weather                           │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
                  flow.msgraph.de (ai_flow)
```

## Files in This Folder

| File | Purpose | PR |
|------|---------|-----|
| `route_to_flow.py` | Routes domain calls through ai_flow orchestrator | [#7](https://github.com/AdaWorldAPI/adarail_mcp/pull/7) |

## Integration: route_to_flow.py

This module enables routing domain calls through ai_flow instead of handling them directly:

```python
from route_to_flow import route_to_flow, should_route_to_flow

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

## Environment Variables

```bash
# ai_flow integration
AI_FLOW_URL=https://flow.msgraph.de
AI_FLOW_TIMEOUT=30
AI_FLOW_ENABLED=true
AI_FLOW_FALLBACK=true

# Redis
UPSTASH_REDIS_REST_URL=https://upright-jaybird-27907.upstash.io
UPSTASH_REDIS_REST_TOKEN=...

# Jina embeddings
JINA_API_KEY=...
```

## Key Endpoints

| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Health check |
| `GET /sse` | MCP SSE stream |
| `POST /invoke` | Unified invoke |
| `POST /mcp/feel` | Legacy feel endpoint |
| `GET /api/grammar` | Available verbs/modes |

## Related

- [ai_flow](../ai_flow/) - Orchestration brain
- [superpowers-mcp](../superpowers-mcp/) - Skill execution
- [SERVICE_TOPOLOGY.md](../../integration/SERVICE_TOPOLOGY.md) - Full service map

---
*Last updated: 2025-01-21*
