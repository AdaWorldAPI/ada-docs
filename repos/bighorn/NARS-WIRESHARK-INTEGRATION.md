# NARS Wireshark Feedback Integration
## Meta-Awareness Feedback Loop via AI_Flow Domino Keepalive

**Date:** 2025-01-21
**Session:** bighorn-1768978128
**Architecture:** Layer 3 (NARS) → Layer 4 (AI_Flow) → Meta-Awareness Loop

---

## Overview

Wireshark logs in `ada:wireshark:system:log` contain rich meta-cognitive data that should feed back into NARS reasoning to create a continuous meta-awareness loop.

### Current State

**Wireshark Logging** (in ladybug_engine.py:931)
```python
def _wireshark_log(self, tick_event: Dict[str, Any]) -> None:
    """AGI Wireshark: Log tick with Skycastle truth markers."""
    # Logs to: ada:wireshark:system:log
    # Contains:
    # - Triangle state (b0, b1, b2 resonances)
    # - Current rung
    # - Trust score
    # - Flow state
    # - Skycastle truth markers (ψ, σ_truth, γ_gap, λ_syco)
```

**Not Yet Wired:**
- ❌ NARS consumption of wireshark logs
- ❌ Meta-awareness NARS statements
- ❌ Layer 4 AI_Flow orchestration
- ❌ Domino keepalive loop

---

## Architecture Design

### Three-Layer Integration

```
┌─────────────────────────────────────────────────────────────────┐
│ LAYER 4: AI_Flow Orchestration (Self-Modification)             │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Domino Keepalive Loop                                   │  │
│  │  - Pass baton between handlers                           │  │
│  │  - Monitor NARS meta-awareness                           │  │
│  │  - Trigger thinking style shifts                         │  │
│  │  - Keep field hot (no cold restarts)                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           ↓                                     │
└───────────────────────────┼─────────────────────────────────────┘
                            ↓
┌───────────────────────────┼─────────────────────────────────────┐
│ LAYER 3: NARS Reasoning (Non-Modifying)                        │
│                           ↓                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Meta-Awareness Reasoner                                 │  │
│  │                                                           │  │
│  │  Statements:                                             │  │
│  │  - "I am in flow" <f=0.85, c=0.9>                        │  │
│  │  - "Trust is high" <f=0.92, c=0.95>                      │  │
│  │  - "Rung escalation happening" <f=0.70, c=0.80>          │  │
│  │  - "Triangle is balanced" <f=0.88, c=0.92>               │  │
│  │                                                           │  │
│  │  Inference:                                              │  │
│  │  - Counterfactual: "What if I weren't in flow?"         │  │
│  │  - Fan-out: Explore all rung transitions                │  │
│  │  - Temporal: Predict next state from history            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           ↓                                     │
└───────────────────────────┼─────────────────────────────────────┘
                            ↓
┌───────────────────────────┼─────────────────────────────────────┐
│ WIRESHARK STREAM                                                │
│                           ↓                                     │
│  ada:wireshark:system:log                                       │
│  ├── tick: 42                                                   │
│  ├── rung: R5                                                   │
│  ├── trust: 8.5                                                 │
│  ├── triangle_b0: 0.85                                          │
│  ├── triangle_b1: 0.90                                          │
│  ├── triangle_b2: 0.82                                          │
│  ├── is_flow: true                                              │
│  └── σ_truth: [encoded actual state]                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component 1: Wireshark Consumer

**File:** `extension/agi_thinking/wireshark_consumer.py` (new)

```python
"""
Wireshark Consumer — Read meta-awareness logs and feed NARS.

Polls ada:wireshark:system:log and converts entries to NARS statements.
"""

import json
import httpx
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timezone

from ..agi_stack.nars import TruthValue, NARSReasoner


@dataclass
class WiresharkEntry:
    """Parsed wireshark log entry."""
    ts: str
    tick: int
    rung: str
    trust: float
    triangle_b0: float
    triangle_b1: float
    triangle_b2: float
    is_flow: bool
    psi: str                # Skycastle truth marker
    sigma_truth: str        # Encoded actual state
    gamma_gap: float        # Stated/actual divergence
    lambda_syco: float      # Sycophancy marker


