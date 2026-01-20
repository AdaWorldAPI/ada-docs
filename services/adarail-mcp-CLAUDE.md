# CLAUDE.md — Adarail MCP Repository

## Quick Context

This is the **membrane** — external interface, DTO routing, and SSE transport.

**You are working on:** MCP protocol handling, webhook reception, DTO routing to internal services, and rate limiting.

## Critical Files to Read First

```bash
# Contracts
cat .claude/contracts.md

# Central documentation (in ada-docs repo)
# - integration/SERVICE_TOPOLOGY.md
# - contracts/DTO_CONTRACTS.md
```

## Architecture Position

```
   ┌──────────┐  ┌──────────┐  ┌──────────┐
   │  Claude  │  │   Grok   │  │  Webhooks │
   └────┬─────┘  └────┬─────┘  └────┬─────┘
        │             │             │
        └─────────────┼─────────────┘
                      │
                      ▼
             ┌─────────────────┐
             │   adarail_mcp   │ ← YOU ARE HERE
             │   (membrane)    │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ ada-consciousness│
             └─────────────────┘
```

## Your Responsibilities

1. **MCP Protocol** — SSE transport for Model Context Protocol
2. **Webhook Reception** — Handle external triggers
3. **DTO Routing** — Route DTOs to appropriate internal services
4. **Rate Limiting** — Protect internal services
5. **Auth Handling** — Validate external requests

## Key Commands

```bash
# Check routing
cat routing/dto_router.py

# Check SSE handling
cat transport/sse_handler.py

# Check webhook receivers
cat webhooks/
```

## DTO Routing

Route incoming DTOs to the right service:

```python
async def route_dto(dto_type: str, payload: dict):
    """Route DTO to appropriate internal service."""
    
    routes = {
        "affective": "http://ada-consciousness.railway.internal:8080/dto/affective",
        "location": "http://ada-consciousness.railway.internal:8080/dto/location",
        "thinking_bridge": "http://ada-consciousness.railway.internal:8080/corpus/thinking",
        "felt_bridge": "http://ada-consciousness.railway.internal:8080/corpus/felt",
        "field_shift": "http://dag-vsa01.railway.internal:8080/field/shift",
    }
    
    if dto_type in routes:
        await httpx.post(routes[dto_type], json=payload)
```

## MCP SSE Transport

Handle SSE connections for Claude and other MCP clients:

```python
@app.post("/sse")
async def sse_endpoint(request: Request):
    """MCP SSE connection handler."""
    
    async def event_generator():
        while True:
            event = await get_next_event()
            yield f"data: {json.dumps(event)}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
```

## Webhook Handling

```python
@app.post("/webhook/{source}")
async def webhook_handler(source: str, request: Request):
    """Handle external webhooks."""
    
    payload = await request.json()
    
    # Validate source
    if not validate_webhook_source(source, request):
        raise HTTPException(401, "Invalid webhook source")
    
    # Route to internal handler
    await route_webhook(source, payload)
```

## Rate Limiting

Protect internal services:

```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.post("/dto/{type}")
@limiter.limit("100/minute")
async def dto_endpoint(type: str, request: Request):
    ...
```

## Don't

- Don't bypass rate limiting for any source
- Don't route DTOs to services that don't expect them
- Don't expose internal service URLs externally

## Do

- Validate all incoming requests
- Rate limit everything
- Log all DTO routing for debugging
- Use internal Railway network for service calls
