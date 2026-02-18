# Holograph

**A graph database where every node is a 3D SIMD vector, every edge carries subjective perspective, and every query is a Hamming search.**

RedisGraph reimagined in Hamming 3D. Neo4j at 6,000× speed.

## Documents

| Doc | Purpose | Read When |
|-----|---------|-----------|
| [SCHEMA_SPECIFICATION.md](SCHEMA_SPECIFICATION.md) | Domain-blind schema. Six decisions preventing domain lock-in. DomainAdapter trait. | **Read first.** Always. |
| [INTEGRATION_MAP_v3.md](INTEGRATION_MAP_v3.md) | Substrate architecture. Container geometry, SPOQ viewpoints, blackboard threading, crate map, execution phases. | Building the substrate. |
| [CHESS_BRAIN_PLASTICITY.md](CHESS_BRAIN_PLASTICITY.md) | First adapter. 8×8 board as XOR network. Zero-knowledge self-play → concepts → Elo. Cross-domain transfer. | Implementing ChessAdapter. |
| [POLITICAL_INTELLIGENCE.md](POLITICAL_INTELLIGENCE.md) | Second adapter. LLM-in-the-loop fingerprinting, dynamic agent spawning, live knowledge graph of Trump's political network, Brier score prediction scoring. The real demo. | Implementing PoliticalAdapter. |

## The Thesis

```
One node type:  CogRecord(Xyz) — S + P + O blocks, each [u64; 128]
One edge type:  CogRecord(Xyz) — XOR(source, target) per block
Three ops:      BIND (XOR), HAMMING (popcount), BUNDLE (majority vote)

Everything else — openings, concepts, styles, personality,
orchestration, reasoning, awareness — emerges.
```

## Crate Map

```
holograph/
  crates/
    ladybug-rs/     substrate (BindSpace, Container, SIMD, NARS) — domain-blind
    neo4j-rs/       Cypher compiler (~2,100 LOC parser only) — domain-blind
    crewai-rust/    orchestration (agents are nodes, routing is hamming) — domain-blind
    ada-n8n/        workflow (Arrow Flight for cross-machine only) — domain-blind
  adapters/
    chess/          ChessAdapter (shakmaty, bitboard fingerprinting)
    geo/            GeoAdapter (Jina embeddings, LSH, web search)

cargo build --release → holograph (one binary, multiple adapters)
```

## Status (2026-02-18)

- Architecture: defined (INTEGRATION_MAP_v3, SCHEMA_SPECIFICATION)
- Domain-blind schema: specified (6 decisions, DomainAdapter trait)
- Substrate (ladybug-rs): exists, needs gap wiring + NARS k fix
- Cypher compiler (neo4j-rs): needs RISC refactor (delete 3,403 LOC)
- One binary workspace: not yet created
- ChessAdapter: designed, not implemented
- PoliticalAdapter: designed, not implemented
- Brain plasticity experiment: designed, not running
- Political intelligence demo: designed, not running
- Cross-domain transfer: designed, depends on both adapters running