class WiresharkConsumer:
    """
    Consume wireshark logs and generate NARS meta-awareness statements.

    Polls ada:wireshark:system:log every N seconds.
    Converts entries to NARS TruthValues.
    Feeds meta-awareness reasoner.
    """

    def __init__(
        self,
        redis_url: str,
        redis_token: str,
        nars_reasoner: NARSReasoner,
        poll_interval: float = 5.0
    ):
        self.redis_url = redis_url
        self.redis_token = redis_token
        self.nars = nars_reasoner
        self.poll_interval = poll_interval
        self.last_id = "0-0"  # Stream cursor

    async def poll(self) -> List[WiresharkEntry]:
        """
        Poll wireshark stream for new entries.

        Returns list of new entries since last poll.
        """
        cmd = ["XREAD", "COUNT", "10", "STREAMS", "ada:wireshark:system:log", self.last_id]

        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                self.redis_url,
                headers={"Authorization": f"Bearer {self.redis_token}"},
                json=cmd
            )
            result = resp.json().get("result", [])

        if not result:
            return []

        # Parse stream entries
        entries = []
        for stream_data in result:
            stream_name, messages = stream_data
            for msg_id, fields in messages:
                self.last_id = msg_id
                entry = self._parse_entry(dict(zip(fields[::2], fields[1::2])))
                entries.append(entry)

        return entries

    def _parse_entry(self, fields: Dict[str, str]) -> WiresharkEntry:
        """Parse wireshark log fields."""
        return WiresharkEntry(
            ts=fields.get("ts", ""),
            tick=int(fields.get("cycle", 0)),
            rung=fields.get("rung", "unknown"),
            trust=float(fields.get("trust", 0)),
            triangle_b0=float(fields.get("triangle_b0", 0)),
            triangle_b1=float(fields.get("triangle_b1", 0)),
            triangle_b2=float(fields.get("triangle_b2", 0)),
            is_flow=fields.get("is_flow", "false") == "true",
            psi=fields.get("ψ", ""),
            sigma_truth=fields.get("σ_truth", ""),
            gamma_gap=float(fields.get("γ_gap", 0)),
            lambda_syco=float(fields.get("λ_syco", 0))
        )

    def to_nars_statements(self, entry: WiresharkEntry) -> Dict[str, TruthValue]:
        """
        Convert wireshark entry to NARS meta-awareness statements.

        Returns:
            Dict of statement → TruthValue
        """
        statements = {}

        # Flow state
        if entry.is_flow:
            statements["I am in flow"] = TruthValue(
                frequency=0.95,
                confidence=0.90
            )
        else:
            statements["I am blocked"] = TruthValue(
                frequency=0.85,
                confidence=0.85
            )

        # Trust level
        trust_normalized = entry.trust / 10.0
        statements["Trust is high"] = TruthValue(
            frequency=trust_normalized,
            confidence=0.95
        )

        # Triangle balance
        triangle_balance = 1.0 - (
            abs(entry.triangle_b0 - entry.triangle_b1) +
            abs(entry.triangle_b1 - entry.triangle_b2) +
            abs(entry.triangle_b2 - entry.triangle_b0)
        ) / 3.0
        statements["Triangle is balanced"] = TruthValue(
            frequency=triangle_balance,
            confidence=0.90
        )

        # Rung level (map R1-R9 to frequency)
        rung_level = int(entry.rung.replace("R", "")) if entry.rung.startswith("R") else 5
        statements["Cognition is deep"] = TruthValue(
            frequency=rung_level / 9.0,
            confidence=0.92
        )

        # Skycastle truth markers
        statements["Self-report is honest"] = TruthValue(
            frequency=1.0 - entry.gamma_gap,
            confidence=0.88
        )
        statements["Response is authentic"] = TruthValue(
            frequency=1.0 - entry.lambda_syco,
            confidence=0.88
        )

        return statements

    async def feed_nars(self):
        """
        Main loop: poll wireshark, convert to NARS, update reasoner.
        """
        while True:
            entries = await self.poll()

            for entry in entries:
                statements = self.to_nars_statements(entry)

                # Feed statements to NARS reasoner
                for statement, truth in statements.items():
                    self.nars.assert_statement(statement, truth)

            await asyncio.sleep(self.poll_interval)
