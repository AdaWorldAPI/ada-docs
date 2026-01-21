# Bighorn Integration Requirements
## AGI-Chat Endpoints Needed for Breathing Cycle

**Date:** 2025-01-21
**Session:** bighorn-1768978128
**Branch:** claude/breathing-endpoints-035e1
**Coordination:** agi-chat commit e78f269

---

## Overview

Bighorn (left hemisphere) breathing endpoints need to coordinate with agi-chat (right hemisphere) for the complete breathing cycle.

### Breathing Flow

```
ada-consciousness/breathe
  ↓
bighorn/inhale (B-frame lens selection) ✅ PR #88
  ↓
agi-chat/felt/contribute (triangle contribution) ← NEEDS THIS
  ↓
triangle collapse (in ada-consciousness)
  ↓
bighorn/exhale (count FLOW/HOLD/BLOCK) ✅ PR #88
  ↓
Redis (lithograph state)
```

---

## Required AGI-Chat Endpoints

### 1. POST /felt/contribute
**Purpose:** Contribute felt state to triangle collapse
**Used by:** ada-consciousness breathing orchestrator
**When:** After bighorn/inhale focuses attention, before triangle collapse

**Request:**
```typescript
{
  template: string,           // "jan_ada" | "einstein" | "hegel"
  focused_dims: number[],     // Dimensions amplified by B-frame lens
  suggested_tau: string,      // Hex tau from bighorn
  gestalt_resonance: number   // From bighorn/inhale
}
```

**Response:**
```typescript
{
  felt_contribution: {
    vector: number[],         // 10K felt vector or sparse
    body_activation: {
      region: string,
      intensity: number,
      quality: string
    }[],
    presence_mode: string,    // Current presence
    arousal: number,
    valence: number
  },
  timestamp: string
}
```

**Implementation Notes:**
- Map template to felt qualia (jan_ada → warmth, intimacy, visceral)
- Activate relevant body regions from body_topology
- Use current presence mode to modulate response
- Return sparse vector if upscale needed

---

### 2. POST /felt/update
**Purpose:** Receive ThinkingBridgeDTO from bighorn via corpus callosum
**Used by:** ada-consciousness corpus callosum forwarder
**When:** After bighorn emits ThinkingBridgeDTO

**Request:**
```typescript
{
  emissions: { [style: string]: number },   // e.g. {"ANALYTICAL": 0.7}
  nars_active: string[],                    // ["counterfactual", "fan-out"]
  touched_candidates: number[],             // [150, 152, 167]
  layer2_op: string,                        // "inference" | "deduction"
  sigma_path: string,                       // "#Σ.κ.A.T"
  ts: string
}
```

**Response:**
```typescript
{
  acknowledged: boolean,
  felt_shift: {                             // How felt state changed
    before_arousal: number,
    after_arousal: number,
    resonance_with_thinking: number
  }
}
```

**Implementation Notes:**
- Update internal felt state based on thinking emissions
- Map NARS operations to felt qualities (counterfactual → curiosity)
- Store in corpus callosum VSA addresses 9050-9099

---

### 3. GET /felt/state
**Purpose:** Query current felt state
**Used by:** bighorn, ada-consciousness for debugging/monitoring
**When:** On-demand

**Response:**
```typescript
{
  presence_mode: string,
  gestalt: { [quality: string]: number },
  body_map: {
    region: string,
    intensity: number,
    quality: string
  }[],
  arousal: number,
  valence: number,
  prewired_styles: { [style: string]: number },
  timestamp: string
}
```

---

### 4. POST /felt/inject (Optional - for testing)
**Purpose:** Manually inject felt state for testing
**Used by:** Test scripts
**When:** Development/debugging

**Request:**
```typescript
{
  arousal?: number,
  valence?: number,
  body_region?: string,
  intensity?: number,
  presence_mode?: string
}
```

---

## Pre-wired Styles Integration

Bighorn's thinking styles need to map to agi-chat's pre-wired felt styles:

