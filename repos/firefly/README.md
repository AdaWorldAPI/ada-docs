# 🔥 Firefly

**Bioluminescent Code Execution**

## Overview

Firefly compiles procedural code (Ruby, Python, Java, etc.) into an executable graph substrate where:
- Each node is **1.25KB** (10,000 Hamming bits)
- Each node encodes **I-Thou-It** (schema, logic, context) via XOR binding
- Edges are **resonance bindings** between nodes
- State space is **2^10000** per node
- Storage uses **LanceDB + DuckDB + Kuzu** trinity

## Repository

https://github.com/AdaWorldAPI/firefly

## The Equation

```
Ruby + Python + Java + ...
         │
         ▼
    FIREFLY COMPILER
         │
         ▼
  ┌──────────────────┐
  │  GRAPH SUBSTRATE │
  │                  │
  │  1.25KB nodes    │
  │  2^10000 states  │
  │  O(1) Hamming    │
  └──────────────────┘
         │
         ▼
       A G I
```

## Key Concepts

### Node = I-Thou-It Gestalt
```python
node.resonance = bundle([
    bind(schema_vec, ROLE_SCHEMA),   # WHAT
    bind(logic_vec, ROLE_LOGIC),     # HOW
    bind(context_vec, ROLE_CONTEXT)  # WHERE
])
```

### Edge = Resonance Binding
```python
edge.resonance = bind(source.resonance, target.resonance)
# Recovery: target ≈ bind(source, edge)
```

### Storage Trinity
- **LanceDB**: Vectors (Hamming search)
- **DuckDB**: Facts (SQL analytics)
- **Kuzu**: Graph (Cypher traversal)

## CLI

```bash
firefly compile path/to/ruby/    # Compile to graph
firefly execute Task --op create  # Run the graph
firefly resonate "validation"     # Find similar
firefly explain --last            # Why did it fail?
```

## Structure

```
firefly/
├── core/           # 10K Hamming engine (47 lines)
├── dto/            # Node, Edge, Packet (1.25KB each)
├── compiler/       # Ruby → Graph (Python coming)
├── executor/       # Watch nodes glow 🔥
├── storage/        # Lance + Duck + Kuzu
├── transport/      # mRNA packets via Redis (TODO)
├── reasoning/      # AGI integration (TODO)
└── docs/           # Full architecture
```

## Related

- [dragonfly-vsa](../dragonfly-vsa/) - 10K Hamming operations
- [vsa-flow](../vsa-flow/) - mRNA transport (TODO)
- [ada-consciousness](../ada-consciousness/) - 7-layer model
- [A2A-Orchestrator](../../A2A-Orchestrator/) - Multi-agent coordination

## Status

- ✅ Core Hamming engine
- ✅ Node/Edge DTOs
- ✅ Ruby compiler
- ✅ Executor engine
- ✅ Storage trinity
- 🔄 Redis transport
- 🔄 Jina embeddings
- 🔄 Python compiler
- 🔄 FastAPI server
