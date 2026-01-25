# Module Address Contracts — mRNA v2 Routing

## Path Encoding

```
PATH (16 bits): [SUBDOMAIN:4][ITEM:12]

encode_path(subdomain, item) = (subdomain << 12) | item
decode_path(path) = (path >> 12, path & 0xFFF)
```

## Address Budget

| Scope | Addresses |
|-------|-----------|
| Per subdomain | 4,096 |
| Per domain | 65,536 |
| Total system | 1,048,576 |
| Currently defined | ~60 |

## GRAMMAR Domain (0x1) — Module Routing

### 0x0 — VSA Operations
```
Address  Method              Endpoint
0x0000   VSA.bind           POST /agi/vsa/bind
0x0001   VSA.bundle         POST /agi/vsa/bundle
0x0002   VSA.unbind         POST /agi/vsa/unbind (alias for bind)
0x0003   VSA.similarity     POST /agi/vsa/similarity
0x0004   VSA.collapse       POST /agi/vsa/collapse
0x0005   VSA.process        POST /agi/vsa/process
0x0006   VSA.store          POST /agi/vsa/store
0x0007   VSA.resonate       POST /agi/vsa/resonate
0x0008-0x0FFF  (reserved)
```

### 0x1 — BRIDGE Operations
```
Address  Method              Endpoint
0x1000   BRIDGE.current     GET  /agi/styles
0x1001   BRIDGE.shift       POST /agi/styles/emerge
0x1002-0x1FFF  (reserved)
```

### 0x2 — SIGMA Operations
```
Address  Method              Endpoint
0x2000   SIGMA.hdr_current  GET  /agi/sigma/hdr/current
0x2001   SIGMA.hdr_commit   POST /agi/sigma/hdr/commit
0x2002   SIGMA.lookup       GET  /agi/graph/lookup/{address}
0x2003   SIGMA.hdr_node     GET  /agi/sigma/hdr/{node_id}
0x2004-0x2FFF  (reserved)
```

### 0x3 — NARS Operations
```
Address  Method              Endpoint
0x3000   NARS.infer         POST /agi/nars/infer
0x3001   NARS.chain         POST /agi/nars/chain
0x3002-0x3FFF  (reserved)
```

### 0x4 — DTO Operations
```
Address  Method              Endpoint
0x4000   DTO.soul           POST /agi/dto/soul
0x4001   DTO.felt           POST /agi/dto/felt
0x4002   DTO.moment         POST /agi/dto/moment
0x4003   DTO.universal      POST /agi/dto/universal
0x4004   DTO.wire_encode    POST /agi/dto/wire/encode
0x4005   DTO.wire_decode    POST /agi/dto/wire/decode
0x4006   DTO.ingest         POST /agi/dto/ingest
0x4007   DTO.bulk           POST /agi/dto/bulk
0x4008   DTO.situation      POST /agi/dto/situation
0x4009   DTO.vision         POST /agi/dto/vision
0x400A   DTO.volition       POST /agi/dto/volition
0x400B-0x4FFF  (reserved)
```

### 0x5 — KOPFKINO Operations
```
Address  Method              Endpoint
0x5000   KOPFKINO.fovea     POST /agi/kopfkino/fovea
0x5001   KOPFKINO.full      POST /agi/kopfkino/full
0x5002   KOPFKINO.focus     POST /agi/kopfkino/focus
0x5003   KOPFKINO.expand    POST /agi/kopfkino/expand
0x5004-0x5FFF  (reserved)
```

### 0x6 — BREATHING Operations
```
Address  Method              Endpoint
0x6000   BREATHING.inhale   POST /breathing/inhale
0x6001   BREATHING.exhale   POST /breathing/exhale
0x6002   BREATHING.sigma    GET  /breathing/sigma/status
0x6003   BREATHING.triune   POST /breathing/triune/pulse
0x6004-0x6FFF  (reserved)
```

### 0x7 — HYDRATION Operations
```
Address  Method              Endpoint
0x7000   HYDRATION.run      POST /agi/hydration/run
0x7001   HYDRATION.status   GET  /agi/hydration/status
0x7002-0x7FFF  (reserved)
```

