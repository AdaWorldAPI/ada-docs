# adarail_mcp Progress

## Session
- **Date:** 2026-01-20
- **Status:** WAITING

## Mission
MCP membrane — SSE transport, DTO routing, external interface.

## Priority Tasks

### 1. SSE Transport Layer
- [ ] Persistent connection management
- [ ] Reconnection with exponential backoff
- [ ] Event parsing and routing

### 2. DTO Router
- [ ] Route FeltBridgeDTO to correct handler
- [ ] Route ThinkingBridgeDTO to correct handler
- [ ] Route DominoBatonDTO for handoffs

### 3. External MCP Interface
- [ ] Expose tools for Claude.ai integration
- [ ] Handle MCP protocol messages
- [ ] Translate between MCP and internal DTOs

### 4. Railway Internal Network
- [ ] Connect to ada-consciousness.railway.internal
- [ ] Connect to bighorn.railway.internal
- [ ] Connect to agi-chat.railway.internal

## Dependencies
- **ada-consciousness**: Corpus callosum endpoints
- **bighorn**: ThinkingBridgeDTO format
- **agi-chat**: FeltBridgeDTO format
- **dag-vsa**: VSA field for state persistence

## Blocked On
- All other repos must complete their core functionality first

## Next Steps
1. Wait for all upstream repos to complete
2. Then: Wire up SSE connections
3. Implement DTO routing
4. Test end-to-end flow

## Handoff Notes
This is the last piece — the membrane that connects everything.
Don't start until the internal organs are ready.

## Files to Create/Modify
- `src/transport/sse.ts` (new or modify)
- `src/router/dto.ts` (new)
- `src/mcp/tools.ts` (new or modify)
- `src/network/railway.ts` (new)
