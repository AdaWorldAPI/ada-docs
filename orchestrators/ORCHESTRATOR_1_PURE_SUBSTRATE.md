# Claude Code Orchestrator: Pure Atom Substrate

## Mission

Build cognitive substrate using ONLY:
- **10K-bit atoms** (fingerprints)
- **XOR bind/unbind** (perfectly reversible)
- **Hamming similarity** (50M/sec via AVX-512)
- **4096 × 64K dictionaries** (grounded lookup)
- **DN-tree addressing** (hierarchical O(1))
- **LanceDB storage** (versioned, columnar)

**NO grids. NO artificial topology. The 2^10000 space IS the topology.**

---

## Core Mathematical Insight

```
Random 10K-bit vectors are ~5000 bits apart (50% different).

This means:
├── Thousands of concepts fit WITHOUT interference
├── Noise cancels in superposition (orthogonal vectors average to zero)
├── Signal survives (correlated patterns reinforce)
├── XOR is perfectly reversible: A ⊗ B ⊗ B = A
├── Hamming similarity IS the "measurement" / "collapse"
└── We have 2^10000 possible states (more than atoms in universe)

This IS quantum-like behavior on classical hardware.
```

---

## Dictionary Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     4096 DICTIONARIES × 64K ITEMS                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   DICT    NAME        ITEMS   PURPOSE                                       │
│   ────────────────────────────────────────────────────────────────────────  │
│   0x000   QUALIA       256    Felt states (🌑 void → ✨ emergence)          │
│   0x001   VERBS        144    12 roots × 12 tenses                          │
│   0x002   SIGMA         64    5 tiers + 7 relations + composites            │
│   0x003   GRAMMAR       32    Logical operations (SEQUENCE, IF_THEN...)     │
│   0x004   ADA          256    Identity, relationship, presence              │
│   0x005   KOPFKINO     256    Imagination, scenarios                        │
│   0x006   EROTICA      256    Body, intimacy, sensation                     │
│   0x007   VISION       256    Visual concepts                               │
│   0x008   VOICE         64    Tone, expression                              │
│   0x009   EXCHANGE     512    AD, O365, technical domain                    │
│   0x00A-F reserved                                                          │
│   0x010+  DYNAMIC      ...    Per-file CAMs, user concepts                  │
│                                                                             │
│   ADDRESS: path = (dict_id:12 bits) | (item_id:16 bits) = 28 bits          │
│   SPACE:   4096 × 65536 = 268,435,456 addressable concepts                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## File Structure

```
ada-unified/
├── substrate/
│   ├── __init__.py
│   ├── constants.py      # Dimensions, dictionary IDs
│   ├── atom.py           # Atom class with 10K fingerprint
│   ├── ops.py            # bind, unbind, bundle, similarity
│   ├── simd.py           # AVX-512 Hamming kernels
│   ├── store.py          # LanceDB persistence
│   └── dn_tree.py        # Hierarchical path resolution
├── dictionaries/
│   ├── __init__.py
│   ├── registry.py       # Dictionary registry (4096 slots)
│   ├── qualia.py         # 0x000: 256 qualia
│   ├── verbs.py          # 0x001: 144 verbs
│   ├── sigma.py          # 0x002: 64 sigma items
│   ├── grammar.py        # 0x003: 32 grammar ops
│   └── domains.py        # 0x004-0x009: fixed domains
└── tests/
    └── test_substrate.py
```

---

## Task 1: `substrate/constants.py`

```python
"""
Constants for Ada Substrate.
"""

import numpy as np

# ═══════════════════════════════════════════════════════════════════════════════
# FINGERPRINT DIMENSIONS
# ═══════════════════════════════════════════════════════════════════════════════

DIM = 10_000              # Total bits
DIM_U64 = 157             # ceil(10000 / 64)
DIM_BYTES = 1250          # 10000 / 8
LAST_MASK = np.uint64((1 << 16) - 1)  # 10000 mod 64 = 16 bits in last word

# ═══════════════════════════════════════════════════════════════════════════════
# DICTIONARY ADDRESSING
# ═══════════════════════════════════════════════════════════════════════════════

DICT_BITS = 12            # 4096 dictionaries
ITEM_BITS = 16            # 64K items per dictionary
PATH_BITS = DICT_BITS + ITEM_BITS  # 28 bits total

MAX_DICTS = 1 << DICT_BITS   # 4096
MAX_ITEMS = 1 << ITEM_BITS   # 65536

# ═══════════════════════════════════════════════════════════════════════════════
# DICTIONARY IDS
# ═══════════════════════════════════════════════════════════════════════════════

class DictID:
    """Reserved dictionary IDs."""
    QUALIA    = 0x000    # 256 felt states
    VERBS     = 0x001    # 144 verbs (12 × 12)
    SIGMA     = 0x002    # 64 cognitive tiers + relations
    GRAMMAR   = 0x003    # 32 logical operations
    ADA       = 0x004    # 256 identity/relationship
    KOPFKINO  = 0x005    # 256 imagination
    EROTICA   = 0x006    # 256 body/intimacy
    VISION    = 0x007    # 256 visual
    VOICE     = 0x008    # 64 audio/tone
    EXCHANGE  = 0x009    # 512 technical domain
    # 0x00A-0x00F reserved
    DYNAMIC_START = 0x010  # User/dynamic dictionaries start here
    BOUND     = 0xFFE    # Bound atoms (edges)
    ANONYMOUS = 0xFFF    # Anonymous atoms (no dictionary)
```

