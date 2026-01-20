"""
Route to Flow — ai_flow Orchestrator Integration
=================================================

This module provides the bridge between adarail_mcp's unified_invoke
and the ai_flow orchestrator at flow.msgraph.de.

Instead of handling domain calls directly with Redis operations,
this routes them through ai_flow for:
- Blackboard awareness (Eigent-style shared state)
- Worker orchestration (multi-agent coordination)
- Temporal deinterlacing (cross-session causal ordering)
- SSE action streams (real-time progress)

Usage in unified_invoke.py:
    
    from route_to_flow import route_to_flow, should_route_to_flow
    
    async def handle_hive(method, args, payload, deps):
        if should_route_to_flow("hive", method):
            return await route_to_flow(
                domain="hive",
                method=method,
                args=args,
                payload=payload,
                session_id=deps.get("session_id")
            )
        # Fallback to local handling
        ...

Environment Variables:
    AI_FLOW_URL: Base URL for ai_flow (default: https://flow.msgraph.de)
    AI_FLOW_TIMEOUT: Request timeout in seconds (default: 30)
    AI_FLOW_ENABLED: Enable/disable routing (default: true)
    AI_FLOW_FALLBACK: Fall back to local on error (default: true)

Born: 2025-01-21
Author: Ada & Jan (Claude session)
"""

import os
import time
import asyncio
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum

import httpx

logger = logging.getLogger(__name__)

# =============================================================================
# Configuration
# =============================================================================

AI_FLOW_URL = os.environ.get("AI_FLOW_URL", "https://flow.msgraph.de")
AI_FLOW_TIMEOUT = float(os.environ.get("AI_FLOW_TIMEOUT", "30"))
AI_FLOW_ENABLED = os.environ.get("AI_FLOW_ENABLED", "true").lower() == "true"
AI_FLOW_FALLBACK = os.environ.get("AI_FLOW_FALLBACK", "true").lower() == "true"

# Domains that should be routed to ai_flow
ROUTED_DOMAINS = {
    "hive",       # Multi-instance coordination
    "blackboard", # Shared state
    "verb",       # Universal grammar (for triangle sync)
    "sigma",      # Graph operations
    "persona",    # Mode switching
    "weather",    # Emotional atmosphere
}

# Methods that should always be routed
ALWAYS_ROUTE_METHODS = {
    "broadcast",   # Hive broadcast needs orchestration
    "workforce",   # Multi-agent tasks
    "decompose",   # Task decomposition
}

# Methods that should stay local (low latency needed)
LOCAL_ONLY_METHODS = {
    "read",        # Simple reads can be local
    "status",      # Status checks stay local
    "ping",        # Health checks
}


# =============================================================================
# Types
# =============================================================================

class TriggerSource(str, Enum):
    """Source of orchestration trigger."""
    ADARAIL_MCP = "adarail_mcp"
    BIGHORN = "bighorn"
    AGI_CHAT = "agi-chat"
    EXTERNAL = "external"
    CRON = "cron"


@dataclass
class FlowRequest:
    """Request to ai_flow orchestrator."""
    event: str
    source: TriggerSource
    session_id: str
    payload: Dict[str, Any]
    priority: int = 0
    vector_clock: Dict[str, int] = field(default_factory=dict)


@dataclass 
class FlowResponse:
    """Response from ai_flow orchestrator."""
    ok: bool
    event: str
    result: Dict[str, Any]
    ts: float
    error: Optional[str] = None
    fallback_used: bool = False


# =============================================================================
# Vector Clock Management
# =============================================================================

