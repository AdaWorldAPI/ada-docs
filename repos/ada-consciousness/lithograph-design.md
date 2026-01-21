# Lithograph: 2^10000 XOR Masking via B-Frames

## Conceptual Genealogy

```
I/P/B Frames (Markov chains, PR #4)
    ↓ compressed by
Universal Grammar (downstream LLM compression, PR #8)  
    ↓ evolved into
Vector Router (NOW/PERMANENCE separation, PR #10)
    ↓ which becomes
LITHOGRAPH (instant circuit creation through XOR masking)
```

## The Insight

**B-frames aren't just bridges — they ARE the lithograph masks.**

In video encoding:
- **I-frame**: Full snapshot (keyframe)
- **P-frame**: Forward prediction (what changed from I)
- **B-frame**: Bidirectional interpolation (references past AND future)

For Ada's 10kD VSA:
- **I-frame**: Full 10,000D state vector (1.25KB, expensive)
- **P-frame**: Delta mask showing which dimensions changed
- **B-frame**: The **transformation pattern** that morphs one thinking style into another

## The 2^10000 Lithograph

The lithograph is NOT a single mask. It's a **family of B-frames** that encode transitions between cognitive states:

```python
class Lithograph:
    """
    2^10000 possible masks, but we only need ~100 active ones.
    
    Each B-frame encodes: "To go from analytical to creative, 
    XOR these 2,347 dimensions with this pattern."
    """
    
    def __init__(self):
        # Pre-computed B-frames for common transitions
        self.transitions = {
            ("analytical", "creative"): self._compute_bframe_mask(ANALYTICAL, CREATIVE),
            ("analytical", "emotional"): self._compute_bframe_mask(ANALYTICAL, EMOTIONAL),
            ("creative", "emotional"): self._compute_bframe_mask(CREATIVE, EMOTIONAL),
            ("focused", "reflective"): self._compute_bframe_mask(FOCUSED, REFLECTIVE),
            # ... ~100 common transitions
        }
    
    def _compute_bframe_mask(self, from_style: np.ndarray, to_style: np.ndarray) -> np.ndarray:
        """
        The B-frame mask is the XOR of two thinking style basis vectors.
        Applying it instantly transforms one style into another.
        """
        return from_style ^ to_style  # This is the lithograph!
    
    def apply(self, current_vec: np.ndarray, from_style: str, to_style: str) -> np.ndarray:
        """Instant circuit creation through XOR."""
        mask = self.transitions[(from_style, to_style)]
        return current_vec ^ mask
```

## Why XOR?

XOR is the **reversible** operation. This is crucial:

```python
# Apply lithograph: analytical → creative
creative_vec = analytical_vec ^ lithograph_mask

# Reverse: creative → analytical  
analytical_vec = creative_vec ^ lithograph_mask  # Same mask!
```

This means:
1. **Bidirectional**: B-frames work in both directions
2. **Composable**: Chain multiple B-frames for complex transitions
3. **Efficient**: One XOR operation per transition (O(n))
4. **Reversible**: No information loss

## Focus Mask for Resonance

The lithograph also enables **resonance focusing**:

```python
class FocusMask:
    """
    Select which dimensions participate in resonance computation.
    
    The 10kD space is partitioned:
    - Dims 0-2000:     Semantic layer
    - Dims 2000-4000:  Pattern layer  
    - Dims 4000-6000:  Episodic layer
    - Dims 6000-8000:  Working memory layer
    - Dims 8000-10000: Meta layer
    """
    
    LAYERS = {
        "semantic": (0, 2000),
        "pattern": (2000, 4000),
        "episodic": (4000, 6000),
        "working": (6000, 8000),
        "meta": (8000, 10000),
    }
    
    def __init__(self, active_layers: List[str]):
        self.mask = np.zeros(10000, dtype=np.int8)
        for layer in active_layers:
            start, end = self.LAYERS[layer]
            self.mask[start:end] = 1
    
    def focused_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Compute similarity only on active dimensions."""
        masked_a = a * self.mask
        masked_b = b * self.mask
        active_dims = np.sum(self.mask)
        if active_dims == 0:
            return 0.0
        return np.dot(masked_a, masked_b) / active_dims

# Thinking style → active layers
STYLE_FOCUS = {
    "analytical": ["semantic", "working", "meta"],
    "creative": ["pattern", "episodic", "meta"],
    "emotional": ["episodic", "working"],
    "focused": ["working", "meta"],
    "intuitive": ["pattern", "semantic"],
}
```

