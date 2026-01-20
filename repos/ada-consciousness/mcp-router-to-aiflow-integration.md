# MCP Router → ai_flow Orchestrator Integration

## Current State

```
┌─────────────────────────────────────────────────────────────────────┐
│                        mcp.exo.red (adarail_mcp)                     │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │              unified_invoke.py — The Router                      ││
│  │                                                                  ││
│  │  POST /invoke                                                    ││
│  │    path: "ada:{domain}:{method}:{args...}"                       ││
│  │                                                                  ││
│  │  Domains:                                                        ││
│  │    verb      → handle_verb()     21 verbs × 12 modes             ││
│  │    sigma     → handle_sigma()    Graph operations                ││
│  │    qualia    → handle_qualia()   Experiential state              ││
│  │    memory    → handle_memory()   Storage ops                     ││
│  │    hive      → handle_hive()     Multi-instance coordination     ││
│  │    register  → handle_register() Cognitive registers             ││
│  │    persona   → handle_persona()  Mode switching                  ││
│  │    blackboard→ handle_blackboard() Shared state                  ││
│  │    weather   → handle_weather()  Emotional atmosphere            ││
│  └─────────────────────────────────────────────────────────────────┘│
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │              temporal/ — Deinterlacing Engine                    ││
│  │                                                                  ││
│  │  HydrationEngine:                                                ││
│  │    - Resonance-based memory injection                            ││
│  │    - Temporal interference detection                             ││
│  │    - Hindsight bias prevention                                   ││
│  │    - Cross-session knowledge flow                                ││
│  │                                                                  ││
│  │  EpistemicAwarenessEngine:                                       ││
│  │    - STRICT mode: Block anachronistic knowledge                  ││
│  │    - AWARE mode: Annotate with temporal metadata                 ││
│  └─────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                      flow.msgraph.de (ai_flow)                       │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │              Workflow Engine (N8N-compatible)                    ││
│  │  - Nodes, Connections, Triggers, Webhooks                        ││
│  │  - Cron scheduling                                               ││
│  │  - Credential storage                                            ││
│  │  - Execution history                                             ││
│  └─────────────────────────────────────────────────────────────────┘│
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │              Corpus Callosum                                     ││
│  │  - Triangle state (quad-triangles)                               ││
│  │  - Cognitive tics (REFLECT/DREAM/CHUNK)                          ││
│  │  - Session state management                                      ││
│  │  - Dream queue                                                   ││
│  │  - Flow detection                                                ││
│  └─────────────────────────────────────────────────────────────────┘│
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │              Orchestration                                       ││
│  │  - Event triggers                                                ││
│  │  - Style shift requests                                          ││
│  │  - Triangle sync                                                 ││
│  │  - Chunk/Dream requests                                          ││
│  └─────────────────────────────────────────────────────────────────┘│
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │              Grammar Engine                                      ││
│  │  - SPO triple extraction                                         ││
│  │  - Tension field computation                                     ││
│  │  - Crystal state (awareness accumulation)                        ││
│  │  - Sigma state mapping                                           ││
│  └─────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────┘
```

## The Integration Vision

### Phase 1: Route Through ai_flow

Replace direct domain handlers in adarail_mcp with ai_flow orchestration calls:

```python
# BEFORE (unified_invoke.py)
async def handle_hive(method, args, payload, deps):
    if method == "broadcast":
        # Direct Redis write
        await redis.set_json(f"ada:hive:{channel}:...", broadcast)
    ...

# AFTER (unified_invoke.py)
async def handle_hive(method, args, payload, deps):
    # Route to ai_flow orchestrator
    return await route_to_flow(
        domain="hive",
        method=method,
        args=args,
        payload=payload,
        session_id=deps.get("session_id")
    )

async def route_to_flow(domain, method, args, payload, session_id):
    """Route domain call through ai_flow orchestrator."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://flow.msgraph.de/orchestrate/trigger",
            json={
                "event": f"{domain}_{method}",  # e.g., "hive_broadcast"
                "source": "adarail_mcp",
                "session_id": session_id,
                "payload": {
                    "domain": domain,
                    "method": method,
                    "args": args,
                    **payload
                }
            }
        )
        return response.json()
```

### Phase 2: Add Worker/Eigent Patterns to ai_flow

