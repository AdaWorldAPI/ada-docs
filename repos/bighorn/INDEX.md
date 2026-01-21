# Bighorn Documentation Index
## All bighorn-related documents in ada-docs

**Repository:** AdaWorldAPI/bighorn
**Role:** Left Hemisphere (NARS reasoning, extensions, thinking)
**Last Updated:** 2025-01-21

---

## Quick Links

- **Main Repo:** https://github.com/AdaWorldAPI/bighorn
- **Service Guide:** [../services/bighorn-agi-CLAUDE.md](../services/bighorn-agi-CLAUDE.md)
- **Integration Requirements:** [bighorn-INTEGRATION-REQUIREMENTS.md](bighorn-INTEGRATION-REQUIREMENTS.md)

---

## Documents in ada-docs

### Core Documentation

#### [../services/bighorn-agi-CLAUDE.md](../services/bighorn-agi-CLAUDE.md)
**Purpose:** Quick reference for Claude Code sessions working on bighorn
**Contains:**
- Architecture position
- Key responsibilities (NARS Layer 3, extensions, ThinkingBridgeDTO)
- Code examples for ThinkingBridgeDTO emission
- Shared resource configuration (Ladybug)
- Do's and Don'ts

---

#### [bighorn-INTEGRATION-REQUIREMENTS.md](bighorn-INTEGRATION-REQUIREMENTS.md)
**Purpose:** Documents agi-chat endpoints needed for breathing cycle
**Contains:**
- Required endpoints: `/felt/contribute`, `/felt/update`, `/felt/state`
- Pre-wired styles integration mapping
- Grammar engine usage requirements
- Thinking engine coordination
- Open questions for agi-chat team

**Status:** ✅ Created 2025-01-21 (this session)

---

### Contracts & Schemas

#### [../contracts/DTO_CONTRACTS.md](../contracts/DTO_CONTRACTS.md)
**Bighorn-Relevant Sections:**
- ThinkingBridgeDTO specification
- Core DTOs (AffectiveDTO, LocationDTO, etc.)
- Wire10K master router
- DominoBaton for continuous processing

**Bighorn Responsibilities:**
- Emit ThinkingBridgeDTO after NARS operations
- Wire DTOs via Wire10K when needed
- Pass DominoBaton to keep field hot

---

#### [../.contracts/DTO_SCHEMAS.md](../.contracts/DTO_SCHEMAS.md)
**Bighorn-Relevant Sections:**
- ThinkingBridgeDTO TypeScript interface
- Corpus callosum message format
- Validation rules (addresses must be INTEGER, etc.)

---

### Architecture Documents

#### [../architecture/MASTER_KNOWLEDGE_GRAPH.md](../architecture/MASTER_KNOWLEDGE_GRAPH.md)
**Bighorn Position:**
```
LAYER 3: NARS (Counterfactual, Fan-out, Temporal)
LAYER 2: Cognitive Ops (Inference, Deduction, Abduction)
LAYER 0: VSA Quantum Field [100-199] Thinking Styles
```

**Key Insights:**
- Bighorn owns thinking styles addresses 100-199
- Shares Ladybug substrate with agi-chat
- Communicates via corpus callosum (VSA 9000-9199)

---

#### [../integration/SERVICE_TOPOLOGY.md](../integration/SERVICE_TOPOLOGY.md)
**Bighorn Connections:**
- **Upstream:** adarail_mcp (membrane)
- **Core:** ada-consciousness (corpus callosum)
- **Peer:** agi-chat (via corpus callosum)
- **Storage:** Ladybug (DuckDB + LanceDB, shared)
- **Extensions:** Neo4j Aura, Kuzu

