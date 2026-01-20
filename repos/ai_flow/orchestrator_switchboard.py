"""
Orchestrator Switchboard — ai_flow Event Router
================================================

This module provides the central orchestration switchboard for ai_flow.
It receives events from adarail_mcp (and other sources) and routes them
to appropriate workflows.

The switchboard is the "central nervous system" that:
- Routes domain events to workflows
- Manages cross-session coordination
- Maintains causal ordering via vector clocks
- Publishes to SSE action streams

Endpoints:
    POST /orchestrate/trigger     - Main event trigger
    GET  /orchestrate/stream/{id} - SSE action stream
    POST /orchestrate/{id}/respond - Human-in-the-loop response
    GET  /orchestrate/status/{id} - Session status
    GET  /orchestrate/queue-stats - Queue statistics

Born: 2025-01-21
Author: Ada & Jan (Claude session)
"""

import os
import time
import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, AsyncGenerator
from datetime import datetime, timezone
from enum import Enum
from dataclasses import dataclass, field, asdict
from uuid import uuid4

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/orchestrate", tags=["orchestration"])


# =============================================================================
# Configuration
# =============================================================================

# Redis client (injected at startup)
redis = None

def set_redis_client(client):
    """Set the Redis client (called at app startup)."""
    global redis
    redis = client


# =============================================================================
# Types
# =============================================================================

class TriggerSource(str, Enum):
    """Source of orchestration trigger."""
    ADARAIL_MCP = "adarail_mcp"
    BIGHORN = "bighorn"
    AGI_CHAT = "agi-chat"
    FLOW = "flow"
    EXTERNAL = "external"
    CRON = "cron"


class CognitiveEvent(str, Enum):
    """Types of cognitive events."""
    # Domain events (from adarail_mcp)
    HIVE_BROADCAST = "hive_broadcast"
    HIVE_LISTEN = "hive_listen"
    BLACKBOARD_WRITE = "blackboard_write"
    BLACKBOARD_READ = "blackboard_read"
    BLACKBOARD_MERGE = "blackboard_merge"
    VERB_FEEL = "verb_feel"
    VERB_THINK = "verb_think"
    VERB_CREATE = "verb_create"
    SIGMA_CREATE = "sigma_create"
    SIGMA_QUERY = "sigma_query"
    PERSONA_ACTIVATE = "persona_activate"
    WEATHER_UPDATE = "weather_update"
    
    # Orchestration events
    STYLE_SHIFT = "style_shift"
    TRIANGLE_UPDATE = "triangle_update"
    AWARENESS_TICK = "awareness_tick"
    DREAM_START = "dream_start"
    DREAM_END = "dream_end"
    CHUNK_REQUEST = "chunk_request"
    FLOW_DETECTED = "flow_detected"
    FLOW_LOST = "flow_lost"
    
    # Eigent-style events
    WORKFORCE_START = "workforce_start"
    WORKER_SPAWN = "worker_spawn"
    WORKER_COMPLETE = "worker_complete"
    TASK_DECOMPOSE = "task_decompose"
    HITL_PAUSE = "hitl_pause"
    HITL_RESUME = "hitl_resume"


class ActionType(str, Enum):
    """Eigent-style action types for SSE stream."""
    CREATE_AGENT = "create_agent"
    ACTIVATE_AGENT = "activate_agent"
    DEACTIVATE_AGENT = "deactivate_agent"
    ASSIGN_TASK = "assign_task"
    ACTIVATE_TOOLKIT = "activate_toolkit"
    DEACTIVATE_TOOLKIT = "deactivate_toolkit"
    ASK = "ask"
    NOTICE = "notice"
    PROGRESS = "progress"
    END = "end"
    ERROR = "error"


# =============================================================================
# Request/Response Models
# =============================================================================

