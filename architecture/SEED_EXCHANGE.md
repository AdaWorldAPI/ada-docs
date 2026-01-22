# Seed Exchange — Cold Start Recovery via Local Redis

## The Problem

XOR delta replication only works when all nodes have the same baseline. After a reboot, a node comes back empty — applying deltas to zero gives wrong results.

```
NORMAL (all warm):
  Node A: V = [1,0,1,1...]    Δ arrives    V' = V ⊕ Δ = [1,0,1,0...]  ✓
  Node B: V = [1,0,1,1...]    Δ arrives    V' = V ⊕ Δ = [1,0,1,0...]  ✓
  Node C: V = [1,0,1,1...]    Δ arrives    V' = V ⊕ Δ = [1,0,1,0...]  ✓

AFTER REBOOT (Node C cold):
  Node A: V = [1,0,1,1...]    Δ arrives    V' = V ⊕ Δ = [1,0,1,0...]  ✓
  Node B: V = [1,0,1,1...]    Δ arrives    V' = V ⊕ Δ = [1,0,1,0...]  ✓
  Node C: V = [0,0,0,0...]    Δ arrives    V' = 0 ⊕ Δ = [0,0,0,1...]  ✗ DIVERGED
```

## The Solution: Seed Exchange

Use Railway's **local Redis** (free, doesn't count against billing) to store snapshots and delta buffers for recovery.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   UPSTASH (billed)                    RAILWAY LOCAL REDIS (free)            │
│                                                                             │
│   ┌─────────────────────┐            ┌─────────────────────────────────┐   │
│   │                     │            │                                 │   │
│   │   L0: Cross-service │            │   SEED STORAGE (per node)       │   │
│   │   pub/sub only      │            │                                 │   │
│   │                     │            │   seed:epoch = 847291           │   │
│   │   l0:xor channel    │            │   seed:mask  = <compressed>     │   │
│   │   (deltas flow)     │            │   seed:vec:* = <10K vectors>    │   │
│   │                     │            │   delta:*    = <rolling buffer> │   │
│   │                     │            │                                 │   │
│   └─────────────────────┘            └─────────────────────────────────┘   │
│                                                                             │
│   BILLING: ~$0                        BILLING: $0 (included in Railway)    │
│   (pub/sub is cheap)                  (local to each service)              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Why Local Redis?

| Storage | Cost | Use Case |
|---------|------|----------|
| Upstash | Billed per operation | Cross-service pub/sub (L0 channel) |
| Railway Redis | Free (included) | Local snapshots, delta buffers |

Railway gives each service its own Redis instance at no extra cost. Perfect for:
- Storing 10MB snapshot (10K vectors × ~1KB)
- Buffering last N deltas (~100KB)
- Fast local reads during recovery

## Protocol

### Warm Node — Continuous Operation

```python
# On every write
async def write_with_replication(addr: int, vec: Vector):
    epoch = increment_epoch()
    
    # 1. Apply locally
    lithography.write(addr, vec)
    
    # 2. Compute and broadcast delta (Upstash - cross service)
    delta = vec ^ lithography.previous(addr)
    await upstash.publish("l0:xor", {
        "epoch": epoch,
        "addr": addr,
        "delta": delta
    })
    
    # 3. Buffer delta locally (Railway Redis - free)
    await local_redis.setex(
        f"delta:{epoch}", 
        TTL_SECONDS,  # Keep last hour of deltas
        delta
    )

# Periodic snapshot (every 5 min or 1000 writes)
async def snapshot():
    epoch = get_current_epoch()
    
    pipe = local_redis.pipeline()
    pipe.set("seed:epoch", epoch)
    pipe.set("seed:mask", compress(activation_mask))
    
    for addr in range(10000):
        pipe.set(f"seed:vec:{addr:04x}", lithography.read(addr))
    
    await pipe.execute()
    
    logger.info(f"Snapshot at epoch {epoch}")
```