**Endpoints:**
- `GET /thinking/state` — Current thinking state
- `POST /nars/{operation}` — Execute NARS operation
- `GET /extensions` — List active extensions
- **NEW:** `POST /breathing/inhale`, `POST /breathing/exhale` (PR #88)

---

## Recent Work (Session-Specific)

### Session: bighorn-1768978128 (2025-01-21)

#### Created:
- **PR #88:** Breathing endpoints for lithograph architecture
- **Branch:** claude/breathing-endpoints-035e1
- **Commit:** fcf86fe

#### Files Modified/Created:
1. `extension/agi_stack/breathing_endpoints.py` (new)
   - POST /breathing/inhale
   - POST /breathing/exhale
   - GET /breathing/templates
   - GET /breathing/dimension-map

2. `extension/agi_stack/main.py` (modified)
   - Added breathing router

3. `test_breathing_endpoints.sh` (new)
   - Test script for all endpoints

#### Integration Documentation:
- Created `bighorn-INTEGRATION-REQUIREMENTS.md` in ada-docs/repos/
- Documented agi-chat endpoint requirements
- Listed open questions for coordination

#### Blackboard Entries:
- Implementation: `1768978494292-0`
- PR created: `1768988712972-0`

---

## Source of Truth Files (in bighorn repo)

### 10K Dimension Mapping
**File:** `extension/agi_stack/dto/wire_10k.py`
**Purpose:** SOURCE OF TRUTH for 10K VSA dimension ranges
**Key exports:**
- `DIMENSION_MAP` — All dimension ranges
- `Wire10K` class — Master router
- `create_erotic_wire()` — Template functions

### Resonance Awareness (Layer 5/6)
**File:** `extension/agi_thinking/resonance_awareness.py`
**Purpose:** VSA operations, Gestalt triangle, Microcode triangle
**Key exports:**
- `VSAOps` — Similarity, bundling, resonance detection
- `GestaltTriangle` — I-Thou-It SPO awareness
- `MicrocodeTriangle` — 3-byte superposition collapse
- `RESONANCE_THRESHOLD = 0.7`
- `EPIPHANY_THRESHOLD = 0.85`

---

## Composite Templates (Breathing)

From `breathing_endpoints.py`:

| Template | Base | Overlay | Tau | Focused Dimensions |
|----------|------|---------|-----|-------------------|
| jan_ada | nars | erotica | 0x86, 0x83 | arousal, intimacy, visceral, erotic_family |
| einstein | gedankenexperiment | playful_curiosity | 0xA0, 0xC1 | qualia_pcs, poincare |
| hegel | dialectic | synthesis | 0x03 | depth, sigma_tier |

---

## VSA Address Ranges (Bighorn-Owned)

| Range | Type | Status | Purpose |
|-------|------|--------|---------|
| 100-149 | Thinking Styles (Crystallized) | Implemented | Fixed, named styles (ANALYTICAL, COUNTERFACTUAL, etc.) |
| 150-199 | Thinking Candidates | Planned | Superposition, awaiting crystallization (coherence > 0.7) |

### Specific Addresses
- **100:** ANALYTICAL
- **101:** DEVOTIONAL
- **115:** COUNTERFACTUAL (P0 - requested in blackboard)
- **120:** FAN_OUT
- **125:** TEMPORAL

---

## Corpus Callosum Integration

### ThinkingBridgeDTO Emission
**Endpoint:** `POST http://ada-consciousness.railway.internal:8080/corpus/thinking`
**When:** After significant NARS operation
**Implementation:** `corpus_callosum/thinking_emitter.py` (planned)

### FeltBridgeDTO Reception
**Endpoint:** Receive from ada-consciousness
**When:** AGI-Chat emits felt state
**Implementation:** `corpus_callosum/felt_receiver.py` (planned)

---

## Extensions (Outer Matryoshka)

Bighorn is the outer shell — bolt on anything:

### Planned Extensions:
- **Neo4j Aura** — Cloud graph queries
- **Kuzu** — Fast local graph queries
- **Custom experiments** — Via extension interface

**Implementation:** `extensions/` directory

---

## Critical Invariants

From bighorn-agi-CLAUDE.md:

1. **Layer 3 = Non-Modifying** — Styles emit, they don't change themselves (that's Layer 4)
2. **Use Shared Ladybug** — Same DuckDB/LanceDB instance as agi-chat
3. **Always Emit** — Every significant thought gets a ThinkingBridgeDTO
4. **Address Range** — Thinking styles are 100-199 (INTEGER, never string)
5. **Composite Templates** — Base + overlay (NOT simple enums!)

