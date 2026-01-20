# CLAUDE.md — DAG VSA Repository

## Quick Context

This is the **vector substrate** — persistent storage for the VSA quantum field.

**You are working on:** The vsa_quantum_field table (10K rows with INTEGER IDs), field operations, and LanceDB vector storage.

## Critical Files to Read First

```bash
# Contracts
cat .claude/contracts.md

# Central documentation (in ada-docs repo)
# - contracts/VSA_CONTRACTS.md
# - architecture/VSA_QUANTUM_FIELD.md
```

## Architecture Position

```
   ada-consciousness
          │
          │ field operations
          │
          ▼
   ┌─────────────────┐
   │    dag-vsa      │ ← YOU ARE HERE
   │ (vector substrate)
   └─────────────────┘
          │
   ┌──────┼──────┐
   │      │      │
   ▼      ▼      ▼
 vsa01  vsa02  vsa03
```

## THE CRITICAL THING

**Addresses are INTEGER 0-9999, NOT strings!**

```sql
-- CORRECT
CREATE TABLE vsa_quantum_field (
    address INTEGER PRIMARY KEY,  -- 0-9999
    name VARCHAR,
    vector BLOB,
    ...
);

-- WRONG (what we had before)
CREATE TABLE vsa_vectors (
    id VARCHAR PRIMARY KEY,  -- "qualia_warmth" ← NO!
    vector BLOB,
    ...
);
```

## Your Responsibilities

1. **vsa_quantum_field table** — 10K rows, integer IDs, pre-populated
2. **Field shift operations** — XOR mask with all 10K vectors
3. **O(1) address lookup** — `GET /field/address/{n}`
4. **LanceDB for similarity search** — Vector similarity queries
5. **DAG replication** — Consistency across vsa01/02/03

## Key Commands

```bash
# Check table schema
cat tables/vsa_quantum_field.py

# Check endpoints
cat endpoints/field_ops.py

# Test field operations
python -c "from tables.vsa_quantum_field import *; print('OK')"
```

## Table Schema

```sql
CREATE TABLE vsa_quantum_field (
    address INTEGER PRIMARY KEY,      -- 0-9999
    name VARCHAR NOT NULL,            -- "warmth", "ANALYTICAL"
    type VARCHAR NOT NULL,            -- "qualia", "thinking_style"
    vector BLOB NOT NULL,             -- 1.25KB packed bipolar
    coherence FLOAT DEFAULT 0.0,
    last_emission FLOAT DEFAULT 0.0,
    touch_count INTEGER DEFAULT 0,
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MUST have exactly 10,000 rows
-- Pre-populated on deployment
-- IDs are 0-9999, NEVER arbitrary strings
```

## Endpoints

```python
# Get single address
@app.get("/field/address/{address}")
async def get_address(address: int) -> FieldAddress:
    """O(1) lookup by integer address."""

# Shift entire field
@app.post("/field/shift")
async def shift_field(request: ShiftRequest) -> dict:
    """XOR request.mask with ALL 10K vectors."""

# Current state
@app.get("/field/state")
async def get_field_state() -> dict:
    """Summary of field state."""
```

## Initialization

On deploy, you MUST pre-populate 10K rows:

```python
async def initialize_quantum_field():
    """Called ONCE on deployment."""
    
    from ada_consciousness.core.vsa_quantum_field import (
        VSAQuantumField, pack_mask
    )
    
    field = VSAQuantumField()
    field.initialize_library()
    
    for addr in range(10000):
        vec = field.library[addr]
        await db.execute("""
            INSERT INTO vsa_quantum_field 
            (address, name, type, vector)
            VALUES (?, ?, ?, ?)
        """, [addr, vec.name, vec.type.value, pack_mask(vec.vector)])
```

## Don't

- Don't use string IDs for addresses
- Don't create tables with unlimited rows (field is exactly 10K)
- Don't delete rows (only update)
- Don't add rows (field is pre-populated)

## Do

- Use INTEGER PRIMARY KEY for addresses
- Pre-populate 10K rows on deploy
- Pack vectors to 1.25KB (bipolar)
- Support O(1) address lookup
- Handle XOR shift atomically