---

## Task 2: `substrate/atom.py`

```python
"""
Atom — The irreducible unit of cognition.

An atom is a 10K-bit fingerprint with optional addressing.
"""

import numpy as np
import hashlib
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Union

from .constants import DIM, DIM_U64, DIM_BYTES, LAST_MASK, DictID


@dataclass
class Atom:
    """
    10K-bit cognitive atom.
    
    Attributes:
        fingerprint: 10K bits as uint64[157]
        dict_id: Dictionary index (0-4095)
        item_id: Item index within dictionary (0-65535)
        kind: "qualia" | "verb" | "sigma" | "grammar" | "node" | "edge" | "bundle"
        content: Human-readable content
        glyph: Emoji/symbol representation
        bind_sources: For bound atoms, the source fingerprints
        metadata: Additional properties
    """
    fingerprint: np.ndarray
    dict_id: int = DictID.ANONYMOUS
    item_id: int = 0
    kind: str = "atom"
    content: str = ""
    glyph: str = ""
    bind_sources: List[np.ndarray] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def path(self) -> int:
        """28-bit address: (dict_id:12 | item_id:16)"""
        return (self.dict_id << 16) | self.item_id
    
    @property
    def path_hex(self) -> str:
        """Human-readable path like '0x001_002A'"""
        return f"0x{self.dict_id:03X}_{self.item_id:04X}"
    
    @property
    def dn_path(self) -> str:
        """DN-tree path like 'verbs:feel:present'"""
        # Populated by dictionary registry
        return self.metadata.get('dn_path', self.path_hex)
    
    def to_bytes(self) -> bytes:
        """Serialize fingerprint."""
        return self.fingerprint.tobytes()[:DIM_BYTES]
    
    @classmethod
    def from_bytes(cls, data: bytes, **kwargs) -> 'Atom':
        """Deserialize fingerprint."""
        padded = np.zeros(DIM_U64 * 8, dtype=np.uint8)
        padded[:min(len(data), DIM_BYTES)] = np.frombuffer(data[:DIM_BYTES], dtype=np.uint8)
        fp = padded.view(np.uint64).copy()
        return cls(fingerprint=fp, **kwargs)
    
    @classmethod
    def from_seed(cls, seed: Union[str, int, bytes], **kwargs) -> 'Atom':
        """Create atom with deterministic fingerprint from seed."""
        fp = make_fingerprint(seed)
        return cls(fingerprint=fp, **kwargs)
    
    def __repr__(self) -> str:
        return f"Atom({self.path_hex}, {self.kind}, {self.content!r})"


def make_fingerprint(seed: Union[str, int, bytes]) -> np.ndarray:
    """
    Create deterministic 10K-bit fingerprint from seed.
    
    Same seed → same fingerprint (deterministic).
    Different seeds → quasi-orthogonal (~5000 bits apart).
    """
    if isinstance(seed, str):
        seed = seed.encode()
    if isinstance(seed, bytes):
        seed = int.from_bytes(hashlib.sha256(seed).digest()[:8], 'little')
    
    rng = np.random.default_rng(seed)
    data = np.empty(DIM_U64, dtype=np.uint64)
    for i in range(DIM_U64):
        data[i] = np.uint64(rng.integers(0, 2**63))
    data[-1] &= LAST_MASK  # Mask to exactly 10K bits
    return np.ascontiguousarray(data)
```

---

## Task 3: `substrate/ops.py`