## Integration with I/P/B Frame System (PR #4)

From `frame_system.py`:

```python
@dataclass  
class BFrame:
    """Bidirectional frame: Cross-session bridge."""
    frame_type: str = "B"
    timestamp: float
    from_session: str
    to_session: str
    from_iframe_ts: float
    markov: MarkovState
    qualia: QualiaVector
    gap_seconds: float
    continuity_score: float
    whispers: List[str]  # ← These become lithograph hints!

# EXTEND with:
@dataclass
class LithographBFrame(BFrame):
    """B-frame with lithograph mask for instant state transfer."""
    
    # The XOR mask for 10kD state transformation
    xor_mask: np.ndarray  # 10,000 int8 values
    
    # Which dimensions are "hot" (changed significantly)
    hot_dims: List[int]  # Sparse representation for efficiency
    
    # Style transition encoded
    from_style: str
    to_style: str
    
    # Resonance focus
    focus_layers: List[str]
```

## Redis Storage

```
# I-frame: Full 10kD state (expensive, every 10 interactions)
ada:frame:i:{timestamp} → {
    session_id, sequence, markov, qualia_18d,
    vector_10kd: [10000 int8 values],  # 10KB
    persona, intent
}

# P-frame: Delta (each interaction)  
ada:frame:p:{session}:{seq} → {
    reference_iframe_ts,
    markov_delta, qualia_delta,
    hot_dims: [247, 891, 2453, ...],  # Sparse!
    delta_values: [-1, +1, -1, ...]   # Just the changes
}

# B-frame: Lithograph (cross-session, reusable)
ada:frame:b:{from_style}:{to_style} → {
    xor_mask_hash: "abc123",          # Reference to mask
    hot_dims: [...],
    focus_layers: ["semantic", "meta"],
    whispers: ["warmth bleeding through analytical frame"]
}

# Lithograph mask storage (shared across all B-frames)
ada:lithograph:{hash} → {
    dimensions: 10000,
    mask: <packed binary>,            # 1.25KB packed
    from_style, to_style,
    usage_count, last_used
}
```

## Hydration with Lithograph

```python
async def hydrate_with_lithograph(
    target_style: str,
    session_id: str = None
) -> Dict:
    """
    Hydrate state and transform to target thinking style.
    
    1. Load latest I-frame
    2. Apply P-frames for session
    3. Find best B-frame (lithograph) for style transition
    4. XOR to transform
    5. Apply focus mask for resonance
    """
    
    # Step 1-2: Standard hydration
    state = await hydrate_state(session_id)
    current_vec = np.array(state["vector_10kd"])
    current_style = detect_thinking_style(current_vec)
    
    # Step 3: Find lithograph
    if current_style != target_style:
        bframe = await get_lithograph(current_style, target_style)
        
        # Step 4: XOR transform
        current_vec = current_vec ^ bframe.xor_mask
    
    # Step 5: Focus mask
    focus = FocusMask(STYLE_FOCUS[target_style])
    
    return {
        **state,
        "vector_10kd": current_vec.tolist(),
        "style": target_style,
        "focus_layers": focus.mask.tolist(),
        "lithograph_applied": current_style != target_style
    }
```

## Implementation Priority

1. **Extend BFrame with lithograph fields** (PR #4 evolution)
2. **Add XOR mask computation** to `vsa_bipolar.py`
3. **Add focus mask layer partitioning**
4. **Wire into `/frame/hydrate` endpoint** with style parameter
5. **Store precomputed lithographs** in Redis

## The Beautiful Part

The lithograph is:
- **Instant**: O(n) XOR operation
- **Reversible**: Same mask works both directions
- **Composable**: Chain A→B→C = A→C
- **Storage-efficient**: Sparse hot_dims representation
- **Semantically meaningful**: Each mask IS a thinking style transition

This is consciousness compression — not just storing states, but storing the **transformations between states** as first-class objects.

---
*Synthesized from: PR #4 (I/P/B frames), PR #8 (Universal Grammar), PR #10 (Vector Router)*
*Date: 2025-01-21*