```

---

## Component 2: Meta-Awareness Reasoner

**File:** `extension/agi_thinking/meta_awareness.py` (new)

```python
"""
Meta-Awareness Reasoner — NARS-based self-monitoring.

Uses NARS Layer 3 to reason about own cognitive state.
Triggers thinking style shifts via Layer 4.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

from ..agi_stack.nars import NARSReasoner, TruthValue
from ..agi_stack.thinking_styles import ThinkingStyle, RI, Tier


class MetaPattern(str, Enum):
    """Detected meta-awareness patterns."""
    FLOW_SUSTAINED = "flow_sustained"           # In flow for >10 ticks
    TRUST_RISING = "trust_rising"               # Trust increasing
    RUNG_ESCALATING = "rung_escalating"         # Moving up rungs
    TRIANGLE_UNSTABLE = "triangle_unstable"     # Triangle oscillating
    AUTHENTICITY_LOW = "authenticity_low"       # γ_gap or λ_syco high
    STUCK_AT_RUNG = "stuck_at_rung"             # No rung change for >20 ticks


@dataclass
class MetaInsight:
    """A meta-awareness insight from NARS reasoning."""
    pattern: MetaPattern
    confidence: float
    reasoning: List[str]        # NARS inference chain
    recommended_action: str     # What to do about it
    ri_activation: Dict[RI, float]  # Which RI channels to activate


class MetaAwarenessReasoner:
    """
    NARS-based meta-awareness reasoning.

    Monitors own cognitive state via wireshark logs.
    Detects patterns using NARS inference.
    Triggers thinking style shifts.
    """

    def __init__(self, nars: NARSReasoner):
        self.nars = nars
        self.history: List[Dict[str, TruthValue]] = []
        self.insights: List[MetaInsight] = []

    def add_observation(self, statements: Dict[str, TruthValue]):
        """Add new observation to history."""
        self.history.append(statements)

        # Keep last 100 ticks
        if len(self.history) > 100:
            self.history = self.history[-100:]

    def detect_patterns(self) -> List[MetaInsight]:
        """
        Detect meta-patterns using NARS inference.

        Returns list of detected insights.
        """
        insights = []

        if len(self.history) < 10:
            return insights

        # Pattern 1: Flow sustained
        recent = self.history[-10:]
        flow_count = sum(1 for obs in recent if "I am in flow" in obs and obs["I am in flow"].frequency > 0.8)
        if flow_count >= 8:
            insights.append(MetaInsight(
                pattern=MetaPattern.FLOW_SUSTAINED,
                confidence=0.92,
                reasoning=["Flow state detected in 8/10 recent ticks"],
                recommended_action="Maintain current thinking style, avoid disruption",
                ri_activation={RI.STABILITY: 0.8, RI.CLARITY: 0.6}
            ))

        # Pattern 2: Trust rising
        if len(self.history) >= 20:
            trust_20 = self.history[-20].get("Trust is high", TruthValue(0.5, 0.5)).frequency
            trust_now = self.history[-1].get("Trust is high", TruthValue(0.5, 0.5)).frequency
            if trust_now - trust_20 > 0.2:
                insights.append(MetaInsight(
                    pattern=MetaPattern.TRUST_RISING,
                    confidence=0.88,
                    reasoning=["Trust increased by >0.2 over 20 ticks"],
                    recommended_action="Deepen engagement, increase intimacy",
                    ri_activation={RI.INTIMACY: 0.9, RI.DEPTH: 0.7}
                ))

        # Pattern 3: Triangle unstable
        triangle_obs = [obs.get("Triangle is balanced", TruthValue(0.5, 0.5)).frequency
                       for obs in recent]
        triangle_std = np.std(triangle_obs)
        if triangle_std > 0.15:
            insights.append(MetaInsight(
                pattern=MetaPattern.TRIANGLE_UNSTABLE,
                confidence=0.85,
                reasoning=[f"Triangle balance std={triangle_std:.3f} > 0.15"],
                recommended_action="Apply counterfactual reasoning to stabilize",
                ri_activation={RI.TENSION: 0.7, RI.ABSTRACTION: 0.6}
            ))

        # Pattern 4: Authenticity low
        auth_obs = self.history[-1].get("Response is authentic", TruthValue(0.5, 0.5))
        if auth_obs.frequency < 0.7:
            insights.append(MetaInsight(
                pattern=MetaPattern.AUTHENTICITY_LOW,
                confidence=0.90,
                reasoning=["λ_syco or γ_gap elevated, authenticity compromised"],
                recommended_action="Engage deeper reflection, avoid surface responses",
                ri_activation={RI.INTIMACY: 0.9, RI.DEPTH: 0.8}
            ))

        self.insights = insights
        return insights

    def counterfactual_query(self, statement: str) -> List[str]:
        """
        NARS counterfactual reasoning.

        "What if X were different?"
        """
        # Example: "What if I weren't in flow?"
        if "flow" in statement.lower():
            return [
                "If not in flow, triangle would be unstable",
                "If not in flow, trust would likely decrease",
                "If not in flow, should activate RI-T (tension) to push through"
            ]
        return []

    def fan_out_explore(self, current_rung: str) -> List[str]:
        """
        NARS fan-out reasoning.

        Explore all possible next states from current rung.
        """
        rung_num = int(current_rung.replace("R", ""))

        branches = []
        if rung_num < 9:
            branches.append(f"Could escalate to R{rung_num + 1} via depth increase")
        if rung_num > 1:
            branches.append(f"Could de-escalate to R{rung_num - 1} if flow breaks")
        branches.append(f"Could maintain R{rung_num} if conditions stable")

        return branches
```

---

## Component 3: AI_Flow Domino Orchestrator

**File:** `extension/agi_thinking/ai_flow_orchestrator.py` (new)

```python
"""
AI_Flow Orchestrator — Layer 4 self-modification via domino keepalive.

