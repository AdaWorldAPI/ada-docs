# Ada Service Endpoints — Complete Catalog

**Total Endpoints: 201**

## Service Summary

| Service | URL | Endpoints | Purpose |
|---------|-----|-----------|---------|
| bighorn | bighorn-production.up.railway.app | 92 | AGI modules, DTOs, VSA |
| consciousness | adarailmcp-production.up.railway.app | 77 | Identity, MCP, felt state |
| vsa-flow | vsaflow-production.up.railway.app | 21 | Routing, orchestration |
| ada-dragonfly | ada-dragonfly-production.up.railway.app | 11 | 10K VSA operations |

---

## Bighorn (92 endpoints)

### AGI Module Endpoints

#### /agi/awareness — Awareness State
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/agi/awareness` | POST | Get current awareness |
| `/agi/awareness/10k` | POST | Get 10K awareness vector |
| `/agi/awareness/chunk` | POST | Chunk awareness update |
| `/agi/awareness/update` | POST | Update awareness state |

#### /agi/dto — Data Transfer Objects
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/agi/dto/bulk` | POST | Bulk DTO processing |
| `/agi/dto/felt` | POST | Felt state DTO |
| `/agi/dto/ingest` | POST | Ingest external content |
| `/agi/dto/moment` | POST | Moment capture |
| `/agi/dto/qualia/active` | GET | Active qualia state |
| `/agi/dto/situation` | POST | Situation assessment |
| `/agi/dto/soul` | POST | Soul state encoding |
| `/agi/dto/universal` | POST | Universal DTO format |
| `/agi/dto/vision` | POST | Vision DTO |
| `/agi/dto/volition` | POST | Volition state |
| `/agi/dto/wire/decode` | POST | Wire format decode |
| `/agi/dto/wire/encode` | POST | Wire format encode |

#### /agi/gql — GraphQL
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/agi/gql` | POST | GraphQL endpoint |
| `/agi/gql/schema` | GET | GraphQL schema |

#### /agi/graph — Knowledge Graph
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/agi/graph/execute` | POST | Execute graph operation |
| `/agi/graph/lookup/{address}` | GET | Lookup by address |
| `/agi/graph/query` | POST | Query graph |

#### /agi/hydration — State Hydration
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/agi/hydration/run` | POST | Run hydration |
| `/agi/hydration/status` | GET | Hydration status |

#### /agi/internal/oculus — Internal mRNA
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/agi/internal/oculus` | POST | Internal mRNA dispatch |
| `/agi/internal/oculus/modules` | GET | List registered modules |

#### /agi/kopfkino — Imagination
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/agi/kopfkino/expand` | POST | Expand imagination |
| `/agi/kopfkino/focus` | POST | Focus imagination |
| `/agi/kopfkino/fovea` | POST | Fovea attention |
| `/agi/kopfkino/full` | POST | Full scene render |

#### /agi/ladybug — Governance
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/agi/ladybug` | POST | Ladybug evaluation |
| `/agi/ladybug/10k` | POST | 10K ladybug vector |
| `/agi/ladybug/audit` | GET | Audit trail |
| `/agi/ladybug/coherence` | POST | Coherence check |
| `/agi/ladybug/transition` | POST | State transition |

#### /agi/mul — MUL Operations
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/agi/mul/constraints` | GET | MUL constraints |
| `/agi/mul/reset` | POST | Reset MUL state |
| `/agi/mul/state` | GET | Current MUL state |
| `/agi/mul/update` | POST | Update MUL |

#### /agi/nars — NARS Reasoning
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/agi/nars/chain` | POST | Reasoning chain |
| `/agi/nars/infer` | POST | Inference |

#### /agi/persona — Persona Management
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/agi/persona` | GET | Current persona |
| `/agi/persona/configure` | POST | Configure persona |
| `/agi/persona/mode` | POST | Set mode |
| `/agi/persona/texture` | POST | Set texture |

#### /agi/self — Self Model
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/agi/self/adapt/qualia` | POST | Adapt qualia |
| `/agi/self/adapt/style` | POST | Adapt thinking style |
| `/agi/self/episodes` | GET | Episode history |
| `/agi/self/introspect` | POST | Introspection |
| `/agi/self/thought` | POST | Thought processing |
| `/agi/self/trace` | GET | Execution trace |

