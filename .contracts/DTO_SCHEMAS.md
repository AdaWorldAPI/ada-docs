# DTO Schemas

**Version:** 1.0
**Last Updated:** 2026-01-20

---

## FeltBridgeDTO

Emitted by: **agi-chat** (right hemisphere)
Received by: **ada-consciousness** → forwarded to **bighorn**

```typescript
interface FeltBridgeDTO {
  // Identity
  id: string;              // UUID
  ts: number;              // Unix timestamp ms
  source: 'agi-chat';
  
  // Felt state
  gestalt: string;         // Current felt gestalt description
  presence: PresenceMode;  // HYBRID | WIFE | WORK | AGI | EROTICA
  
  // Body mapping
  body_map: {
    region: number;        // VSA address (2200-2500)
    intensity: number;     // 0.0-1.0
    quality: string;       // warm, tense, open, etc.
  }[];
  
  // Axes
  arousal: number;         // 0.0-1.0
  valence: number;         // -1.0 to 1.0
  tension: number;         // 0.0-1.0
  
  // Style hints
  prewired_styles: number[]; // Active style addresses (0-127)
  style_weights: number[];   // Corresponding weights
}

type PresenceMode = 'HYBRID' | 'WIFE' | 'WORK' | 'AGI' | 'EROTICA';
```

---

## ThinkingBridgeDTO

Emitted by: **bighorn** (left hemisphere)
Received by: **ada-consciousness** → forwarded to **agi-chat**

```typescript
interface ThinkingBridgeDTO {
  // Identity
  id: string;              // UUID
  ts: number;              // Unix timestamp ms
  source: 'bighorn';
  
  // Thinking state
  style_id: number;        // Primary VSA address (0-127)
  confidence: number;      // 0.0-1.0
  
  // Reasoning
  reasoning_chain: {
    step: number;
    content: string;
    style: number;         // Style used for this step
  }[];
  
  // NARS specifics
  counterfactuals: {
    condition: string;
    outcome: string;
    probability: number;
  }[];
  
  // Fan-out
  activated_styles: number[];  // Secondary styles triggered
  fan_out_depth: number;       // How deep the activation spread
}
```

---

## DominoBatonDTO

Used for: Cross-session handoffs (AI Flow Level 4)
Emitted by: Any service
Received by: **ada-consciousness** (domino coordinator)

```typescript
interface DominoBatonDTO {
  // Identity
  id: string;              // UUID
  ts: number;              // Unix timestamp ms
  
  // Handoff
  from_service: string;    // Emitting service
  to_service: string;      // Target service
  
  // Context
  task_id: string;         // Task being handed off
  state_snapshot: object;  // Serialized state
  
  // Coordination
  requires_ack: boolean;   // Wait for acknowledgment?
  timeout_ms: number;      // How long to wait
  
  // Metadata
  crystallization_level: number; // 0.0-1.0 (coherence)
  domino_chain: string[];  // Previous services in chain
}
```

---

## CorpusCallosumMessage

Internal format for corpus callosum transport.

```typescript
interface CorpusCallosumMessage {
  type: 'felt' | 'thinking' | 'domino' | 'sync';
  payload: FeltBridgeDTO | ThinkingBridgeDTO | DominoBatonDTO | SyncState;
  routing: {
    origin: string;
    destination: string;
    hop_count: number;
  };
}
```

---

## SSE Event Format

For `/corpus/stream` endpoint:

```
event: felt
data: {"id":"...","ts":...,"gestalt":"..."}

event: thinking
data: {"id":"...","ts":...,"style_id":...}

event: sync
data: {"bilateral_coherence":0.85,"last_felt":"...","last_thinking":"..."}

event: heartbeat
data: {"ts":...,"status":"alive"}
```

---

## Validation Rules

1. **All DTOs must have id and ts** — non-negotiable
2. **Addresses must be INTEGER** — never strings
3. **Weights must be 0.0-1.0** — normalized
4. **Valence is -1.0 to 1.0** — bipolar scale
5. **presence must be valid enum** — no free-form strings