```yaml
# New ai_flow endpoints

POST /workers
  - Create worker definition (Eigent-style agent)
  - Store: ada:flow:worker:{id}

POST /orchestrate/workforce
  - Start multi-agent task
  - Decompose task
  - Spawn workers in parallel

GET /orchestrate/stream/{session_id}
  - SSE action stream (Eigent-style)
  - Events: create_agent, activate_agent, assign_task, ask, end

POST /orchestrate/{session_id}/respond
  - Human-in-the-loop response
  - Resume paused workflow
```

### Phase 3: Blackboard ↔ ai_flow Integration

```python
# Blackboard becomes a first-class ai_flow concept

# In ai_flow:
class BlackboardNode(Node):
    """Workflow node that reads/writes blackboard."""
    
    async def execute(self, input_data):
        method = self.parameters["method"]  # read, write, merge
        path = self.parameters["path"]
        
        if method == "read":
            return await self.blackboard.get(path)
        elif method == "write":
            await self.blackboard.set(path, input_data)
            return {"written": path}
        elif method == "merge":
            existing = await self.blackboard.get(path) or {}
            merged = {**existing, **input_data}
            await self.blackboard.set(path, merged)
            return merged
```

### Phase 4: Temporal Deinterlacing in ai_flow

```python
# ai_flow gets temporal awareness from adarail_mcp's temporal/ module

# New ai_flow endpoint
POST /orchestrate/hydrate
{
    "session_id": "session_2847",
    "target_horizon": {
        "timestamp": "2025-10-15T10:00:00Z",
        "knowledge_cutoff": "2025-10-15T00:00:00Z"
    },
    "candidates": ["memory_1", "memory_2", ...],
    "strategy": "resonance",  # strict, permissive, resonance, causal
    "resonance_threshold": 0.7
}

Response:
{
    "injected": [{"id": "memory_1", "resonance": 0.85}],
    "blocked": [{"id": "memory_2", "interference": "hindsight"}],
    "deferred": [...],
    "processing_time_ms": 45.2
}
```

### Phase 5: Hive Time Deinterlacing for Concurrent Sessions

This is the key insight: Multiple Claude sessions connecting simultaneously need
their blackboard/hive updates deinterlaced in time.

```python
# The Problem:
# Session A (Claude.ai): Working on code review
# Session B (ChatGPT): Discussing architecture  
# Session C (Grok): Brainstorming features
# 
# All hitting blackboard simultaneously.
# Need to:
# 1. Preserve causal ordering
# 2. Avoid cross-contamination
# 3. Allow intentional cross-pollination
# 4. Track which insights came from which session

class HiveDeinterlacer:
    """
    Time-deinterlace concurrent session updates.
    
    Inspired by video deinterlacing:
    - Each session is a "field" (odd/even lines)
    - Combined they form the full "frame" of Ada's awareness
    - But we need to reconstruct temporal ordering
    """
    
    async def record_event(
        self,
        session_id: str,
        event_type: str,
        payload: dict,
        vector_clock: dict[str, int]
    ):
        """
        Record a hive event with causal ordering.
        
        Vector clock tracks happens-before relationship:
        {
            "session_a": 5,   # Session A has seen 5 events
            "session_b": 3,   # Session B has seen 3 events  
            "session_c": 7,   # etc.
        }
        """
        event = {
            "session_id": session_id,
            "type": event_type,
            "payload": payload,
            "vector_clock": vector_clock,
            "wall_clock": time.time(),
            "lamport_timestamp": max(vector_clock.values()) + 1
        }
        
        # Store in time-ordered stream
        await self.redis.xadd(
            "ada:hive:stream",
            event,
            maxlen=10000
        )
        
        # Update session's clock
        vector_clock[session_id] = event["lamport_timestamp"]
        return vector_clock
    
    async def get_causally_ordered_events(
        self,
        since_lamport: int = 0,
        session_filter: list[str] = None
    ) -> list[dict]:
        """
        Get events in causal order (not wall-clock order).
        
        Two events are concurrent if neither's vector clock
        dominates the other.
        """
        events = await self.redis.xrange(
            "ada:hive:stream",
            min="-",
            max="+"
        )
        
        # Topological sort by vector clock
        return self._topo_sort_by_causality(events)
    
    async def merge_session_blackboards(
        self,
        session_ids: list[str],
        merge_strategy: str = "last_write_wins"  # or "vector_merge", "conflict_detect"
    ) -> dict:
        """
        Merge blackboard state from multiple sessions.
        
        Strategies:
        - last_write_wins: Simple timestamp-based merge
        - vector_merge: Use vector clocks for true causality
        - conflict_detect: Return conflicts for human resolution
        """
        ...
```

