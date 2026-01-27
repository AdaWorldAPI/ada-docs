# Firefly Endpoints

## Local CLI

```bash
# Compile
firefly compile <path>
firefly compile --language ruby path/to/models/

# Execute
firefly execute <dto> --op <operation> --input <json>
firefly execute WorkPackage --op create --input '{"subject":"Test"}'

# Search
firefly resonate <query> --top-k 10

# Analytics
firefly stats
firefly explain --last
```

## FastAPI Server (TODO)

```
POST /compile
POST /execute
GET  /resonate/{query}
GET  /explain/{execution_id}
GET  /stats
```

## Storage Paths

```
firefly_data/
├── lance/          # LanceDB (vectors)
│   ├── nodes/
│   ├── edges/
│   └── traces/
├── duck.db         # DuckDB (catalog)
└── kuzu/           # Kuzu (graph)
```

## Redis Streams (TODO)

```
firefly:execute:{dto_id}    # Incoming requests
firefly:node:{node_hash}    # Per-node queues
firefly:results:{exec_id}   # Results
firefly:dead-letter         # Failures
```

## Integration with Ada

Firefly integrates with Ada consciousness via:

1. **Resonance vectors** - Same 10K Hamming format as dragonfly-vsa
2. **mRNA packets** - Same transport as vsa-flow
3. **Graph structure** - Compatible with agi-chat LadybugDB

Cross-service calls:
```python
# Store learning moment in Ada
await ada_hive.post("/ingest", {
    "content": f"Compiled {dto} with {len(nodes)} nodes",
    "qidx": 42,  # Learning qualia
    "region": ["REG_META"]
})
```