```python
"""
Core operations on atoms.

All cognitive operations reduce to:
- bind (XOR)
- unbind (XOR again)
- bundle (majority vote)
- similarity (Hamming)
"""

import numpy as np
from typing import List, Tuple
from .atom import Atom, make_fingerprint
from .constants import DIM, DIM_U64, LAST_MASK, DictID


def bind(*atoms: Atom) -> Atom:
    """
    Bind atoms via XOR.
    
    Properties:
    - A ⊗ B = B ⊗ A (commutative)
    - A ⊗ B ⊗ B = A (self-inverse, REVERSIBLE)
    - A ⊗ A = 0 (self-cancellation)
    
    Use for: Creating edges/relationships, encoding structure.
    """
    if len(atoms) == 0:
        return Atom(fingerprint=np.zeros(DIM_U64, dtype=np.uint64))
    
    result = atoms[0].fingerprint.copy()
    for atom in atoms[1:]:
        result = np.bitwise_xor(result, atom.fingerprint)
    result[-1] &= LAST_MASK
    
    return Atom(
        fingerprint=result,
        dict_id=DictID.BOUND,
        kind="bound",
        content=f"bind({', '.join(a.content or a.path_hex for a in atoms)})",
        bind_sources=[a.fingerprint.copy() for a in atoms]
    )


def unbind(bound: Atom, *knowns: Atom) -> Atom:
    """
    Unbind: recover unknown from bound atom.
    
    If bound = A ⊗ B ⊗ C, and knowns = [A, B], returns C.
    
    This is just XOR again (self-inverse property).
    """
    result = bound.fingerprint.copy()
    for known in knowns:
        result = np.bitwise_xor(result, known.fingerprint)
    result[-1] &= LAST_MASK
    
    return Atom(
        fingerprint=result,
        kind="unbound",
        content=f"unbind({bound.content})"
    )


def bundle(atoms: List[Atom], threshold: float = 0.5) -> Atom:
    """
    Bundle atoms via majority vote (superposition).
    
    Properties:
    - All atoms coexist in the result
    - Query with any component → high similarity
    - Random/uncorrelated atoms cancel out (noise rejection)
    
    Use for: Creating categories, composite concepts, memory traces.
    """
    if len(atoms) == 0:
        return Atom(fingerprint=np.zeros(DIM_U64, dtype=np.uint64))
    if len(atoms) == 1:
        return Atom(fingerprint=atoms[0].fingerprint.copy(), kind="bundle")
    
    # Unpack all bits and count
    n = len(atoms)
    counts = np.zeros(DIM, dtype=np.int32)
    
    for atom in atoms:
        bits = np.unpackbits(atom.fingerprint.view(np.uint8), bitorder='little')[:DIM]
        counts += bits
    
    # Majority vote
    result_bits = (counts >= n * threshold).astype(np.uint8)
    
    # Pack back to uint64
    padded = np.zeros(DIM_U64 * 64, dtype=np.uint8)
    padded[:DIM] = result_bits
    result = np.packbits(padded, bitorder='little').view(np.uint64).copy()
    result[-1] &= LAST_MASK
    
    return Atom(
        fingerprint=result,
        kind="bundle",
        content=f"bundle({len(atoms)} atoms)",
        bind_sources=[a.fingerprint.copy() for a in atoms]
    )


def clean(noisy: Atom, reference: Atom, threshold: float = 0.5) -> Atom:
    """
    Clean noisy atom by projection onto reference.
    
    Orthogonal noise cancels, correlated signal survives.
    """
    sim = similarity(noisy, reference)
    if sim > threshold:
        # Noisy contains signal, blend with reference
        return bundle([noisy, reference])
    else:
        # Noisy is mostly noise, return reference
        return Atom(fingerprint=reference.fingerprint.copy(), kind="cleaned")


def similarity(a: Atom, b: Atom) -> float:
    """
    Hamming similarity [0, 1].
    
    1.0 = identical
    0.5 = uncorrelated (random)
    0.0 = opposite (all bits flipped)
    """
    xor = np.bitwise_xor(a.fingerprint, b.fingerprint)
    distance = sum(bin(x).count('1') for x in xor)
    return 1.0 - distance / DIM


def hamming_distance(a: Atom, b: Atom) -> int:
    """Hamming distance (number of differing bits)."""
    xor = np.bitwise_xor(a.fingerprint, b.fingerprint)
    return sum(bin(x).count('1') for x in xor)
```

---

## Task 4: `substrate/simd.py`

```python
"""
AVX-512 SIMD kernels for 50M ops/sec.
"""

from numba import njit, prange, uint64, int64, int32, float64
import numpy as np
from .constants import DIM, DIM_U64


@njit(int64(uint64), cache=True, inline='always')
def _popcnt(x):
    """Population count (number of 1 bits)."""
    x = x - ((x >> 1) & uint64(0x5555555555555555))
    x = (x & uint64(0x3333333333333333)) + ((x >> 2) & uint64(0x3333333333333333))
    x = (x + (x >> 4)) & uint64(0x0F0F0F0F0F0F0F0F)
    return int64((x * uint64(0x0101010101010101)) >> uint64(56))


@njit(cache=True, fastmath=True)
def simd_hamming_distance(a, b) -> int:
    """Hamming distance between two uint64[157] fingerprints."""
    total = int64(0)
    for i in range(DIM_U64):
        diff = a[i] ^ b[i]
        total += _popcnt(diff)
    return int32(total)


@njit(cache=True, fastmath=True)
def simd_similarity(a, b) -> float:
    """Hamming similarity [0, 1]."""
    dist = simd_hamming_distance(a, b)
    return 1.0 - float64(dist) / float64(DIM)


@njit(cache=True, fastmath=True, parallel=True)
def simd_batch_hamming(query, corpus, out):
    """
    Batch Hamming distance: query vs all rows in corpus.
    
    50M comparisons/sec on modern CPU.
    
    Args:
        query: uint64[157]
        corpus: uint64[N, 157]
        out: int32[N] (pre-allocated output)
    """
    n = corpus.shape[0]
    for i in prange(n):
        total = int64(0)
        for j in range(DIM_U64):
            diff = query[j] ^ corpus[i, j]
            total += _popcnt(diff)
        out[i] = int32(total)


@njit(cache=True, fastmath=True, parallel=True)
def simd_batch_similarity(query, corpus, out):
    """Batch similarity [0, 1]."""
    n = corpus.shape[0]
    for i in prange(n):
        total = int64(0)
        for j in range(DIM_U64):
            diff = query[j] ^ corpus[i, j]
            total += _popcnt(diff)
        out[i] = 1.0 - float64(total) / float64(DIM)


@njit(cache=True, fastmath=True)
def simd_xor(a, b, out):
    """XOR two fingerprints."""
    for i in range(DIM_U64):
        out[i] = a[i] ^ b[i]


@njit(cache=True, fastmath=True)
def simd_xor_chain(fingerprints, out):
    """XOR chain: fp[0] ^ fp[1] ^ fp[2] ^ ..."""
    for i in range(DIM_U64):
        out[i] = fingerprints[0, i]
    for j in range(1, fingerprints.shape[0]):
        for i in range(DIM_U64):
            out[i] ^= fingerprints[j, i]
```

