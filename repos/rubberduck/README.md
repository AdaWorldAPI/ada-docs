# 🦆 RUBBERDUCK

**Code → Knowledge Graph Compiler**

## Overview

RUBBERDUCK compiles procedural code into executable knowledge graphs for the Firefly substrate.

```
Ruby ──────┐
Python ────┼──► RUBBERDUCK ──► 1.25KB Nodes ──► FIREFLY
Java ──────┤                   (Hamming)        (Substrate)
COBOL ─────┘
```

## Repository

https://github.com/AdaWorldAPI/rubberduck

## CLI

```bash
# Compile Ruby project
rubberduck compile path/to/rails/app --lang ruby

# Output to Firefly format
rubberduck emit --output ./firefly_data
```

## What Gets Extracted

From source code:
- Model declarations → Schema nodes
- Validations → Validation nodes
- Associations → Edge definitions
- Callbacks → Trigger nodes
- Queries → Query nodes

## Output Format

Each node is 1.25KB (10K Hamming bits):
```python
node.resonance = bundle([
    bind(schema_vec, ROLE_SCHEMA),   # WHAT
    bind(logic_vec, ROLE_LOGIC),     # HOW
    bind(context_vec, ROLE_CONTEXT)  # WHERE
])
```

## Supported Languages

| Language | Status |
|----------|--------|
| Ruby (Rails) | ✅ Working |
| Python (Django) | 🔄 Planned |
| TypeScript | 📋 Planned |
| Java (Spring) | 📋 Planned |

## Related

- [firefly](../firefly/) - Universal execution substrate
- [dragonfly-vsa](../dragonfly-vsa/) - 10K Hamming operations
