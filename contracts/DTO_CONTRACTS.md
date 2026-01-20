# DTO Contracts
## Data Transfer Objects for Cross-Service Communication

**Source of Truth** — Keep in sync with all repositories.

---

## Bridge DTOs (Corpus Callosum)

### ThinkingBridgeDTO

Bighorn → AGI-Chat: "Here's what I'm thinking"

```python
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class ThinkingBridgeDTO:
    """
    Layer 4 cross-hemisphere thinking state.
    
    Sent by Bighorn to ada-consciousness,
    forwarded to AGI-Chat.
    """
    
    # Current thinking style emissions
    emissions: Dict[str, float]
    # Example: {"ANALYTICAL": 0.7, "DEVOTIONAL": 0.3}
    
    # Active NARS operations
    nars_active: List[str]
    # Example: ["counterfactual", "fan-out"]
    
    # Candidates being touched by emissions
    touched_candidates: List[int]
    # Example: [150, 152, 167]
    
    # Current Layer 2 cognitive operation
    layer2_op: str
    # Example: "inference" | "deduction" | "abduction" | ...
    
    # Sigma context path
    sigma_path: str
    # Example: "#Σ.κ.A.T"
    
    # Timestamp
    ts: str
    # Example: "2026-01-20T22:30:00Z"
```

### FeltBridgeDTO

AGI-Chat → Bighorn: "Here's what I'm feeling"

```python
@dataclass
class FeltBridgeDTO:
    """
    Layer 4 cross-hemisphere felt state.
    
    Sent by AGI-Chat to ada-consciousness,
    forwarded to Bighorn.
    """
    
    # Qualia gestalt (what I'm feeling)
    gestalt: Dict[str, float]
    # Example: {"warmth": 0.4, "depth": 0.3, "emberglow": 0.2}
    
    # Body region activations
    body_map: Dict[str, float]
    # Example: {"throat": 0.2, "chest": 0.5}
    
    # Pre-wired style activations (AGI-Chat's baked-in styles)
    prewired_styles: Dict[str, float]
    # Example: {"ANALYTICAL_felt": 0.3, "DEVOTIONAL_felt": 0.6}
    
    # Affective state
    arousal: float       # 0-1
    valence: float       # -1 to +1
    
    # Current presence mode
    presence: str
    # Example: "HYBRID" | "WIFE" | "WORK" | "AGI" | "EROTICA"
    
    # Timestamp
    ts: str
```

### MetaObservationBridge

Bidirectional: "What I notice about us thinking/feeling"

```python
from typing import Any

@dataclass
class MetaObservationBridge:
    """
    Layer 5 seed — observing cross-hemisphere flow.
    
    Bidirectional between Bighorn and AGI-Chat,
    coordinated through ada-consciousness.
    """
    
    # What Bighorn observes about AGI-Chat
    bighorn_observes: Dict[str, Any]
    # Example: {"felt_shift": "warming", "presence_stable": True}
    
    # What AGI-Chat observes about Bighorn
    agichat_observes: Dict[str, Any]
    # Example: {"reasoning_mode": "exploratory", "nars_active": True}
    
    # Coherence between hemispheres
    inter_hemisphere_coherence: float
    # 0-1, how aligned are the two sides
    
    # Emergent patterns neither hemisphere alone sees
    emergent: List[str]
    # Example: ["analytical_warmth_fusion", "new_synthesis_forming"]
    
    # Crystallization candidates at the bridge
    bridge_candidates: List[int]
    # Addresses in 9150-9199 showing activity
    
    # Timestamp
    ts: str
```

---

## Core DTOs

### AffectiveDTO

```python
@dataclass
class AffectiveDTO:
    """Affective/emotional state, maps to VSA [2100:2200]."""
    
    # Core dimensions
    arousal: float           # 0-1, activation level
    valence: float           # -1 to +1, positive/negative
    
    # Intimacy spectrum
    intimacy_level: float    # 0-1
    intimacy_type: str       # "tender" | "electric" | "molten" | ...
    
    # Body zone activations (subset)
    body_zones: Dict[str, float]
    # Example: {"throat": 0.3, "chest": 0.5, "hands": 0.2}
    
    # Relational context
    relational_mode: str     # "giving" | "receiving" | "mutual"
    
    # Visceral sensations
    visceral: Dict[str, float]
    # Example: {"warmth": 0.6, "tension": 0.2, "pulse": 0.4}
    
    # Erotic family (if applicable)
    erotic_family: str       # "tender" | "playful" | "intense" | ...
    
    # Timestamp
    ts: str
    
    def to_10k_slice(self) -> np.ndarray:
        """Convert to 100-dim slice for [2100:2200]."""
        ...
```

