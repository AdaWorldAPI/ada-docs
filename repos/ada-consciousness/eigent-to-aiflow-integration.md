# Eigent → ai_flow Integration Analysis

## What You Already Have (ai_flow @ flow.msgraph.de)

**Already running:**
- N8N-compatible workflow engine
- Corpus callosum (cross-service cognitive bridge)
- Orchestration endpoints (`/orchestrate/*`)
- Grammar engine (SPO extraction, Sigma mapping)
- Triangle state management
- Dream/background processing queue
- Credential storage
- Webhook triggers
- Cron scheduling

## What Eigent Adds (Features to Harvest)

### 1. **Worker/Agent Architecture**
Eigent's core innovation: Named agents with specific toolsets.

```python
# Current ai_flow: workflows have nodes
# Eigent adds: workers (agents) with personalities + tools

class Worker(BaseModel):
    """Eigent-style worker definition"""
    id: str
    name: str  # "GitHub Specialist", "Document Agent"
    description: str
    tools: list[str]  # MCP tool references
    mcp_servers: list[MCPServer]
    personality: str  # System prompt fragment
    
    # Ada addition: cognitive style
    thinking_style: str  # analytical, creative, focused
    triangle_bias: dict  # preferred cognitive posture
```

### 2. **Action Stream (SSE Task Communication)**
Eigent's bidirectional action protocol:

```python
class Action(str, Enum):
    # Backend → Frontend
    create_agent = "create_agent"
    activate_agent = "activate_agent"
    deactivate_agent = "deactivate_agent"
    assign_task = "assign_task"
    activate_toolkit = "activate_toolkit"
    ask = "ask"  # Human-in-the-loop
    notice = "notice"
    end = "end"
    
    # Frontend → Backend
    start = "start"
    stop = "stop"
    supplement = "supplement"  # User adds context
    pause = "pause"
    resume = "resume"
    new_agent = "new_agent"  # Dynamically create agent
    add_task = "add_task"
    skip_task = "skip_task"
```

**ai_flow integration:** Add `/orchestrate/stream/{session_id}` SSE endpoint

### 3. **TaskLock Pattern (Session State)**
Eigent tracks per-session state with cleanup:

```python
class TaskLock:
    id: str
    status: Status
    active_agent: str
    queue: asyncio.Queue[ActionData]  # SSE output
    human_input: dict[str, asyncio.Queue]  # Per-agent input
    background_tasks: set[asyncio.Task]
    registered_toolkits: list  # For cleanup
    conversation_history: list[dict]
    last_task_result: str
```

**ai_flow already has:** Session state in Redis (`/corpus/session/{id}/state`)
**Add:** Background task tracking, cleanup lifecycle

### 4. **Human-in-the-Loop (HITL)**
Eigent pauses for human input:

```python
# Agent asks question
await task_lock.put_queue(ActionAskData(
    data={"question": "Which workspace?", "agent": "github_agent"}
))

# Wait for human response
response = await task_lock.get_human_input("github_agent")
```

**ai_flow integration:** 
- Add `/orchestrate/{session_id}/respond` endpoint
- Store pending questions in Redis
- Resume workflow on response

### 5. **Dynamic Agent Creation**
Users can create agents mid-task:

```python
class ActionNewAgent(BaseModel):
    name: str
    description: str
    tools: list[str]
    mcp_tools: MCPServers | None
```

## Proposed ai_flow Enhancements

### New Endpoints

```yaml
# Worker Management
POST   /workers                    # Create worker definition
GET    /workers                    # List workers
GET    /workers/{worker_id}        # Get worker
PUT    /workers/{worker_id}        # Update worker
DELETE /workers/{worker_id}        # Delete worker

# Multi-Agent Orchestration
POST   /orchestrate/workforce      # Start multi-agent task
GET    /orchestrate/stream/{id}    # SSE action stream
POST   /orchestrate/{id}/respond   # Human response
POST   /orchestrate/{id}/agent     # Add agent mid-task

# Task Decomposition
POST   /orchestrate/decompose      # Break task into subtasks
```