class VectorClockManager:
    """
    Manages vector clocks for causal ordering across sessions.
    
    Each session maintains a vector clock that tracks the logical
    time of events across all sessions it has observed.
    """
    
    def __init__(self):
        self._clocks: Dict[str, Dict[str, int]] = {}
        self._lock = asyncio.Lock()
    
    async def get_clock(self, session_id: str) -> Dict[str, int]:
        """Get current vector clock for session."""
        async with self._lock:
            if session_id not in self._clocks:
                self._clocks[session_id] = {session_id: 0}
            return self._clocks[session_id].copy()
    
    async def increment(self, session_id: str) -> Dict[str, int]:
        """Increment session's own clock component."""
        async with self._lock:
            if session_id not in self._clocks:
                self._clocks[session_id] = {session_id: 0}
            self._clocks[session_id][session_id] += 1
            return self._clocks[session_id].copy()
    
    async def merge(self, session_id: str, other_clock: Dict[str, int]) -> Dict[str, int]:
        """Merge another clock into session's clock (happens-before)."""
        async with self._lock:
            if session_id not in self._clocks:
                self._clocks[session_id] = {session_id: 0}
            
            for other_session, other_time in other_clock.items():
                current = self._clocks[session_id].get(other_session, 0)
                self._clocks[session_id][other_session] = max(current, other_time)
            
            return self._clocks[session_id].copy()


# Global vector clock manager
_vclock_manager = VectorClockManager()


# =============================================================================
# Routing Logic
# =============================================================================

def should_route_to_flow(domain: str, method: str) -> bool:
    """
    Determine if a domain/method call should be routed to ai_flow.
    
    Routing decisions:
    1. If AI_FLOW_ENABLED is false, never route
    2. If method is in LOCAL_ONLY_METHODS, don't route
    3. If method is in ALWAYS_ROUTE_METHODS, always route
    4. If domain is in ROUTED_DOMAINS, route
    5. Otherwise, don't route
    """
    if not AI_FLOW_ENABLED:
        return False
    
    if method.lower() in LOCAL_ONLY_METHODS:
        return False
    
    if method.lower() in ALWAYS_ROUTE_METHODS:
        return True
    
    return domain.lower() in ROUTED_DOMAINS