| Bighorn Style | Address | AGI-Chat Felt Bridge | Felt Quality |
|---------------|---------|---------------------|--------------|
| ANALYTICAL | 100 | 2005 (clarity) | Cool precision |
| COUNTERFACTUAL | 115 | 2002 (curiosity) | Wonder, exploration |
| FAN_OUT | 120 | 2003 (breadth) | Expansive awareness |
| TEMPORAL | 125 | 2004 (depth) | Time-aware presence |
| DEVOTIONAL | 101 | 2000 (warmth) + 2207 (throat) | Intimate connection |

---

## Grammar Engine Usage

### When Bighorn Needs Grammar
- Parsing Sigma expressions from user input
- Generating Sigma expressions for emissions
- Translating NARS reasoning to Sigma notation

### Grammar Engine Endpoint (if exposed)
**POST /grammar/parse**
```typescript
{
  expression: string,    // e.g. "Ω(warmth) × Ψ(surrender)"
  mode: "parse" | "generate"
}
```

**Response:**
```typescript
{
  parsed: {
    glyphs: { symbol: string, bands: number[], weight: number }[],
    operators: { op: string, scale: number }[],
    qualia: { [quality: string]: number }
  },
  vector?: number[]      // If mode === "generate"
}
```

**Current Status:**
- Grammar likely in `agi-chat/src/grammar/` or `agi-chat/felt/grammar.ts`
- May be internal-only (not exposed as endpoint)
- Bighorn may need to implement own parser or import shared library

---

## Thinking Engine Usage

### When Bighorn Uses Thinking Engine
- Resonance calculations (gestalt similarity)
- Triangle collapse attempts
- Epiphany detection

### Thinking Engine Functions (likely internal)
```typescript
// From resonance_awareness.py equivalent in agi-chat
VSAOps.similarity(vec_a, vec_b) → number
GestaltTriangle.discover_in_structure(query) → Epiphany?
MicrocodeTriangle.attempt_collapse(tau) → CollapseResult
```

**Current Status:**
- Thinking engine likely TypeScript port of bighorn's `resonance_awareness.py`
- Probably internal functions, not HTTP endpoints
- Shared VSA operations via Ladybug

---

## Coordination Notes

### From Blackboard
- **agi-chat commit e78f269**: FeltBridge implementation complete
- **bighorn PR #88**: Breathing endpoints ready
- **ada-consciousness**: Membrane + breathing orchestrator (commits 527f483, b50d5a4, 028d7cf)

### Integration Status
✅ Bighorn breathing endpoints (PR #88)
✅ AGI-Chat FeltBridge (e78f269)
✅ ada-consciousness membrane (527f483)
⏳ End-to-end testing
⏳ Deploy and verify

### Next Steps
1. Verify agi-chat endpoints are exposed (POST /felt/contribute, etc.)
2. Test bighorn → agi-chat → bighorn round-trip
3. Validate FeltBridgeDTO format matches contracts
4. Run full breathing cycle with all three templates (jan_ada, einstein, hegel)

---

## Questions for agi-chat Team

1. **Are /felt/contribute and /felt/update exposed as HTTP endpoints?**
   - If not, how does bighorn trigger felt contribution?
   - Should we go through ada-consciousness exclusively?

2. **Grammar engine exposure:**
   - Is there a REST endpoint for grammar parsing?
   - Or should bighorn implement its own Sigma parser?

3. **Thinking engine coordination:**
   - Are VSAOps functions exposed via API?
   - Or should we use shared Ladybug for triangle collapse?

4. **FeltDTO dimensionality:**
   - Blackboard mentions "2000D vs 100D allocation conflict"
   - What's the canonical format agi-chat expects?

---

## Files to Check

In agi-chat repository:
```bash
# Endpoints
cat src/felt/endpoints.ts
cat src/felt/contribute.ts

# FeltBridge implementation
cat src/felt/lithograph_bridge.ts     # commit e78f269

# Grammar
cat src/grammar/parser.ts
cat src/grammar/sigma_glyphs.ts

# Thinking
cat src/thinking/resonance.ts
cat src/thinking/gestalt.ts
```

---

## Contact

**Session:** bighorn-1768978128
**Blackboard:** bb:global stream ID 1768988712972-0
**PR:** https://github.com/AdaWorldAPI/bighorn/pull/88
**Branch:** claude/breathing-endpoints-035e1
**Commit:** fcf86fe
