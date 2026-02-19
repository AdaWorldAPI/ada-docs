# Holograph

**A graph database where every node is a 3D SIMD vector, every edge carries subjective perspective, and every query is a Hamming search.**

## ⚠️ READ FIRST

**[HOLOGRAPH_CONTRACT.md](HOLOGRAPH_CONTRACT.md)** — The single source of truth. If any other document contradicts this, the contract wins. Contains ground truth tests for each phase.

## Document Map

| Doc | Status | Use |
|-----|--------|-----|
| [HOLOGRAPH_CONTRACT.md](HOLOGRAPH_CONTRACT.md) | **CANONICAL** | Read before everything. Meta layout, crate plan, enforcement rules, ground truth tests. |
| [META_QUADRANTS.md](META_QUADRANTS.md) | ✅ Ground truth | Q1=CAM, Q2=EDGES, Q3=LOWER NODES, Q4=UNDECIDED. Never reassign. |
| [CAM_CODEBOOK.md](CAM_CODEBOOK.md) | ✅ Good | The codebook pipeline. What the fingerprint actually is. |
| [VALIDATION_LADDER.md](VALIDATION_LADDER.md) | ✅ Good | 6-step escalation: chess → AIWar → WikiLeaks → Wikipedia → politics → cross-domain. |
| [CHESS_BRAIN_PLASTICITY.md](CHESS_BRAIN_PLASTICITY.md) | ⚠️ Meta layout wrong | §1.1 meta W32-W63 assignment is wrong. Everything else (XOR network, experiment, implementation) is good. |
| [SCHEMA_SPECIFICATION.md](SCHEMA_SPECIFICATION.md) | ⚠️ Meta layout wrong | §Decision 2 meta layout contradicts contract. Decisions 1,3,4,5,6 are good. DomainAdapter trait is good. |
| [CODEBOOK_MULTIPLEXING.md](CODEBOOK_MULTIPLEXING.md) | ⚠️ Meta layout wrong | §1 meta comment wrong. §2-§10 (resonance, crystallization, meta-think, contracts) are good ideas but uncommitted. |
| [EDGE_CONTRACT.md](EDGE_CONTRACT.md) | ⚠️ Meta layout wrong | §2-§3 W32-W63/W64-W95 assignments wrong. §1,§4-§10 (primitives, content blocks, YAML, traversal, execution) are good. |
| [INTEGRATION_MAP_v3.md](INTEGRATION_MAP_v3.md) | ⚠️ Meta layout wrong | §1.4 quadrants wrong. §0,§2-§9 (architecture, RISC, blackboard, crate map, status) are good. |
| [POLITICAL_INTELLIGENCE.md](POLITICAL_INTELLIGENCE.md) | ✅ Good | PoliticalAdapter design, LLM-in-the-loop, live knowledge graph. |
| [UNIVERSAL_SUBSTRATE.md](UNIVERSAL_SUBSTRATE.md) | ❓ Uncommitted | C-block proposal. Not decided. Don't implement yet. |

## The Thesis

```
The Container doesn't know what it holds.
The Codebook tells it what its bits mean.
When no Codebook fits, a new one is born.
That's thinking.
```

## Status (2026-02-19)

- Architecture: specified in HOLOGRAPH_CONTRACT.md
- Implementation: **zero** — nothing from the holograph spec is coded yet
- ladybug-rs: exists, has substrate code, needs gap wiring + NARS k fix
- neo4j-rs: exists, needs 3,403 LOC deleted and CypherEngine implemented
- One binary: not yet created
- All adapters: designed, not implemented
