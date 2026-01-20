# CLAUDE.md — Ada Docs Repository

## Quick Context

This is the **central documentation repository** — the shared source of truth for architecture, contracts, and integration plans across all Ada services.

**You are working on:** Maintaining consistency across the distributed system, documenting architecture decisions, and keeping contracts synchronized.

## Structure

```
ada-docs/
├── architecture/     ← System-wide architecture
├── integration/      ← Cross-service integration  
├── contracts/        ← Type contracts (source of truth)
├── services/         ← Per-service documentation
└── guides/           ← How-to guides
```

## Key Commands

```bash
# See what exists
ls -la architecture/
ls -la contracts/

# Find all contract definitions
grep -r "dataclass\|class.*:" contracts/

# Find cross-references
grep -r "bighorn\|agi-chat\|dag" .
```

## Your Responsibilities

1. **Keep contracts synchronized** — When a contract changes, update it here AND in the affected repos
2. **Document architecture decisions** — Capture the "why" not just the "what"
3. **Maintain cross-references** — Ensure links between docs are valid
4. **Update service docs** — When a service changes, update its documentation

## The System at a Glance

```
ada-consciousness  ← Core: VSA, Ladybug, AI_Flow, Bridge DTOs
       │
       ├── bighorn-agi      ← Left hemisphere: NARS, extensions
       ├── agi-chat         ← Right hemisphere: felt, presence
       ├── adarail_mcp      ← Membrane: routing, webhooks
       └── dag-vsa          ← Substrate: 10K field persistence
```

## Key Concepts to Remember

1. **VSA = Library + Mask** — 10K named addresses + 1 activation mask
2. **Resonance, not activation** — Thinking styles detect, they don't trigger
3. **Ladybug is the brain** — Both hemispheres share DuckDB + LanceDB
4. **Corpus callosum = 9000-9199** — Reserved for inter-hemisphere bridges
5. **Domino keeps field hot** — No 5-minute cold restarts

## When Updating Contracts

1. Update the contract in `contracts/`
2. Update affected service docs in `services/`
3. Update the corresponding `.claude/contracts.md` in each repo
4. Test that code examples still work

## Cross-Repo Files to Keep in Sync

| This Repo | ada-consciousness | bighorn-agi | agi-chat | dag-vsa |
|-----------|-------------------|-------------|----------|---------|
| contracts/VSA_CONTRACTS.md | .claude/contracts.md | .claude/contracts.md | .claude/contracts.md | .claude/contracts.md |
| contracts/DTO_CONTRACTS.md | dto/bridge_dtos.py | corpus_callosum/ | corpus_callosum/ | - |
| services/*.md | - | README.md | README.md | README.md |