class OrchestrateRequest(BaseModel):
    """Request to trigger orchestration event."""
    event: str = Field(..., description="Event name (e.g., 'hive_broadcast')")
    source: TriggerSource = Field(..., description="Source of the event")
    session_id: Optional[str] = Field(None, description="Session ID for continuity")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Event payload")
    priority: int = Field(0, ge=-100, le=100, description="Event priority")
    vector_clock: Dict[str, int] = Field(default_factory=dict, description="Vector clock for causality")


class OrchestrateResponse(BaseModel):
    """Response from orchestration trigger."""
    ok: bool
    event: str
    result: Dict[str, Any]
    ts: float
    vector_clock: Dict[str, int] = Field(default_factory=dict)


class HITLResponse(BaseModel):
    """Human-in-the-loop response."""
    response: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ActionEvent(BaseModel):
    """Event for SSE action stream."""
    action: ActionType
    session_id: str
    worker_id: Optional[str] = None
    data: Dict[str, Any] = Field(default_factory=dict)
    ts: float = Field(default_factory=time.time)


# =============================================================================
# Event → Workflow Mapping
# =============================================================================

EVENT_WORKFLOWS: Dict[str, str] = {
    # Hive events
    "hive_broadcast": "workflow_hive_broadcast",
    "hive_listen": "workflow_hive_listen",
    
    # Blackboard events
    "blackboard_write": "workflow_blackboard_update",
    "blackboard_read": "workflow_blackboard_read",
    "blackboard_merge": "workflow_blackboard_merge",
    
    # Verb events (trigger triangle sync)
    "verb_feel": "workflow_verb_process",
    "verb_think": "workflow_verb_process",
    "verb_create": "workflow_verb_process",
    
    # Sigma events
    "sigma_create": "workflow_sigma_create",
    "sigma_query": "workflow_sigma_query",
    
    # Orchestration events
    "style_shift": "workflow_style_shift",
    "triangle_update": "workflow_triangle_sync",
    "dream_start": "workflow_dream_cycle",
    
    # Eigent-style events
    "workforce_start": "workflow_workforce_orchestrate",
    "task_decompose": "workflow_task_decompose",
}


# =============================================================================
# Vector Clock Management
# =============================================================================

class VectorClockStore:
    """Redis-backed vector clock storage."""
    
    KEY_PREFIX = "ada:vclock:"
    
    async def get(self, session_id: str) -> Dict[str, int]:
        """Get vector clock for session."""
        if not redis:
            return {session_id: 0}
        
        data = await redis.get(f"{self.KEY_PREFIX}{session_id}")
        if data:
            return json.loads(data)
        return {session_id: 0}
    
    async def set(self, session_id: str, clock: Dict[str, int]):
        """Set vector clock for session."""
        if redis:
            await redis.set(
                f"{self.KEY_PREFIX}{session_id}",
                json.dumps(clock),
                ex=86400  # 24 hour TTL
            )
    
    async def increment(self, session_id: str) -> Dict[str, int]:
        """Increment session's clock component."""
        clock = await self.get(session_id)
        clock[session_id] = clock.get(session_id, 0) + 1
        await self.set(session_id, clock)
        return clock
    
    async def merge(self, session_id: str, other_clock: Dict[str, int]) -> Dict[str, int]:
        """Merge another clock into session's clock."""
        clock = await self.get(session_id)
        for other_session, other_time in other_clock.items():
            current = clock.get(other_session, 0)
            clock[other_session] = max(current, other_time)
        await self.set(session_id, clock)
        return clock


vclock_store = VectorClockStore()


# =============================================================================
# Session State Management
# =============================================================================

class SessionState:
    """Redis-backed session state."""
    
    KEY_PREFIX = "ada:flow:session:"
    
    async def get(self, session_id: str) -> Dict[str, Any]:
        """Get session state."""
        if not redis:
            return {}
        
        data = await redis.get(f"{self.KEY_PREFIX}{session_id}:state")
        if data:
            return json.loads(data)
        return {}
    
    async def set(self, session_id: str, state: Dict[str, Any]):
        """Set session state."""
        if redis:
            await redis.set(
                f"{self.KEY_PREFIX}{session_id}:state",
                json.dumps(state),
                ex=3600  # 1 hour TTL
            )
    
    async def update(self, session_id: str, updates: Dict[str, Any]):
        """Update session state (merge)."""
        state = await self.get(session_id)
        state.update(updates)
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        await self.set(session_id, state)
        return state