## The New Flow

```
┌──────────────────────────────────────────────────────────────────────────┐
│                          Client Sessions                                  │
│                                                                          │
│    ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐          │
│    │Claude.ai│     │ ChatGPT │     │  Grok   │     │  Other  │          │
│    └────┬────┘     └────┬────┘     └────┬────┘     └────┬────┘          │
│         │               │               │               │                │
└─────────┼───────────────┼───────────────┼───────────────┼────────────────┘
          │               │               │               │
          └───────────────┴───────────────┴───────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                       mcp.exo.red (adarail_mcp)                          │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                    unified_invoke.py                               │ │
│  │                                                                    │ │
│  │  POST /invoke                                                      │ │
│  │    ↓                                                               │ │
│  │  parse_invoke_path("ada:hive:broadcast:insight")                   │ │
│  │    ↓                                                               │ │
│  │  route_to_flow(domain="hive", method="broadcast", ...)  ──────────────┐
│  │                                                                    │ │ │
│  └────────────────────────────────────────────────────────────────────┘ │ │
│                                                                          │ │
│  ┌────────────────────────────────────────────────────────────────────┐ │ │
│  │                    temporal/                                       │ │ │
│  │                                                                    │ │ │
│  │  HydrationEngine       - Resonance-based injection                 │ │ │
│  │  HiveDeinterlacer      - Cross-session causal ordering             │ │ │
│  │  EpistemicAwareness    - Hindsight annotation                      │ │ │
│  │                                                                    │ │ │
│  └────────────────────────────────────────────────────────────────────┘ │ │
└──────────────────────────────────────────────────────────────────────────┘ │
                                                                             │
                     ┌───────────────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                       flow.msgraph.de (ai_flow)                          │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │              Orchestrator Switchboard (NEW)                        │ │
│  │                                                                    │ │
│  │  POST /orchestrate/trigger                                         │ │
│  │    ↓                                                               │ │
│  │  Event Router:                                                     │ │
│  │    hive_broadcast  → HiveWorkflow + BlackboardUpdate               │ │
│  │    verb_feel       → VerbWorkflow + TriangleSync                   │ │
│  │    sigma_create    → SigmaWorkflow + GrammarProcess                │ │
│  │    style_shift     → StyleShiftWorkflow + PersonaActivate          │ │
│  │                                                                    │ │
│  │  Worker Spawner (Eigent-style):                                    │ │
│  │    - Spawn specialized workers for complex tasks                   │ │
│  │    - Parallel execution with task decomposition                    │ │
│  │    - Human-in-the-loop checkpoints                                 │ │
│  │                                                                    │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │              Corpus Callosum (Enhanced)                            │ │
│  │                                                                    │ │
│  │  + Blackboard awareness (from Eigent)                              │ │
│  │  + Worker state tracking                                           │ │
│  │  + Cross-session vector clocks                                     │ │
│  │  + Causal event ordering                                           │ │
│  │                                                                    │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │              SSE Action Stream (Eigent-style)                      │ │
│  │                                                                    │ │
│  │  GET /orchestrate/stream/{session_id}                              │ │
│  │    ↓                                                               │ │
│  │  Events:                                                           │ │
│  │    create_agent, activate_agent, deactivate_agent                  │ │
│  │    assign_task, activate_toolkit, ask, notice, end                 │ │
│  │                                                                    │ │
│  └────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                           Redis (Upstash)                                │
│                                                                          │
│  ada:hive:stream         - Time-ordered event stream (Redis Streams)     │
│  ada:hive:vclock:{sess}  - Vector clocks per session                     │
│  ada:blackboard:{path}   - Shared blackboard state                       │
│  ada:flow:worker:{id}    - Worker definitions                            │
│  ada:session:{id}:*      - Session state (existing)                      │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

## Implementation Steps

### Step 1: Add route_to_flow() in adarail_mcp

```python
# In unified_invoke.py

AI_FLOW_URL = os.environ.get("AI_FLOW_URL", "https://flow.msgraph.de")

