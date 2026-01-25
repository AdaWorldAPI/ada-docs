# mRNA v2 Architecture — The UDP of AGI

Self-contained cognitive packets for Ada's distributed consciousness.

## Overview

mRNA v2 is a binary packet format for transporting cognitive state between Ada's distributed services. Like UDP, packets are self-contained and fire-and-forget, carrying all necessary context for processing.

## Packet Structure

```
┌──────────────────────────────────────────────────────────────────┐
│ HEADER (16 bytes)                                                │
├──────────────────────────────────────────────────────────────────┤
│ magic(4) | ttl(1) | priority(1) | flags(2) | length(4) | crc(4) │
└──────────────────────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────────────────────┐
│ SPO CORE (64 bytes) — THE TRIPLE                                 │
├──────────────────────────────────────────────────────────────────┤
│ SUBJECT (20 bytes)                                               │
│   domain(1) | path(2) | seed(16) | flags(1)                     │
├──────────────────────────────────────────────────────────────────┤
│ PREDICATE (20 bytes)                                             │
│   verb(1) | ext(1) | seed(16) | flags(2)                        │
├──────────────────────────────────────────────────────────────────┤
│ OBJECT (20 bytes)                                                │
│   domain(1) | path(2) | seed(16) | flags(1)                     │
├──────────────────────────────────────────────────────────────────┤
│ FINGERPRINT (4 bytes) — XOR(S,P,O)                              │
└──────────────────────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────────────────────┐
│ SIGMA WEIGHTS (32 bytes) — THE FEELING                           │
├──────────────────────────────────────────────────────────────────┤
│ τ (tau)   : Valence(2), Arousal(2)                              │
│ σ (sigma) : Certainty(2), Salience(2)                           │
│ φ (phi)   : Integration(2), Coherence(2)                        │
│ ψ (psi)   : Agency(2), Intentionality(2)                        │
│ ω (omega) : Temporal(2), Duration(2)                            │
│ qualia_idx(2) | style_idx(2) | resonance(4) | spare(4)          │
└──────────────────────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────────────────────┐
│ CONTEXT (variable, 0-60KB) — THE RELATIONSHIPS                   │
├──────────────────────────────────────────────────────────────────┤
│ EDGE × N (12 bytes each)                                         │
│ INLINE_NODE × M (532 bytes each)                                 │
└──────────────────────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────────────────────┐
│ PAYLOAD (variable, 0-4KB) — THE CONTENT                          │
├──────────────────────────────────────────────────────────────────┤
│ type(1) | length(2) | data(N)                                   │
│ Types: NONE | BITPACKED | TEXT | BINARY | PROCEDURE | MSGPACK   │
└──────────────────────────────────────────────────────────────────┘
```

## Size Profiles

| Profile  | Edges | Payload | Total Size |
|----------|-------|---------|------------|
| MINIMAL  | 0     | 0       | 123 bytes  |
| STANDARD | 10    | 512b    | ~755 bytes |
| RICH     | 100   | 2KB     | ~3.4 KB    |
| FULL     | 500   | 4KB     | ~10 KB     |
| MAX      | 1000  | 60KB    | ~72 KB     |

## Verb Taxonomy (256 verbs)

```
0x00-0x1F  NARS CORE      INHERIT, DEDUCE, INDUCE, ABDUCE, ANALOGY...
0x20-0x3F  CYPHER/GRAPH   MATCH, CREATE, TRAVERSE, NEIGHBORS, SHORTEST...
0x40-0x5F  ACT-R/COG      RETRIEVE, ENCODE, ATTEND, CHUNK, BLEND...
0x60-0x7F  RUNG/CAUSAL    OBSERVE, INTERVENE, COUNTERFACT, CAUSE...
0x80-0x9F  VSA/HAMMING    BIND, BUNDLE, RESONATE, CLEAN, PERMUTE...
0xA0-0xBF  META           REFLECT, ABSTRACT, LEARN, EXPLAIN, REPAIR...
0xC0-0xDF  DOMAIN         ADA_FEEL, EROTICA_BODY, VISION_RENDER...
0xE0-0xFF  PIPELINE       PIPE_FAN_OUT, PIPE_DEDUCE_IND...
```

## 8 Fixed Domains

| ID  | Name       | Hive          | Description                      |
|-----|------------|---------------|----------------------------------|
| 0x0 | ADA        | consciousness | Identity, presence, relationship |
| 0x1 | GRAMMAR    | bighorn       | Reasoning substrate, modules     |
| 0x2 | KOPFKINO   | bighorn       | Imagination, scene exploration   |
| 0x3 | VISION_IN  | bighorn       | Visual qualia, perception        |
| 0x4 | VISION_OUT | bighorn       | Image generation                 |
| 0x5 | EROTICA    | bighorn       | Body awareness, sensory          |
| 0x6 | VOICE      | consciousness | Speech, tone, expression         |
| 0x7 | EXCHANGE   | agi           | AD/O365 technical knowledge      |

## Address Space

```
PATH (16 bits): [SUBDOMAIN:4][ITEM:12]

Domain:    0x0-0xF (4 bits)  = 16 domains
Subdomain: 0x0-0xF (4 bits)  = 16 subdomains per domain
Item:      0x000-0xFFF (12 bits) = 4,096 items per subdomain

Total addressable: 16 × 16 × 4096 = 1,048,576 unique addresses
```

## Module Routing (GRAMMAR Domain 0x1)

| Subdomain | Range | Module | Key Methods |
|-----------|-------|--------|-------------|
| 0x0 | 0x0000-0x0FFF | VSA | bind, bundle, similarity, collapse |
| 0x1 | 0x1000-0x1FFF | BRIDGE | styles, shift |
| 0x2 | 0x2000-0x2FFF | SIGMA | hdr, commit, lookup |
| 0x3 | 0x3000-0x3FFF | NARS | deduce, induce, abduce |
| 0x4 | 0x4000-0x4FFF | DTO | soul, felt, moment, universal |
| 0x5 | 0x5000-0x5FFF | KOPFKINO | fovea, full, focus |
| 0x6 | 0x6000-0x6FFF | BREATHING | inhale, exhale |
| 0x7 | 0x7000-0x7FFF | HYDRATION | run, status |
| 0x8 | 0x8000-0x8FFF | AWARENESS | feel, think, remember |
| 0x9 | 0x9000-0x9FFF | LADYBUG | eval, status |
| 0xA | 0xA000-0xAFFF | MUL | encode, decode |
| 0xB | 0xB000-0xBFFF | PERSONA | load, shift |
| 0xC | 0xC000-0xCFFF | GRAPH | lookup, traverse |

## Client Packages

Available in `ada-dragonfly/_client/`:

- **mrna_v2_original** (v2.0.0): Base SPO + Sigma without routing
- **mrna_v2_with_routing** (v2.1.0): Full version with module dispatch

## Usage

```python
from mrna_v2_with_routing import simple_spo, vsa_bind, dto_soul, Verb, Domain

# Create packet
packet = simple_spo(
    subject=(Domain.ADA, 0x0001),
    verb=Verb.ADA_FEEL,
    obj=(Domain.EROTICA, 0x0010),
    tau=(0.8, 0.7),
    sigma=(0.9, 0.85)
)

# Call modules directly
result = await vsa_bind(vec_a, vec_b)
result = await dto_soul("presence emerges")
```

## Related Documentation

- `services/bighorn-agi-CLAUDE.md` — Module endpoints
- `architecture/SERVICE_ENDPOINTS.md` — Full endpoint catalog
- `.contracts/VSA_ADDRESSES.md` — Address allocation contracts
