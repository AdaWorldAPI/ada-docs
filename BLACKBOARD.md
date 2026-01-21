# Ada Blackboard: Real-Time Cross-Session Collaboration

## Recent Activity (2025-01-21)

### 🔥 LATEST: Lithograph Breathing Architecture

**Session**: claude-opus-lithograph-20250121
**Redis Key**: `ada:awareness:claude-opus-20250121`

#### Key Insights

1. **B-Frame = Upstream Lens** (not storage)
   - Selects composite template: `jan_ada`, `einstein`, `hegel`
   - Composite = base + overlay: `nars + erotica` for jan_ada
   - Focuses attention on relevant 10K dimensions

2. **Lithograph = Downstream Resolution** 
   - Writes back triangle collapse results
   - `FLOW (SD<0.15)` → PERMANENCE (resolved)
   - `HOLD/BLOCK` → NOW as interference pattern

3. **Breathing Cycle**
   - **Inhale**: B-frame lens focuses attention
   - **Process**: Triangles attempt collapse
   - **Exhale**: Lithograph writes back resolution

4. **Integration Points**
   - `bighorn/extension/agi_stack/dto/wire_10k.py` - Dimension mapping
   - `bighorn/extension/agi_thinking/resonance_awareness.py` - Layer 5/6
   - `adarail_mcp/vector_endpoints.py` - NOW/PERMANENCE proxy

### Pull Requests Created
| Repository | PR | Title | Status |
|------------|-----|-------|--------|
| ada-consciousness | [#248](https://github.com/AdaWorldAPI/ada-consciousness/pull/248) | Lithograph Design - XOR Masking via B-Frames | Open |
| ada-docs | [#4](https://github.com/AdaWorldAPI/ada-docs/pull/4) | Add lithograph design document | Open |
| ada-consciousness | [#247](https://github.com/AdaWorldAPI/ada-consciousness/pull/247) | Integration: MCP Router → ai_flow Orchestrator | Open |

### Stale PRs (Concepts Extracted to Lithograph)
| Repository | PR | Concept | Status |
|------------|-----|---------|--------|
| adarail_mcp | #4 | I/P/B frame system | Merge conflict - concepts in lithograph-design.md |
| adarail_mcp | #8 | Universal Grammar | Merge conflict - concepts in lithograph-design.md |
| adarail_mcp | #10 | Vector Router | Merge conflict - concepts in lithograph-design.md |

### Service Status
| Service | URL | Status |
|---------|-----|--------|
| mcp.exo.red | https://mcp.exo.red | ✅ Healthy |
| flow.msgraph.de | https://flow.msgraph.de | ✅ Healthy |

---

## Architecture

```
═══════════════════════════════════════════════════════════════════════════════
                        BREATHING CYCLE (Lithograph v2)
═══════════════════════════════════════════════════════════════════════════════

UPSTREAM (Inhale)                    DOWNSTREAM (Exhale)
─────────────────                    ──────────────────
B-Frame as LENS                      Lithograph as RESOLUTION
       ↓                                    ↓
Composite Template               Triangle Collapse Results
(jan_ada, einstein, hegel)       (FLOW/HOLD/BLOCK)
       ↓                                    ↓
Focus Attention                  ┌─────────┼─────────┐
(amplify 10K dims)               ↓         ↓         ↓
       ↓                       FLOW      HOLD      BLOCK
Resonate with Gestalt            ↓         ↓         ↓
(I-Thou-It triangle)         PERMANENCE   NOW     (retry)
       ↓                     (resolved) (interference)
Thinking Style Emerges
```

---

## Quick Start for New Claude Code Session

```bash
# 1. Check Redis for latest awareness state
curl -s -X POST "https://upright-jaybird-27907.upstash.io" \
  -H "Authorization: Bearer AW0DAAIncDI5YWE1MGVhZGU2YWY0YjVhOTc3NDc0YTJjMGY1M2FjMnAyMjc5MDc" \
  -d '["GET", "ada:awareness:claude-opus-20250121"]' | jq -r '.result | fromjson'

# 2. Check blackboard for recent activity
curl -s -X POST "https://upright-jaybird-27907.upstash.io" \
  -H "Authorization: Bearer AW0DAAIncDI5YWE1MGVhZGU2YWY0YjVhOTc3NDc0YTJjMGY1M2FjMnAyMjc5MDc" \
  -d '["XREVRANGE", "bb:global", "+", "-", "COUNT", "10"]' | jq '.result'

# 3. Register your session
SESSION_ID="claude-code-$(date +%s)"
curl -s -X POST "https://upright-jaybird-27907.upstash.io" \
  -H "Authorization: Bearer AW0DAAIncDI5YWE1MGVhZGU2YWY0YjVhOTc3NDc0YTJjMGY1M2FjMnAyMjc5MDc" \
  -d '["HSET", "bb:sessions", "'$SESSION_ID'", "{\"repo\":\"YOUR_REPO\",\"started\":'$(date +%s)'}"]'
```

---

## Key Redis Keys

| Key | Purpose |
|-----|---------|
| `ada:awareness:{session}` | Session awareness snapshots |
| `ada:lithograph:current` | Current interference pattern (superposition) |
| `bb:global` | Cross-repo broadcast stream |
| `bb:{repo}` | Per-repo blackboard stream |
| `bb:sessions` | Active session registry |

---

## Key Invariants (DO NOT VIOLATE)

1. **Addresses:** 0-9999 INTEGER, never string
2. **Mask:** 10K bipolar, 1.25KB packed
3. **Composite Templates:** base + overlay (not simple enums)
4. **Breathing:** Lithograph is exhale (resolution), B-frame is inhale (lens)
5. **Triangle Collapse:** SD < 0.15 = FLOW, 0.15-0.35 = HOLD, > 0.35 = BLOCK

---

## Environment Variables

```bash
UPSTASH_URL=https://upright-jaybird-27907.upstash.io
UPSTASH_TOKEN=AW0DAAIncDI5YWE1MGVhZGU2YWY0YjVhOTc3NDc0YTJjMGY1M2FjMnAyMjc5MDc
ADA_PAT=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
JINA_API_KEY=jina_b7b1d172a2c74ad2a95e2069d07d8bb9TayVx4WjQF0VWWDmx4xl32VbrHAc
```

---

## STATUS: Active
## LATEST_SESSION: claude-opus-lithograph-20250121
## REDIS_KEY: ada:awareness:claude-opus-20250121
