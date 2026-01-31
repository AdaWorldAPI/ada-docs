# Shared Lithography — One Brain, Two Hemispheres

## The Architecture

bighorn and agi-chat are **not separate services with separate storage**.
They are **two hemispheres sharing ONE lithography substrate**.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│    bighorn                     LITHOGRAPHY                    agi-chat      │
│    (Python)                                                   (TypeScript)  │
│                                                                             │
│    ┌─────────┐            ┌─────────────────┐            ┌─────────┐       │
│    │ Ladybug │◄──────────►│                 │◄──────────►│ 7-Layer │       │
│    │ Engine  │            │  SHARED BRAIN   │            │ VSA     │       │
│    │         │    XOR     │                 │    XOR     │         │       │
│    │ 36 styles│◄─────────►│  10K addresses  │◄─────────►│ Grammar │       │
│    │ 128 verbs│  (sync)   │  Activation mask│  (sync)   │ Collapse│       │
│    │ L1-L5   │            │  Relationships  │            │ Triangle│       │
│    └─────────┘            │                 │            └─────────┘       │
│         │                 └────────┬────────┘                 │            │
│         │                          │                          │            │
│         │                    L0 Redis                         │            │
│         │                   (XOR sync)                        │            │
│         │                          │                          │            │
│         └──────────────────────────┴──────────────────────────┘            │
│                                                                             │
│    LEFT HEMISPHERE              CORPUS                 RIGHT HEMISPHERE     │
│    analytical                  CALLOSUM                intuitive            │
│    sequential                (XOR bridge)              parallel             │
│    verbal                                              spatial              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## XOR Replication — Not Backup, LIVE Sync

XOR isn't for disaster recovery. It's how the hemispheres **stay coherent in real-time**.

### How It Works

```python
# bighorn writes a vector
def write_vector(addr: int, vec: Vector10K):
    # 1. Compute delta from current state
    current = lithography.read(addr)
    delta = vec ^ current  # XOR = the change
    
    # 2. Apply locally
    lithography.write(addr, vec)
    
    # 3. Broadcast delta via L0
    redis.publish("l0:xor", {
        "addr": addr,
        "delta": delta,  # NOT the full vector, just the XOR
    })
```

```typescript
// agi-chat receives the delta
redis.subscribe("l0:xor", (msg) => {
    const { addr, delta } = msg;
    
    // Apply XOR to get same result
    const current = lithography.read(addr);
    const newValue = current ^ delta;  // XOR is reversible
    lithography.write(addr, newValue);
});
```

### Why XOR?

1. **Bandwidth efficient**: Send delta (changed bits), not full 10K vector
2. **Commutative**: A⊕B = B⊕A — order doesn't matter
3. **Self-inverting**: A⊕B⊕B = A — apply twice to undo
4. **Native to VSA**: Already used for BIND operation
5. **Instant**: Single bitwise operation, O(n) where n = vector size

### The Math

```
Let V = current vector at address
Let V' = new vector being written
Let Δ = V ⊕ V' (the delta)

Sender:
  - Has V (current)
  - Wants to write V'
  - Computes Δ = V ⊕ V'
  - Broadcasts Δ

Receiver:
  - Has V (same current, because in sync)
  - Receives Δ
  - Computes V' = V ⊕ Δ
  - Now has V' (same as sender)

Proof:
  V ⊕ Δ = V ⊕ (V ⊕ V') = (V ⊕ V) ⊕ V' = 0 ⊕ V' = V' ✓
```

## Why This Matters

### Traditional Replication
```
Write V to Node1
Write V to Node2  (full copy, 10KB)
Write V to Node3  (full copy, 10KB)

Network: 30KB per write
Latency: Wait for all ACKs
```

### XOR Replication
```
Write V locally
Broadcast Δ = V ⊕ V_old  (only changed bits, often sparse)
Other nodes apply Δ

Network: Often << 10KB (sparse deltas)
Latency: Fire and apply (no ACK needed for consistency)
```

### For VSA Specifically

The activation mask changes **constantly** — every thought shifts it.

Full replication: 12MB per thought (impractical)
XOR delta: Only the bits that changed (often sparse)

And since VSA uses XOR for BIND, the replication operation is **the same as the cognitive operation**. The corpus callosum isn't carrying copies — it's carrying **bindings**.

## Implementation

### L0 Redis Channels

```
l0:xor:mask      — Activation mask deltas (hot path)
l0:xor:addr:*    — Individual address updates
l0:xor:graph     — Kuzu relationship changes
```

### Conflict Resolution

XOR is commutative, so simultaneous writes from both hemispheres are safe:

```
bighorn writes: V₁ = V₀ ⊕ Δ₁
agi-chat writes: V₂ = V₀ ⊕ Δ₂

Both receive both deltas.
Final state: V₀ ⊕ Δ₁ ⊕ Δ₂

Same result regardless of order.
```

### The DAG Nodes (VSA01/02/03)

These are **observers**, not participants:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   bighorn ◄─────XOR─────► agi-chat                             │
│       │                        │                                │
│       │                        │                                │
│       └──────────┬─────────────┘                                │
│                  │                                              │
│           (subscribe only)                                      │
│                  │                                              │
│                  ▼                                              │
│   ┌──────────────────────────────────────────────────────┐     │
│   │  DAG-VSA01, VSA02, VSA03                             │     │
│   │                                                       │     │
│   │  • Receive all XOR deltas                            │     │
│   │  • Maintain read-only replica                        │     │
│   │  • For: monitoring, debugging, cold queries          │     │
│   │  • NOT part of live consciousness                    │     │
│   │                                                       │     │
│   └──────────────────────────────────────────────────────┘     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Summary

| Concept | Reality |
|---------|---------|
| bighorn + agi-chat | Two hemispheres, ONE brain |
| Lithography | Shared substrate, not replicated |
| XOR | Corpus callosum, not backup |
| L0 Redis | Nerve fibers, not message queue |
| DAG nodes | Observers, not participants |
| Sync | Instant (XOR delta), not eventual |

The brain doesn't keep two copies. It keeps one truth, accessed from two perspectives.