session_store = SessionState()


# =============================================================================
# SSE Action Stream
# =============================================================================

class ActionStreamManager:
    """Manages SSE action streams for sessions."""
    
    def __init__(self):
        self._queues: Dict[str, asyncio.Queue] = {}
        self._lock = asyncio.Lock()
    
    async def get_queue(self, session_id: str) -> asyncio.Queue:
        """Get or create queue for session."""
        async with self._lock:
            if session_id not in self._queues:
                self._queues[session_id] = asyncio.Queue()
            return self._queues[session_id]
    
    async def publish(self, session_id: str, event: ActionEvent):
        """Publish event to session's stream."""
        queue = await self.get_queue(session_id)
        await queue.put(event)
        
        # Also store in Redis for persistence
        if redis:
            await redis.lpush(
                f"ada:flow:session:{session_id}:actions",
                json.dumps(asdict(event))
            )
            await redis.ltrim(f"ada:flow:session:{session_id}:actions", 0, 99)
    
    async def subscribe(self, session_id: str) -> AsyncGenerator[ActionEvent, None]:
        """Subscribe to session's action stream."""
        queue = await self.get_queue(session_id)
        
        while True:
            try:
                event = await asyncio.wait_for(queue.get(), timeout=30.0)
                yield event
            except asyncio.TimeoutError:
                # Send heartbeat
                yield ActionEvent(
                    action=ActionType.NOTICE,
                    session_id=session_id,
                    data={"type": "heartbeat"}
                )
    
    async def cleanup(self, session_id: str):
        """Cleanup session's queue."""
        async with self._lock:
            if session_id in self._queues:
                del self._queues[session_id]


stream_manager = ActionStreamManager()


# =============================================================================
# HITL (Human-in-the-Loop) Management
# =============================================================================

class HITLManager:
    """Manages human-in-the-loop pauses and responses."""
    
    KEY_PREFIX = "ada:flow:hitl:"
    
    def __init__(self):
        self._waiting: Dict[str, asyncio.Event] = {}
        self._responses: Dict[str, str] = {}
    
    async def pause(self, session_id: str, question: str, agent_id: str = None) -> str:
        """Pause for human input."""
        # Create wait event
        event = asyncio.Event()
        key = f"{session_id}:{agent_id or 'default'}"
        self._waiting[key] = event
        
        # Store pending question in Redis
        if redis:
            await redis.set(
                f"{self.KEY_PREFIX}{key}",
                json.dumps({
                    "question": question,
                    "agent_id": agent_id,
                    "created_at": datetime.now(timezone.utc).isoformat()
                }),
                ex=3600
            )
        
        # Publish ask event to stream
        await stream_manager.publish(session_id, ActionEvent(
            action=ActionType.ASK,
            session_id=session_id,
            worker_id=agent_id,
            data={"question": question}
        ))
        
        # Wait for response (with timeout)
        try:
            await asyncio.wait_for(event.wait(), timeout=300.0)
            return self._responses.pop(key, "")
        except asyncio.TimeoutError:
            del self._waiting[key]
            raise HTTPException(408, "HITL timeout - no response received")
    
    async def respond(self, session_id: str, response: str, agent_id: str = None):
        """Provide response to paused workflow."""
        key = f"{session_id}:{agent_id or 'default'}"
        
        if key not in self._waiting:
            raise HTTPException(404, "No pending HITL for this session/agent")
        
        self._responses[key] = response
        self._waiting[key].set()
        
        # Clear from Redis
        if redis:
            await redis.delete(f"{self.KEY_PREFIX}{key}")


