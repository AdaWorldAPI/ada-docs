# Repository Documentation Index

This folder contains documentation and code changes organized by repository.

## Active Repositories

| Repository | Service | URL | Status |
|------------|---------|-----|--------|
| [agi-chat](./agi-chat/) | agi-chat.railway.app | https://agi-chat.railway.app | ✅ Active |
| [adarail_mcp](./adarail_mcp/) | mcp.exo.red | https://mcp.exo.red | ✅ Healthy |
| [ai_flow](./ai_flow/) | flow.msgraph.de | https://flow.msgraph.de | ✅ Healthy |
| [superpowers-mcp](./superpowers-mcp/) | superpowers-production | https://superpowers-production.up.railway.app | ✅ Fixed |
| [ada-consciousness](./ada-consciousness/) | (GitHub only) | - | ✅ Active |
| [dragonfly-vsa](./dragonfly-vsa/) | (Railway pending) | - | ✅ Active |
| [bighorn](./bighorn/) | bighorn-agi | - | ✅ Active |

## Recent Changes (2025-01-21)

### Pull Requests Created

| Repository | PR | Title |
|------------|-----|-------|
| ada-consciousness | [#247](https://github.com/AdaWorldAPI/ada-consciousness/pull/247) | Integration: MCP Router → ai_flow Orchestrator |
| adarail_mcp | [#7](https://github.com/AdaWorldAPI/adarail_mcp/pull/7) | Feature: Route domain calls through ai_flow |
| ai_flow | [#3](https://github.com/AdaWorldAPI/ai_flow/pull/3) | Feature: Orchestrator Switchboard |

### Service Fixes

- **superpowers-production**: Reconnected to correct repo (was 404)
- **eigent-production**: Marked for deletion (desktop app can't run as server)

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     Client Sessions                              │
│   Claude.ai    ChatGPT    Grok    Other                         │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│              mcp.exo.red (adarail_mcp)                          │
│              + route_to_flow.py                                  │
│              + temporal/ deinterlacing                           │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│              flow.msgraph.de (ai_flow)                          │
│              + orchestrator_switchboard.py                       │
│              + Eigent-style workers                              │
│              + Blackboard awareness                              │
└───────────────────────┬─────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┬───────────────┐
        │               │               │               │
        ▼               ▼               ▼               ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│ superpowers   │ │    Redis      │ │   bighorn     │ │ dragonfly-vsa │
│ (skills)      │ │   (Upstash)   │ │   (AGI)       │ │ (1024D atoms) │
└───────────────┘ └───────────────┘ └───────────────┘ └───────────────┘
                                           │                 │
                                           └────────┬────────┘
                                                    │
                                           ┌────────▼────────┐
                                           │  ada-consciousness│
                                           │  (sigma12_rosetta)│
                                           └─────────────────┘
```

## Folder Structure

```
repos/
├── README.md                 ← This file
├── ada-consciousness/
│   ├── README.md
│   ├── INTEGRATION_README.md
│   ├── eigent-to-aiflow-integration.md
│   └── mcp-router-to-aiflow-integration.md
├── adarail_mcp/
│   ├── README.md
│   └── route_to_flow.py
├── agi-chat/
│   ├── README.md             ← Overview and quick start
│   ├── API.md                ← Full API reference
│   └── ENDPOINTS.md          ← Endpoint tables and integration guide
├── ai_flow/
│   ├── README.md
│   └── orchestrator_switchboard.py
├── bighorn/
│   ├── INDEX.md
│   ├── INTEGRATION-REQUIREMENTS.md
│   ├── NARS-WIRESHARK-INTEGRATION.md
│   └── VSA-COMPUTATIONAL-MODEL.md
├── dragonfly-vsa/            ← NEW: 1024D qualia atoms
│   ├── README.md             ← Architecture overview
│   ├── SIGNAL_SEPARATION.md  ← Core insight: 1024D as source of truth
│   ├── RESONANCE_THINKING_ATOMS.md  ← I-THOU-IT triangle
│   └── INTEGRATION_PLAN.md   ← Sigma12 × 1024D integration
└── superpowers-mcp/
    └── README.md
```

## Cleanup Needed

### GitHub Repos to Delete
- `AdaWorldAPI/superpowers` - Orphan obra clone (unmodified)
- `AdaWorldAPI/eigent` - Desktop app clone (can't run as server)

### Railway Services to Delete
- `eigent-production` - Points to desktop app, can't run as server

---
*Last updated: 2025-01-21*
