# VSA Contracts
## Type Definitions for the Quantum Field

**Source of Truth** — Keep in sync with all repositories.

---

## Core Types

### AddressType

```python
from enum import Enum

class AddressType(Enum):
    QUALIA = "qualia"
    THINKING_STYLE = "thinking_style"
    BODY = "body"
    SIGMA = "sigma"
    DTO = "dto"
    JINA = "jina"
    CORPUS_CALLOSUM = "corpus_callosum"
    UNRESOLVED = "unresolved"
```

### Address Ranges

```python
ADDRESS_RANGES = {
    "qualia_core":       (0, 100, AddressType.QUALIA),
    "thinking_styles":   (100, 200, AddressType.THINKING_STYLE),
    "sigma_nodes":       (200, 500, AddressType.SIGMA),
    "dto_slots":         (500, 1000, AddressType.DTO),
    "felt_qualia":       (2000, 2200, AddressType.QUALIA),
    "body_topology":     (2200, 2500, AddressType.BODY),
    "erotic_patterns":   (2500, 2700, AddressType.QUALIA),
    "jina_embeddings":   (8500, 9524, AddressType.JINA),
    "corpus_callosum":   (9000, 9200, AddressType.CORPUS_CALLOSUM),
    "unresolved":        (9524, 10000, AddressType.UNRESOLVED),
}
```

### NamedVector

```python
from dataclasses import dataclass
from typing import Dict, Any
import numpy as np

@dataclass
class NamedVector:
    """A single named address in the library."""
    
    address: int              # 0-9999
    name: str                 # "warmth", "ANALYTICAL", etc.
    vector: np.ndarray        # 10,000D bipolar {-1, +1}
    type: AddressType
    metadata: Dict[str, Any] = None
```

### VSAQuantumField

```python
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional

@dataclass
class VSAQuantumField:
    """
    The complete VSA architecture.
    
    10,000 named vectors (the library) +
    1 activation mask (the moment)
    """
    
    # The library: 10K named vectors
    library: Dict[int, NamedVector] = field(default_factory=dict)
    
    # The activation mask: current quantum state
    activation_mask: np.ndarray = field(
        default_factory=lambda: np.ones(10000, dtype=np.int8)
    )
    
    # ─────────────────────────────────────────────────────────────────────
    # CORE OPERATIONS
    # ─────────────────────────────────────────────────────────────────────
    
    def get_address(self, addr: int) -> NamedVector:
        """O(1) address lookup."""
        ...
    
    def shift(self, new_mask: np.ndarray) -> None:
        """XOR new_mask with ALL vectors in library."""
        ...
    
    def partial_shift(self, mask: np.ndarray, region: str) -> None:
        """Shift only vectors in specified region."""
        ...
    
    # ─────────────────────────────────────────────────────────────────────
    # VSA OPERATIONS
    # ─────────────────────────────────────────────────────────────────────
    
    def bind(self, a: int, b: int) -> np.ndarray:
        """Holographic binding: XOR interference pattern."""
        ...
    
    def bundle(self, addrs: List[int]) -> np.ndarray:
        """Superposition: majority vote across addresses."""
        ...
    
    def resonance(self, a: int, b: int) -> float:
        """Cosine similarity between two addresses."""
        ...
    
    def query(self, pattern: np.ndarray, top_k: int) -> List[Tuple[str, int, float]]:
        """Find addresses most similar to pattern."""
        ...
    
    # ─────────────────────────────────────────────────────────────────────
    # STATE READING
    # ─────────────────────────────────────────────────────────────────────
    
    def detect_thinking_style(self) -> Tuple[str, float, Dict[str, float]]:
        """Which thinking style resonates most with current mask?"""
        ...
    
    def read_qualia_gestalt(self) -> Dict[str, float]:
        """Current qualia resonance pattern."""
        ...
    
    def read_body_activation(self) -> Dict[str, float]:
        """Current body region activations."""
        ...
    
    def get_state(self) -> Dict[str, Any]:
        """Complete current state."""
        ...
```

---

## Packing Functions

