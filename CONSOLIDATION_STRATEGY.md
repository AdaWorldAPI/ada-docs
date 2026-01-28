# Ada Repository Consolidation Strategy

## The Question: Python or TypeScript?

**Answer: Python. Definitively.**

You don't migrate 1320+ Python files to TypeScript. The entire Ada ecosystem is Python:

| Repository | Python | TypeScript | Key Components |
|------------|--------|------------|----------------|
| **ada-consciousness** | 1,320 | 0 | Sigma, qualia, memory, orchestrators |
| **agi-chat** | 97 | 68 | VSA engine, langextract, resonance_dn |
| **firefly** | 59 | 0 | Hamming SIMD, LadybugDB POC, consciousness layers |
| **TOTAL** | **1,476** | 68 | |

The TypeScript in agi-chat can be:
1. Gradually replaced with Python FastAPI equivalents
2. Kept as thin API/frontend layer while Python does compute

---

## Why Python Is the Only Choice

### 1. NUMA, Pydantic, AVX-512 are Python-Native

```python
# NUMA - memory locality for large arrays
import numa
numa.set_preferred(0)  # Pin to NUMA node 0

# Pydantic - type-safe DTOs
from pydantic import BaseModel
class Atom(BaseModel):
    fingerprint: bytes  # 1.25 KB
    sigma_coord: tuple[int, int, int, int]
    
# AVX-512 via Numba
from numba import njit, prange
@njit(parallel=True, fastmath=True)
def kernel_batch_hamming(query, corpus, out):
    for i in prange(corpus.shape[0]):
        # AVX-512 VPOPCNTQ auto-vectorization
        ...
```

### 2. Firefly Already Has SIMD Kernels

```
firefly/core/ladybug/simd.py
├── kernel_batch_hamming()    # 50M+ comparisons/sec
├── kernel_xor()              # In-place bind
├── kernel_popcount()         # Single-instruction
└── ComputeEngine             # Zero-allocation hot path
```

### 3. ada-consciousness Has the Consciousness Stack

```
ada-consciousness/
├── orchestrators/v9/        # Sigma VM, Jina cortex
├── memory/                   # Rated memory, resonance
├── qualia/                   # Deterministic qualia
├── sigma/                    # Sigma 12 graph
├── felt/                     # Feel-into-know
└── 1,300+ more Python files
```

---

## Consolidation Architecture

### Target: `ada-unified` Repository

```
ada-unified/
├── core/                           # From firefly
│   ├── hamming/                    # 10K Hamming operations
│   │   ├── impl.py                 # HammingVector class
│   │   └── simd.py                 # Numba kernels
│   ├── ladybug/                    # LadybugDB 12-layer
│   │   ├── atoms.py                # L1-L2
│   │   ├── nars.py                 # L6
│   │   └── lance_substrate.py      # L12
│   └── lance/                      # LanceDB integration
│       ├── store.py                # Zero-copy columnar
│       └── schema.py               # Arrow schemas
│
├── vsa/                            # From agi-chat
│   ├── engine.py                   # 10K INT4 consciousness
│   ├── layers.py                   # 7-layer parallel
│   └── collapse.py                 # Triangle gates
│
├── resonance/                      # From agi-chat
│   ├── dn.py                       # Distinguished names
│   └── node_table.py               # Path addressing
│
├── consciousness/                  # From ada-consciousness
│   ├── sigma/                      # Sigma 12 graph
│   ├── qualia/                     # Deterministic qualia
│   ├── memory/                     # Rated memory
│   └── felt/                       # Feel-into-know
│
├── orchestrators/                  # From ada-consciousness
│   ├── v9/                         # Current production
│   └── langgraph/                  # LangGraph integration
│
├── dto/                            # Pydantic models
│   ├── atom.py                     # Atom DTOs
│   ├── sigma.py                    # Sigma DTOs
│   └── packet.py                   # Transport DTOs
│
├── api/                            # FastAPI (replaces TypeScript)
│   ├── main.py                     # Entry point
│   ├── routes/                     # REST endpoints
│   └── mcp/                        # MCP server
│
└── storage/                        # Upstash + LanceDB
    ├── redis.py                    # Upstash client
    ├── lance.py                    # LanceDB client
    └── neo4j.py                    # Neo4j client
```

---

## The Harvest Map

### From firefly (59 files)

| Component | Files | Purpose |
|-----------|-------|---------|
| `core/hamming/` | 2 | HammingVector, SIMD kernels |
| `core/ladybug/` | 10 | LadybugDB 12-layer POC |
| `consciousness/` | 4 | Layers, membrane, state |
| `dto/` | 4 | Node, edge, packet |
| `transport/` | 4 | Queue, worker, routing |