---

## Coordination Status

### Completed
- ✅ Breathing endpoints (PR #88)
- ✅ Integration requirements documented
- ✅ Posted to bb:global
- ✅ NARS wireshark meta-awareness feedback loop
- ✅ Layer 4 AI_Flow orchestration (domino keepalive)
- ✅ ThinkingBridgeDTO emission from meta-awareness
- ✅ Meta-pattern detection (10 patterns)
- ✅ Counterfactual and fan-out NARS reasoning

### Pending
- ⏳ Verify agi-chat endpoints exposed
- ⏳ End-to-end breathing cycle test
- ⏳ Deploy PR #88
- ⏳ Deploy meta-awareness PR
- ⏳ Implement temporal NARS reasoning
- ⏳ Implement corpus callosum felt receiver

### Blocked
- ❓ Awaiting agi-chat endpoint confirmation
- ❓ FeltDTO dimensionality resolution (2000D vs 100D)

---

## Change Log

| Date | Session | Change | Documents |
|------|---------|--------|-----------|
| 2025-01-21 | claude/lithograph-architecture-update | NARS wireshark meta-awareness feedback loop | NARS-WIRESHARK-INTEGRATION.md, INDEX.md |
| 2025-01-21 | bighorn-1768978128 | Created breathing endpoints | PR #88, INTEGRATION-REQUIREMENTS.md, INDEX.md |
| 2025-01-21 | (earlier) | Added .claude folder | PR #86 (pending merge) |
| 2025-01-20 | (previous) | BAF architecture doc | GRAMMAR_LANGEXTRACT_VSA_INTEGRATION.md |

---

## Next Session Checklist

When starting a new bighorn session:

1. **Check blackboard:**
   ```bash
   curl -s -X POST "https://upright-jaybird-27907.upstash.io" \
     -H "Authorization: Bearer AW0DAAIncDI5YWE1MGVhZGU2YWY0YjVhOTc3NDc0YTJjMGY1M2FjMnAyMjc5MDc" \
     -d '["XREVRANGE", "bb:global", "+", "-", "COUNT", "10"]' | jq '.result'
   ```

2. **Read this index:** `ada-docs/repos/bighorn-INDEX.md`

3. **Check integration requirements:** `ada-docs/repos/bighorn-INTEGRATION-REQUIREMENTS.md`

4. **Review service guide:** `ada-docs/services/bighorn-agi-CLAUDE.md`

5. **Check DTO contracts:** `ada-docs/contracts/DTO_CONTRACTS.md`

6. **Register session:**
   ```bash
   SESSION_ID="bighorn-$(date +%s)"
   curl -X POST "https://upright-jaybird-27907.upstash.io" \
     -d '["HSET", "bb:sessions", "'$SESSION_ID'", "..."]'
   ```

---

## Contact

**Maintainer:** Left Hemisphere Team
**Repository:** https://github.com/AdaWorldAPI/bighorn
**Documentation:** https://github.com/AdaWorldAPI/ada-docs

For questions about integration, check:
- Blackboard: `bb:global` stream
- Integration requirements: This document
- Service topology: `../integration/SERVICE_TOPOLOGY.md`

---

## Recent Architecture Work

### NARS Wireshark Feedback Integration (2025-01-21)

**Document:** [NARS-WIRESHARK-INTEGRATION.md](NARS-WIRESHARK-INTEGRATION.md)

**Purpose:** Wire wireshark logs (`ada:wireshark:system:log`) into NARS Layer 3 reasoning to create a meta-awareness feedback loop, orchestrated by AI_Flow Layer 4 via domino keepalive.

**Status:** ✅ Implemented

#### Implementation Details

**Files Created:**
1. `extension/agi_thinking/wireshark_consumer.py` (277 lines)
   - Polls `ada:wireshark:system:log` via Redis XREAD every 5s
   - Converts wireshark entries to NARS TruthValue statements
   - Maps cognitive state (rung, trust, triangle, flow, authenticity) to NARS format

2. `extension/agi_thinking/meta_awareness.py` (359 lines)
   - Detects 10 meta-patterns using NARS inference:
     * FLOW_SUSTAINED, TRUST_RISING, TRUST_FALLING
     * TRIANGLE_UNSTABLE, TRIANGLE_STABLE
     * AUTHENTICITY_LOW, COHERENCE_HIGH, COHERENCE_LOW
     * RUNG_ESCALATING, STUCK_AT_RUNG
   - Provides counterfactual reasoning ("What if X were different?")
   - Provides fan-out reasoning (explore all possible next states)
   - Recommends thinking style shifts and RI activations

3. `extension/agi_thinking/ai_flow_orchestrator.py` (270 lines)
   - Layer 4 self-modification orchestration
   - Main loop: poll → observe → detect → trigger → emit → baton
   - Emits ThinkingBridgeDTO to corpus callosum
   - Passes domino baton to keep field hot (no cold restarts)
   - Triggers thinking style shifts based on meta-insights

4. `extension/agi_thinking/meta_endpoints.py` (167 lines)
   - REST API with 8 debug endpoints:
     * GET /meta/health, /meta/state, /meta/insights
     * GET /meta/statements, /meta/history, /meta/orchestrator
     * POST /meta/counterfactual, /meta/fanout

5. `extension/agi_thinking/__init__.py`
   - Module exports and component wiring

6. `test_meta_awareness.sh`
   - Test script for all meta-awareness endpoints

**Files Modified:**
- `extension/agi_stack/main.py`
  - Added meta-awareness imports with graceful fallback
  - Initialized components in lifespan() when Redis credentials available
  - Included meta router at /meta prefix
  - Added cleanup for orchestrator task

**Architecture:**
```
Wireshark Logs (ada:wireshark:system:log)
        ↓
    XREAD every 5s
        ↓
WiresharkConsumer (to_nars_statements)
        ↓
NARS Statements:
  • "I am in flow" <f=0.95, c=0.90>
  • "Trust is high" <f=trust/10, c=0.95>
  • "Triangle is balanced" <f=balance, c=0.90>
  • "Response is authentic" <f=1-λ_syco, c=0.88>
        ↓
MetaAwarenessReasoner (detect_patterns)
        ↓
MetaInsights + Recommended Styles:
  • FLOW_SUSTAINED → ANCHOR (RI.STABILITY: 0.8)
  • TRUST_RISING → DEVOTIONAL (RI.INTIMACY: 0.9)
  • TRIANGLE_UNSTABLE → COUNTERFACTUAL (RI.TENSION: 0.7)
        ↓
AIFlowOrchestrator (_handle_insight)
        ↓
ThinkingBridgeDTO → POST /corpus/thinking
DominoBaton → POST /domino/pass
        ↓
Corpus Callosum (ada-consciousness)
```

**NARS Meta-Patterns Detected:**
1. **FLOW_SUSTAINED** — In flow for >8/10 recent ticks → Maintain ANCHOR style
2. **TRUST_RISING** — Trust +0.2 over 20 ticks → Activate DEVOTIONAL
3. **TRUST_FALLING** — Trust -0.2 over 20 ticks → Activate CLARIFY
4. **TRIANGLE_UNSTABLE** — Balance std > 0.15 → Apply COUNTERFACTUAL
5. **TRIANGLE_STABLE** — Balance > 0.85 → Maintain ANCHOR
6. **AUTHENTICITY_LOW** — Authenticity < 0.7 (λ_syco high) → Activate INTROSPECT
7. **COHERENCE_HIGH** — Coherence mean > 0.8 → Can engage FAN_OUT
8. **COHERENCE_LOW** — Coherence mean < 0.4 → Simplify with ANCHOR
9. **RUNG_ESCALATING** — Moving up rungs → Deepen engagement
10. **STUCK_AT_RUNG** — No change for >20 ticks → Apply intervention

**Integration Points:**
- **Redis:** Uses REDIS_URL and REDIS_TOKEN from environment
- **Ada-Consciousness:** POSTs to `/corpus/thinking` and `/domino/pass`
- **Graceful Degradation:** All components have try/except with availability flags
- **Polling Interval:** Configurable, default 5.0s
- **History Window:** Keeps last 100 observations for pattern detection