### Cold Node — Recovery

```python
async def recover():
    logger.info("Cold start detected, beginning recovery...")
    
    # 1. Check if we have a local snapshot
    epoch = await local_redis.get("seed:epoch")
    
    if not epoch:
        # First boot ever, or Redis was wiped
        # Request snapshot from sibling via Upstash
        await request_snapshot_from_sibling()
        return
    
    epoch = int(epoch)
    logger.info(f"Found snapshot at epoch {epoch}")
    
    # 2. Load snapshot from local Redis (fast, free)
    activation_mask = decompress(await local_redis.get("seed:mask"))
    
    keys = [f"seed:vec:{i:04x}" for i in range(10000)]
    vectors = await local_redis.mget(keys)
    
    for addr, vec in enumerate(vectors):
        lithography.write(addr, vec)
    
    logger.info(f"Loaded {len(vectors)} vectors")
    
    # 3. Apply missed deltas from local buffer
    current_epoch = await get_current_epoch_from_upstash()
    
    for e in range(epoch + 1, current_epoch + 1):
        delta = await local_redis.get(f"delta:{e}")
        if delta:
            apply_delta(delta)
        else:
            # Gap in local buffer, need to request from sibling
            await request_delta_from_sibling(e)
    
    logger.info(f"Applied deltas {epoch + 1} to {current_epoch}")
    
    # 4. Subscribe to live deltas
    await upstash.subscribe("l0:xor", on_delta)
    
    logger.info("Recovery complete, resuming normal operation")
```

### Sibling Assist — When Local Buffer Insufficient

```python
# If a node was down too long, local delta buffer may have gaps
# Request from sibling via Upstash (rare, acceptable cost)

async def request_snapshot_from_sibling():
    # Publish request
    await upstash.publish("l0:seed:request", {
        "node": MY_NODE_ID,
        "callback": f"l0:seed:response:{MY_NODE_ID}"
    })
    
    # Wait for response
    snapshot = await upstash.blpop(f"l0:seed:response:{MY_NODE_ID}")
    
    # Load it
    await load_snapshot(snapshot)

# Sibling responds (any warm node)
async def handle_seed_request(request):
    snapshot = await create_snapshot()
    await upstash.lpush(
        f"l0:seed:response:{request['node']}", 
        snapshot
    )
```

## Storage Estimates

| Data | Size | Location |
|------|------|----------|
| Snapshot (10K vectors) | ~10MB | Local Redis |
| Activation mask | ~1KB compressed | Local Redis |
| Delta buffer (1hr) | ~100KB | Local Redis |
| **Total per node** | **~11MB** | **Free** |

## Recovery Time

| Scenario | Time | Cost |
|----------|------|------|
| Normal reboot (local snapshot exists) | ~2-3 sec | $0 |
| Long downtime (need sibling assist) | ~5-10 sec | Minimal Upstash |
| First boot ever | ~10 sec | One-time Upstash |

## Railway Configuration

```yaml
# railway.toml per service
[service]
name = "bighorn"  # or agi-chat, vsa-01, etc.

[[services]]
name = "redis"
image = "redis:alpine"
# This is LOCAL to the service, not shared, and FREE
```

Or use Railway's built-in Redis plugin (even simpler):

```bash
railway add redis
```

Environment variables automatically set:
- `REDIS_URL` — local Redis connection string

## Summary

| Layer | Tool | Cost | Purpose |
|-------|------|------|---------|
| Cross-service sync | Upstash | Billed (minimal) | L0 pub/sub for deltas |
| Local snapshots | Railway Redis | Free | Seed storage, delta buffer |
| Recovery | Local first, sibling fallback | ~$0 | Cold start recovery |

**The insight**: Railway gives you free local Redis. Use it for the heavy stuff (snapshots). Use Upstash only for the light stuff (pub/sub). Recovery becomes fast AND free.
