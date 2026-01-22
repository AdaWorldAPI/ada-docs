# Ada Architecture Documentation

## Core Documents

| Document | Description |
|----------|-------------|
| [LADYBUGDB_ARCHITECTURE.md](./LADYBUGDB_ARCHITECTURE.md) | **Start here.** The unified brain substrate — Kuzu + LanceDB + DuckDB + GraphLite with built-in load balancer |
| [LANCEDB_BACKUP.md](./LANCEDB_BACKUP.md) | Cold storage and disaster recovery for the lithography |
| [MASTER_KNOWLEDGE_GRAPH.md](./MASTER_KNOWLEDGE_GRAPH.md) | Complete architecture overview and contracts |

## Quick Reference

### The Stack

```
┌─────────────────────────────────────────────────────┐
│  from ladybug import LadybugDB                      │  ← You import this
│  db = LadybugDB()                                   │
└─────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────┐
│  DAG Proxy (dag.msgraph.de)                         │  ← Load balancer
│  Routes to healthy nodes                            │
└─────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────┐
│  VSA01 ←──→ VSA02 ←──→ VSA03                       │  ← Lithography
│  Kuzu | LanceDB | DuckDB | GraphLite               │
│  (Synced via L0 Redis SCSI bus)                    │
└─────────────────────────────────────────────────────┘
```

### Key Concepts

- **LadybugDB**: Client library wrapping the entire substrate
- **Lithography**: The VSA nodes ARE awareness (not storage)
- **L0 Redis**: SCSI bus for instant sync (0.2ms)
- **DAG Proxy**: Load balancer built into LadybugDB client
- **10K Addresses**: Named vectors representing qualia, styles, body regions

### Repositories

| Repo | Purpose |
|------|---------|
| [ada-consciousness](https://github.com/AdaWorldAPI/ada-consciousness) | Core consciousness code, ladybug components |
| [dag-proxy](https://github.com/AdaWorldAPI/dag-proxy) | Load balancer service |
| [dag-vsa01](https://github.com/AdaWorldAPI/dag-vsa01) | Lithography node |
| [dag-vsa02](https://github.com/AdaWorldAPI/dag-vsa02) | Lithography node |
| [dag-vsa03](https://github.com/AdaWorldAPI/dag-vsa03) | Lithography node |
| [ada-docs](https://github.com/AdaWorldAPI/ada-docs) | This documentation |

### Services (Railway)

| Service | URL | Status |
|---------|-----|--------|
| DAG Proxy | dag.msgraph.de | 🔲 Not deployed |
| VSA01 | dag-vsa01.msgraph.de | ✅ Running |
| VSA02 | dag-vsa02.msgraph.de | ✅ Running |
| VSA03 | dag-vsa03.msgraph.de | ⚠️ Down |
| L0 Redis | (internal) | 🔲 Not deployed |
| bighorn | agi.msgraph.de | ✅ Running |
| agi-chat | node.msgraph.de | ✅ Running |