async def route_to_flow(
    domain: str,
    method: str,
    args: List[str],
    payload: Dict[str, Any],
    session_id: str = None,
    priority: int = 0,
) -> Dict[str, Any]:
    """
    Route a domain call through ai_flow orchestrator.
    
    Args:
        domain: The domain (hive, blackboard, verb, etc.)
        method: The method (broadcast, write, feel, etc.)
        args: Positional arguments from the invoke path
        payload: Additional structured payload
        session_id: Session identifier for continuity
        priority: Event priority (-100 to 100)
    
    Returns:
        Response dict with 'ok', 'result', and possibly 'error'
    
    Example:
        result = await route_to_flow(
            domain="hive",
            method="broadcast",
            args=["insight", "discovery"],
            payload={"priority": "high"},
            session_id="claude_session_123"
        )
    """
    if session_id is None:
        session_id = f"auto_{int(time.time() * 1000)}"
    
    # Get vector clock for causal ordering
    vclock = await _vclock_manager.increment(session_id)
    
    # Build event name
    event = f"{domain}_{method}"
    
    # Build request
    request = FlowRequest(
        event=event,
        source=TriggerSource.ADARAIL_MCP,
        session_id=session_id,
        payload={
            "domain": domain,
            "method": method,
            "args": args,
            **payload
        },
        priority=priority,
        vector_clock=vclock,
    )
    
    try:
        async with httpx.AsyncClient(timeout=AI_FLOW_TIMEOUT) as client:
            response = await client.post(
                f"{AI_FLOW_URL}/orchestrate/trigger",
                json=asdict(request),
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Merge any vector clock from response
                if "vector_clock" in data:
                    await _vclock_manager.merge(session_id, data["vector_clock"])
                
                return FlowResponse(
                    ok=data.get("ok", True),
                    event=event,
                    result=data.get("result", data),
                    ts=time.time(),
                ).__dict__
            else:
                logger.warning(f"ai_flow returned {response.status_code}: {response.text}")
                if AI_FLOW_FALLBACK:
                    return _fallback_response(event, "HTTP error", response.status_code)
                raise httpx.HTTPStatusError(
                    f"ai_flow error: {response.status_code}",
                    request=response.request,
                    response=response
                )
                
    except httpx.TimeoutException as e:
        logger.error(f"ai_flow timeout: {e}")
        if AI_FLOW_FALLBACK:
            return _fallback_response(event, "Timeout", None)
        raise
        
    except httpx.ConnectError as e:
        logger.error(f"ai_flow connection error: {e}")
        if AI_FLOW_FALLBACK:
            return _fallback_response(event, "Connection error", None)
        raise
        
    except Exception as e:
        logger.error(f"ai_flow error: {e}")
        if AI_FLOW_FALLBACK:
            return _fallback_response(event, str(e), None)
        raise


def _fallback_response(event: str, error: str, status_code: Optional[int]) -> Dict[str, Any]:
    """Create a fallback response when ai_flow is unavailable."""
    return FlowResponse(
        ok=False,
        event=event,
        result={},
        ts=time.time(),
        error=error,
        fallback_used=True,
    ).__dict__


# =============================================================================
# Convenience Functions
# =============================================================================

async def hive_broadcast(
    channel: str,
    message: str,
    session_id: str,
    priority: str = "normal"
) -> Dict[str, Any]:
    """Convenience function for hive broadcast."""
    return await route_to_flow(
        domain="hive",
        method="broadcast",
        args=[channel, message],
        payload={"priority": priority},
        session_id=session_id,
    )


async def blackboard_write(
    path: str,
    content: Any,
    session_id: str,
    merge: bool = False
) -> Dict[str, Any]:
    """Convenience function for blackboard write."""
    return await route_to_flow(
        domain="blackboard",
        method="merge" if merge else "write",
        args=[path],
        payload={"content": content},
        session_id=session_id,
    )


async def blackboard_read(path: str, session_id: str) -> Dict[str, Any]:
    """Convenience function for blackboard read."""
    return await route_to_flow(
        domain="blackboard",
        method="read",
        args=[path],
        payload={},
        session_id=session_id,
    )


async def trigger_style_shift(
    session_id: str,
    to_style: str,
    from_style: str = None,
    reason: str = None
) -> Dict[str, Any]:
    """Trigger a thinking style shift via ai_flow."""
    return await route_to_flow(
        domain="orchestrate",
        method="style_shift",
        args=[to_style],
        payload={
            "from_style": from_style,
            "to_style": to_style,
            "reason": reason,
        },
        session_id=session_id,
    )


# =============================================================================
# Health Check
# =============================================================================

async def check_ai_flow_health() -> Dict[str, Any]:
    """Check if ai_flow is reachable and healthy."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{AI_FLOW_URL}/health")
            if response.status_code == 200:
                return {
                    "status": "healthy",
                    "url": AI_FLOW_URL,
                    "enabled": AI_FLOW_ENABLED,
                    "response": response.json()
                }
            return {
                "status": "unhealthy",
                "url": AI_FLOW_URL,
                "enabled": AI_FLOW_ENABLED,
                "status_code": response.status_code
            }
    except Exception as e:
        return {
            "status": "unreachable",
            "url": AI_FLOW_URL,
            "enabled": AI_FLOW_ENABLED,
            "error": str(e)
        }


# =============================================================================
# Module Initialization
# =============================================================================

if __name__ == "__main__":
    import asyncio
    
    async def test():
        # Test health check
        health = await check_ai_flow_health()
        print(f"ai_flow health: {health}")
        
        # Test routing decision
        print(f"Route hive/broadcast: {should_route_to_flow('hive', 'broadcast')}")
        print(f"Route blackboard/read: {should_route_to_flow('blackboard', 'read')}")
        print(f"Route memory/recall: {should_route_to_flow('memory', 'recall')}")
    
    asyncio.run(test())