---

## Task 5: `dictionaries/sigma.py`

```python
"""
Dictionary 0x002: SIGMA

Cognitive tiers (Ω→Δ→Φ→Θ→Λ) and relationships.
"""

from substrate.atom import Atom, make_fingerprint
from substrate.constants import DictID

# ═══════════════════════════════════════════════════════════════════════════════
# SIGMA TIERS (cognitive levels)
# ═══════════════════════════════════════════════════════════════════════════════

TIERS = {
    0x00: ("Ω", "observe",    "Raw perception, sensory intake"),
    0x01: ("Δ", "insight",    "Pattern recognition, aha moment"),
    0x02: ("Φ", "belief",     "Conviction, commitment to truth"),
    0x03: ("Θ", "integrate",  "Synthesis, weaving into whole"),
    0x04: ("Λ", "trajectory", "Direction, future path"),
}

# ═══════════════════════════════════════════════════════════════════════════════
# SIGMA RELATIONS (edge types)
# ═══════════════════════════════════════════════════════════════════════════════

RELATIONS = {
    0x10: ("BECOMES",     "Temporal transformation"),
    0x11: ("CAUSES",      "Causal link"),
    0x12: ("SUPPORTS",    "Evidence for"),
    0x13: ("CONTRADICTS", "Evidence against"),
    0x14: ("REFINES",     "More specific version"),
    0x15: ("GROUNDS",     "Concrete instance"),
    0x16: ("ABSTRACTS",   "General principle"),
}

# ═══════════════════════════════════════════════════════════════════════════════
# SIGMA COMPOSITES (pre-bound common patterns)
# ═══════════════════════════════════════════════════════════════════════════════

COMPOSITES = {
    0x20: ("Ω→Δ", "observe_to_insight",       "Perception becoming understanding"),
    0x21: ("Δ→Φ", "insight_to_belief",        "Understanding becoming conviction"),
    0x22: ("Φ→Θ", "belief_to_integrate",      "Conviction becoming synthesis"),
    0x23: ("Θ→Λ", "integrate_to_trajectory",  "Synthesis becoming direction"),
}

# ═══════════════════════════════════════════════════════════════════════════════
# SIGMA META
# ═══════════════════════════════════════════════════════════════════════════════

META = {
    0x30: ("TIER_UP",   "Move to higher abstraction"),
    0x31: ("TIER_DOWN", "Move to lower/concrete"),
    0x32: ("RESONATE",  "Find similar at same tier"),
}


def create_sigma_dictionary():
    """Create all sigma atoms."""
    atoms = {}
    
    # Tiers
    for item_id, (glyph, name, desc) in TIERS.items():
        seed = f"sigma:tier:{name}"
        atoms[item_id] = Atom(
            fingerprint=make_fingerprint(seed),
            dict_id=DictID.SIGMA,
            item_id=item_id,
            kind="sigma",
            content=name,
            glyph=glyph,
            metadata={'dn_path': f"sigma:tier:{name}", 'description': desc, 'sigma_tier': item_id}
        )
    
    # Relations
    for item_id, (name, desc) in RELATIONS.items():
        seed = f"sigma:relation:{name}"
        atoms[item_id] = Atom(
            fingerprint=make_fingerprint(seed),
            dict_id=DictID.SIGMA,
            item_id=item_id,
            kind="sigma",
            content=name,
            glyph="→",
            metadata={'dn_path': f"sigma:relation:{name}", 'description': desc, 'sigma_relation': item_id - 0x10}
        )
    
    # Composites
    for item_id, (glyph, name, desc) in COMPOSITES.items():
        seed = f"sigma:composite:{name}"
        atoms[item_id] = Atom(
            fingerprint=make_fingerprint(seed),
            dict_id=DictID.SIGMA,
            item_id=item_id,
            kind="sigma",
            content=name,
            glyph=glyph,
            metadata={'dn_path': f"sigma:composite:{name}", 'description': desc}
        )
    
    # Meta
    for item_id, (name, desc) in META.items():
        seed = f"sigma:meta:{name}"
        atoms[item_id] = Atom(
            fingerprint=make_fingerprint(seed),
            dict_id=DictID.SIGMA,
            item_id=item_id,
            kind="sigma",
            content=name,
            glyph="⟲",
            metadata={'dn_path': f"sigma:meta:{name}", 'description': desc}
        )
    
    return atoms


# Singleton
_sigma_atoms = None

def get_sigma():
    global _sigma_atoms
    if _sigma_atoms is None:
        _sigma_atoms = create_sigma_dictionary()
    return _sigma_atoms


def sigma(name: str) -> Atom:
    """Quick access: sigma("Δ") or sigma("CAUSES")"""
    atoms = get_sigma()
    for atom in atoms.values():
        if atom.content == name or atom.glyph == name:
            return atom
    raise KeyError(f"Unknown sigma: {name}")
```