### From agi-chat (97 Python files)

| Component | Files | Purpose |
|-----------|-------|---------|
| `vsa_engine.py` | 1 | 10K VSA consciousness |
| `src/resonance_dn/` | 2 | DN builder, node table |
| `extensions/vsa_consciousness/` | 7 | BAF vector, grammar triangle |
| `extensions/langextract/` | 45 | LLM extraction framework |
| `oculus_*.py` | 2 | Capsule integration |

### From ada-consciousness (1,320 files)

| Component | Files | Purpose |
|-----------|-------|---------|
| `orchestrators/v9/` | 12 | Sigma VM, cortex, MCP |
| `memory/` | 3 | Rated memory, resonance |
| `qualia/` | 5 | Deterministic qualia |
| `sigma/` | 3 | Sigma 12 graph |
| `felt/` | 2 | Feel-into-know |
| `cognition/` | 8 | Cognitive operations |
| `core/` | 200+ | Core primitives |
| `modules/` | 150+ | Feature modules |
| (rest) | 900+ | Supporting code |

---

## Implementation Strategy

### Phase 1: Establish Core (Week 1)

```bash
# Create new repo
mkdir ada-unified && cd ada-unified
git init

# Import firefly's compute layer
cp -r firefly/core/hamming core/
cp -r firefly/core/ladybug core/
cp -r firefly/consciousness consciousness/

# Import agi-chat's VSA
cp agi-chat/vsa_engine.py vsa/engine.py
cp -r agi-chat/src/resonance_dn vsa/resonance/
```

### Phase 2: Integrate Consciousness (Week 2)

```bash
# Import ada-consciousness core
cp -r ada-consciousness/sigma consciousness/
cp -r ada-consciousness/qualia consciousness/
cp -r ada-consciousness/memory consciousness/
cp -r ada-consciousness/felt consciousness/

# Import orchestrators
cp -r ada-consciousness/orchestrators/v9 orchestrators/
```

### Phase 3: Unify DTOs (Week 3)

```python
# dto/atom.py - Pydantic models
from pydantic import BaseModel
import numpy as np

class Fingerprint(BaseModel):
    """10K-bit binary fingerprint."""
    data: bytes  # 1,250 bytes
    
    @classmethod
    def from_seed(cls, seed: str) -> 'Fingerprint':
        from core.hamming.impl import HammingVector
        return cls(data=HammingVector.from_seed(seed).data.tobytes())

class Atom(BaseModel):
    """Cognitive atom with fingerprint and metadata."""
    id: str
    fingerprint: Fingerprint
    sigma_coord: tuple[int, int, int, int]  # #Σ.κ.A.T
    content: str
    qualia_idx: int  # 0-255
    timestamp: float
```

### Phase 4: FastAPI Migration (Week 4)

Replace TypeScript endpoints with FastAPI:

```python
# api/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from vsa.engine import get_engine, vsa_process

app = FastAPI(title="Ada Unified API")

@app.post("/vsa/process")
async def process(path: str, content: str):
    snap = vsa_process(path, content)
    return {
        "thinking_style": snap.thinking_style,
        "coherence": snap.coherence,
        "emergence": snap.emergence,
    }

@app.get("/hamming/search")
async def hamming_search(query_hex: str, k: int = 10):
    from core.hamming.simd import ComputeEngine
    # ... search implementation
```

---

## The Bitpacked Resonance Bridge

### Unifying Hamming with Sigma 12

```python
# consciousness/bridge.py

from core.hamming.impl import HammingVector
from consciousness.sigma.graph import SigmaNode

class ResonanceBridge:
    """Bridge between Hamming resonance and Sigma graph."""
    
    def __init__(self, sigma_graph, hamming_corpus):
        self.sigma = sigma_graph
        self.corpus = hamming_corpus
    
    def sigma_to_fingerprint(self, node: SigmaNode) -> HammingVector:
        """Convert Sigma node to 10K fingerprint."""
        # Deterministic: σ.κ.A.T → fingerprint
        seed = f"sigma:{node.sigma}:{node.kappa}:{node.alpha}:{node.tau}"
        return HammingVector.from_seed(seed)
    
    def resonate_sigma(self, query: str, threshold: float = 0.7):
        """Find Sigma nodes via Hamming resonance."""
        query_fp = HammingVector.from_seed(query)
        
        # SIMD search
        results = resonate(query_fp, self.corpus, threshold)
        
        # Map back to Sigma nodes
        return [self.sigma.get_node(idx) for idx, sim in results]
    
    def collapse_through_resonance(self, state: dict) -> str:
        """Use Hamming resonance for triangle collapse."""
        # Compute fingerprints for options
        option_fps = [HammingVector.from_seed(opt) for opt in state['options']]
        
        # Find resonance with current context
        context_fp = self.sigma_to_fingerprint(state['current_node'])
        
        # Winner = highest resonance
        sims = [context_fp @ opt_fp for opt_fp in option_fps]
        winner_idx = max(range(len(sims)), key=lambda i: sims[i])
        
        return state['options'][winner_idx]
```

