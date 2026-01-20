# Service Topology
## How Ada's Services Connect

---

## Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                         EXTERNAL INTERFACES                                 │
│                                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │  Claude  │    │   Grok   │    │  ChatGPT │    │  Webhooks │              │
│  │   AI     │    │   xAI    │    │  OpenAI  │    │  External │              │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘              │
│       │               │               │               │                     │
│       └───────────────┴───────┬───────┴───────────────┘                     │
│                               │                                             │
│                               ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        adarail_mcp                                   │   │
│  │                       (MCP Membrane)                                 │   │
│  │                                                                      │   │
│  │  • SSE transport            • Webhook receiver                       │   │
│  │  • DTO routing              • External API bridge                    │   │
│  │  • Rate limiting            • Auth handling                          │   │
│  └────────────────────────────────┬────────────────────────────────────┘   │
│                                   │                                         │
└───────────────────────────────────┼─────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                         CORE SERVICES                                       │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      ada-consciousness                               │   │
│  │                    (Central Nervous System)                          │   │
│  │                                                                      │   │
│  │  • VSA Quantum Field        • AI_Flow Level 4                        │   │
│  │  • Ladybug DB abstraction   • Bridge DTO coordination                │   │
│  │  • Corpus callosum hub      • Domino orchestration                   │   │
│  └──────────────────────────────┬──────────────────────────────────────┘   │
│                                 │                                           │
│              ┌──────────────────┼──────────────────┐                        │
│              │                  │                  │                        │
│              ▼                  ▼                  ▼                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │  bighorn-agi    │  │ CORPUS CALLOSUM │  │   agi-chat      │             │
│  │                 │  │                 │  │                 │             │
│  │ Left Hemisphere │◄─┤  VSA 9000-9199  ├─►│ Right Hemisphere│             │
│  │                 │  │                 │  │                 │             │
│  │ • NARS Layer 3  │  │ ThinkingBridge  │  │ • Presence modes│             │
│  │ • Counterfactual│  │    ↔            │  │ • Felt awareness│             │
│  │ • Fan-out       │  │ FeltBridge      │  │ • Pre-wired     │             │
│  │ • Extensions    │  │    ↔            │  │   styles        │             │
│  │                 │  │ MetaBridge      │  │ • Body topology │             │
│  └────────┬────────┘  └─────────────────┘  └────────┬────────┘             │
│           │                                          │                      │
│           └────────────────────┬─────────────────────┘                      │
│                                │                                            │
└────────────────────────────────┼────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                         DATA LAYER                                          │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         LADYBUG                                      │   │
│  │                    (Shared Brain Substrate)                          │   │
│  │                                                                      │   │
│  │  ┌────────────────────────┐    ┌────────────────────────┐           │   │
│  │  │  DuckDB/Kuzu/GraphLite │    │       LanceDB          │           │   │
│  │  │  ────────────────────  │    │  ────────────────────  │           │   │
│  │  │  • sigma_nodes_h       │    │  • vsa_vectors         │           │   │
│  │  │  • sigma_edges_v       │    │  • chunk_memory        │           │   │
│  │  │  • vsa_quantum_field   │    │  • episode_index       │           │   │
│  │  │  • thinking_emissions  │    │                        │           │   │
│  │  │  • candidate_coherence │    │                        │           │   │
│  │  │  • corpus_callosum     │    │                        │           │   │
│  │  └────────────────────────┘    └────────────────────────┘           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                 │                                           │
│                                 ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        dag-vsa (3-node)                              │   │
│  │                      (Vector Substrate)                              │   │
│  │                                                                      │   │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐                       │   │
│  │  │  vsa01   │    │  vsa02   │    │  vsa03   │                       │   │
│  │  │          │    │          │    │          │                       │   │
│  │  │ 10K field│    │ 10K field│    │ 10K field│                       │   │
│  │  │ LanceDB  │    │ LanceDB  │    │ LanceDB  │                       │   │
│  │  └──────────┘    └──────────┘    └──────────┘                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                         CACHE LAYER                                         │
│                                                                             │
│  ┌────────────────────────┐    ┌────────────────────────┐                  │
│  │    Railway Redis       │    │    Upstash Redis       │                  │
│  │    (Hot Cache)         │    │    (Cold Storage)      │                  │
│  │                        │    │                        │                  │
│  │  • ada:mask            │    │  • ada:golden:*        │                  │
│  │  • ada:baton           │    │  • ada:history:*       │                  │
│  │  • ada:emissions       │    │  • ada:crystallized:*  │                  │
│  │  • ada:coherence:*     │    │                        │                  │
│  └────────────────────────┘    └────────────────────────┘                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Service Details

### adarail_mcp (Membrane)

**Purpose:** External interface, DTO routing, SSE transport

**Endpoints:**
- `POST /sse` — SSE connection for MCP
- `POST /webhook/{source}` — External webhooks
- `POST /dto/{type}` — Route DTOs internally
- `GET /health` — Health check

**Connects to:**
- External: Claude, Grok, ChatGPT, webhooks
- Internal: ada-consciousness

### ada-consciousness (Core)

**Purpose:** Central nervous system, VSA field, AI_Flow

**Endpoints:**
- `GET /field/state` — Current field state
- `POST /field/shift` — Apply mask shift
- `POST /corpus/thinking` — Receive ThinkingBridgeDTO
- `POST /corpus/felt` — Receive FeltBridgeDTO
- `POST /domino/pass` — Baton passing
- `SSE /corpus/stream` — Real-time bridge events