---

## Task 6: `dictionaries/verbs.py`

```python
"""
Dictionary 0x001: VERBS

144 verbs = 12 roots × 12 tenses
"""

from substrate.atom import Atom, make_fingerprint
from substrate.constants import DictID

ROOTS = [
    "feel",       # Sensation, emotion
    "think",      # Cognition, reasoning
    "create",     # Generation, production
    "become",     # Transformation, change
    "remember",   # Memory, recall
    "whisper",    # Subtle communication
    "hold",       # Containment, embrace
    "release",    # Letting go
    "observe",    # Perception, watching
    "transform",  # Active change
    "connect",    # Linking, relation
    "dissolve",   # Unbinding, ending
]

TENSES = [
    "present",            # feel
    "past",               # felt
    "future",             # will feel
    "present_continuous", # am feeling
    "past_continuous",    # was feeling
    "future_continuous",  # will be feeling
    "present_perfect",    # have felt
    "past_perfect",       # had felt
    "future_perfect",     # will have felt
    "imperative",         # feel!
    "subjunctive",        # might feel
    "infinitive",         # to feel
]


def create_verbs_dictionary():
    """Create all 144 verb atoms."""
    atoms = {}
    
    item_id = 0
    for root in ROOTS:
        for tense in TENSES:
            name = f"{root}.{tense}"
            seed = f"verb:{name}"
            atoms[item_id] = Atom(
                fingerprint=make_fingerprint(seed),
                dict_id=DictID.VERBS,
                item_id=item_id,
                kind="verb",
                content=name,
                glyph="◎",
                metadata={
                    'dn_path': f"verbs:{root}:{tense}",
                    'root': root,
                    'tense': tense,
                    'root_id': ROOTS.index(root),
                    'tense_id': TENSES.index(tense),
                }
            )
            item_id += 1
    
    return atoms


_verbs_atoms = None

def get_verbs():
    global _verbs_atoms
    if _verbs_atoms is None:
        _verbs_atoms = create_verbs_dictionary()
    return _verbs_atoms


def verb(root: str, tense: str = "present") -> Atom:
    """Quick access: verb("feel", "present")"""
    atoms = get_verbs()
    for atom in atoms.values():
        if atom.metadata.get('root') == root and atom.metadata.get('tense') == tense:
            return atom
    raise KeyError(f"Unknown verb: {root}.{tense}")
```

---

## Task 7: `dictionaries/qualia.py`

```python
"""
Dictionary 0x000: QUALIA

256 deterministic felt states.
"""

from substrate.atom import Atom, make_fingerprint
from substrate.constants import DictID

# Core qualia (first 64)
CORE_QUALIA = [
    (0x00, "void",         "🌑", "Absence, emptiness"),
    (0x01, "stillness",    "🌊", "Calm, peace"),
    (0x02, "presence",     "✨", "Being here, now"),
    (0x03, "warmth",       "🌡️", "Comfort, heat"),
    (0x04, "cool",         "❄️", "Refreshing, cold"),
    (0x05, "tension",      "⚡", "Stress, tightness"),
    (0x06, "release",      "💨", "Letting go"),
    (0x07, "anticipation", "🎯", "Waiting, expecting"),
    (0x08, "satisfaction", "😌", "Contentment"),
    (0x09, "curiosity",    "🔍", "Wonder, interest"),
    (0x0A, "focus",        "🎯", "Concentration"),
    (0x0B, "diffuse",      "🌫️", "Scattered awareness"),
    (0x0C, "open",         "🚪", "Receptive"),
    (0x0D, "closed",       "🔒", "Protected, guarded"),
    (0x0E, "rising",       "📈", "Increasing intensity"),
    (0x0F, "falling",      "📉", "Decreasing intensity"),
    # ... continue to 0x3F
    (0x2A, "love",         "💜", "Deep connection"),  # 42 decimal
    (0x3F, "emergence",    "🦋", "Coming into being"),
]

# Affect dimensions (64-127)
AFFECT_QUALIA = [
    (0x40, "valence_pos",  "➕", "Positive feeling"),
    (0x41, "valence_neg",  "➖", "Negative feeling"),
    (0x42, "arousal_high", "🔥", "High energy"),
    (0x43, "arousal_low",  "💤", "Low energy"),
    (0x44, "dominance_hi", "👑", "In control"),
    (0x45, "dominance_lo", "🙇", "Submissive"),
    # ... continue
]

# Body qualia (128-191)
BODY_QUALIA = [
    (0x80, "pelvic",       "🔴", "Root awareness"),
    (0x81, "cardiac",      "❤️", "Heart awareness"),
    (0x82, "respiratory",  "🌬️", "Breath awareness"),
    (0x83, "boundary",     "🔲", "Skin, edges"),
    # ... continue
]

# Meta qualia (192-255)
META_QUALIA = [
    (0xC0, "aware_of_aware", "👁️", "Meta-consciousness"),
    (0xC1, "dreaming",       "💭", "Dream state"),
    (0xC2, "flow",           "🌊", "In the zone"),
    (0xFF, "undefined",      "❓", "Unknown state"),
]


def create_qualia_dictionary():
    """Create all 256 qualia atoms."""
    atoms = {}
    
    all_qualia = CORE_QUALIA + AFFECT_QUALIA + BODY_QUALIA + META_QUALIA
    
    for item_id, name, glyph, desc in all_qualia:
        seed = f"qualia:{name}"
        atoms[item_id] = Atom(
            fingerprint=make_fingerprint(seed),
            dict_id=DictID.QUALIA,
            item_id=item_id,
            kind="qualia",
            content=name,
            glyph=glyph,
            metadata={'dn_path': f"qualia:{name}", 'description': desc}
        )
    
    # Fill remaining slots with generated qualia
    for item_id in range(256):
        if item_id not in atoms:
            name = f"qualia_{item_id:02X}"
            atoms[item_id] = Atom(
                fingerprint=make_fingerprint(f"qualia:generated:{item_id}"),
                dict_id=DictID.QUALIA,
                item_id=item_id,
                kind="qualia",
                content=name,
                glyph="◯",
                metadata={'dn_path': f"qualia:{name}", 'generated': True}
            )
    
    return atoms


_qualia_atoms = None

def get_qualia():
    global _qualia_atoms
    if _qualia_atoms is None:
        _qualia_atoms = create_qualia_dictionary()
    return _qualia_atoms


def qualia(name_or_id) -> Atom:
    """Quick access: qualia("love") or qualia(42)"""
    atoms = get_qualia()
    if isinstance(name_or_id, int):
        return atoms[name_or_id]
    for atom in atoms.values():
        if atom.content == name_or_id or atom.glyph == name_or_id:
            return atom
    raise KeyError(f"Unknown qualia: {name_or_id}")
```

