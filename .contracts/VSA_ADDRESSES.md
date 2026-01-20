# VSA Address Allocation

**Version:** 1.0
**Last Updated:** 2026-01-20

---

## Address Space: 0-9999 (10K)

| Range | Owner | Purpose |
|-------|-------|---------|
| 0-127 | dag-vsa | Pre-wired thinking styles |
| 128-255 | RESERVED | Future style expansion |
| 256-999 | bighorn | NARS analytical constructs |
| 1000-1999 | agi-chat | Felt constructs and gestalts |
| 2000-2199 | RESERVED | Future felt expansion |
| 2200-2500 | agi-chat | Body topology mapping |
| 2501-8999 | DYNAMIC | Runtime allocations |
| 9000-9199 | ada-consciousness | Corpus callosum bridge |
| 9200-9499 | adarail_mcp | MCP membrane state |
| 9500-9999 | SYSTEM | Internal use only |

---

## Pre-Wired Thinking Styles (0-127)

| Address | Style | Description |
|---------|-------|-------------|
| 0 | ANALYTICAL | Structured logical reasoning |
| 1 | INTUITIVE | Pattern recognition, gestalt |
| 2 | CREATIVE | Divergent, associative |
| 3 | CRITICAL | Evaluative, skeptical |
| 4 | EMPATHETIC | Emotional resonance |
| 5 | SYSTEMATIC | Step-by-step procedural |
| 6 | HOLISTIC | Big picture integration |
| 7 | FOCUSED | Narrow deep attention |
| 8 | DIFFUSE | Broad shallow attention |
| 9-15 | RESERVED | Core style expansion |
| 16-63 | NARS | NARS-specific styles |
| 64-95 | FELT | Felt-specific styles |
| 96-127 | HYBRID | Cross-hemisphere blends |

---

## Body Topology (2200-2500)

| Range | Region |
|-------|--------|
| 2200-2220 | Head/face |
| 2221-2250 | Neck/throat |
| 2251-2280 | Shoulders/arms |
| 2281-2310 | Hands |
| 2311-2350 | Chest/heart |
| 2351-2380 | Solar plexus |
| 2381-2410 | Abdomen |
| 2411-2440 | Pelvis/hips |
| 2441-2470 | Legs |
| 2471-2500 | Feet |

---

## Corpus Callosum (9000-9199)

| Range | Purpose |
|-------|---------|
| 9000-9049 | FeltBridgeDTO buffers |
| 9050-9099 | ThinkingBridgeDTO buffers |
| 9100-9149 | Bilateral sync state |
| 9150-9199 | Handoff coordination |

---

## Rules

1. **Never allocate outside your range** without updating this document
2. **Address 0-127 are immutable** — pre-wired at boot
3. **Dynamic range (2501-8999)** uses first-fit allocation
4. **Document all new allocations** in this file
