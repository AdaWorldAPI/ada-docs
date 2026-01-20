# Claude Code Bootstrap Strategy

## Environment Setup (One-Time in Claude Code Settings)

```bash
# Claude Code Environment Variables
ADA_PAT=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
ADA_DOCS_REPO=AdaWorldAPI/ada-docs
```

---

## Progress Sharing Folders in ada-docs

```
ada-docs/
├── .progress/                    # Git-tracked progress sharing
│   ├── README.md                 # How to use progress folders
│   ├── ada-consciousness/
│   │   └── CURRENT.md           # What's being worked on
│   ├── bighorn/
│   │   └── CURRENT.md
│   ├── agi-chat/
│   │   └── CURRENT.md
│   ├── dag-vsa/
│   │   └── CURRENT.md
│   └── adarail_mcp/
│       └── CURRENT.md
├── .queue/                       # Cross-repo task queue
│   ├── PENDING.md               # Tasks awaiting pickup
│   ├── IN_PROGRESS.md           # Currently executing
│   └── COMPLETED.md             # Done tasks (rotate weekly)
└── .contracts/                   # Shared type definitions
    ├── VSA_ADDRESSES.md         # Allocated address ranges
    ├── DTO_SCHEMAS.md           # FeltBridgeDTO, ThinkingBridgeDTO
    └── INVARIANTS.md            # Cross-repo rules
```

---

## Bootstrap Prompt (First Message in Any Repo)

### Option A: Full Bootstrap (Recommended First Time)

```
Read $ADA_PAT from env. Fetch ada-docs:

curl -H "Authorization: token $ADA_PAT" \
  "https://api.github.com/repos/AdaWorldAPI/ada-docs/contents/.progress/$(basename $PWD)/CURRENT.md" \
  | jq -r '.content' | base64 -d

Then read CLAUDE.md in this repo. Check .progress for my last state. Continue or await instructions.
```

### Option B: Quick Resume (Subsequent Sessions)

```
$ADA_PAT → ada-docs/.progress/{this-repo}/CURRENT.md → resume
```

### Option C: Cross-Repo Handoff (When Switching Repos)

```
Before: Push state to ada-docs/.progress/{this-repo}/CURRENT.md
After: Pull state from ada-docs/.progress/{target-repo}/CURRENT.md + .queue/PENDING.md
```

---

## Recommended First Repository: ada-consciousness

### Why Start Here?

1. **Central nervous system** — everything connects through it
2. **Has VSA substrate** — needs to be running before others can write
3. **Corpus callosum endpoints** — bighorn and agi-chat depend on these
4. **Ladybug shared instance** — must be initialized first

### First Session Prompt for ada-consciousness:

```
Environment: ADA_PAT is set.

1. Fetch ada-docs repo for context:
   curl -sH "Authorization: token $ADA_PAT" \
     "https://api.github.com/repos/AdaWorldAPI/ada-docs/zipball/main" -o /tmp/ada-docs.zip
   unzip -q /tmp/ada-docs.zip -d /tmp && mv /tmp/AdaWorldAPI-ada-docs-* /tmp/ada-docs

2. Read /tmp/ada-docs/architecture/MASTER_KNOWLEDGE_GRAPH.md
3. Read /tmp/ada-docs/.progress/ada-consciousness/CURRENT.md (if exists)
4. Read this repo's CLAUDE.md and .claude/agents.json

5. Your mission: Implement corpus callosum endpoints
   - POST /corpus/felt (receive FeltBridgeDTO from agi-chat)
   - POST /corpus/thinking (receive ThinkingBridgeDTO from bighorn)
   - GET /corpus/stream (SSE for real-time sync)

6. When done, push progress:
   Update ada-docs/.progress/ada-consciousness/CURRENT.md via API

Begin.
```

---

## Sequence Recommendation

```
┌─────────────────────────────────────────────────────────────┐
│  SESSION 1: ada-consciousness                               │
│  Goal: Corpus callosum endpoints + Ladybug init             │
│  Output: .progress/ada-consciousness/CURRENT.md             │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  SESSION 2: dag-vsa                                         │
│  Goal: 10K address table + O(1) lookup                      │
│  Depends: Ladybug from session 1                            │
│  Output: .progress/dag-vsa/CURRENT.md                       │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  SESSION 3: bighorn                                         │
│  Goal: ThinkingBridgeDTO emission + NARS styles             │
│  Depends: VSA addresses from session 2                      │
│  Output: .progress/bighorn/CURRENT.md                       │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  SESSION 4: agi-chat                                        │
│  Goal: FeltBridgeDTO emission + presence modes              │
│  Depends: Corpus callosum from session 1                    │
│  Output: .progress/agi-chat/CURRENT.md                      │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  SESSION 5: adarail_mcp                                     │
│  Goal: SSE routing + DTO forwarding                         │
│  Depends: All above                                         │
│  Output: .progress/adarail_mcp/CURRENT.md                   │
└─────────────────────────────────────────────────────────────┘
```

---

## CURRENT.md Template

```markdown
# {repo} Progress

## Session
- **Date:** 2026-01-20
- **Claude Instance:** {session-id if available}
- **Status:** IN_PROGRESS | BLOCKED | COMPLETE

## Completed
- [ ] Task 1
- [x] Task 2

## Current Focus
Working on: {description}
File: {path}
Line: {approx}

## Blocked On
- Waiting for: {other-repo} to complete {task}
- Issue: {description}

## Next Steps
1. {next task}
2. {next task}

## Handoff Notes
{Any context the next session needs}

## Files Modified
- src/corpus_callosum/index.ts (new)
- src/ladybug/init.ts (modified)
```

---

## Quick Reference Commands

### Check In (End of Session)
```bash
# In Claude Code, before closing:
Update ada-docs/.progress/{repo}/CURRENT.md with:
- What was done
- Current state
- Next steps
- Any blockers
```

### Check Out (Start of Session)
```bash
# First message:
Fetch ada-docs/.progress/{repo}/CURRENT.md
Read CLAUDE.md
Resume from last state
```

### Cross-Repo Query
```bash
# When you need info from another repo:
Fetch ada-docs/.progress/{other-repo}/CURRENT.md
Check if {dependency} is complete
If blocked, add to ada-docs/.queue/PENDING.md
```

---

## The One-Liner Bootstrap

For maximum simplicity, put this in your first message:

```
ADA_PAT in env. Fetch ada-docs, read .progress/{this-repo}/CURRENT.md and CLAUDE.md here. Resume or init.
```

That's it. 23 words. Claude Code will:
1. Use the PAT from environment
2. Fetch the central docs
3. Find its last progress state
4. Read local context
5. Either resume or start fresh
