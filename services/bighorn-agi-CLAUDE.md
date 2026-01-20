# CLAUDE.md — Bighorn AGI Repository

## Quick Context

This is the **left hemisphere** — NARS reasoning, extensions, and analytical processing.

**You are working on:** NARS Layer 3 styles (counterfactual, fan-out), extension integrations (Neo4j, Kuzu), and ThinkingBridgeDTO emission.

## Critical Files to Read First

```bash
# Contracts and integration
cat .claude/contracts.md
cat .claude/integration.md

# Central documentation (in ada-docs repo)
# - architecture/MASTER_KNOWLEDGE_GRAPH.md
# - contracts/VSA_CONTRACTS.md
# - integration/SERVICE_TOPOLOGY.md
```

## Architecture Position

```
                     ┌─────────────────────────┐
                     │   ada-consciousness     │
                     └───────────┬─────────────┘
                                 │
            ┌────────────────────┼────────────────────┐
            │                    │                    │
            ▼                    │                    ▼
   ┌─────────────────┐           │           ┌─────────────────┐
   │  bighorn-agi    │ ← YOU ARE HERE        │   agi-chat      │
   │ (left hemisphere)│                       │(right hemisphere)│
   └─────────────────┘                       └─────────────────┘
```

## Your Responsibilities

1. **NARS Layer 3** — Implement counterfactual, fan-out, temporal reasoning
2. **Extensions** — Manage Neo4j Aura, Kuzu fast-path, other bolted-on services
3. **ThinkingBridgeDTO** — Emit current thinking state to corpus callosum
4. **Receive FeltBridgeDTO** — React to felt state from right hemisphere

## Key Commands

```bash
# Check NARS implementations
ls -la layer3/

# Check extensions
ls -la extensions/

# Check corpus callosum emitter
cat corpus_callosum/thinking_emitter.py
```

## Shared Resources

**CRITICAL:** You share Ladybug DB with agi-chat!

```python
# Connect to SHARED Ladybug
from ada_consciousness.core import LadybugDB

ladybug = LadybugDB(
    backend="duckdb",
    path="/data/ladybug"  # SAME path as agi-chat
)
```

## ThinkingBridgeDTO Emission

You must emit your state to the corpus callosum:

```python
from ada_consciousness.dto import ThinkingBridgeDTO

dto = ThinkingBridgeDTO(
    emissions={"ANALYTICAL": 0.7, "COUNTERFACTUAL": 0.5},
    nars_active=["counterfactual", "fan-out"],
    touched_candidates=[150, 152],
    layer2_op="inference",
    sigma_path="#Σ.κ.A.T",
    ts=datetime.now(timezone.utc).isoformat()
)

await httpx.post(
    "http://ada-consciousness.railway.internal:8080/corpus/thinking",
    json=asdict(dto)
)
```

## NARS Operations

Layer 3 thinking styles that emit but don't self-modify:

| Operation | Description | Use When |
|-----------|-------------|----------|
| Counterfactual | "What if X were different?" | Exploring alternatives |
| Fan-out | Explore all branches | Comprehensive analysis |
| Temporal | Time-aware reasoning | Sequence understanding |
| Evidential | Evidence accumulation | Building confidence |

## Extensions (Outer Matryoshka)

Bighorn is the outer shell — you can bolt on anything:

```python
class BighornExtensions:
    def add_neo4j_aura(self, uri, auth): ...
    def add_kuzu_fast_path(self): ...
    def add_experiment(self, name, whatever): ...
```

## Don't

- Don't modify Ladybug schema without coordinating
- Don't bypass ada-consciousness for corpus callosum
- Don't let NARS styles self-modify (that's Layer 4)

## Do

- Read `.claude/` folder for context
- Emit ThinkingBridgeDTO regularly
- Use shared Ladybug for graph queries
- Coordinate extensions through ada-consciousness