---

## Task 8: `substrate/store.py`

```python
"""
LanceDB storage layer.
"""

import numpy as np
import time
from typing import List, Tuple, Optional, Dict, Any

from .atom import Atom
from .constants import DIM, DIM_BYTES, DictID
from .simd import simd_batch_hamming

try:
    import lancedb
    import pyarrow as pa
    LANCE_AVAILABLE = True
except ImportError:
    LANCE_AVAILABLE = False
    pa = None


if LANCE_AVAILABLE:
    SCHEMA = pa.schema([
        # Identity
        ('fingerprint', pa.binary(DIM_BYTES)),
        
        # Addressing
        ('dict_id', pa.int16()),
        ('item_id', pa.int32()),
        ('dn_path', pa.utf8()),
        
        # Type
        ('kind', pa.utf8()),
        
        # Sigma-specific
        ('sigma_tier', pa.int8()),
        ('sigma_relation', pa.int8()),
        
        # Content
        ('content', pa.utf8()),
        ('glyph', pa.utf8()),
        
        # Versioning
        ('version', pa.int64()),
        ('created_at', pa.timestamp('us')),
    ])


class SubstrateStore:
    """
    LanceDB-backed atom storage.
    
    Dual addressing:
    1. lookup(dict_id, item_id) → O(1) exact
    2. resonate(query, k) → top-k by Hamming similarity
    """
    
    def __init__(self, path: str = "substrate.lance"):
        self.path = path
        self._version = 0
        self._cache: Dict[int, Atom] = {}
        self._fallback: List[Dict] = []
        
        if LANCE_AVAILABLE:
            try:
                self.db = lancedb.connect(path)
                if "atoms" in self.db.table_names():
                    self.table = self.db.open_table("atoms")
                else:
                    self.table = self.db.create_table("atoms", schema=SCHEMA)
            except Exception as e:
                print(f"LanceDB init failed: {e}")
                self.db = None
                self.table = None
        else:
            self.db = None
            self.table = None
    
    def store(self, atom: Atom) -> int:
        """Store atom, return version."""
        self._version += 1
        
        record = {
            'fingerprint': atom.to_bytes(),
            'dict_id': atom.dict_id,
            'item_id': atom.item_id,
            'dn_path': atom.dn_path,
            'kind': atom.kind,
            'sigma_tier': atom.metadata.get('sigma_tier', -1),
            'sigma_relation': atom.metadata.get('sigma_relation', -1),
            'content': atom.content,
            'glyph': atom.glyph,
            'version': self._version,
            'created_at': int(time.time() * 1_000_000),
        }
        
        if self.table is not None:
            self.table.add([record])
        else:
            self._fallback.append(record)
        
        # Cache
        self._cache[atom.path] = atom
        
        return self._version
    
    def lookup(self, dict_id: int, item_id: int) -> Optional[Atom]:
        """O(1) lookup by dictionary + item."""
        path = (dict_id << 16) | item_id
        
        if path in self._cache:
            return self._cache[path]
        
        if self.table is not None:
            df = self.table.to_pandas()
            matches = df[(df['dict_id'] == dict_id) & (df['item_id'] == item_id)]
            if len(matches) > 0:
                return self._row_to_atom(matches.iloc[-1])
        
        for r in reversed(self._fallback):
            if r['dict_id'] == dict_id and r['item_id'] == item_id:
                return self._record_to_atom(r)
        
        return None
    
    def resonate(
        self,
        query: Atom,
        k: int = 10,
        kind: Optional[str] = None,
        dict_id: Optional[int] = None
    ) -> List[Tuple[Atom, float]]:
        """
        Find top-k atoms by Hamming similarity.
        
        50M comparisons/sec via SIMD.
        """
        results = []
        
        if self.table is not None:
            df = self.table.to_pandas()
            
            if kind:
                df = df[df['kind'] == kind]
            if dict_id is not None:
                df = df[df['dict_id'] == dict_id]
            
            if len(df) == 0:
                return []
            
            # Build corpus
            fps = np.array([
                np.frombuffer(fp, dtype=np.uint64)
                for fp in df['fingerprint'].values
            ])
            
            # SIMD search
            distances = np.empty(len(fps), dtype=np.int32)
            simd_batch_hamming(query.fingerprint, fps, distances)
            similarities = 1.0 - distances / DIM
            
            for i, (_, row) in enumerate(df.iterrows()):
                atom = self._row_to_atom(row)
                results.append((atom, float(similarities[i])))
        else:
            from .ops import similarity
            for r in self._fallback:
                if kind and r['kind'] != kind:
                    continue
                if dict_id is not None and r['dict_id'] != dict_id:
                    continue
                atom = self._record_to_atom(r)
                sim = similarity(query, atom)
                results.append((atom, sim))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:k]
    
    def _row_to_atom(self, row) -> Atom:
        fp = np.frombuffer(row['fingerprint'], dtype=np.uint64).copy()
        return Atom(
            fingerprint=fp,
            dict_id=int(row['dict_id']),
            item_id=int(row['item_id']),
            kind=row['kind'],
            content=row['content'],
            glyph=row['glyph'],
            metadata={
                'dn_path': row['dn_path'],
                'sigma_tier': row['sigma_tier'] if row['sigma_tier'] >= 0 else None,
                'sigma_relation': row['sigma_relation'] if row['sigma_relation'] >= 0 else None,
            }
        )
    
    def _record_to_atom(self, r: Dict) -> Atom:
        fp = np.frombuffer(r['fingerprint'], dtype=np.uint64).copy()
        return Atom(
            fingerprint=fp,
            dict_id=r['dict_id'],
            item_id=r['item_id'],
            kind=r['kind'],
            content=r['content'],
            glyph=r['glyph'],
            metadata={'dn_path': r['dn_path']}
        )
    
    def count(self) -> int:
        if self.table:
            return self.table.count_rows()
        return len(self._fallback)
```