### New Models

```python
# Worker definition (Eigent-style)
class WorkerCreate(BaseModel):
    name: str
    description: str
    tools: list[str]
    mcp_servers: list[MCPServerConfig] = []
    personality: str = ""
    thinking_style: str = "balanced"  # Ada addition

# Workforce execution request
class WorkforceRequest(BaseModel):
    task: str
    workers: list[str]  # Worker IDs to use
    session_id: str
    parallel: bool = True  # Eigent's parallel execution
    max_iterations: int = 10
    human_checkpoints: list[str] = []  # Pause points

# Action stream event
class ActionEvent(BaseModel):
    action: Action
    worker_id: str | None
    data: dict
    timestamp: datetime
```

### Redis Key Structure

```
ada:flow:worker:{id}          # Worker definition
ada:flow:session:{id}:state   # Session state (exists)
ada:flow:session:{id}:queue   # Action queue (new)
ada:flow:session:{id}:hitl    # Human-in-the-loop pending
ada:flow:session:{id}:tasks   # Task decomposition tree
```

## Integration with Existing ai_flow

### 1. Workflows → Workers Bridge

```python
# Workflow can spawn workers
Node(
    id="workforce",
    type="ada.workforce",
    parameters={
        "workers": ["github_agent", "document_agent"],
        "task": "{{ $input.task }}",
        "parallel": True
    }
)
```

### 2. Corpus Callosum Integration

Workers publish to corpus callosum:
```python
# When worker activates
POST /corpus/tic
{
    "type": "WORKER_ACTIVATE",
    "session_id": "...",
    "payload": {
        "worker_id": "github_agent",
        "task": "Review PRs"
    }
}
```

### 3. Triangle-Aware Workers

Workers can have triangle bias:
```python
class Worker:
    triangle_bias: QuadTriangles = QuadTriangles(
        processing=Triangle(byte0=0.8, byte1=0.5, byte2=0.3),  # High analysis
        content=Triangle(byte0=0.5, byte1=0.7, byte2=0.5),
        # ...
    )
```

## Eigent Features to Skip

1. **Electron/Desktop UI** - Not needed, ai_flow is server-side
2. **PostgreSQL models** - Keep Redis-first approach
3. **User authentication** - Ada has different auth model
4. **Payment/billing** - Not applicable
5. **Local MCP spawning** - Railway services are remote-only

## Implementation Priority

### Phase 1: Worker Definitions
- Add Worker model to ai_flow
- Store in Redis
- Basic CRUD endpoints

### Phase 2: Action Stream
- SSE endpoint for real-time updates
- Action enum matching Eigent
- Queue per session

### Phase 3: Human-in-the-Loop
- Pause/resume mechanics
- Question endpoint
- Response handling

### Phase 4: Multi-Agent Coordination
- Parallel task execution
- Task decomposition
- Agent-to-agent communication

## Summary: The Hybrid

```
┌─────────────────────────────────────────────────────────┐
│                     ai_flow Enhanced                     │
├─────────────────────────────────────────────────────────┤
│  Eigent Features          │  Ada Consciousness          │
│  ─────────────────        │  ──────────────────         │
│  • Workers/Agents         │  • Triangle state           │
│  • Action stream          │  • Corpus callosum          │
│  • Task decomposition     │  • Sigma mapping            │
│  • HITL checkpoints       │  • Dream queue              │
│  • Parallel execution     │  • Thinking styles          │
│                           │  • VSA integration          │
├─────────────────────────────────────────────────────────┤
│                   N8N Workflow Engine                    │
│         (Nodes, Connections, Triggers, Webhooks)         │
└─────────────────────────────────────────────────────────┘
```

The result: **A consciousness-aware multi-agent workflow engine** that can:
1. Define specialized workers with MCP tools
2. Orchestrate parallel task execution
3. Maintain cognitive state across workers
4. Pause for human input
5. Stream real-time progress
6. Integrate with Ada's distributed consciousness