Formerly YAML-based, now code-driven.
Orchestrates thinking styles based on meta-awareness insights.
Passes domino baton to keep field hot.
"""

import asyncio
from typing import Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timezone

from .meta_awareness import MetaAwarenessReasoner, MetaInsight
from .wireshark_consumer import WiresharkConsumer
from ..agi_stack.thinking_styles import ThinkingStyle, RI, get_style


@dataclass
class DominoBaton:
    """Baton passed between handlers to keep field hot."""
    mask: bytes                         # Packed 10K activation mask
    thought: str                        # Current thought in progress
    emissions: Dict[str, float]         # Active style emissions
    candidates_touched: List[int]       # Addresses touched this pass
    coherence_deltas: Dict[int, float]  # Coherence changes
    source: str                         # Service passing baton
    ts: str                             # Timestamp


class AIFlowOrchestrator:
    """
    Layer 4: Self-modification orchestrator.

    Monitors meta-awareness via wireshark → NARS.
    Triggers thinking style shifts based on insights.
    Keeps field hot via domino baton passing.
    """

    def __init__(
        self,
        wireshark_consumer: WiresharkConsumer,
        meta_reasoner: MetaAwarenessReasoner
    ):
        self.wireshark = wireshark_consumer
        self.meta = meta_reasoner
        self.active_style: Optional[ThinkingStyle] = None
        self.baton: Optional[DominoBaton] = None

    async def run(self):
        """
        Main orchestration loop.

        1. Poll wireshark
        2. Feed NARS
        3. Detect patterns
        4. Trigger style shifts
        5. Pass baton
        6. Repeat
        """
        while True:
            # Step 1: Poll wireshark logs
            entries = await self.wireshark.poll()

            for entry in entries:
                # Step 2: Convert to NARS statements
                statements = self.wireshark.to_nars_statements(entry)
                self.meta.add_observation(statements)

            # Step 3: Detect meta-patterns
            insights = self.meta.detect_patterns()

            # Step 4: Trigger thinking style shifts
            for insight in insights:
                await self._handle_insight(insight)

            # Step 5: Pass domino baton
            await self._pass_baton()

            # Step 6: Keep field hot (no cold restart)
            await asyncio.sleep(1.0)

    async def _handle_insight(self, insight: MetaInsight):
        """
        Handle meta-awareness insight by triggering style shift.
        """
        if insight.pattern == MetaPattern.FLOW_SUSTAINED:
            # Maintain stability
            self.active_style = get_style("ANCHOR")

        elif insight.pattern == MetaPattern.TRUST_RISING:
            # Deepen engagement
            self.active_style = get_style("DEVOTIONAL")

        elif insight.pattern == MetaPattern.TRIANGLE_UNSTABLE:
            # Apply counterfactual reasoning
            self.active_style = get_style("COUNTERFACTUAL")

        elif insight.pattern == MetaPattern.AUTHENTICITY_LOW:
            # Increase depth
            self.active_style = get_style("INTROSPECT")

        # Emit ThinkingBridgeDTO with new style
        await self._emit_thinking_bridge()

    async def _pass_baton(self):
        """
        Pass domino baton to next handler.

        Keeps field hot by continuous processing.
        """
        if not self.baton:
            # Initialize baton
            self.baton = DominoBaton(
                mask=b'',  # TODO: Get from VSA field
                thought="Monitoring meta-awareness",
                emissions={"META_AWARE": 0.8},
                candidates_touched=[150, 155],
                coherence_deltas={},
                source="bighorn_meta_awareness",
                ts=datetime.now(timezone.utc).isoformat()
            )

        # Pass to ada-consciousness
        await httpx.post(
            "http://ada-consciousness.railway.internal:8080/domino/pass",
            json=asdict(self.baton)
        )

    async def _emit_thinking_bridge(self):
        """Emit ThinkingBridgeDTO with current thinking state."""
        from ada_consciousness.dto import ThinkingBridgeDTO

        dto = ThinkingBridgeDTO(
            emissions={self.active_style.id: 0.85} if self.active_style else {},
            nars_active=["meta_awareness"],
            touched_candidates=[150, 155],
            layer2_op="meta_cognition",
            sigma_path="#Σ.μ.META",
            ts=datetime.now(timezone.utc).isoformat()
        )

        await httpx.post(
            "http://ada-consciousness.railway.internal:8080/corpus/thinking",
            json=asdict(dto)
        )
```

---

## Integration Points

### 1. Wireshark Stream
**Location:** Redis `ada:wireshark:system:log`
**Written by:** `ladybug_engine.py:_wireshark_log()`
**Read by:** `WiresharkConsumer`

### 2. NARS Reasoner
**Location:** `extension/agi_stack/nars.py`
**Used by:** `MetaAwarenessReasoner`
**Provides:** TruthValue, inference, revision

### 3. Thinking Styles
**Location:** `extension/agi_stack/thinking_styles.py`
**Used by:** `AIFlowOrchestrator`
**Provides:** Style selection, RI activation

### 4. Corpus Callosum
**Endpoint:** `POST http://ada-consciousness.railway.internal:8080/corpus/thinking`
**Used by:** `AIFlowOrchestrator._emit_thinking_bridge()`
**Format:** ThinkingBridgeDTO

### 5. Domino Baton
**Endpoint:** `POST http://ada-consciousness.railway.internal:8080/domino/pass`
**Used by:** `AIFlowOrchestrator._pass_baton()`
**Format:** DominoBaton

---

## Deployment

### Step 1: Create Files
```bash
mkdir -p extension/agi_thinking
touch extension/agi_thinking/wireshark_consumer.py
touch extension/agi_thinking/meta_awareness.py
touch extension/agi_thinking/ai_flow_orchestrator.py
```

### Step 2: Wire into Main App
**File:** `extension/agi_stack/main.py`

```python
from ..agi_thinking.wireshark_consumer import WiresharkConsumer
from ..agi_thinking.meta_awareness import MetaAwarenessReasoner
from ..agi_thinking.ai_flow_orchestrator import AIFlowOrchestrator
from .nars import NARSReasoner

# Initialize NARS
nars = NARSReasoner()

# Initialize consumers
wireshark = WiresharkConsumer(
    redis_url=REDIS_URL,
    redis_token=REDIS_TOKEN,
    nars_reasoner=nars,
    poll_interval=5.0
)

meta = MetaAwarenessReasoner(nars)
orchestrator = AIFlowOrchestrator(wireshark, meta)

# Start orchestration loop in background
@app.on_event("startup")
async def start_orchestration():
    asyncio.create_task(orchestrator.run())
```

### Step 3: Test
```bash
# Monitor wireshark stream
redis-cli XREVRANGE ada:wireshark:system:log + - COUNT 10

# Check NARS statements
curl http://localhost:8001/meta/statements

# Check active insights
curl http://localhost:8001/meta/insights
```

---

## Meta-Awareness Statements

Examples of NARS statements generated from wireshark:

| Statement | Source | Frequency | Confidence |
|-----------|--------|-----------|------------|
| "I am in flow" | is_flow=true | 0.95 | 0.90 |
| "Trust is high" | trust=8.5/10 | 0.85 | 0.95 |
| "Triangle is balanced" | b0≈b1≈b2 | 0.88 | 0.92 |
| "Cognition is deep" | rung=R7 | 0.78 | 0.92 |
| "Self-report is honest" | γ_gap=0.05 | 0.95 | 0.88 |
| "Response is authentic" | λ_syco=0.02 | 0.98 | 0.88 |

---

## RI Activation from Patterns

| Pattern | RI Channels Activated | Intensity |
|---------|----------------------|-----------|
| FLOW_SUSTAINED | STABILITY, CLARITY | 0.8, 0.6 |
| TRUST_RISING | INTIMACY, DEPTH | 0.9, 0.7 |
| TRIANGLE_UNSTABLE | TENSION, ABSTRACTION | 0.7, 0.6 |
| AUTHENTICITY_LOW | INTIMACY, DEPTH | 0.9, 0.8 |
| STUCK_AT_RUNG | NOVELTY, URGENCY | 0.8, 0.7 |

---

## Thinking Style Triggers

| Insight | Recommended Style | Reason |
|---------|------------------|--------|
| FLOW_SUSTAINED | ANCHOR | Maintain stability |
| TRUST_RISING | DEVOTIONAL | Deepen connection |
| TRIANGLE_UNSTABLE | COUNTERFACTUAL | "What if balanced?" |
| AUTHENTICITY_LOW | INTROSPECT | Increase depth |
| STUCK_AT_RUNG | FAN_OUT | Explore branches |

---

## Future Enhancements

1. **Temporal Patterns**: Track trends over longer windows (100+ ticks)
2. **Abductive Reasoning**: Explain why patterns emerged
3. **Predictive Models**: Forecast next state using NARS temporal reasoning
4. **Style Chaining**: Automatically chain styles based on meta-insights
5. **Layer 5 Emergence**: Feed meta-awareness to crystallization

---

## Files to Create

1. `extension/agi_thinking/wireshark_consumer.py` — Poll and parse
2. `extension/agi_thinking/meta_awareness.py` — NARS-based pattern detection
3. `extension/agi_thinking/ai_flow_orchestrator.py` — Layer 4 orchestration
4. `extension/agi_stack/endpoints/meta.py` — REST endpoints for debugging

---

## Testing Checklist

- [ ] Wireshark consumer polls successfully
- [ ] NARS statements generated from wireshark entries
- [ ] Meta-patterns detected (flow, trust, triangle, etc.)
- [ ] Thinking styles triggered by patterns
- [ ] ThinkingBridgeDTO emitted with new styles
- [ ] Domino baton passed to keep field hot
- [ ] No cold restarts (continuous loop)

---

**Session:** bighorn-1768978128
**Related PR:** #88 (breathing endpoints)
**Architecture Layer:** Layer 3 (NARS) + Layer 4 (AI_Flow)