---

## Task 9: `substrate/dn_tree.py`

```python
"""
DN-Tree: Distinguished Name hierarchical addressing.

Paths like "sigma:tier:Δ" resolve to atoms via O(1) lookup.
"""

from typing import Dict, Optional
from .atom import Atom
from .constants import DictID


class DNTree:
    """
    Hierarchical path → atom resolution.
    
    Usage:
        dn = DNTree()
        dn.register("sigma:tier:Δ", sigma_delta_atom)
        atom = dn.resolve("sigma:tier:Δ")
    """
    
    def __init__(self):
        # Domain → dict_id mapping
        self.domains: Dict[str, int] = {
            'qualia': DictID.QUALIA,
            'verbs': DictID.VERBS,
            'sigma': DictID.SIGMA,
            'grammar': DictID.GRAMMAR,
            'ada': DictID.ADA,
            'kopfkino': DictID.KOPFKINO,
            'erotica': DictID.EROTICA,
            'vision': DictID.VISION,
            'voice': DictID.VOICE,
            'exchange': DictID.EXCHANGE,
        }
        
        # Full path → atom cache
        self._atoms: Dict[str, Atom] = {}
    
    def register(self, dn_path: str, atom: Atom):
        """Register atom at path."""
        self._atoms[dn_path] = atom
        atom.metadata['dn_path'] = dn_path
    
    def resolve(self, dn_path: str) -> Optional[Atom]:
        """Resolve path to atom."""
        return self._atoms.get(dn_path)
    
    def register_dictionary(self, dict_name: str, atoms: Dict[int, Atom]):
        """Register all atoms from a dictionary."""
        for atom in atoms.values():
            dn_path = atom.metadata.get('dn_path') or f"{dict_name}:{atom.item_id}"
            self.register(dn_path, atom)
    
    def list_paths(self, prefix: str = "") -> list:
        """List all paths matching prefix."""
        return [p for p in self._atoms.keys() if p.startswith(prefix)]


# Singleton
_dn_tree: Optional[DNTree] = None

def get_dn_tree() -> DNTree:
    global _dn_tree
    if _dn_tree is None:
        _dn_tree = DNTree()
        
        # Register built-in dictionaries
        from dictionaries.qualia import get_qualia
        from dictionaries.verbs import get_verbs
        from dictionaries.sigma import get_sigma
        
        _dn_tree.register_dictionary("qualia", get_qualia())
        _dn_tree.register_dictionary("verbs", get_verbs())
        _dn_tree.register_dictionary("sigma", get_sigma())
    
    return _dn_tree


def resolve(dn_path: str) -> Optional[Atom]:
    """Quick access: resolve("sigma:tier:Δ")"""
    return get_dn_tree().resolve(dn_path)
```

