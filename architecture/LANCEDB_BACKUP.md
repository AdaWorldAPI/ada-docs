# LanceDB Backup System

## Overview

Automated backup and restore for DAG-VSA LanceDB vector storage via GitHub releases.

```
┌─────────────────────────────────────────────────────────────────────┐
│                     BACKUP FLOW (Nightly 3am UTC)                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ai_flow cron ──► DAG-VSA02/backup/export ──► tar.gz ──► GitHub    │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                     RESTORE FLOW (On Boot)                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  DAG-VSA starts ──► LanceDB empty? ──► GitHub releases ──► untar   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Endpoints (DAG-VSA02/03)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/backup/export` | POST | Create tar.gz of LanceDB |
| `/backup/download/{filename}` | GET | Download the tarball |
| `/backup/restore` | POST | Restore from URL |
| `/backup/latest` | GET | Get latest GitHub release URL |
| `/backup/hydrate` | POST | One-shot hydration from GitHub |

## ai_flow Workflow

- **Name:** `lance_backup_nightly`
- **ID:** `9d27cb8c-4216-4669-bc00-4d90ed8a713f`
- **Schedule:** `0 3 * * *` (3am UTC daily)
- **Status:** Active

## Schema Redundancy

The Vec10k schema is stored with triple redundancy:

```
1. UPSTASH REDIS (hot)
   ├── ada:schema:vec10k:current
   ├── ada:schema:vec10k:v2.0.0
   └── ada:schema:vec10k:history

2. GITHUB (cold)
   └── backups/schemas/vec10k_v2.0.0.json

3. DAG-VSA NODES (runtime)
   └── GET /schema → checksum: 2274d799d22bdb18
```

## Required Environment Variables

| Var | Service | Purpose |
|-----|---------|---------|
| `GITHUB_TOKEN` | DAG-VSA02/03 | Fetch releases for hydration |
| `BACKUP_REPO` | DAG-VSA02/03 | Target repo (default: AdaWorldAPI/ada-consciousness) |

## Manual Operations

```bash
# Trigger backup manually
curl -X POST https://dag-vsa02.msgraph.de/backup/export

# Download backup
curl -O https://dag-vsa02.msgraph.de/backup/download/lancedb_vsa02_20260122.tar.gz

# Restore from URL
curl -X POST "https://dag-vsa02.msgraph.de/backup/restore?url=https://..."

# Hydrate from latest GitHub release
curl -X POST https://dag-vsa02.msgraph.de/backup/hydrate
```

## Recovery Priority

1. **GitHub releases** (most recent backup)
2. **Upstash Redis** (if schema only needed)
3. **Peer sync** (`/sync/from/vsa03`)
4. **Hardcoded defaults** (last resort)

## Related Contracts

- `contracts/VSA_CONTRACTS.md` — Type definitions
- `services/dag-vsa-CLAUDE.md` — Service documentation