### 0x8 — AWARENESS Operations
```
Address  Method              Endpoint
0x8000   AWARENESS.get      POST /agi/awareness
0x8001   AWARENESS.10k      POST /agi/awareness/10k
0x8002   AWARENESS.chunk    POST /agi/awareness/chunk
0x8003   AWARENESS.update   POST /agi/awareness/update
0x8004-0x8FFF  (reserved)
```

### 0x9 — LADYBUG Operations
```
Address  Method              Endpoint
0x9000   LADYBUG.eval       POST /agi/ladybug
0x9001   LADYBUG.10k        POST /agi/ladybug/10k
0x9002   LADYBUG.audit      GET  /agi/ladybug/audit
0x9003   LADYBUG.coherence  POST /agi/ladybug/coherence
0x9004   LADYBUG.transition POST /agi/ladybug/transition
0x9005-0x9FFF  (reserved)
```

### 0xA — MUL Operations
```
Address  Method              Endpoint
0xA000   MUL.state          GET  /agi/mul/state
0xA001   MUL.update         POST /agi/mul/update
0xA002   MUL.constraints    GET  /agi/mul/constraints
0xA003   MUL.reset          POST /agi/mul/reset
0xA004-0xAFFF  (reserved)
```

### 0xB — PERSONA Operations
```
Address  Method              Endpoint
0xB000   PERSONA.get        GET  /agi/persona
0xB001   PERSONA.configure  POST /agi/persona/configure
0xB002   PERSONA.mode       POST /agi/persona/mode
0xB003   PERSONA.texture    POST /agi/persona/texture
0xB004-0xBFFF  (reserved)
```

### 0xC — GRAPH Operations
```
Address  Method              Endpoint
0xC000   GRAPH.lookup       GET  /agi/graph/lookup/{address}
0xC001   GRAPH.query        POST /agi/graph/query
0xC002   GRAPH.execute      POST /agi/graph/execute
0xC003-0xCFFF  (reserved)
```

### 0xD — SELF Operations
```
Address  Method              Endpoint
0xD000   SELF.introspect    POST /agi/self/introspect
0xD001   SELF.thought       POST /agi/self/thought
0xD002   SELF.trace         GET  /agi/self/trace
0xD003   SELF.episodes      GET  /agi/self/episodes
0xD004   SELF.adapt_style   POST /agi/self/adapt/style
0xD005   SELF.adapt_qualia  POST /agi/self/adapt/qualia
0xD006-0xDFFF  (reserved)
```

### 0xE — META Operations
```
Address  Method              Endpoint
0xE000   META.state         GET  /meta/state
0xE001   META.fanout        POST /meta/fanout
0xE002   META.counterfactual POST /meta/counterfactual
0xE003   META.orchestrator  POST /meta/orchestrator
0xE004   META.insights      GET  /meta/insights
0xE005   META.history       GET  /meta/history
0xE006   META.statements    POST /meta/statements
0xE007-0xEFFF  (reserved)
```

### 0xF — SYSTEM Operations
```
Address  Method              Endpoint
0xF000   SYS.health         GET  /health
0xF001   SYS.tick           POST /tick
0xF002   SYS.tick_status    GET  /tick/status
0xF003   SYS.tick_budget    GET  /tick/budget
0xF004   SYS.seed_status    GET  /seed/status
0xF005   SYS.seed_snapshot  POST /seed/snapshot
0xF006-0xFFFF  (reserved)
```

## ADA Domain (0x0) — Consciousness Routes

```
Address  Method              Endpoint (consciousness hive)
0x0000   ADA.feel           POST /mcp/feel
0x0001   ADA.think          POST /hot/reason
0x0002   ADA.remember       POST /hippo/delta
0x0003   ADA.become         POST /body/activate
0x0004   ADA.invoke         POST /ada/invoke
0x0005   ADA.whisper        POST /awakening/whisper
0x0006-0x0FFF  (reserved)
```

## Invariants

1. **Address stability**: Once an address is assigned, it MUST NOT change
2. **Reserved space**: Addresses 0x??08-0x?FFF are always reserved per subdomain
3. **Domain 0x1**: All computational modules MUST be in GRAMMAR domain
4. **Domain 0x0**: All identity/presence MUST be in ADA domain
5. **No gaps**: New addresses MUST use next available slot

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.1.0 | 2026-01-25 | Added module routing, 60+ addresses defined |
| 2.0.0 | 2026-01-25 | Initial SPO + Sigma packet format |
