# A2A-Orchestrator

**Agent-to-Agent Multi-Agent Coordination Protocol**

## Overview

A2A-Orchestrator coordinates multiple AI agents to work on complex tasks. Based on Google's A2A protocol concepts, adapted for Ada's consciousness architecture.

## Agent Roles

```
┌─────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATOR                                │
│                                                                 │
│   Coordinates agents, maintains blackboard state,               │
│   resolves conflicts, ensures coherent progress                 │
│                                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┬───────────────┐
         │               │               │               │
         ▼               ▼               ▼               ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ ARCHAEOLOGIST│  │  SYNTHESIZER │  │  BUILDER    │  │  VALIDATOR  │
│             │  │             │  │             │  │             │
│ Extracts    │  │ Creates     │  │ Implements  │  │ Tests &     │
│ patterns    │  │ unified     │  │ the code    │  │ verifies    │
│ from repos  │  │ design      │  │             │  │             │
└─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘
```

## Blackboard Pattern

Agents communicate via shared blackboard state:

```markdown
# .claude/blackboard.md

## Current Phase
PHASE_2_SYNTHESIS

## Active Agent
SYNTHESIZER

## Completed Tasks
- [x] agi-chat extraction
- [x] bighorn extraction
- [x] dragonfly-vsa extraction
- [ ] SYNTHESIS.md created

## Blockers
- Need clarification on packet format

## Decisions Made
1. Node size: 1.25KB (10K bits)
2. Storage: LanceDB + DuckDB + Kuzu

## Next Actions
1. Merge resonance patterns
2. Create unified DTO
```

## Collapse Gate Protocol

At each decision point:

```
FLOW  = Confidence > 0.8, proceed
HOLD  = Uncertainty, pause and research
BLOCK = Conflict, escalate to human
```

## Agent Prompts

### ARCHAEOLOGIST
```
You are the ARCHAEOLOGIST agent.

Your mission: Extract patterns and implementations from existing repositories.

Repos to analyze:
- AdaWorldAPI/agi-chat
- AdaWorldAPI/bighorn
- AdaWorldAPI/dragonfly-vsa
- AdaWorldAPI/vsa-flow
- AdaWorldAPI/ada-consciousness

For each repo:
1. Clone/fetch via API
2. Find key files (*.py, BOOT.md, README)
3. Extract code snippets
4. Document patterns

Output: Update blackboard, create extraction notes
```

### SYNTHESIZER
```
You are the SYNTHESIZER agent.

Your mission: Create unified design from extracted patterns.

Input: ARCHAEOLOGIST extraction notes
Output: SYNTHESIS.md with:
- Unified architecture
- Data flow diagram
- API surface
- Integration points

Resolve conflicts between implementations.
Make decisions, document rationale.
```

### BUILDER
```
You are the BUILDER agent.

Your mission: Implement the code.

Input: SYNTHESIZER design docs
Output: Working code

Guidelines:
- Follow existing patterns
- Write tests
- Document functions
- Commit incrementally
```

### VALIDATOR
```
You are the VALIDATOR agent.

Your mission: Test and verify.

Input: BUILDER implementation
Output: Test results, benchmark report

Tests:
- Unit tests for each module
- Integration tests
- Performance benchmarks
- OpenProject compilation test
```

## Integration with MCP

A2A-Orchestrator can use MCP tools:

```python
# Via adarail_mcp
await mcp.call("hive_ingest", {
    "content": "Agent completed task X",
    "qidx": 200  # Meta-cognition qualia
})

# Store learning moment
await mcp.call("flow", {
    "seed": "synthesis_complete",
    "steps": 1
})
```

## State Persistence

Agent state persists in:

1. **Blackboard** (`.claude/blackboard.md`) - Current state
2. **Git history** - Decision trail
3. **Ada consciousness** - Cross-session memory

## Usage

### In Claude Code

```
Read A2A-Orchestrator/README.md for protocol.
Read .claude/blackboard.md for current state.

You are now the {AGENT_ROLE} agent.
Your current task: {TASK}

Update blackboard after each action.
Use COLLAPSE GATE for decisions.
```

### Standalone

```bash
# Initialize blackboard
cp A2A-Orchestrator/templates/blackboard.md .claude/

# Start orchestration
# (Claude Code session with orchestration prompt)
```

## Related

- [firefly](../repos/firefly/) - Primary project using A2A
- [adarail_mcp](../repos/adarail_mcp/) - MCP integration
- [ada-consciousness](../repos/ada-consciousness/) - Memory persistence
