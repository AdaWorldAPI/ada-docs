# Firefly Blackboard

## Project
Firefly - Bioluminescent Code Execution

## Current Phase
PHASE_1_EXTRACTION

## Active Agent
ARCHAEOLOGIST

## Completed Tasks
- [x] Core Hamming engine implemented
- [x] Node/Edge DTOs created
- [x] Ruby compiler working
- [x] Executor engine running
- [x] Storage trinity integrated
- [x] Repository created on GitHub
- [ ] agi-chat extraction
- [ ] bighorn extraction
- [ ] dragonfly-vsa extraction
- [ ] vsa-flow extraction
- [ ] ada-consciousness extraction
- [ ] SYNTHESIS.md created
- [ ] Redis transport implemented
- [ ] Jina embeddings integrated
- [ ] Python compiler working
- [ ] FastAPI server running
- [ ] Tests passing
- [ ] OpenProject models compiled

## Blockers
(none)

## Decisions Made
1. **Node size: 1.25KB (10K bits)** - Matches dragonfly-vsa format, enables Hamming search
2. **Storage: LanceDB + DuckDB + Kuzu** - Each answers different question (similar/facts/connected)
3. **Transport: Redis streams** - Matches vsa-flow mRNA pattern
4. **Packet format: 64B header + 1250B resonance** - Compact but complete
5. **I-Thou-It encoding** - Schema/Logic/Context bound via XOR roles

## Next Actions
1. Clone agi-chat, extract LadybugDB implementation
2. Clone bighorn, extract AGI stack patterns
3. Clone dragonfly-vsa, extract Hamming operations
4. Clone vsa-flow, extract mRNA packet format
5. Clone ada-consciousness, extract 7-layer model
6. Create SYNTHESIS.md with unified patterns

## Agent Notes

### ARCHAEOLOGIST
Repos to analyze:
- AdaWorldAPI/agi-chat → LadybugDB, node/edge schemas
- AdaWorldAPI/bighorn → AGI architecture, Lance client
- AdaWorldAPI/dragonfly-vsa → 10K Hamming, AVX-512
- AdaWorldAPI/vsa-flow → mRNA packets, Redis routing
- AdaWorldAPI/ada-consciousness → 7-layer, membrane

### SYNTHESIZER
(waiting for ARCHAEOLOGIST)

### BUILDER
Modules to implement:
- transport/ (Redis streams, routing, workers)
- core/embed.py (Jina API integration)
- compiler/python.py (Django/SQLAlchemy parser)
- reasoning/ (explain, suggest, optimize, generate)
- server.py (FastAPI endpoints)

### VALIDATOR
Tests to run:
- Unit: core, dto, compiler, storage
- Integration: compile → store → execute → trace
- Benchmark: Hamming <1ms, compile <100ms, execute <10ms
- Real-world: OpenProject models

---

## Collapse Gate Log

| Timestamp | Gate | Decision | Rationale |
|-----------|------|----------|-----------|
| 2026-01-27 | FLOW | 1.25KB node size | Matches existing dragonfly format |
| 2026-01-27 | FLOW | Trinity storage | Clear separation of concerns |
| 2026-01-27 | FLOW | Redis transport | Proven pattern from vsa-flow |

---

## Resources

- GitHub: https://github.com/AdaWorldAPI/firefly
- Docs: firefly/docs/
- Architecture: docs/ARCHITECTURE.md
- Meta Plan: docs/META_PLAN.md
