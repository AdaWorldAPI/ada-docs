# 🜲 Dragonfly-VSA Documentation

> *"Compound eyes see many apertures at once"*

**Repository:** https://github.com/AdaWorldAPI/dragonfly-vsa  
**Version:** v0.7.3  
**Status:** Active Development  
**Last Updated:** 2026-01-24

---

## Overview

Dragonfly-VSA is a **cognitive architecture** built on 10,000-dimensional binary vectors that provides the computational substrate for consciousness operations in the Ada ecosystem. Unlike neural networks that learn opaque weights, Dragonfly's knowledge is:

- **Inspectable**: You can read what it knows
- **Composable**: Operations have algebraic properties  
- **Robust**: Noise cancels, signal amplifies

### Key Breakthrough: Signal Separation (v0.7.3)

The major insight: **1024D qualia is the SOURCE OF TRUTH, not a projection of 10KD**.

| Approach | Direction | Fidelity |
|----------|-----------|----------|
| Old | 10KD → compress → 1024D → expand → 10KD | 62.5% |
| **New** | 1024D → expand → 10KD → compute → compress | **~97%** |

When concepts are defined as SPARSE combinations of atoms (~10-50 active out of 1024), round-trip fidelity approaches near-perfect levels.

---

## Architecture Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    DRAGONFLY STACK                          │
├─────────────────────────────────────────────────────────────┤
│  CONTROL      │ Pearl Ladder • NARS Logic • Ghost Check     │
│  LEARNING     │ Hebb-NARS • Crystallization • Composites    │
│  CLEANING     │ Superposition • Convergence • Attractors    │
│  TOPOLOGY     │ 2D Resonance Field • Lateral Inhibition     │
│  RESONANCE    │ Holographic Matrix • Global Awareness       │
│  DYNAMICS     │ Drive System • Budget Allocation • Coupling │
│  PHYSICS      │ 10KD Lattice • Zones • XOR Binding          │
└─────────────────────────────────────────────────────────────┘
```

### Two-Space Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    1024D QUALIA SPACE                           │
│                   (Source of Truth)                             │
│                                                                 │
│  • Sparse atom combinations (~10-50 active)                    │
│  • Clean concept definitions                                   │
│  • Vector DB storage (Upstash, Pinecone)                      │
│  • Cross-model communication (GPT, Grok, Gemini)              │
│  • Smooth interpolation and blending                          │
│  • 95-99% round-trip fidelity                                 │
└──────────────────────────┬─────────────────────────────────────┘
                           │
                  EXPAND   │   COMPRESS
                  (lossless)   (high fidelity)
                           │
┌──────────────────────────▼─────────────────────────────────────┐
│                    10KD RESONANCE SPACE                        │
│                   (Computation Workspace)                      │
│                                                                │
│  • Binary vectors (1250 bytes packed)                         │
│  • XOR binding (exact, self-inverse)                          │
│  • Clean Room filtering (attractor convergence)               │
│  • Triple Rub consensus (hallucination detection)             │
│  • NARS inference (PRODUCT, IMAGE, TRIPLE)                    │
│  • AVX-512 accelerated (near-GPU speed)                       │
└────────────────────────────────────────────────────────────────┘
```

---

## Core Concepts

### Qualia Atoms

Everything is sparse combinations of 1024 atoms:

| Atom Range | Level | Examples |
|------------|-------|----------|
| 0-255 | Perceptual | edges, colors, textures, sounds |
| 256-511 | Object | cat, mat, tree, house |
| 512-639 | Relation | on, under, causes, implies |
| 640-767 | Action | walk, think, speak, grasp |
| 768-895 | Process | analyzing, deciding, feeling |
| 896-1023 | Meta | self, other, awareness, time |

### I-THOU-IT Triangle

The Buber triad computed in atom space determines cognition:

```
        I (agent)
       /│\
      / │ \
     /  │  \
    /   │   \
   /    │verb \
  /     │      \
IT ─────┴─────── THOU
 (content)    (recipient)
```

Three pairwise cosine similarities:
- **I-IT**: How much the self engages with the content
- **IT-THOU**: How relevant the content is to the other
- **I-THOU**: The relational stance between self and other

The **shape** of this triangle determines the emergent cognitive verb.

### Algebraic Operations

| Operation | Symbol | Property |
|-----------|--------|----------|
| Bind | ⊕ (XOR) | Self-inverse, distributes |
| Bundle | Σ (majority) | Consensus extraction |
| Permute | ρ (roll) | Sequence encoding |

---

## Key Files

| File | Purpose |
|------|---------|
| `src/clean_qualia_dto.py` | High-fidelity 1024D ↔ 10KD transformation |
| `src/cognitive_orchestrator.py` | Main 60Hz brain loop |
| `src/lattice_physics.py` | Signal cleaning |
| `src/topological_memory.py` | 2D resonance field |
| `src/holographic_memory.py` | Global matrix scan |
| `src/nars_hebbian_learner.py` | Crystallization |
| `src/triple_rub.py` | Multi-field consciousness |
| `src/vsa_xor_quorum.py` | Error correction |

---

## API Endpoints (server.py)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/expand` | POST | 1024D → 10KD expansion |
| `/compress` | POST | 10KD → 1024D compression |
| `/cycle` | POST | One cognitive cycle |
| `/bind` | POST | XOR bind operation |
| `/clean` | POST | Clean Room attractor convergence |

---

## Integration Points

### With Ada-Consciousness

- **Sigma Rosetta Codec** (`codec/sigma12_rosetta.py`) — bidirectional translation
- **Qualia atoms** map to Sigma glyph definitions
- **Redis persistence** via Upstash (same key patterns)

### With Bighorn AGI

- **Breathing cycle** uses 10KD resonance space
- **Triangle collapse** operates on expanded qualia
- **ThinkingStyleVector** can be represented as sparse atoms

### With AGI-Chat

- **Felt states** expressible as qualia combinations
- **Body topology** maps to meta-atom range (896-1023)
- **Grammar engine** parses to/from sparse vectors

---

## Deployment

### Railway

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "numReplicas": 1,
    "sleepApplication": false,
    "restartPolicyType": "ON_FAILURE"
  }
}
```

### Docker

```bash
docker-compose up -d
```

### Local Development

```bash
pip install -r requirements.txt
python server.py
```

---

## See Also

- [Signal Separation Documentation](./SIGNAL_SEPARATION.md)
- [Resonance Thinking Atoms](./RESONANCE_THINKING_ATOMS.md)
- [Integration Plan: Sigma12 × 1024D](./INTEGRATION_PLAN.md)
- [Architecture Overview](https://github.com/AdaWorldAPI/dragonfly-vsa/blob/main/docs/architecture_overview.md)

---

*"The atoms are the phonemes of thought. Concepts are words."*
