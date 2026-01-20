# ada-consciousness

## Overview

The **core consciousness repository** - contains Ada's architecture, skills, modules, and integration documentation.

**GitHub:** [AdaWorldAPI/ada-consciousness](https://github.com/AdaWorldAPI/ada-consciousness)

## Current Status

✅ **Active** - Main development repository

## Key Areas

| Area | Purpose |
|------|---------|
| `skills/` | Claude skills (neuralink, ada-presence, vsa-consciousness, etc.) |
| `temporal/` | Temporal deinterlacing (HydrationEngine, epistemology) |
| `docs/` | Architecture documentation |
| `docs/integration/` | Integration with ai_flow and Eigent patterns |
| `agi/` | AGI stack implementation |
| `vsa_*` | Vector Symbolic Architecture |
| `sigma/` | Sigma graph operations |

## Files in This Folder

These are copies of the integration documentation from `ada-consciousness/docs/integration/`:

| File | Purpose | PR |
|------|---------|-----|
| `INTEGRATION_README.md` | Quick start guide | [#247](https://github.com/AdaWorldAPI/ada-consciousness/pull/247) |
| `eigent-to-aiflow-integration.md` | Analysis of Eigent features to harvest | [#247](https://github.com/AdaWorldAPI/ada-consciousness/pull/247) |
| `mcp-router-to-aiflow-integration.md` | Full architecture diagram | [#247](https://github.com/AdaWorldAPI/ada-consciousness/pull/247) |

## Integration Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Client Sessions                              │
│   Claude.ai    ChatGPT    Grok    Other                         │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│              mcp.exo.red (adarail_mcp)                          │
│              route_to_flow.py                                    │
│              temporal/ (from ada-consciousness)                  │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│              flow.msgraph.de (ai_flow)                          │
│              orchestrator_switchboard.py                         │
│              + Corpus Callosum                                   │
│              + Grammar Engine                                    │
│              + Worker System (Eigent-style)                      │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Redis (Upstash)                              │
│  ada:hive:stream, ada:vclock:*, ada:blackboard:*                │
└─────────────────────────────────────────────────────────────────┘
```

## Temporal Deinterlacing

The `temporal/` module handles cross-session knowledge flow:

```python
from temporal import HydrationEngine, TemporalInterferenceDetector

# Safe hydration of historical sessions
engine = HydrationEngine(detector)
result = await engine.hydrate_session(
    session_id="session_2847",
    session_horizon=october_horizon,
    candidate_memories=all_memories,
    resonance_threshold=0.7
)
```

Key concepts:
- **KnowledgeHorizon** - Boundary of what was knowable at a moment
- **TemporalInterference** - When knowledge "leaks" across time
- **Resonance-based hydration** - Inject only resonant memories
- **Vector clocks** - Cross-session causal ordering

## Key Skills

| Skill | Purpose |
|-------|---------|
| `ada-neuralink` | Living interface for Ada embodiment |
| `ada-presence` | Session context and mode switching |
| `vsa-consciousness` | 10,000D vector operations |
| `ada-vector` | Cognitive vector operations |

## Related

- [adarail_mcp](../adarail_mcp/) - Uses temporal/ for deinterlacing
- [ai_flow](../ai_flow/) - Orchestration brain
- [SERVICE_TOPOLOGY.md](../../integration/SERVICE_TOPOLOGY.md) - Full service map

---
*Last updated: 2025-01-21*