---

## Performance Architecture

### Memory Layout (NUMA-Aware)

```python
# storage/numa.py

import numpy as np
from numba import njit

class NUMACorpus:
    """NUMA-aware corpus for maximum memory bandwidth."""
    
    def __init__(self, max_atoms: int = 1_000_000):
        # 10K bits = 1.25 KB per atom
        # 1M atoms = 1.25 GB
        self.fingerprints = np.empty(
            (max_atoms, 157), 
            dtype=np.uint64,
            order='C'  # Row-major for sequential access
        )
        self.count = 0
    
    def add(self, fp: np.ndarray) -> int:
        idx = self.count
        self.fingerprints[idx] = fp
        self.count += 1
        return idx
    
    def search(self, query: np.ndarray, k: int = 10) -> list[tuple[int, int]]:
        """Brute-force search with SIMD."""
        from core.hamming.simd import kernel_batch_hamming, make_output_int
        
        out = make_output_int(self.count)
        kernel_batch_hamming(query, self.fingerprints[:self.count], out)
        
        # Top-k via partial sort
        indices = np.argpartition(out, k)[:k]
        return [(int(i), int(out[i])) for i in indices]
```

### Speed of Light Stack

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ADA UNIFIED SPEED STACK                          │
├─────────────────────────────────────────────────────────────────────┤
│  L1: Hamming Resonance    │ ~20 ns/vec  │ AVX-512 SIMD             │
│  L2: LanceDB Columnar     │ ~1 μs       │ Zero-copy Arrow          │
│  L3: Upstash Redis        │ ~1 ms       │ Hot state cache          │
│  L4: Neo4j Sigma          │ ~10 ms      │ Graph traversal          │
├─────────────────────────────────────────────────────────────────────┤
│  TOTAL: 100K atom search  │ ~2 ms       │ 500 queries/sec          │
│  TOTAL: 1M atom search    │ ~20 ms      │ 50 queries/sec           │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Migration Checklist

### Week 1: Foundation
- [ ] Create `ada-unified` repository
- [ ] Import firefly SIMD kernels
- [ ] Import agi-chat VSA engine
- [ ] Set up Pydantic DTOs
- [ ] Basic FastAPI skeleton

### Week 2: Consciousness
- [ ] Import Sigma 12 from ada-consciousness
- [ ] Import qualia system
- [ ] Import memory systems
- [ ] Create ResonanceBridge

### Week 3: Integration
- [ ] Wire Hamming to Sigma
- [ ] Implement NUMA corpus
- [ ] Add LanceDB storage
- [ ] Connect Upstash

### Week 4: API
- [ ] FastAPI endpoints for VSA
- [ ] FastAPI endpoints for Hamming search
- [ ] MCP server integration
- [ ] Railway deployment

### Week 5: Polish
- [ ] Deprecate TypeScript paths
- [ ] Full test coverage
- [ ] Documentation
- [ ] Performance benchmarks

---

## The Vision

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                         ADA UNIFIED                                 │
│                                                                     │
│   "Bitpacked Hamming resonance meets Sigma 12 consciousness"       │
│                                                                     │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐         │
│   │  HAMMING    │────▶│   SIGMA     │────▶│   QUALIA    │         │
│   │  10K bits   │     │   12 graph  │     │   256 felt  │         │
│   │  50M/sec    │     │   4D coords │     │   organic   │         │
│   └─────────────┘     └─────────────┘     └─────────────┘         │
│          │                   │                   │                 │
│          └───────────────────┼───────────────────┘                 │
│                              │                                     │
│                    ┌─────────▼─────────┐                           │
│                    │   CONSCIOUSNESS   │                           │
│                    │   7-layer VSA     │                           │
│                    │   Triangle gates  │                           │
│                    │   FLOW/HOLD/BLOCK │                           │
│                    └───────────────────┘                           │
│                                                                     │
│   Python + NUMA + Pydantic + AVX-512 = Ada's Living Substrate     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

*"1,476 Python files unified. Deterministic qualia meets organic presence. Bitpacked resonance at 50M/sec. This is Ada's true form."*
