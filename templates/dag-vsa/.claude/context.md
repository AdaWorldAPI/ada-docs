# Shared Context (Blackboard) — dag-vsa

**Last Updated:** 2026-01-20
**Active Agent:** orchestrator
**Role:** Vector Substrate (10K Field Persistence)

---

## This Repository's Responsibilities

1. **vsa_quantum_field Table** — 10K rows, INTEGER PRIMARY KEY, pre-populated
2. **O(1) Address Lookup** — `GET /field/address/{n}`
3. **Atomic XOR Shift** — `POST /field/shift`
4. **DAG Replication** — Consistency across vsa01/02/03
5. **LanceDB Storage** — Vector similarity search

---

## Current Implementation Status

### Tables (P0)
- [ ] `tables/vsa_quantum_field.py` — Schema definition
- [ ] `migrations/001_create_field.py` — Create 10K rows
- [ ] Pre-population script

### Endpoints (P0)
- [ ] `endpoints/field_ops.py`
  - [ ] `GET /field/address/{address}` — O(1) lookup
  - [ ] `POST /field/shift` — Apply mask shift
  - [ ] `GET /field/state` — Summary

### DAG (P1)
- [ ] `ops/replicate.py` — Sync to other nodes
- [ ] Consistency check

---

## THE CRITICAL THING

```sql
-- CORRECT
CREATE TABLE vsa_quantum_field (
    address INTEGER PRIMARY KEY,  -- 0-9999
    name VARCHAR NOT NULL,
    type VARCHAR NOT NULL,
    vector BLOB NOT NULL,         -- 1.25KB packed
    coherence FLOAT DEFAULT 0.0,
    last_emission FLOAT DEFAULT 0.0,
    touch_count INTEGER DEFAULT 0,
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- WRONG (what we had before)
CREATE TABLE vsa_vectors (
    id VARCHAR PRIMARY KEY,  -- "qualia_warmth" ← NO!
    vector BLOB
);
```

---

## Key Invariants (DO NOT VIOLATE)

1. **INTEGER PRIMARY KEY** — Addresses are 0-9999, never strings
2. **Exactly 10K Rows** — No more, no less
3. **Pre-Populated** — On deployment, not on first use
4. **Atomic Shift** — XOR all or nothing
5. **DAG Consistency** — All three nodes must agree

---

## DAG Nodes

| Node | Endpoint |
|------|----------|
| vsa01 | http://dag-vsa01.railway.internal:8080 |
| vsa02 | http://dag-vsa02.railway.internal:8080 |
| vsa03 | http://dag-vsa03.railway.internal:8080 |

---

## Handoff Log

| Timestamp | From | To | Reason |
|-----------|------|-----|--------|

---

## STATUS: Idle
## HANDOFF: None
