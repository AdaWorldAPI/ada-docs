# DAG-VSA Topology — Triple Redundancy Vector Store

## Service Status (2026-01-25)

| Node | URL | Endpoints | State | Purpose |
|------|-----|-----------|-------|---------|
| dag-vsa01 | dag-vsa01.msgraph.de | 8 | **healthy** | Felt state engine (21D×10K tensor) |
| dag-vsa02 | dag-vsa02.msgraph.de | 19 | degraded (0 vectors) | Vector store primary + backup |
| dag-vsa03 | dag-vsa03.msgraph.de | 14 | degraded (0 vectors) | Vector store replica |

## dag-vsa01 — Felt State Engine

**Status:** ✅ Healthy, Redis connected  
**Dimensions:** 21D × 10,000 tensor  
**Uptime:** Active

```
/felt/delta       POST  Delta update
/felt/history     GET   Felt history
/felt/load        POST  Load felt state
/felt/save        POST  Save felt state
/felt/state       GET   Current state
/felt/tick        POST  Tick felt state
/felt/update_self POST  Self-update
/health           GET   Health check
```

## dag-vsa02 — Vector Store Primary

**Status:** ⚠️ Degraded (0 vectors stored)  
**Schema:** v2.0.0  
**Tables:**
- `vec10k_bipolar`: Binary {-1, +1}, 1,250 bytes/vector
- `vec10k_int4`: Quantized [-8..+7], 5,000 bytes/vector
- `vec10k_schema`: Full float32, 40,000 bytes/vector

```
/backup/download/{filename}  GET   Download backup
/backup/export               POST  Export backup
/backup/hydrate              POST  Hydrate from backup
/backup/latest               GET   Latest backup info
/backup/restore              POST  Restore from backup
/drain                       POST  Drain node
/drain/prepare               POST  Prepare drain
/health                      GET   Health check
/hydrate/status              GET   Hydration status
/schema                      GET   Schema info
/sync/from/{peer_node}       POST  Sync from peer
/tables                      GET   List tables
/vectors/batch               POST  Batch operations
/vectors/count               GET   Vector count
/vectors/diff/{peer_node}    GET   Diff with peer
/vectors/get/{vector_id}     GET   Get vector
/vectors/list                GET   List vectors
/vectors/upsert              POST  Upsert vector
/vectors/upsert_all          POST  Upsert all vectors
```

## dag-vsa03 — Vector Store Replica

**Status:** ⚠️ Degraded (0 vectors stored)  
**Schema:** v2.0.0  
**Role:** Replica for redundancy

```
/drain                       POST  Drain node
/drain/prepare               POST  Prepare drain
/health                      GET   Health check
/hydrate/status              GET   Hydration status
/schema                      GET   Schema info
/sync/from/{peer_node}       POST  Sync from peer
/tables                      GET   List tables
/vectors/batch               POST  Batch operations
/vectors/count               GET   Vector count
/vectors/diff/{peer_node}    GET   Diff with peer
/vectors/get/{vector_id}     GET   Get vector
/vectors/list                GET   List vectors
/vectors/upsert              POST  Upsert vector
/vectors/upsert_all          POST  Upsert all vectors
```

## Architecture

```
                    ┌─────────────────────┐
                    │   ada-dragonfly     │
                    │  (10KD operations)  │
                    │    11 endpoints     │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
    ┌─────────────────┐ ┌─────────────┐ ┌─────────────┐
    │   dag-vsa01     │ │  dag-vsa02  │ │  dag-vsa03  │
    │  Felt Engine    │ │  Primary    │ │  Replica    │
    │  21D × 10K      │ │  + Backup   │ │             │
    │  8 endpoints    │ │ 19 endpoints│ │ 14 endpoints│
    │    HEALTHY      │ │  DEGRADED   │ │  DEGRADED   │
    └─────────────────┘ └─────────────┘ └─────────────┘
              │                │                │
              └────────────────┴────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │    Upstash Redis    │
                    │    (L0 hot cache)   │
                    └─────────────────────┘
```

## Issue: dag-vsa02/03 Not Connected

The vector stores are running but have 0 vectors stored. They need to be:

1. **Hydrated** from backup or populated fresh
2. **Connected** to vsa-flow/ada-dragonfly for routing
3. **Synced** between each other for quorum

### To Hydrate dag-vsa02:
```python
import httpx

# Check current state
state = httpx.get("https://dag-vsa02.msgraph.de/health").json()
print(f"Vectors: {state['total_vectors']}")  # Currently 0

# If backup exists, restore
httpx.post("https://dag-vsa02.msgraph.de/backup/restore")

# Or upsert vectors directly
httpx.post("https://dag-vsa02.msgraph.de/vectors/upsert", json={
    "id": "test_vector",
    "vector": [...],  # 10K bipolar or int4
    "meta": "{}"
})
```

### To Sync dag-vsa03 from dag-vsa02:
```python
httpx.post("https://dag-vsa03.msgraph.de/sync/from/vsa02")
```

## Total Endpoints

| Node | Count |
|------|-------|
| dag-vsa01 | 8 |
| dag-vsa02 | 19 |
| dag-vsa03 | 14 |
| **Total** | **41** |

## Related

- `SERVICE_ENDPOINTS.md` — Full endpoint catalog
- `SERVICE_INVENTORY.md` — Service counts
- `/mnt/skills/user/vsa-consciousness/` — VSA consciousness skill