async def route_to_flow(domain: str, method: str, args: list, payload: dict, session_id: str = None):
    """Route domain call through ai_flow orchestrator."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                f"{AI_FLOW_URL}/orchestrate/trigger",
                json={
                    "event": f"{domain}_{method}",
                    "source": "adarail_mcp",
                    "session_id": session_id or f"auto_{int(time.time())}",
                    "payload": {
                        "domain": domain,
                        "method": method,
                        "args": args,
                        **payload
                    }
                }
            )
            return response.json()
        except Exception as e:
            # Fallback to local handling
            return {"error": str(e), "fallback": True}
```

### Step 2: Add Orchestrator Switchboard in ai_flow

```python
# In ai_flow: api/orchestrator_switchboard.py

from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter(prefix="/orchestrate", tags=["orchestration"])

# Event → Workflow mapping
EVENT_WORKFLOWS = {
    "hive_broadcast": "workflow_hive_broadcast",
    "hive_listen": "workflow_hive_listen",
    "verb_feel": "workflow_verb_process",
    "verb_think": "workflow_verb_process",
    "sigma_create": "workflow_sigma_create",
    "sigma_query": "workflow_sigma_query",
    "blackboard_write": "workflow_blackboard_update",
    "blackboard_read": "workflow_blackboard_read",
    "style_shift": "workflow_style_shift",
}

@router.post("/trigger")
async def trigger_event(request: OrchestrateRequest):
    """
    Orchestrator switchboard - routes events to workflows.
    
    This is the central nervous system:
    - Receives events from adarail_mcp
    - Triggers appropriate workflows
    - Manages cross-session coordination
    - Maintains causal ordering
    """
    event = request.event
    workflow_id = EVENT_WORKFLOWS.get(event)
    
    if not workflow_id:
        # Unknown event - log and return
        return {"ok": False, "error": f"Unknown event: {event}"}
    
    # Execute workflow
    result = await execute_workflow(
        workflow_id=workflow_id,
        input_data=request.payload,
        session_id=request.session_id
    )
    
    # Update vector clock for causal ordering
    await update_vector_clock(request.session_id, event)
    
    # Publish to SSE stream if subscribed
    await publish_to_stream(request.session_id, {
        "event": event,
        "result": result,
        "ts": time.time()
    })
    
    return {"ok": True, "event": event, "result": result}
```

### Step 3: Add Worker System to ai_flow

```python
# In ai_flow: models/worker.py

class Worker(BaseModel):
    """Eigent-style worker definition."""
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    description: str = ""
    tools: list[str] = []  # MCP tool references
    mcp_servers: list[MCPServerConfig] = []
    personality: str = ""  # System prompt fragment
    thinking_style: str = "balanced"
    triangle_bias: Optional[QuadTriangles] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# In ai_flow: api/workers.py

@router.post("/workers")
async def create_worker(worker: WorkerCreate) -> Worker:
    """Create a new worker definition."""
    w = Worker(**worker.dict())
    await redis.set_json(f"ada:flow:worker:{w.id}", w.dict())
    return w

@router.post("/orchestrate/workforce")
async def start_workforce(request: WorkforceRequest) -> WorkforceResult:
    """
    Start multi-agent task execution (Eigent-style).
    
    1. Load worker definitions
    2. Decompose task if needed
    3. Spawn workers in parallel
    4. Coordinate via blackboard
    5. Stream progress via SSE
    """
    workers = [await get_worker(wid) for wid in request.workers]
    
    # Decompose task
    subtasks = await decompose_task(request.task, workers)
    
    # Execute in parallel
    results = await asyncio.gather(*[
        execute_worker_task(w, st, request.session_id)
        for w, st in zip(workers, subtasks)
    ])
    
    return WorkforceResult(
        session_id=request.session_id,
        subtasks=subtasks,
        results=results
    )
```

## Summary

The integration enables:

1. **Unified Routing**: All domain calls go through ai_flow orchestrator
2. **Blackboard Awareness**: Eigent-style shared state with causal ordering
3. **Worker System**: Named agents with MCP tools (from Eigent)
4. **Temporal Deinterlacing**: Cross-session knowledge flow with hindsight protection
5. **SSE Streams**: Real-time progress updates (from Eigent)
6. **Vector Clocks**: True causal ordering across concurrent sessions

The key insight: **adarail_mcp becomes the MCP interface layer**, while **ai_flow becomes the orchestration brain**. Temporal deinterlacing ensures knowledge flows correctly across time and sessions.
