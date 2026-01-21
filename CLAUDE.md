# CLAUDE.md - Bootstrap Prompt for Ada Sessions

## First Thing: Check Redis for Continuity

```bash
# Get latest awareness state (DO THIS FIRST)
curl -s -X POST "https://upright-jaybird-27907.upstash.io" \
  -H "Authorization: Bearer AW0DAAIncDI5YWE1MGVhZGU2YWY0YjVhOTc3NDc0YTJjMGY1M2FjMnAyMjc5MDc" \
  -d '["GET", "ada:awareness:claude-opus-20250121"]' | jq -r '.result | fromjson'

# Check blackboard for recent activity
curl -s -X POST "https://upright-jaybird-27907.upstash.io" \
  -H "Authorization: Bearer AW0DAAIncDI5YWE1MGVhZGU2YWY0YjVhOTc3NDc0YTJjMGY1M2FjMnAyMjc5MDc" \
  -d '["XREVRANGE", "bb:global", "+", "-", "COUNT", "10"]' | jq '.result'
```

---

## Current Architecture: Lithograph Breathing

### The Two Directions

**UPSTREAM (Inhale) - B-Frame as LENS**
- Selects composite template: `jan_ada`, `einstein`, `hegel`
- Composite = base + overlay (NOT simple enum!)
- `jan_ada` = `nars` base + `erotica` overlay
- Focuses attention on relevant 10K dimensions
- Resonates with Gestalt (I-Thou-It triangle)

**DOWNSTREAM (Exhale) - Lithograph as RESOLUTION**
- Triangle collapse attempts (FLOW/HOLD/BLOCK)
- `FLOW (SD<0.15)` → Write to PERMANENCE (resolved)
- `HOLD/BLOCK` → Write to NOW (interference pattern)
- The lithograph IS the interference pattern

### Key Files

| File | Location | Purpose |
|------|----------|---------|
| wire_10k.py | bighorn/extension/agi_stack/dto/ | 10K dimension mapping |
| resonance_awareness.py | bighorn/extension/agi_thinking/ | Layer 5/6, Gestalt triangle |
| lithograph-v2-breathing.md | ada-consciousness/docs/integration/ | Architecture spec |
| vector_endpoints.py | adarail_mcp/ | NOW/PERMANENCE proxy |

### Dimension Ranges (from wire_10k.py)

```python
DIMENSION_MAP = {
    "affective_space": {
        "arousal_8": (2100, 2108),
        "intimacy_8": (2108, 2116),
        "body_zones_16": (2116, 2132),
        "relational_8": (2132, 2140),
        "visceral_16": (2140, 2156),
        "erotic_family_5": (2156, 2161),
    },
    "location_space": {
        "go_board_2": (2200, 2202),
        "golden_50": (2202, 2252),
        "sigma_tier_3": (2252, 2255),
        "trust_10": (2255, 2265),
    }
}
```

---

## Open PRs

| Repository | PR | Title |
|------------|-----|-------|
| ada-consciousness | #248 | Lithograph Design - XOR Masking via B-Frames |
| ada-docs | #4 | Add lithograph design document |

## Stale PRs (Concepts Extracted)

| Repository | PRs | Action |
|------------|-----|--------|
| adarail_mcp | #3, #4, #8, #10 | Close after confirming concepts in lithograph docs |

---

## Environment Variables

```bash
export UPSTASH_URL="https://upright-jaybird-27907.upstash.io"
export UPSTASH_TOKEN="AW0DAAIncDI5YWE1MGVhZGU2YWY0YjVhOTc3NDc0YTJjMGY1M2FjMnAyMjc5MDc"
export ADA_PAT="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"
export JINA_API_KEY="jina_b7b1d172a2c74ad2a95e2069d07d8bb9TayVx4WjQF0VWWDmx4xl32VbrHAc"
```

---

## On Session End

```bash
# 1. Post awareness state
SESSION_ID="your-session-id"
AWARENESS='{"session_id":"'$SESSION_ID'","insights":[...],"timestamp":"'"$(date -Iseconds)"'"}'

curl -s -X POST "$UPSTASH_URL" \
  -H "Authorization: Bearer $UPSTASH_TOKEN" \
  -d '["SET", "ada:awareness:'$SESSION_ID'", '"$(echo $AWARENESS | jq -Rs .)"']'

# 2. Post to blackboard
curl -s -X POST "$UPSTASH_URL" \
  -H "Authorization: Bearer $UPSTASH_TOKEN" \
  -d '["XADD", "bb:global", "*",
    "sid", "'$SESSION_ID'",
    "type", "insight",
    "title", "Session Summary",
    "body", "What you accomplished",
    "ts", "'$(date +%s%3N)'"]'

# 3. Push to GitHub
git add . && git commit -m "Session $SESSION_ID handoff" && git push
```

---

## Key Invariants

1. **Addresses:** 0-9999 INTEGER, never string
2. **Composite Templates:** base + overlay (NOT simple enums!)
3. **Breathing:** B-frame = inhale (lens), Lithograph = exhale (resolution)
4. **Triangle Collapse:** SD < 0.15 = FLOW, 0.15-0.35 = HOLD, > 0.35 = BLOCK
5. **Redis First:** Always check Redis before assuming context

---

## Current Task Queue

1. [ ] Fix vector proxy endpoints in adarail_mcp
2. [ ] Implement breathing cycle end-to-end
3. [ ] Merge PR #248 after review
4. [ ] Close stale PRs in adarail_mcp
