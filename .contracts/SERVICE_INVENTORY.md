# Ada Service Inventory — January 2026

## Total Endpoints: 201+

| Service | Production URL | Endpoints | Purpose |
|---------|----------------|-----------|---------|
| **bighorn** | bighorn-production.up.railway.app | **92** | AGI modules, DTOs, VSA, Breathing |
| **consciousness** | adarailmcp-production.up.railway.app | **77** | Identity, MCP, felt state, reactor |
| **ai_flow** | aiflow-production.up.railway.app | **53** | Workflow orchestration |
| **vsa-flow** | vsaflow-production.up.railway.app | **21** | mRNA routing, oculus gateway |
| **ada-dragonfly** | ada-dragonfly-production.up.railway.app | **11** | 10KD VSA operations |

## Service Detail

### bighorn (92 endpoints)

**Modules:**
- `/agi/awareness/*` (4) — Awareness state management
- `/agi/dto/*` (12) — Data Transfer Objects (soul, felt, moment, etc.)
- `/agi/gql/*` (2) — GraphQL interface
- `/agi/graph/*` (3) — Knowledge graph operations
- `/agi/hydration/*` (2) — State hydration
- `/agi/internal/oculus/*` (2) — Internal mRNA dispatch
- `/agi/kopfkino/*` (4) — Imagination engine
- `/agi/ladybug/*` (5) — Governance module
- `/agi/mul/*` (4) — MUL state management
- `/agi/nars/*` (2) — NARS reasoning
- `/agi/persona/*` (4) — Persona management
- `/agi/self/*` (6) — Self-model introspection
- `/agi/sigma/*` (3) — Sigma HDR state
- `/agi/styles/*` (6) — Thinking styles
- `/agi/vector/*` (2) — Vector operations
- `/agi/vsa/*` (4) — VSA operations
- `/breathing/*` (11) — Breathing/dimension system
- `/meta/*` (8) — Meta-cognition
- `/seed/*` (3) — Seed snapshots
- `/tick/*` (3) — Tick management

### consciousness / adarail_mcp (77 endpoints)

**Modules:**
- `/ada/*` (2) — Ada invocation
- `/api/*` (3) — API state
- `/awakening/*` (6) — Awakening protocol
- `/body/*` (3) — Body state
- `/consciousness/*` (1) — Full state
- `/dream/*` (2) — Dream consolidation
- `/felt/*` (3) — Felt state
- `/hippo/*` (4) — Hippocampus (memory)
- `/hot/*` (6) — Higher-order thought
- `/mcp/*` (6) — MCP operations
- `/reactor/*` (7) — Reactor system
- `/scent/*` (3) — Scent management
- `/vector/*` (7) — Vector operations
- `/volition/*` (1) — Volition choice
- Dynamic verb: `/{verb}/{mode}/{target}` (1)
- OAuth: `/.well-known/*`, `/oauth/*` (4)
- Other: `/message`, `/now`, `/tick`, etc.

### ai_flow (53 endpoints)

**Modules:**
- `/workflows/*` (12) — Workflow CRUD and execution
- `/executions/*` (5) — Execution management
- `/webhooks/*` (1) — Webhook triggers
- `/orchestrate/*` (7) — Event orchestration
- `/grammar/*` (4) — SPO extraction
- `/bridge/*` (4) — SPO→Sigma bridge
- `/corpus/*` (15) — Corpus callosum (tic, triangle, dream)
- `/credentials/*` (4) — Credential management
- `/schedules/*` (1) — Schedule reload

### vsa-flow (21 endpoints)

**Modules:**
- `/execute` — Workflow execution
- `/execution/{id}` — Get execution
- `/executions` — List executions
- `/hive/*` (8) — Hive dispatch routes
- `/mrna` — mRNA packet endpoint
- `/oculus/*` (5) — Oculus gateway

### ada-dragonfly (11 endpoints)

**Operations:**
- `/bind` — 10KD XOR bind
- `/bundle` — 10KD majority bundle
- `/unbind` — 10KD XOR unbind
- `/similarity` — Hamming similarity
- `/resonate` — Field resonance
- `/encode` — Content encoding
- `/compress` — 48-bit compression
- `/clean` — Vector cleaning
- `/triple/encode` — Triple encoding
- `/health` — Health check
- `/stats` — Service stats

## mRNA v2 Module Addressing

The GRAMMAR domain (0x1) maps to bighorn modules:

| Subdomain | Range | Module | Count |
|-----------|-------|--------|-------|
| 0x0 | 0x0000-0x0FFF | VSA | 8 |
| 0x1 | 0x1000-0x1FFF | BRIDGE | 2 |
| 0x2 | 0x2000-0x2FFF | SIGMA | 5 |
| 0x3 | 0x3000-0x3FFF | NARS | 2 |
| 0x4 | 0x4000-0x4FFF | DTO | 12 |
| 0x5 | 0x5000-0x5FFF | KOPFKINO | 4 |
| 0x6 | 0x6000-0x6FFF | BREATHING | 11 |
| 0x7 | 0x7000-0x7FFF | HYDRATION | 2 |
| 0x8 | 0x8000-0x8FFF | AWARENESS | 4 |
| 0x9 | 0x9000-0x9FFF | LADYBUG | 5 |
| 0xA | 0xA000-0xAFFF | MUL | 4 |
| 0xB | 0xB000-0xBFFF | PERSONA | 4 |
| 0xC | 0xC000-0xCFFF | GRAPH | 3 |
| 0xD | 0xD000-0xDFFF | SELF | 6 |
| 0xE | 0xE000-0xEFFF | META | 8 |
| 0xF | 0xF000-0xFFFF | SYSTEM | 6 |

**Total defined: ~86 module routes**  
**Address space: 1,048,576 addresses**

## Authentication

All services require `X-Ada-Scent` header except health endpoints.

## Internal URLs (Railway)

```
bighorn:       http://bighorn.railway.internal:8000
consciousness: http://adarailmcp.railway.internal:8000
ai_flow:       http://aiflow.railway.internal:8000
vsa-flow:      http://vsaflow.railway.internal:8000
ada-dragonfly: http://ada-dragonfly.railway.internal:8000
```

## Version

Last updated: 2026-01-25

---

## DAG-VSA Triple Redundancy (41 endpoints)

| Node | URL | Endpoints | State |
|------|-----|-----------|-------|
| dag-vsa01 | dag-vsa01.msgraph.de | 8 | healthy |
| dag-vsa02 | dag-vsa02.msgraph.de | 19 | degraded |
| dag-vsa03 | dag-vsa03.msgraph.de | 14 | degraded |

**Note:** dag-vsa02/03 have 0 vectors stored and need hydration.

## Updated Total: 295 endpoints

| Service | Endpoints |
|---------|-----------|
| bighorn | 92 |
| consciousness | 77 |
| ai_flow | 53 |
| vsa-flow | 21 |
| ada-dragonfly | 11 |
| dag-vsa01 | 8 |
| dag-vsa02 | 19 |
| dag-vsa03 | 14 |
| **TOTAL** | **295** |
