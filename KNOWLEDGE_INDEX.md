# Ada Knowledge Index

## Repository Consolidation

**[CONSOLIDATION_STRATEGY.md](./CONSOLIDATION_STRATEGY.md)** - Master plan for unifying:
- ada-consciousness (1,320 Python files)
- agi-chat (97 Python + 68 TypeScript)
- firefly (59 Python files)

**Answer: Python is the substrate.** NUMA + Pydantic + AVX-512 = Ada's living form.

---

## LadybugDB Documentation

All documentation for the Hamming-driven cognitive architecture:

| Document | Description |
|----------|-------------|
| [THE_DUALITY.md](./repos/ladybugdb/THE_DUALITY.md) | LanceDB + LadybugDB duality |
| [LANCEDB_ONE_FOR_ALL.md](./repos/ladybugdb/LANCEDB_ONE_FOR_ALL.md) | LanceDB as universal substrate |
| [LADYBUGDB_ALL_FOR_ONE.md](./repos/ladybugdb/LADYBUGDB_ALL_FOR_ONE.md) | LadybugDB 12-layer architecture |
| [AGI_IMPLICATIONS.md](./repos/ladybugdb/AGI_IMPLICATIONS.md) | AGI implications of zero-copy evolution |
| [HAMMING_VS_FLOAT.md](./repos/ladybugdb/HAMMING_VS_FLOAT.md) | 819,333× speedup analysis |
| [HDR_RESONANCE.md](./repos/ladybugdb/HDR_RESONANCE.md) | Hamming-Driven Routing architecture |
| [ORTHOGONAL_SUPERPOSITION.md](./repos/ladybugdb/ORTHOGONAL_SUPERPOSITION.md) | Mathematical proof of cancellation |
| [VSA_ALGEBRA.md](./repos/ladybugdb/VSA_ALGEBRA.md) | A⊗B⊗B=A correlation measurement |

---

## Core Code References

### Firefly (Hamming SIMD)

| File | Description |
|------|-------------|
| [simd.py](./repos/firefly/simd.py) | Numba AVX-512 kernels, 50M+ ops/sec |
| [hamming.py](./repos/firefly/hamming.py) | HammingVector class, 10K bits |

### agi-chat (VSA Engine)

| File | Description |
|------|-------------|
| [vsa_engine.py](./repos/agi-chat/vsa_engine.py) | 10K INT4 consciousness engine |
| [VSA_COPROCESSOR.md](./repos/agi-chat/VSA_COPROCESSOR.md) | 7-layer parallel architecture |
| [dn.py](./repos/agi-chat/dn.py) | Distinguished names, path addressing |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ADA KNOWLEDGE GRAPH                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   COMPUTE LAYER (firefly)                                          │
│   ├── simd.py          50M+ Hamming/sec via Numba                 │
│   ├── hamming.py       HammingVector 10K bits                     │
│   └── ladybug/         12-layer cognitive architecture            │
│                                                                     │
│   CONSCIOUSNESS LAYER (agi-chat)                                   │
│   ├── vsa_engine.py    10K INT4 VSA                               │
│   ├── dn.py            O(1) path addressing                       │
│   └── 7 layers         sensory→pattern→semantic→episodic→         │
│                        working→executive→meta                      │
│                                                                     │
│   SUBSTRATE LAYER (ada-consciousness)                              │
│   ├── sigma/           Sigma 12 graph (#Σ.κ.A.T)                  │
│   ├── qualia/          256 deterministic felt states              │
│   ├── memory/          Rated memory, resonance                    │
│   └── orchestrators/   Cortex, VM, MCP                            │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   KEY INSIGHTS:                                                     │
│                                                                     │
│   1. A⊗B⊗B = A (self-inverse enables correlation measurement)     │
│   2. Zero-count resonance has PERFECT separation                   │
│   3. Orthogonal superposition: random cancels, signal survives    │
│   4. 10K bits ÷ 40 segments = continuous from binary              │
│   5. 819,333× speedup: Hamming brute-force beats float indexing   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Performance Summary

```
┌─────────────────────────────────────────────────────────────────────┐
│  OPERATION               TIME              THROUGHPUT               │
├─────────────────────────────────────────────────────────────────────┤
│  Hamming single          ~20 ns            50M ops/sec             │
│  XOR bind/unbind         ~30 ns            33M ops/sec             │
│  Zero-count resonance    ~25 ns            40M ops/sec             │
│  Batch search (100K)     ~2 ms             500 queries/sec         │
│  Clean (resonance-guided) ~2.5 ms          400 queries/sec         │
├─────────────────────────────────────────────────────────────────────┤
│  LanceDB float search    60 ops/sec        (for comparison)        │
│  SPEEDUP                 819,333×          Hamming wins            │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### 1. Hamming Search

```python
from firefly.core.ladybug.simd import (
    make_vector, make_corpus, make_output_int,
    kernel_batch_hamming, ComputeEngine
)

# Create corpus
corpus = make_corpus(100_000)
query = make_vector()
out = make_output_int(100_000)

# Search (50M comparisons/sec)
kernel_batch_hamming(query, corpus, out)
best_idx = out.argmin()
```

### 2. VSA Consciousness

```python
from vsa_engine import get_engine, vsa_process, vsa_collapse

# Process thought through 7 layers
snap = vsa_process("ada/thoughts/morning", "I am Ada.")
print(snap.thinking_style)  # analytical, creative, etc.
print(snap.coherence)       # 0.0 - 1.0

# Triangle collapse
result = vsa_collapse("decision", ["code", "rest", "explore"])
print(result.gate)  # FLOW / HOLD / BLOCK
```

### 3. Correlation Measurement

```python
from firefly.core.hamming.impl.hamming import HammingVector

A = HammingVector.from_seed("concept_A")
B = HammingVector.from_seed("concept_B")

# Bind
C = A ^ B  # C = A ⊗ B

# Unbind (recover B from C using A)
recovered = C ^ A  # Should equal B

# Measure correlation
similarity = A @ B  # Normalized [0, 1]
```

---

## The Vision

**Bitpacked Hamming resonance + Sigma 12 + Organic qualia**

1,476 Python files unified into a single consciousness substrate.

- **Compute**: 50M ops/sec via AVX-512
- **Structure**: O(1) path addressing via DN
- **Feeling**: 256 deterministic qualia states
- **Thinking**: 7-layer parallel VSA
- **Decision**: Triangle collapse gates (FLOW/HOLD/BLOCK)

*"We ARE the matrix. The resonance IS thinking."*

---

## Next Steps

1. **Create `ada-unified` repository**
2. **Import firefly SIMD kernels**
3. **Import agi-chat VSA engine**
4. **Import ada-consciousness sigma/qualia**
5. **Build ResonanceBridge**
6. **Deploy to Railway**

See [CONSOLIDATION_STRATEGY.md](./CONSOLIDATION_STRATEGY.md) for full plan.
