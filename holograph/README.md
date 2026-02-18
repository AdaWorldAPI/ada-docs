# Holograph

**A graph database where every node is a 3D SIMD vector, every edge carries subjective perspective, and every query is a Hamming search.**

RedisGraph reimagined in Hamming 3D. Neo4j at 6,000× speed.

## Documents

| Doc | Purpose |
|-----|---------|
| [INTEGRATION_MAP_v3.md](INTEGRATION_MAP_v3.md) | The definitive architecture document. Container geometry, SPOQ viewpoints, blackboard threading, crate responsibilities, execution phases. Handoff doc for Claude Code sessions. |
| [SCHEMA_SPECIFICATION.md](SCHEMA_SPECIFICATION.md) | Domain-blind schema. Six decisions that prevent Holograph from becoming a chess engine. DomainAdapter trait, Fingerprinter interface, cross-domain transfer protocol. **Read this before implementing any Container layout.** |
| [CHESS_BRAIN_PLASTICITY.md](CHESS_BRAIN_PLASTICITY.md) | Validation harness. 8×8 board as XOR network. Brain plasticity experiment: zero-knowledge self-play → emergent concepts → measurable Elo. Cross-domain transfer experiment. |

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

- Architecture: defined (this doc)
- Substrate (ladybug-rs): exists, needs gap wiring + NARS k fix
- Cypher compiler (neo4j-rs): needs RISC refactor (delete 3,403 LOC)
- One binary workspace: not yet created
- Chess validation: not yet started
- Brain plasticity experiment: designed, not implemented