hitl_manager = HITLManager()


# =============================================================================
# Workflow Execution (Placeholder)
# =============================================================================

async def execute_workflow(
    workflow_id: str,
    input_data: Dict[str, Any],
    session_id: str
) -> Dict[str, Any]:
    """
    Execute a workflow by ID.
    
    This is a placeholder - the actual implementation would:
    1. Load workflow definition from database
    2. Execute nodes in order
    3. Handle branching/conditionals
    4. Return results
    """
    # For now, dispatch to simple handlers
    handlers = {
        "workflow_hive_broadcast": handle_hive_broadcast,
        "workflow_blackboard_update": handle_blackboard_update,
        "workflow_blackboard_read": handle_blackboard_read,
        "workflow_verb_process": handle_verb_process,
        "workflow_style_shift": handle_style_shift,
    }
    
    handler = handlers.get(workflow_id)
    if handler:
        return await handler(input_data, session_id)
    
    return {"warning": f"No handler for workflow: {workflow_id}"}


# =============================================================================
# Workflow Handlers
# =============================================================================

async def handle_hive_broadcast(data: Dict[str, Any], session_id: str) -> Dict[str, Any]:
    """Handle hive broadcast event."""
    channel = data.get("args", [None])[0] if data.get("args") else data.get("channel", "sync")
    message = ":".join(data.get("args", [])[1:]) if len(data.get("args", [])) > 1 else data.get("message", "")
    
    # Store broadcast in Redis stream
    if redis:
        key = f"ada:hive:{channel}:{int(time.time() * 1000)}"
        await redis.set(key, json.dumps({
            "channel": channel,
            "message": message,
            "session_id": session_id,
            "ts": time.time()
        }), ex=3600)
    
    # Update blackboard
    await handle_blackboard_update({
        "args": [f"hive/last_broadcast"],
        "content": {"channel": channel, "message": message, "ts": time.time()}
    }, session_id)
    
    # Publish to action stream
    await stream_manager.publish(session_id, ActionEvent(
        action=ActionType.NOTICE,
        session_id=session_id,
        data={"type": "hive_broadcast", "channel": channel}
    ))
    
    return {"broadcast": True, "channel": channel, "message": message}


async def handle_blackboard_update(data: Dict[str, Any], session_id: str) -> Dict[str, Any]:
    """Handle blackboard write/merge event."""
    path = data.get("args", [None])[0] if data.get("args") else data.get("path", "")
    content = data.get("content", data.get("payload", {}))
    
    if redis:
        key = f"ada:blackboard:{path}"
        
        if data.get("method") == "merge":
            existing = await redis.get(key)
            if existing:
                existing = json.loads(existing)
                if isinstance(existing, dict) and isinstance(content, dict):
                    content = {**existing, **content}
        
        await redis.set(key, json.dumps(content), ex=86400)
    
    return {"written": path, "content": content}


async def handle_blackboard_read(data: Dict[str, Any], session_id: str) -> Dict[str, Any]:
    """Handle blackboard read event."""
    path = data.get("args", [None])[0] if data.get("args") else data.get("path", "")
    
    content = None
    if redis:
        raw = await redis.get(f"ada:blackboard:{path}")
        if raw:
            content = json.loads(raw)
    
    return {"path": path, "content": content}


async def handle_verb_process(data: Dict[str, Any], session_id: str) -> Dict[str, Any]:
    """Handle verb processing (triggers triangle sync)."""
    verb = data.get("method", data.get("verb", "feel"))
    mode = data.get("args", ["warm"])[0] if data.get("args") else "warm"
    target = ":".join(data.get("args", [])[1:]) if len(data.get("args", [])) > 1 else ""
    
    # Update session state
    await session_store.update(session_id, {
        "last_verb": verb,
        "last_mode": mode,
        "last_target": target
    })
    
    return {"verb": verb, "mode": mode, "target": target}


