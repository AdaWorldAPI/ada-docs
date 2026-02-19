# Holograph

**A graph database where every node is a 3D SIMD vector, every edge carries subjective perspective, and every query is a Hamming search.**

RedisGraph reimagined in Hamming 3D. Neo4j at 6,000× speed.

## Documents

| Doc | Purpose | Read When |
|-----|---------|-----------|
| [CAM_CODEBOOK.md](CAM_CODEBOOK.md) | Content Addressable Memory via learned codebook. 8,192 concepts per axis. Multipass cascade. Why the fingerprint is interpretable. Why cross-domain transfer works. | **Read first.** The foundation. |
| [UNIVERSAL_SUBSTRATE.md](UNIVERSAL_SUBSTRATE.md) | Six break points hardened: C-block (4th axis), hierarchical codebook, concept splitting, embodiment vocabulary, temporal codebook, structural validation of cross-domain transfer. 8 contracts. | After CAM_CODEBOOK. The hardening. |
| [SCHEMA_SPECIFICATION.md](SCHEMA_SPECIFICATION.md) | Domain-blind schema. Six decisions preventing domain lock-in. DomainAdapter trait. | After CAM_CODEBOOK. The rules. |
| [VALIDATION_LADDER.md](VALIDATION_LADDER.md) | The escalation path: Chess → AIWar → WikiLeaks → Wikipedia → Live Politics → Cross-Domain. AIWarAdapter + WikiLeaksAdapter full specs. Publication strategy. | Understanding the argument. |
| [INTEGRATION_MAP_v3.md](INTEGRATION_MAP_v3.md) | Substrate architecture. Container geometry, SPOQ viewpoints, blackboard threading, crate map, execution phases. | Building the substrate. |
| [CHESS_BRAIN_PLASTICITY.md](CHESS_BRAIN_PLASTICITY.md) | Step 1: Perfect information. 8×8 board as XOR network. Zero-knowledge self-play → concepts → Elo. | Implementing ChessAdapter. |
| [POLITICAL_INTELLIGENCE.md](POLITICAL_INTELLIGENCE.md) | Steps 4-5: Scale + live intelligence. Wikipedia commodity benchmark, LLM-in-the-loop, dynamic agent spawning, Trump network, Brier score. | Implementing PoliticalAdapter + WikipediaAdapter. |

## The Thesis

```
Content Addressable Memory with learned codebook.

8,192 concepts per axis (S, P, O). 24,576 total vocabulary.
Each bit = one concept in domain-specific vocabulary.
Fingerprint = presence vector: "which concepts activate here?"
Hamming distance = concept overlap. XOR = concept difference. 
Bundle = prototype. Every operation is interpretable.

Multipass fidelity cascade:
  qidx (8 bits) → sketch (512 bits) → belichtungsmesser (448 bits) → full (8,192 bits)

Cross-domain transfer = codebook alignment in shared embedding space.
Same substrate. Same three ops (BIND, HAMMING, BUNDLE). Five domain adapters.
```

## The Six-Step Validation Ladder

| Step | Domain | What It Proves | Hardware | Ground Truth |
|------|--------|---------------|----------|-------------|
| 1 | Chess | Substrate **learns** | Single CPU | Win/loss (Elo) |
| 2 | AIWar | Handles **fog of war** | Single CPU + game | Win rate vs AI difficulty |
| 3 | WikiLeaks | Reads **real intelligence** | Laptop + $300 API | Historical hindsight (Brier) |
| 4 | Wikipedia | **Scales** to 6.8M entities | Laptop + 512 GB SSD | Category rediscovery rate |
| 5 | Live politics | **Generalizes** to current events | Railway + API | Prediction accuracy (Brier) |
| 6 | Cross-domain | Concepts **transfer** | Same | Binding signature correlation |

Same substrate. Same three operations. Same 8-line loop. Only the adapter changes.

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
    aiwar/          AIWarAdapter (fog of war, NARS confidence from visibility)
    wikileaks/      WikiLeaksAdapter (cable corpus, LLM extraction, historical verification)
    wikipedia/      WikipediaAdapter (dump parser, local embeddings, 654 MB sketch index)
    political/      PoliticalAdapter (Jina + LLM, web search, agent spawning)

cargo build --release → holograph (one binary, five adapters)
```

## Status (2026-02-18)

- Architecture: defined (INTEGRATION_MAP_v3, SCHEMA_SPECIFICATION)
- Domain-blind schema: specified (6 decisions, DomainAdapter trait)
- Validation ladder: complete (6 steps, 6 papers, VALIDATION_LADDER)
- Substrate (ladybug-rs): exists, needs gap wiring + NARS k fix
- Cypher compiler (neo4j-rs): needs RISC refactor (delete 3,403 LOC)
- One binary workspace: not yet created
- ChessAdapter: designed, not implemented
- AIWarAdapter: designed, not implemented
- WikiLeaksAdapter: designed, not implemented
- WikipediaAdapter: designed, not implemented
- PoliticalAdapter: designed, not implemented
- Cross-domain transfer: designed, depends on 2+ adapters running
