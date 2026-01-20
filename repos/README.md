# Repository Integration Files

This folder contains files that are staged for merging into their respective repositories.

## Structure

```
repos/
├── adarail_mcp/           # Files for AdaWorldAPI/adarail_mcp
│   ├── README.md          # Integration instructions
│   └── route_to_flow.py   # ai_flow routing module
│
├── ai_flow/               # Files for AdaWorldAPI/ai_flow
│   ├── README.md          # Integration instructions
│   └── orchestrator_switchboard.py  # Event router
│
└── superpowers-mcp/       # Files for AdaWorldAPI/superpowers-mcp
    └── README.md          # Service status and history
```

## Active Pull Requests

| Repository | PR | Files | Status |
|------------|-----|-------|--------|
| adarail_mcp | [#7](https://github.com/AdaWorldAPI/adarail_mcp/pull/7) | `route_to_flow.py` | Open |
| ai_flow | [#3](https://github.com/AdaWorldAPI/ai_flow/pull/3) | `orchestrator_switchboard.py` | Open |

## Usage

1. **Review**: Check the README in each folder for integration instructions
2. **Merge**: Merge the associated PR in the target repository
3. **Cleanup**: Once merged, these files serve as documentation

## Railway Services

| Service | Repository | URL | Status |
|---------|------------|-----|--------|
| adarail-production | adarail_mcp | https://mcp.exo.red | ✅ Active |
| ai-flow-production | ai_flow | https://flow.msgraph.de | ✅ Active |
| superpowers-production | superpowers-mcp | https://superpowers-production.up.railway.app | ✅ Active |

---
*Updated: 2025-01-21*