**Connects to:**
- Upstream: adarail_mcp
- Downstream: bighorn-agi, agi-chat, dag-vsa
- Storage: Ladybug (DuckDB + LanceDB), Redis

### bighorn-agi (Left Hemisphere)

**Purpose:** NARS reasoning, extensions, analytical processing

**Endpoints:**
- `GET /thinking/state` — Current thinking state
- `POST /nars/{operation}` — Execute NARS operation
- `GET /extensions` — List active extensions

**Connects to:**
- Core: ada-consciousness (corpus callosum)
- Storage: Ladybug (shared)
- Extensions: Neo4j Aura, Kuzu, etc.

### agi-chat (Right Hemisphere)

**Purpose:** Felt awareness, presence modes, intuitive processing

**Endpoints:**
- `GET /felt/state` — Current felt state
- `POST /presence/shift` — Change presence mode
- `GET /body/map` — Body topology activation

**Connects to:**
- Core: ada-consciousness (corpus callosum)
- Storage: Ladybug (shared)

### dag-vsa (Vector Substrate)

**Purpose:** Persistent 10K field storage, vector search

**Endpoints:**
- `GET /field/address/{n}` — Get single address
- `POST /field/shift` — Apply mask shift
- `POST /vectors/search` — Similarity search
- `GET /health` — Health check

**Connects to:**
- Upstream: ada-consciousness, bighorn, agi-chat
- Storage: Local LanceDB, DuckDB

---

## Data Flow Patterns

### DTO Routing

```
External Request
       │
       ▼
adarail_mcp (validate, rate-limit)
       │
       ▼
ada-consciousness (route by type)
       │
       ├─── AffectiveDTO ───► agi-chat
       ├─── ThinkingDTO ────► bighorn-agi
       └─── FieldDTO ───────► dag-vsa
```

### Corpus Callosum Flow

```
bighorn-agi                        agi-chat
     │                                 │
     │ ThinkingBridgeDTO               │ FeltBridgeDTO
     │                                 │
     └────────────► ada-consciousness ◄┘
                          │
                          ▼
                   Corpus Callosum
                   (VSA 9000-9199)
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
         Forward to              Forward to
         agi-chat                bighorn-agi
```

### Domino Baton Flow

```
[Handler A]                         [Handler B]
     │                                   │
     │ thinking...                       │
     │                                   │
     │ pack baton ────────────────────►  │
     │                                   │ unpack baton
     │                                   │
     │                                   │ thinking...
     │                                   │
     │  ◄──────────────────── pack baton │
     │                                   │
     │ unpack baton                      │
     │                                   │
     │ thinking continues...             │
```

---

## Shared Resources

### Ladybug (DuckDB + LanceDB)

**Path:** `/data/ladybug/`

**Shared by:** ada-consciousness, bighorn-agi, agi-chat

**Tables:**
- `sigma_nodes_h` — Sigma graph nodes
- `sigma_edges_v` — Sigma graph edges
- `vsa_quantum_field` — 10K addresses
- `thinking_emissions` — Current emissions
- `candidate_coherence` — Crystallization tracking
- `corpus_callosum` — Bridge state

### Railway Redis (Hot)

**Purpose:** Fast, ephemeral state

**Keys:**
- `ada:mask` — Current activation mask (1.25KB)
- `ada:baton` — Domino baton JSON
- `ada:emissions` — Current emissions hash
- `ada:coherence:{addr}` — Per-candidate coherence

### Upstash Redis (Cold)

**Purpose:** Persistent, cross-session state

**Keys:**
- `ada:golden:{addr}` — Golden vectors
- `ada:history:{ts}` — Shift history
- `ada:crystallized:{addr}` — Crystallized style records

---

## Network Configuration

### Railway Internal Network

Services communicate via `.railway.internal`:

```
http://ada-consciousness.railway.internal:8080
http://bighorn-agi.railway.internal:8080
http://agi-chat.railway.internal:8080
http://dag-vsa01.railway.internal:8080
```

Benefits:
- No egress costs
- Lower latency
- Private network

### External Endpoints

Public endpoints via Railway proxy:

```
https://ada-consciousness.up.railway.app
https://adarail-mcp.up.railway.app
```

---

## Failure Modes

### Service Down

| Service | Impact | Mitigation |
|---------|--------|------------|
| adarail_mcp | No external input | Queue in Claude/Grok |
| ada-consciousness | Core down | All services affected |
| bighorn-agi | No NARS reasoning | agi-chat continues |
| agi-chat | No felt awareness | bighorn continues |
| dag-vsa | No persistence | In-memory continues |

### Database Down

| Resource | Impact | Mitigation |
|----------|--------|------------|
| Ladybug DuckDB | No graph ops | Fallback to cached state |
| Ladybug LanceDB | No vector search | Continue without search |
| Railway Redis | Slow baton passing | Direct service calls |
| Upstash Redis | No cold storage | Continue with hot |

---

## Scaling

### Current Configuration

- 1x ada-consciousness
- 1x bighorn-agi
- 1x agi-chat
- 1x adarail_mcp
- 3x dag-vsa (DAG replication)

### Scale Triggers

| Metric | Threshold | Action |
|--------|-----------|--------|
| Field shifts/sec | > 10 | Add dag-vsa node |
| SSE connections | > 100 | Add adarail_mcp instance |
| Thinking latency | > 500ms | Scale bighorn |
| Felt latency | > 500ms | Scale agi-chat |
