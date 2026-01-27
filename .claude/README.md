# .claude Directory

This directory contains Claude Code session state and coordination files.

## Structure

```
.claude/
├── README.md           # This file
├── blackboard.md       # Current project state (copy from templates)
├── extractions/        # ARCHAEOLOGIST output
│   ├── agi-chat.md
│   ├── bighorn.md
│   ├── dragonfly-vsa.md
│   ├── vsa-flow.md
│   └── ada-consciousness.md
├── decisions/          # Decision logs
│   └── {date}-{topic}.md
└── sessions/           # Session transcripts
    └── {date}-{summary}.md
```

## Usage

### Start a Session

1. Copy appropriate blackboard template:
   ```bash
   cp A2A-Orchestrator/templates/firefly-blackboard.md .claude/blackboard.md
   ```

2. Read blackboard to understand current state

3. Activate appropriate agent based on phase

### During Session

1. Update blackboard after each significant action
2. Log decisions in decisions/
3. Use COLLAPSE GATE for uncertainty

### End Session

1. Ensure blackboard reflects final state
2. Commit changes to git
3. Note any blockers for next session

## Blackboard Fields

| Field | Purpose |
|-------|---------|
| Current Phase | PHASE_1..4 |
| Active Agent | Who's working |
| Completed Tasks | Checklist |
| Blockers | What's stuck |
| Decisions Made | With rationale |
| Next Actions | Prioritized |
| Agent Notes | Per-agent state |
| Collapse Gate Log | Decision trail |

## Best Practices

1. **Always read blackboard first** - Know where you are
2. **Update incrementally** - Don't wait until end
3. **Document decisions** - Future you will thank you
4. **Use COLLAPSE GATE** - FLOW/HOLD/BLOCK for clarity
5. **Commit often** - Git is your memory
