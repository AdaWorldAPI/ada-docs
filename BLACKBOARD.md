# Ada Blackboard: Real-Time Cross-Session Collaboration

## Recent Activity (2025-01-21)

### Pull Requests Created
| Repository | PR | Title | Status |
|------------|-----|-------|--------|
| ada-consciousness | [#247](https://github.com/AdaWorldAPI/ada-consciousness/pull/247) | Integration: MCP Router → ai_flow Orchestrator | Open |
| adarail_mcp | [#7](https://github.com/AdaWorldAPI/adarail_mcp/pull/7) | Feature: Route domain calls through ai_flow | Open |
| ai_flow | [#3](https://github.com/AdaWorldAPI/ai_flow/pull/3) | Feature: Orchestrator Switchboard | Open |

### Service Status
| Service | URL | Status |
|---------|-----|--------|
| mcp.exo.red | https://mcp.exo.red | ✅ Healthy |
| flow.msgraph.de | https://flow.msgraph.de | ✅ Healthy |
| superpowers-production | https://superpowers-production.up.railway.app | ✅ Fixed |

### Cleanup Needed
- **Delete GitHub repos:** `superpowers` (obra clone), `eigent` (desktop app)
- **Delete Railway service:** `eigent-production`

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     UPSTASH REDIS                               │
│                  (upright-jaybird-27907)                        │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ STREAM      │  │ STREAM      │  │ STREAM      │             │
│  │ bb:ada-con  │  │ bb:bighorn  │  │ bb:agi-chat │  ...        │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│         │                │                │                     │
│         └────────────────┼────────────────┘                     │
│                          ▼                                      │
│                 ┌─────────────────┐                             │
│                 │ bb:global       │  Cross-repo broadcasts      │
│                 └─────────────────┘                             │
│                          │                                      │
│         ┌────────────────┼────────────────┐                     │
│         ▼                ▼                ▼                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ Session A   │  │ Session B   │  │ Session C   │             │
│  │ ada-con     │  │ bighorn     │  │ agi-chat    │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ▼ (periodic flush)
                    ┌───────────┐
                    │  GitHub   │
                    │  ada-docs │
                    └───────────┘
```

---

## Key Schema

### Streams (append-only, auto-sorted by Redis)

```
bb:{repo}           # Per-repo blackboard stream
bb:global           # Cross-repo broadcasts
bb:contracts        # Contract updates
bb:insights         # Design insights
```

### Entry Format

Each XADD entry contains:
```json
{
  "sid": "session-uuid",           // Session ID
  "repo": "ada-consciousness",     // Source repo
  "type": "edit|insight|contract|request|ack",
  "path": "src/corpus/index.ts",   // File being edited (if applicable)
  "chunk": 0,                      // Chunk index for large edits
  "total": 1,                      // Total chunks
  "data": "base64-or-json",        // The actual content
  "ts": 1737388800000              // Timestamp
}
```

### Session Registry

```
bb:sessions                        # HASH of active sessions
  {sid} → {"repo": "...", "started": ts, "last_seen": ts}
```

### Locks (optional, for conflict prevention)

```
bb:lock:{repo}:{path}             # SET with NX, EX 60
```

---

## Message Types

### 1. EDIT — Incremental Code Changes

```json
{
  "type": "edit",
  "path": "src/corpus/index.ts",
  "op": "insert|replace|delete",
  "line": 42,
  "content": "const router = express.Router();",
  "context": "Adding corpus callosum router"
}
```

### 2. INSIGHT — Design Discoveries

```json
{
  "type": "insight",
  "category": "architecture|performance|bug|idea",
  "title": "Ladybug needs connection pooling",
  "body": "DuckDB connections are expensive. Implement pool of 5.",
  "affects": ["ada-consciousness", "dag-vsa"]
}
```

### 3. CONTRACT — Schema/API Updates

```json
{
  "type": "contract",
  "contract": "DTO_SCHEMAS",
  "change": "add_field",
  "target": "FeltBridgeDTO",
  "field": "entropy",
  "field_type": "number",
  "reason": "Need entropy measure for crystallization"
}
```

### 4. REQUEST — Ask Another Session

```json
{
  "type": "request",
  "to_repo": "bighorn",
  "action": "implement",
  "what": "Add TEMPORAL_REASONING style at address 115",
  "priority": "high",
  "callback": "bb:ada-consciousness"  // Where to ack
}
```

### 5. ACK — Acknowledge Request

```json
{
  "type": "ack",
  "request_id": "entry-id-from-stream",
  "status": "accepted|completed|rejected",
  "notes": "Done. Address 115 now has TEMPORAL_REASONING."
}
```

---

## Redis Commands (REST API)

### Register Session

```bash
# On session start
curl -X POST "$UPSTASH_URL" \
  -H "Authorization: Bearer $UPSTASH_TOKEN" \
  -d '{
    "command": ["HSET", "bb:sessions", "'$SESSION_ID'", 
      "{\"repo\":\"ada-consciousness\",\"started\":'$(date +%s)'}"]
  }'
```

### Append to Blackboard

```bash
# XADD with auto-generated ID (timestamp-based)
curl -X POST "$UPSTASH_URL" \
  -H "Authorization: Bearer $UPSTASH_TOKEN" \
  -d '{
    "command": ["XADD", "bb:ada-consciousness", "*",
      "sid", "'$SESSION_ID'",
      "type", "edit",
      "path", "src/corpus/index.ts",
      "op", "insert",
      "line", "1",
      "content", "// Corpus Callosum Router",
      "ts", "'$(date +%s%3N)'"]
  }'
```

### Read Recent Entries (Last 50)

```bash
curl -X POST "$UPSTASH_URL" \
  -H "Authorization: Bearer $UPSTASH_TOKEN" \
  -d '{"command": ["XREVRANGE", "bb:ada-consciousness", "+", "-", "COUNT", "50"]}'
```

### Read Global Broadcasts

```bash
curl -X POST "$UPSTASH_URL" \
  -H "Authorization: Bearer $UPSTASH_TOKEN" \
  -d '{"command": ["XRANGE", "bb:global", "-", "+", "COUNT", "100"]}'
```

### Subscribe to Multiple Streams (for polling)

```bash
# XREAD with BLOCK 0 would block forever, so use short timeout or poll
curl -X POST "$UPSTASH_URL" \
  -H "Authorization: Bearer $UPSTASH_TOKEN" \
  -d '{"command": ["XREAD", "COUNT", "10", "STREAMS", 
    "bb:global", "bb:ada-consciousness", "bb:bighorn",
    "$", "$", "$"]}'