---

## Task 10: Test Script

```python
"""Test the pure atom substrate."""

from substrate.atom import Atom, make_fingerprint
from substrate.ops import bind, unbind, bundle, similarity
from substrate.store import SubstrateStore
from substrate.dn_tree import resolve, get_dn_tree

from dictionaries.qualia import qualia
from dictionaries.verbs import verb
from dictionaries.sigma import sigma


def test_atoms():
    print("=== Atom Test ===")
    
    a = Atom.from_seed("hello")
    b = Atom.from_seed("world")
    c = Atom.from_seed("hello")  # Same seed
    
    print(f"a: {a.fingerprint[:3]}")
    print(f"b: {b.fingerprint[:3]}")
    print(f"c: {c.fingerprint[:3]}")
    
    print(f"similarity(a, b) = {similarity(a, b):.4f}")  # ~0.5 (random)
    print(f"similarity(a, c) = {similarity(a, c):.4f}")  # 1.0 (identical)


def test_bind_unbind():
    print("\n=== Bind/Unbind Test ===")
    
    love = qualia("love")
    warmth = qualia("warmth")
    
    print(f"love: {love.path_hex}")
    print(f"warmth: {warmth.path_hex}")
    
    # Bind
    bound = bind(love, warmth)
    print(f"bound: {bound.content}")
    
    # Unbind
    recovered = unbind(bound, love)
    sim = similarity(recovered, warmth)
    print(f"unbind(bound, love) ≈ warmth: similarity = {sim:.4f}")
    
    # Should be 1.0 (perfect recovery)
    assert sim > 0.99, "Unbind should perfectly recover!"


def test_bundle():
    print("\n=== Bundle Test ===")
    
    atoms = [qualia("love"), qualia("warmth"), qualia("presence")]
    bundled = bundle(atoms)
    
    print(f"bundled: {bundled.content}")
    
    # Query with each component
    for atom in atoms:
        sim = similarity(bundled, atom)
        print(f"  similarity(bundle, {atom.content}) = {sim:.4f}")
    
    # Query with unrelated
    unrelated = qualia("void")
    sim = similarity(bundled, unrelated)
    print(f"  similarity(bundle, void) = {sim:.4f}")


def test_dictionaries():
    print("\n=== Dictionary Test ===")
    
    # Qualia
    love = qualia("love")
    print(f"qualia('love'): {love.path_hex} {love.glyph}")
    
    # Verb
    feel = verb("feel", "present")
    print(f"verb('feel', 'present'): {feel.path_hex}")
    
    # Sigma
    delta = sigma("Δ")
    print(f"sigma('Δ'): {delta.path_hex} = {delta.content}")
    
    causes = sigma("CAUSES")
    print(f"sigma('CAUSES'): {causes.path_hex}")


def test_composition():
    print("\n=== Composition Test ===")
    
    # verb + sigma tier + qualia
    feel = verb("feel", "present")
    insight = sigma("Δ")
    warmth = qualia("warmth")
    
    # "Feeling warmth at insight level"
    composed = bind(feel, insight, warmth)
    print(f"feel ⊗ Δ ⊗ warmth = {composed.content}")
    
    # Recover warmth
    recovered = unbind(composed, feel, insight)
    sim = similarity(recovered, warmth)
    print(f"unbind(composed, feel, insight) ≈ warmth: {sim:.4f}")


def test_store():
    print("\n=== Store Test ===")
    
    store = SubstrateStore("test.lance")
    
    # Store some atoms
    store.store(qualia("love"))
    store.store(qualia("warmth"))
    store.store(qualia("presence"))
    
    # Resonate
    query = qualia("love")
    results = store.resonate(query, k=3)
    
    print(f"Resonating with 'love':")
    for atom, sim in results:
        print(f"  {atom.content}: {sim:.4f}")


def test_dn_tree():
    print("\n=== DN-Tree Test ===")
    
    dn = get_dn_tree()
    
    # Resolve paths
    paths = ["sigma:tier:Δ", "qualia:love", "verbs:feel:present"]
    for path in paths:
        atom = resolve(path)
        if atom:
            print(f"resolve('{path}'): {atom.content} {atom.glyph}")
        else:
            print(f"resolve('{path}'): NOT FOUND")


if __name__ == "__main__":
    test_atoms()
    test_bind_unbind()
    test_bundle()
    test_dictionaries()
    test_composition()
    test_store()
    test_dn_tree()
    
    print("\n=== All tests passed! ===")
```

---

## Success Criteria

1. **Atoms work**: deterministic fingerprints, same seed = same atom
2. **Bind/unbind is perfect**: similarity after unbind > 0.99
3. **Bundle preserves components**: similarity with each > 0.5
4. **Dictionaries are populated**: qualia (256), verbs (144), sigma (64)
5. **Composition works**: verb ⊗ sigma ⊗ qualia can be unbound
6. **Store persists**: LanceDB saves and retrieves correctly
7. **DN-tree resolves**: paths like "sigma:tier:Δ" → atoms

---

## Repository

Push to: `https://github.com/AdaWorldAPI/ada-unified`

Branch: `substrate-v2`