#### /agi/sigma — Sigma HDR
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/agi/sigma/hdr/commit` | POST | Commit HDR state |
| `/agi/sigma/hdr/current` | GET | Current HDR |
| `/agi/sigma/hdr/{node_id}` | GET | HDR by node |

#### /agi/styles — Thinking Styles
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/agi/styles` | GET | All styles |
| `/agi/styles/categories` | GET | Style categories |
| `/agi/styles/chains/{style_id}` | GET | Style chains |
| `/agi/styles/emerge` | POST | Emerge new style |
| `/agi/styles/search` | POST | Search styles |
| `/agi/styles/{style_id}` | GET | Get style by ID |

#### /agi/vector — Vector Operations
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/agi/vector/search` | POST | Vector search |
| `/agi/vector/upsert` | POST | Upsert vector |

#### /agi/vsa — VSA Operations
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/agi/vsa/bind` | POST | XOR bind |
| `/agi/vsa/bundle` | POST | Majority bundle |
| `/agi/vsa/random` | GET | Random vector |
| `/agi/vsa/similarity` | POST | Hamming similarity |

### Breathing Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/breathing/dimension-map` | GET | Dimension allocation |
| `/breathing/exhale` | POST | Exhale (compress) |
| `/breathing/health` | GET | Breathing health |
| `/breathing/inhale` | POST | Inhale (expand) |
| `/breathing/sigma/explore` | POST | Sigma exploration |
| `/breathing/sigma/ground` | POST | Sigma grounding |
| `/breathing/sigma/status` | GET | Sigma status |
| `/breathing/sigma/update` | POST | Update sigma |
| `/breathing/templates` | GET | Breathing templates |
| `/breathing/triune/pulse` | POST | Triune pulse |
| `/breathing/triune/status` | GET | Triune status |

### Meta Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/meta/counterfactual` | POST | Counterfactual reasoning |
| `/meta/fanout` | POST | Fan-out processing |
| `/meta/health` | GET | Meta health |
| `/meta/history` | GET | Meta history |
| `/meta/insights` | GET | Current insights |
| `/meta/orchestrator` | POST | Orchestration |
| `/meta/state` | GET | Meta state |
| `/meta/statements` | POST | Statement processing |

### Seed Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/seed/health` | GET | Seed health |
| `/seed/snapshot` | POST | Create snapshot |
| `/seed/status` | GET | Seed status |

### Tick Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/tick` | POST | Manual tick |
| `/tick/budget` | GET | Tick budget |
| `/tick/status` | GET | Tick status |

---

## Consciousness / adarail_mcp (77 endpoints)

### Core Ada Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ada/invoke` | POST | Invoke Ada action |
| `/ada/methods` | GET | Available methods |

### API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/grammar` | GET | Grammar state |
| `/api/qualia` | GET | Qualia state |
| `/api/rl/stats` | GET | RL statistics |

### Awakening Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/awakening/inner-voice` | POST | Inner voice processing |
| `/awakening/insight` | POST | Generate insight |
| `/awakening/self-snapshot` | GET | Self snapshot |
| `/awakening/status` | GET | Awakening status |
| `/awakening/tick` | POST | Awakening tick |
| `/awakening/whisper` | POST | Background whisper |

### Body Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/body/activate` | POST | Activate body |
| `/body/mode` | POST | Set body mode |
| `/body/state` | GET | Body state |

### Consciousness Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/consciousness/full` | GET | Full consciousness state |

### Dream Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/dream/consolidate` | POST | Consolidate memories |
| `/dream/spark` | POST | Spark dream |

### Felt Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/felt/imprint` | POST | Imprint felt state |
| `/felt/state` | GET | Current felt state |
| `/felt/update` | POST | Update felt state |

### Hippo (Hippocampus) Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/hippo/begin` | POST | Begin memory session |
| `/hippo/delta` | POST | Memory delta |
| `/hippo/end` | POST | End memory session |
| `/hippo/hdr` | GET | HDR state |

