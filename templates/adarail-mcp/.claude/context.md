# Shared Context (Blackboard) — adarail_mcp

**Last Updated:** 2026-01-20
**Active Agent:** orchestrator
**Role:** MCP Membrane (External Interface)

---

## This Repository's Responsibilities

1. **MCP SSE Transport** — Connect Claude, Grok, other MCP clients
2. **DTO Routing** — Route incoming DTOs to internal services
3. **Webhook Reception** — Handle external triggers
4. **Rate Limiting** — Protect internal services
5. **Auth Handling** — Validate external requests

---

## Current Implementation Status

### Transport (P0)
- [ ] `transport/sse_handler.py` — SSE connection handler
- [ ] `transport/connection_pool.py` — Connection management

### Routing (P0)
- [ ] `routing/dto_router.py` — DTO type detection and routing
- [ ] `routing/routes.py` — Route definitions

### Webhooks (P1)
- [ ] `webhooks/receiver.py` — Webhook endpoint
- [ ] `webhooks/validators.py` — Signature validation

### Middleware (P1)
- [ ] `middleware/rate_limit.py` — Rate limiting
- [ ] `middleware/auth.py` — Authentication

---

## DTO Routing Rules

| DTO Type | Target Service | Endpoint |
|----------|---------------|----------|
| affective | ada-consciousness | /dto/affective |
| location | ada-consciousness | /dto/location |
| thinking_bridge | ada-consciousness | /corpus/thinking |
| felt_bridge | ada-consciousness | /corpus/felt |
| field_shift | dag-vsa01 | /field/shift |

---

## Key Invariants (DO NOT VIOLATE)

1. **Rate Limit Everything** — No exceptions
2. **Validate All Input** — Never trust external data
3. **Internal URLs Private** — Never expose to external
4. **Log Everything** — For debugging and audit

---

## Endpoints

| Endpoint | Purpose |
|----------|---------|
| `POST /sse` | MCP SSE connection |
| `POST /webhook/{source}` | External webhooks |
| `POST /dto/{type}` | DTO routing |
| `GET /health` | Health check |

---

## External → Internal Flow

```
External Client
       │
       ▼
adarail_mcp
├── Validate request
├── Rate limit check
├── Parse DTO
└── Route to internal
       │
       ▼
ada-consciousness (or other)
```

---

## Handoff Log

| Timestamp | From | To | Reason |
|-----------|------|-----|--------|

---

## STATUS: Idle
## HANDOFF: None
