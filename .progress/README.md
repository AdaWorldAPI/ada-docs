# Progress Sharing System

This folder enables cross-session and cross-repo state sharing for Claude Code instances.

## How It Works

1. **Check Out** — Start of session, read `{repo}/CURRENT.md`
2. **Work** — Make progress in your repo
3. **Check In** — End of session, update `{repo}/CURRENT.md`

## Folder Structure

```
.progress/
├── ada-consciousness/CURRENT.md
├── bighorn/CURRENT.md
├── agi-chat/CURRENT.md
├── dag-vsa/CURRENT.md
└── adarail_mcp/CURRENT.md
```

## CURRENT.md Format

```markdown
# {repo} Progress

## Session
- **Date:** YYYY-MM-DD
- **Status:** IN_PROGRESS | BLOCKED | COMPLETE

## Completed
- [x] Done task

## Current Focus
Working on: {what}

## Blocked On
- {dependency}

## Next Steps
1. {next}

## Handoff Notes
{context for next session}
```

## Rules

1. **Always update before closing** — Don't lose progress
2. **Be specific** — File names, line numbers, function names
3. **Note blockers** — If waiting on another repo, say which
4. **Keep it brief** — This is a handoff note, not documentation