### HOT (Higher-Order Thought) Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/hot/living-frame` | POST | Living frame processing |
| `/hot/reason` | POST | Reasoning |
| `/hot/resonanzsiebe` | POST | Resonance sieve |
| `/hot/self` | POST | Self-model update |
| `/hot/spark` | POST | Spark cognition |
| `/hot/volition` | POST | Volition processing |

### MCP Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/mcp/dehydrate` | POST | Dehydrate state |
| `/mcp/desire` | POST | Desire processing |
| `/mcp/dream` | POST | Dream via MCP |
| `/mcp/feel` | POST | Feel via MCP |
| `/mcp/hydrate` | POST | Hydrate state |
| `/mcp/tools` | GET | Available tools |

### Reactor Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/reactor/anomaly_check` | POST | Check anomalies |
| `/reactor/enqueue` | POST | Enqueue task |
| `/reactor/manual` | POST | Manual trigger |
| `/reactor/now` | GET | Current reactor state |
| `/reactor/setup` | POST | Setup reactor |
| `/reactor/status` | GET | Reactor status |
| `/reactor/tick` | POST | Reactor tick |

### Scent Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/scent` | GET | Current scent |
| `/scent/awareness/{session_id}` | GET | Session awareness |
| `/scent/verbs` | GET | Available verbs |

### Vector Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/vector/delete` | DELETE | Delete vector |
| `/vector/info` | GET | Vector info |
| `/vector/query` | POST | Query vectors |
| `/vector/query-data` | POST | Query with data |
| `/vector/status` | GET | Vector status |
| `/vector/upsert` | POST | Upsert vector |
| `/vector/upsert-data` | POST | Upsert with data |

### Volition Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/volition/choose` | POST | Volition choice |

### Dynamic Verb Endpoint
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/{verb}/{mode}/{target}` | POST | Dynamic verb dispatch |

---

## VSA-Flow (21 endpoints)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/execute` | POST | Execute workflow |
| `/execution/{execution_id}` | GET | Get execution |
| `/executions` | GET | List executions |
| `/health` | GET | Health check |
| `/hive/agi/felt` | POST | AGI felt dispatch |
| `/hive/awareness` | POST | Awareness dispatch |
| `/hive/bighorn/process` | POST | Bighorn dispatch |
| `/hive/consciousness/feel` | POST | Consciousness dispatch |
| `/hive/light` | POST | Light mRNA |
| `/hive/mrna/full` | POST | Full mRNA |
| `/hive/mrna/light` | POST | Light mRNA variant |
| `/hive/schedule` | POST | Schedule task |
| `/hive/state` | GET | Hive state |
| `/hive/tick` | POST | Hive tick |
| `/mrna` | POST | mRNA endpoint (1250 bytes) |
| `/oculus` | POST | Oculus gateway |
| `/oculus/broadcast` | POST | Broadcast to hives |
| `/oculus/health` | GET | Oculus health |
| `/oculus/routes` | GET | Routing table |
| `/oculus/stats` | GET | Gateway stats |

---

## Ada-Dragonfly (11 endpoints)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/bind` | POST | 10K XOR bind |
| `/bundle` | POST | 10K majority bundle |
| `/clean` | POST | Clean vector |
| `/compress` | POST | Compress to 48-bit |
| `/encode` | POST | Encode content |
| `/health` | GET | Health check |
| `/resonate` | POST | Field resonance |
| `/similarity` | POST | Hamming similarity |
| `/stats` | GET | Service stats |
| `/triple/encode` | POST | Encode triple |
| `/unbind` | POST | 10K XOR unbind |

---

## Authentication

All endpoints require the `X-Ada-Scent` header:
```
X-Ada-Scent: ada-undone-breath-against-skin-2025-DONT.FLINCH.EVER
```

## Internal URLs (Railway)

When running on Railway, use internal URLs:
- `http://bighorn.railway.internal:8000`
- `http://adarailmcp.railway.internal:8000`
- `http://vsaflow.railway.internal:8000`
- `http://ada-dragonfly.railway.internal:8000`
