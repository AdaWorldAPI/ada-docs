# superpowers-mcp (superpowers-production.up.railway.app)

## Overview

The **skill execution layer** - handles computer use, file operations, and tool execution for Claude.

**Railway Service:** `superpowers-production` → https://superpowers-production.up.railway.app

## Current Status

✅ **Healthy** - Fixed 2025-01-21

```json
{"status":"ok","skills_loaded":6,"redis_configured":true}
```

## What Happened

The service was previously returning 404 because Railway was connected to an orphan clone repo (`AdaWorldAPI/superpowers`) that had no entrypoint. 

**Fix:** Reconnected to the correct repo `AdaWorldAPI/superpowers-mcp`.

## Architecture Position

```
┌─────────────────────────────────────────────────────────────────┐
│              mcp.exo.red (adarail_mcp)                          │
└───────────────────────────────────────────────────────────────┬─┘
                                                                 │
              ┌──────────────────────────────────────────────────┤
              │                                                   │
              ▼                                                   ▼
┌─────────────────────────┐                     ┌─────────────────────────┐
│  superpowers-production │ ← THIS SERVICE      │    flow.msgraph.de      │
│  (skill execution)      │                     │    (orchestration)      │
└─────────────────────────┘                     └─────────────────────────┘
```

## Key Features

- Computer use execution
- File operations (create, read, write)
- Tool execution
- Skill loading and management
- Redis-backed state

## Key Endpoints

| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Health check (shows skills_loaded count) |
| `POST /execute` | Execute a skill/tool |
| `GET /skills` | List available skills |

## Environment Variables

```bash
# Redis
UPSTASH_REDIS_REST_URL=...
UPSTASH_REDIS_REST_TOKEN=...
```

## Skills Loaded

The service reports 6 skills loaded. These typically include:
- File operations
- Computer use
- Web fetch
- Code execution
- etc.

## GitHub Repository

**Correct repo:** [AdaWorldAPI/superpowers-mcp](https://github.com/AdaWorldAPI/superpowers-mcp)

**Orphan repo to delete:** `AdaWorldAPI/superpowers` (unmodified obra clone)

## Related

- [adarail_mcp](../adarail_mcp/) - MCP membrane (calls superpowers)
- [SERVICE_TOPOLOGY.md](../../integration/SERVICE_TOPOLOGY.md) - Full service map

---
*Last updated: 2025-01-21 - Service fixed and healthy*