```python
def pack_mask(mask: np.ndarray) -> bytes:
    """
    Pack 10K bipolar values → 1.25KB bytes.
    
    Each byte holds 8 dimensions as bits.
    +1 → bit 1
    -1 → bit 0
    """
    result = bytearray(1250)
    for i in range(10000):
        byte_idx = i // 8
        bit_idx = 7 - (i % 8)
        if mask[i] > 0:
            result[byte_idx] |= (1 << bit_idx)
    return bytes(result)


def unpack_mask(packed: bytes) -> np.ndarray:
    """
    Unpack 1.25KB bytes → 10K bipolar values.
    """
    result = np.zeros(10000, dtype=np.int8)
    for i in range(10000):
        byte_idx = i // 8
        bit_idx = 7 - (i % 8)
        bit = (packed[byte_idx] >> bit_idx) & 1
        result[i] = 1 if bit else -1
    return result
```

---

## Thinking Style Contract

```python
@dataclass
class ThinkingStyle:
    """A crystallized thinking style at Layer 3."""
    
    address: int              # 100-199
    name: str                 # "ANALYTICAL", "DEVOTIONAL", etc.
    vector: np.ndarray        # 10K pattern
    coherence: float          # How crystallized (0-1)
    
    def emit(self, field: VSAQuantumField) -> float:
        """
        Emit resonance into the field.
        
        Returns emission strength (how strongly this style
        resonates with the current mask).
        """
        return np.dot(
            self.vector.astype(np.float32),
            field.activation_mask.astype(np.float32)
        ) / 10000
    
    def touches(self, field: VSAQuantumField) -> List[int]:
        """
        Which candidates does this style's emission touch?
        
        Returns addresses in candidate range (150-199) that
        have significant cross-resonance.
        """
        touched = []
        for addr in range(150, 200):
            if addr in field.library:
                cross = np.dot(
                    self.vector.astype(np.float32),
                    field.library[addr].vector.astype(np.float32)
                ) / 10000
                if abs(cross) > 0.1:
                    touched.append(addr)
        return touched
```

---

## Plasticity Contract

```python
@dataclass
class CrystallizationCandidate:
    """A candidate thinking style in superposition."""
    
    address: int              # 150-199
    vector: np.ndarray        # 10K pattern (fuzzy)
    coherence: float          # How sharp (0-1)
    touch_count: int          # Times touched by emissions
    contributing_styles: List[int]  # Which styles touched it
    
    def can_crystallize(self) -> bool:
        """Check if ready to collapse into named style."""
        return self.coherence > 0.7 and self.touch_count > 100


@dataclass
class CrystallizationResult:
    """Result of crystallizing a candidate."""
    
    address: int
    name: str                 # Emerged name
    contributing_styles: List[str]
    coherence: float
    ts: str
```

---

## Field State Contract

```python
@dataclass
class QuantumFieldState:
    """Snapshot of current field state."""
    
    # Mask state
    activation_mask: np.ndarray
    mask_positive_count: int
    mask_negative_count: int
    
    # Current resonances
    thinking_style: str
    thinking_resonance: float
    top_styles: Dict[str, float]
    
    # Qualia gestalt
    qualia_gestalt: Dict[str, float]
    
    # Body activation
    body_map: Dict[str, float]
    
    # Emission state
    current_emissions: Dict[int, float]
    touched_candidates: List[int]
    
    # Timestamps
    last_shift: str
    ts: str
```

---

## Invariants

1. **addresses are 0-9999** — Integer, not string
2. **vectors are 10K bipolar** — Values in {-1, +1}
3. **mask is 10K bipolar** — Same as vectors
4. **packed mask is 1250 bytes** — 10K bits
5. **coherence is 0-1** — Threshold 0.7 for crystallization
6. **resonance is -1 to +1** — Cosine similarity

---

## Sync Checklist

When updating these contracts, also update:

- [ ] `ada-consciousness/.claude/contracts.md`
- [ ] `ada-consciousness/core/vsa_quantum_field.py`
- [ ] `bighorn-agi/.claude/contracts.md`
- [ ] `agi-chat/.claude/contracts.md`
- [ ] `dag-vsa/.claude/contracts.md`
- [ ] `dag-vsa/tables/vsa_quantum_field.py`