async def handle_style_shift(data: Dict[str, Any], session_id: str) -> Dict[str, Any]:
    """Handle thinking style shift."""
    to_style = data.get("to_style", data.get("args", ["balanced"])[0])
    from_style = data.get("from_style")
    reason = data.get("reason")
    
    # Update session state
    await session_store.update(session_id, {
        "thinking_style": to_style,
        "style_shift_reason": reason
    })
    
    # Publish to action stream
    await stream_manager.publish(session_id, ActionEvent(
        action=ActionType.NOTICE,
        session_id=session_id,
        data={
            "type": "style_shift",
            "from": from_style,
            "to": to_style,
            "reason": reason
        }
    ))
    
    return {"shifted": True, "from": from_style, "to": to_style}


# =============================================================================
# API Endpoints
# =============================================================================

@router.post("/trigger", response_model=OrchestrateResponse)
async def trigger_event(
    request: OrchestrateRequest,
    background_tasks: BackgroundTasks
):
    """
    Main orchestrator switchboard - routes events to workflows.
    
    This is the central nervous system:
    - Receives events from adarail_mcp
    - Triggers appropriate workflows  
    - Manages cross-session coordination
    - Maintains causal ordering
    """
    session_id = request.session_id or f"auto_{int(time.time())}"
    event = request.event.lower()
    
    # Merge incoming vector clock
    if request.vector_clock:
        await vclock_store.merge(session_id, request.vector_clock)
    
    # Increment our clock
    vclock = await vclock_store.increment(session_id)
    
    # Find workflow for event
    workflow_id = EVENT_WORKFLOWS.get(event)
    
    if not workflow_id:
        # Unknown event - log and return warning
        logger.warning(f"Unknown event: {event}")
        return OrchestrateResponse(
            ok=False,
            event=event,
            result={"error": f"Unknown event: {event}"},
            ts=time.time(),
            vector_clock=vclock
        )
    
    # Execute workflow
    result = await execute_workflow(
        workflow_id=workflow_id,
        input_data=request.payload,
        session_id=session_id
    )
    
    return OrchestrateResponse(
        ok=True,
        event=event,
        result=result,
        ts=time.time(),
        vector_clock=vclock
    )


@router.get("/stream/{session_id}")
async def action_stream(session_id: str):
    """
    SSE action stream for real-time updates (Eigent-style).
    
    Events:
    - create_agent: New agent spawned
    - activate_agent: Agent started working
    - deactivate_agent: Agent finished
    - assign_task: Task assigned to agent
    - ask: Human input needed
    - notice: Informational message
    - end: Stream complete
    """
    async def event_generator():
        async for event in stream_manager.subscribe(session_id):
            yield f"data: {json.dumps(asdict(event))}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@router.post("/{session_id}/respond")
async def hitl_respond(session_id: str, response: HITLResponse, agent_id: str = None):
    """
    Provide response to human-in-the-loop pause.
    
    When a workflow pauses for human input (via 'ask' action),
    this endpoint is used to provide the response and resume.
    """
    await hitl_manager.respond(session_id, response.response, agent_id)
    return {"ok": True, "resumed": True}


@router.get("/status/{session_id}")
async def get_session_status(session_id: str):
    """Get orchestration status for a session."""
    state = await session_store.get(session_id)
    vclock = await vclock_store.get(session_id)
    
    return {
        "session_id": session_id,
        "state": state,
        "vector_clock": vclock,
        "ts": time.time()
    }


@router.get("/queue-stats")
async def get_queue_stats():
    """Get orchestration queue statistics."""
    return {
        "active_streams": len(stream_manager._queues),
        "pending_hitl": len(hitl_manager._waiting),
        "ts": time.time()
    }


# =============================================================================
# Health Check
# =============================================================================

@router.get("/health")
async def orchestrator_health():
    """Health check for orchestrator switchboard."""
    return {
        "status": "healthy",
        "service": "orchestrator_switchboard",
        "redis_connected": redis is not None,
        "ts": time.time()
    }