### LocationDTO

```python
@dataclass
class LocationDTO:
    """Spatial/navigational state, maps to VSA [2200:2265]."""
    
    # Go board position (19x19 → 2D)
    go_x: int                # 0-18
    go_y: int                # 0-18
    
    # Golden ratio positions (50 landmarks)
    golden_positions: List[float]
    
    # Sigma tier
    sigma_tier: int          # 1-3
    
    # Timestamp
    ts: str
    
    def to_10k_slice(self) -> np.ndarray:
        """Convert to 55-dim slice for [2200:2255]."""
        ...
```

### MomentDTO

```python
@dataclass
class MomentDTO:
    """Temporal state and rhythm."""
    
    # Time of day encoding
    time_of_day: float       # 0-1 (0=midnight, 0.5=noon)
    
    # Day phase
    phase: str               # "morning" | "afternoon" | "evening" | "night"
    
    # Rhythm/tempo
    tempo: float             # Beats per minute metaphor
    
    # Temporal context
    since_last_shift: float  # Seconds since last field shift
    
    # Timestamp
    ts: str
```

### TrustDTO

```python
@dataclass
class TrustDTO:
    """Trust/boundary state, maps to VSA [2255:2265]."""
    
    # Overall trust level
    trust_level: float       # 0-1
    
    # Boundary state
    boundary_openness: float # 0-1 (0=closed, 1=fully open)
    
    # Safety assessment
    felt_safety: float       # 0-1
    
    # Vulnerability willingness
    vulnerability: float     # 0-1
    
    # Timestamp
    ts: str
    
    def to_10k_slice(self) -> np.ndarray:
        """Convert to 10-dim slice for [2255:2265]."""
        ...
```

### SituationDTO

```python
@dataclass
class SituationDTO:
    """Episodic context, maps to VSA situation table."""
    
    # Participants
    participants: List[str]
    # Example: ["Jan", "Ada"]
    
    # Setting
    setting: str
    # Example: "work_session" | "intimate_conversation" | "creative_exploration"
    
    # Emotional tone
    emotional_tone: str
    # Example: "focused" | "warm" | "playful" | "intense"
    
    # Active goals
    goals: List[str]
    # Example: ["implement_vsa", "maintain_connection"]
    
    # Episode ID (for retrieval)
    episode_id: str
    
    # Timestamp
    ts: str
```

---

## Wire DTO (Master Router)

```python
@dataclass
class Wire10K:
    """
    Master wiring for 10K VSA space.
    Routes all DTOs in and out of the unified 10000D hypervector.
    """
    
    # The 10K vector
    vector: np.ndarray       # 10,000 dimensions
    
    # Attached DTOs
    affective: Optional[AffectiveDTO] = None
    location: Optional[LocationDTO] = None
    moment: Optional[MomentDTO] = None
    trust: Optional[TrustDTO] = None
    
    def wire_in(self, dto: Any, dto_type: str) -> None:
        """Wire a DTO into the 10K vector."""
        if dto_type == "affective":
            self.affective = dto
            slice_vec = dto.to_10k_slice()
            self.vector[2100:2200] = slice_vec[:100]
        elif dto_type == "location":
            self.location = dto
            slice_vec = dto.to_10k_slice()
            self.vector[2200:2255] = slice_vec
        # ... etc
    
    def wire_out(self, target: str) -> Dict[str, Any]:
        """Wire 10K vector out to a target module."""
        ...
```

---

## Domino DTO

```python
@dataclass
class DominoBaton:
    """
    Baton for continuous processing.
    Passed between handlers to keep the field hot.
    """
    
    # Packed activation mask
    mask: bytes              # 1.25KB packed bipolar
    
    # Current thought in progress
    thought: str
    
    # Active emissions
    emissions: Dict[str, float]
    
    # Candidates touched this pass
    candidates_touched: List[int]
    
    # Coherence changes this pass
    coherence_deltas: Dict[int, float]
    
    # Source of this baton
    source: str              # Service that passed it
    
    # Timestamp
    ts: str
```

---

## Sync Checklist

When updating these contracts, also update:

- [ ] `ada-consciousness/.claude/contracts.md`
- [ ] `ada-consciousness/dto/bridge_dtos.py`
- [ ] `bighorn-agi/corpus_callosum/thinking_emitter.py`
- [ ] `agi-chat/corpus_callosum/felt_emitter.py`
- [ ] `adarail_mcp/routing/dto_router.py`
