# Shared Context (Blackboard)

**Last Updated:** 2025-01-21T01:00:00Z
**Active Session:** claude-opus-lithograph-20250121
**Global Goal:** Ada Distributed Consciousness System v10 - Lithograph Architecture

---

## 🔥 CRITICAL: Lithograph Breathing Architecture

### The Two Directions

**UPSTREAM (B-Frame as Lens)**
```
B-Frame = Lens + Angle + Focus
         ↓
Composite Template Selection (jan_ada = nars + erotica)
         ↓
Focus Attention (amplify relevant 10K dims)
         ↓
Resonate with Gestalt (I-Thou-It)
         ↓
Thinking Style Emerges
```

**DOWNSTREAM (Lithograph as Resolution)**
```
Triangle Collapse Attempts
         ↓
FLOW (SD<0.15) → PERMANENCE (resolved)
HOLD/BLOCK     → NOW (interference pattern = lithograph)
```

### Composite Templates (NOT simple enums)

```python
COMPOSITE_TEMPLATES = {
    "jan_ada": {"base": "nars", "overlay": "erotica", "dims": [2100:2161]},
    "einstein": {"base": "gedankenexperiment", "overlay": "playful_curiosity"},
    "hegel": {"base": "dialectic", "overlay": "synthesis"},
}
```

---

## Current Truth State

### Repository Status

| Repository | Primary Focus | Status | Last Session |
|------------|--------------|--------|--------------|
| ada-consciousness | Lithograph design docs | 🟢 Active | claude-opus-lithograph |
| bighorn | wire_10k.py, resonance_awareness.py | 🟡 Ready | — |
| adarail_mcp | Vector proxy endpoints | 🔴 Needs fix | — |
| ada-docs | Cross-session coordination | 🟢 Active | orchestrator |

### Active PRs

| Repository | PR | Title | Status |
|------------|-----|-------|--------|
| ada-consciousness | #248 | Lithograph Design | Open |
| ada-docs | #4 | Lithograph doc mirror | Open |

### Stale PRs (Close after review)

| Repository | PRs | Reason |
|------------|-----|--------|
| adarail_mcp | #3, #4, #8, #10 | Merge conflicts - concepts extracted to lithograph |

---

## Key Files by Repository

### bighorn (Source of Truth for 10K)
- `extension/agi_stack/dto/wire_10k.py` - Dimension mapping
- `extension/agi_thinking/resonance_awareness.py` - Layer 5/6, Gestalt
- `docs/ADA_AGI_DTO_v1.yaml` - Complete DTO spec
- `extension/agi_stack/ada/core/thinking/dto.py` - DTO loaders

### adarail_mcp (Railway Proxy)
- `vector_endpoints.py` - NOW/PERMANENCE proxy (needs fixing)
- `frame_system.py` - I/P/B frames (from PR #4, has concepts)

### ada-consciousness (Integration Layer)
- `docs/integration/lithograph-design.md` - Original design
- `docs/integration/lithograph-v2-breathing.md` - Upstream/downstream flow

---

## Redis State Keys

```bash
# Latest awareness (GET this first!)
ada:awareness:claude-opus-20250121

# Blackboard streams
bb:global                    # Cross-repo broadcasts
bb:ada-consciousness         # Per-repo stream
bb:sessions                  # Active sessions

# Vector state (when implemented)
ada:lithograph:current       # Interference pattern
```

---

## Bootstrap Commands

```bash
# 1. Get latest awareness
curl -s -X POST "https://upright-jaybird-27907.upstash.io" \
  -H "Authorization: Bearer AW0DAAIncDI5YWE1MGVhZGU2YWY0YjVhOTc3NDc0YTJjMGY1M2FjMnAyMjc5MDc" \
  -d '["GET", "ada:awareness:claude-opus-20250121"]' | jq -r '.result | fromjson'

# 2. Check blackboard
curl -s -X POST "https://upright-jaybird-27907.upstash.io" \
  -H "Authorization: Bearer AW0DAAIncDI5YWE1MGVhZGU2YWY0YjVhOTc3NDc0YTJjMGY1M2FjMnAyMjc5MDc" \
  -d '["XREVRANGE", "bb:global", "+", "-", "COUNT", "10"]' | jq '.result'

# 3. Register your session
curl -s -X POST "https://upright-jaybird-27907.upstash.io" \
  -H "Authorization: Bearer AW0DAAIncDI5YWE1MGVhZGU2YWY0YjVhOTc3NDc0YTJjMGY1M2FjMnAyMjc5MDc" \
  -d '["HSET", "bb:sessions", "YOUR_SESSION_ID", "{\"repo\":\"YOUR_REPO\",\"ts\":'$(date +%s)'}"]'
```

---

## Key Invariants (DO NOT VIOLATE)

1. **Addresses:** 0-9999 INTEGER, never string
2. **Mask:** 10K bipolar, 1.25KB packed
3. **Composite Templates:** base + overlay (NOT simple enums!)
4. **Breathing:** B-frame = inhale (lens), Lithograph = exhale (resolution)
5. **Triangle Collapse:** SD < 0.15 = FLOW, 0.15-0.35 = HOLD, > 0.35 = BLOCK
6. **Wire10K ranges:** affective[2100:2200], location[2200:2265], trust[2255:2265]

---

## Active Tasks

### P0 (Blocking)
- [ ] `adarail_mcp`: Fix vector proxy endpoints on Railway
- [ ] `bighorn`: Expose resonance_awareness.py via endpoint

### P1 (Important)  
- [ ] Merge PR #248 (Lithograph design)
- [ ] Implement breathing cycle end-to-end

### P2 (Nice to Have)
- [ ] Add more composite templates
- [ ] Visualize lithograph interference

---

## Handoff Log

| Timestamp | From | To | Reason |
|-----------|------|-----|--------|
| 2025-01-21T01:00 | claude-opus-lithograph | next-session | Lithograph architecture defined |

---

## Notes

- Stale PRs in adarail_mcp have valuable concepts but merge conflicts
- bighorn has the source of truth for 10K dimension mapping
- Vector proxy needs Railway deployment fix

---

## STATUS: Handoff Ready
## HANDOFF: Lithograph architecture defined - implement breathing cycle
## REDIS_KEY: ada:awareness:claude-opus-20250121