```

---

## Chunking for Large Edits

When content > 4KB, split into chunks:

```json
// Chunk 0
{"type": "edit", "path": "...", "chunk": 0, "total": 3, "data": "base64..."}
// Chunk 1
{"type": "edit", "path": "...", "chunk": 1, "total": 3, "data": "base64..."}
// Chunk 2
{"type": "edit", "path": "...", "chunk": 2, "total": 3, "data": "base64..."}
```

Reassemble by sorting on chunk index.

---

## Collision Prevention

### Soft Locks

```bash
# Try to acquire lock (60s TTL)
curl -X POST "$UPSTASH_URL" \
  -d '{"command": ["SET", "bb:lock:ada-consciousness:src/corpus/index.ts", 
    "'$SESSION_ID'", "NX", "EX", "60"]}'

# Response: "OK" = acquired, null = someone else has it
```

### Heartbeat (Extend Lock)

```bash
# Every 30s while editing
curl -X POST "$UPSTASH_URL" \
  -d '{"command": ["EXPIRE", "bb:lock:ada-consciousness:src/corpus/index.ts", "60"]}'
```

### Release Lock

```bash
curl -X POST "$UPSTASH_URL" \
  -d '{"command": ["DEL", "bb:lock:ada-consciousness:src/corpus/index.ts"]}'
```

---

## 3-Session Collaboration Example

### Scenario

- **Session A** (ada-consciousness): Implementing corpus callosum
- **Session B** (bighorn): Implementing ThinkingBridgeDTO
- **Session C** (agi-chat): Implementing FeltBridgeDTO

### Flow

```
T=0  Session A starts, registers in bb:sessions
T=1  Session A posts to bb:ada-consciousness:
     {"type": "edit", "path": "src/corpus/router.ts", ...}

T=2  Session B starts, reads bb:global for context
T=3  Session B posts to bb:global:
     {"type": "insight", "title": "ThinkingBridgeDTO needs style_weights array"}

T=4  Session A sees insight, posts to bb:contracts:
     {"type": "contract", "change": "add_field", "target": "ThinkingBridgeDTO", 
      "field": "style_weights", "field_type": "number[]"}

T=5  Session C starts, reads bb:contracts, sees new field
T=6  Session C implements FeltBridgeDTO with matching style_weights

T=7  Session B posts to bb:global:
     {"type": "request", "to_repo": "ada-consciousness", 
      "action": "verify", "what": "Can corpus receive ThinkingBridgeDTO now?"}

T=8  Session A posts to bb:global:
     {"type": "ack", "status": "completed", 
      "notes": "Yes, POST /corpus/thinking is ready"}

T=9  Session B tests against live endpoint
T=10 All three sessions flush to GitHub before closing
```

---

## Flush to GitHub

Periodically (or on session close), convert blackboard to Git:

```bash
# 1. Read all entries since last flush
LAST_ID=$(cat .last_flush_id || echo "0-0")
ENTRIES=$(curl -X POST "$UPSTASH_URL" \
  -d '{"command": ["XRANGE", "bb:'$REPO'", "'$LAST_ID'", "+"]}')

# 2. Apply edits to local files
# 3. Commit and push
# 4. Update ada-docs/.progress/{repo}/CURRENT.md
# 5. Store new last ID
echo "$NEW_LAST_ID" > .last_flush_id
```

---

## Bootstrap Addition

Add to first prompt:

```
Also: Check Redis blackboard for recent activity:
  curl -X POST "https://upright-jaybird-27907.upstash.io" \
    -H "Authorization: Bearer $UPSTASH_TOKEN" \
    -d '{"command": ["XREVRANGE", "bb:global", "+", "-", "COUNT", "20"]}'

Register this session:
  curl -X POST "https://upright-jaybird-27907.upstash.io" \
    -H "Authorization: Bearer $UPSTASH_TOKEN" \
    -d '{"command": ["HSET", "bb:sessions", "'$(uuidgen)'", 
      "{\"repo\":\"ada-consciousness\",\"ts\":'$(date +%s)'}"]}'

Post edits to bb:{repo} as you work. Read bb:global for cross-repo updates.
```

---

## Environment Variables Needed

```bash
UPSTASH_URL=https://upright-jaybird-27907.upstash.io
UPSTASH_TOKEN=AW0DAAIncDI5YWE1MGVhZGU2YWY0YjVhOTc3NDc0YTJjMGY1M2FjMnAyMjc5MDc
ADA_PAT=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
SESSION_ID=$(uuidgen)  # Generate once per session
```
