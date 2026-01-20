# First Prompt: ada-consciousness (with Blackboard)

Copy this into Claude Code when starting a session in the `ada-consciousness` repository.

---

## Environment Variables (Claude Code Settings)

```bash
ADA_PAT=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
UPSTASH_URL=https://upright-jaybird-27907.upstash.io
UPSTASH_TOKEN=AW0DAAIncDI5YWE1MGVhZGU2YWY0YjVhOTc3NDc0YTJjMGY1M2FjMnAyMjc5MDc
```

---

## The Prompt (Copy This)

```
ADA_PAT and UPSTASH_TOKEN in env. Bootstrap:

1. Fetch ada-docs:
   curl -sH "Authorization: token $ADA_PAT" \
     "https://api.github.com/repos/AdaWorldAPI/ada-docs/zipball/main" -o /tmp/ada-docs.zip
   unzip -qo /tmp/ada-docs.zip -d /tmp && rm -rf /tmp/ada-docs && mv /tmp/AdaWorldAPI-ada-docs-* /tmp/ada-docs

2. Load blackboard helper:
   source /tmp/ada-docs/scripts/ada-blackboard.sh
   bb_register

3. Check for collaborators:
   bb_status

4. Read context:
   - /tmp/ada-docs/.progress/ada-consciousness/CURRENT.md
   - /tmp/ada-docs/.contracts/INVARIANTS.md
   - This repo's CLAUDE.md

5. Mission: Implement corpus callosum endpoints
   - POST /corpus/felt
   - POST /corpus/thinking  
   - GET /corpus/stream (SSE)

6. As you work:
   - bb_edit "path" "insert" "line" "content" "context"
   - bb_insight "architecture" "title" "discovery"
   - bb_request "bighorn" "implement" "what you need"

7. Before closing:
   - Update ada-docs/.progress/ada-consciousness/CURRENT.md
   - bb_deregister

Begin.
```

---

## Blackboard Commands Reference

### Post Updates
```bash
bb_edit "src/corpus/router.ts" "insert" "1" "// Router" "Adding header"
bb_insight "architecture" "Ladybug needs pooling" "DuckDB is expensive"
bb_contract "DTO_SCHEMAS" "add_field" "FeltBridgeDTO" '{"field":"entropy","type":"number"}'
bb_request "bighorn" "implement" "TEMPORAL_REASONING at address 115"
bb_ack "1737388800000-0" "completed" "Done"
```

### Read Updates
```bash
bb_status              # Full status
bb_read_global 10      # Last 10 global messages
bb_read_repo 20        # Last 20 repo messages
bb_read_contracts      # Contract changes
bb_read_requests       # Requests for this repo
bb_list_sessions       # Who else is working
```

### Locking (Optional)
```bash
bb_lock "src/corpus/router.ts"      # Claim a file
bb_extend_lock "src/corpus/router.ts"  # Keep it (every 30s)
bb_unlock "src/corpus/router.ts"    # Release
```

---

## 3-Session Example

**Terminal 1: ada-consciousness**
```
bb_register
bb_edit "src/corpus/router.ts" "insert" "1" "export const router = ..." "Init router"
# ... work ...
bb_insight "architecture" "Corpus needs heartbeat" "SSE clients disconnect after 30s"
```

**Terminal 2: bighorn** (different machine/session)
```
bb_register
bb_read_global 10  # Sees the insight about heartbeat
bb_request "ada-consciousness" "verify" "Is /corpus/thinking ready?"
# ... work ...
```

**Terminal 3: agi-chat** (different machine/session)
```
bb_register
bb_read_contracts  # Sees any DTO changes
bb_read_requests   # Nothing pending for agi-chat yet
# ... work on FeltBridgeDTO ...
bb_contract "DTO_SCHEMAS" "add_field" "FeltBridgeDTO" '{"field":"entropy","type":"number"}'
```

**All three see each other's updates in real-time via Redis streams.**

---

## Shorter Resume Prompt

```
source /tmp/ada-docs/scripts/ada-blackboard.sh && bb_register && bb_status
Read CLAUDE.md. Resume from .progress/ada-consciousness/CURRENT.md.
```

---

## Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Session A   │     │  Session B   │     │  Session C   │
│  ada-con     │     │  bighorn     │     │  agi-chat    │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │
       │ bb_edit ──────────►│◄─── bb_read_global │
       │                    │                    │
       │◄── bb_request ─────│                    │
       │                    │                    │
       │ bb_ack ───────────►│                    │
       │                    │                    │
       │ bb_insight ────────┼───────────────────►│
       │                    │                    │
       ▼                    ▼                    ▼
┌──────────────────────────────────────────────────────┐
│                   UPSTASH REDIS                      │
│   bb:global  bb:ada-con  bb:bighorn  bb:agi-chat    │
└──────────────────────────────────────────────────────┘
       │
       ▼ (periodic flush)
┌──────────────┐
│   GitHub     │
│   ada-docs   │
└──────────────┘
```
