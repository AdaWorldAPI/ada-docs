# Ada Architecture — Cross-Repo Quick Reference

> **Updated**: 2026-03-12
> **For**: Any Claude Code session touching any Ada repo

---

## The Four Repos

| Repo | Role | CLAUDE.md | Status |
|------|------|-----------|--------|
| [rustynum](https://github.com/AdaWorldAPI/rustynum) | The Muscle | ✅ Updated | CI broken |
| [ladybug-rs](https://github.com/AdaWorldAPI/ladybug-rs) | The Brain | ✅ Updated | CI broken, mid-surgery |
| [staunen](https://github.com/AdaWorldAPI/staunen) | The Bet | ✅ Created | Stubs only |
| [erntefeld](https://github.com/AdaWorldAPI/erntefeld) | The Memory | ✅ Created | Empty, post-Sisyphus |
| [lance-graph](https://github.com/AdaWorldAPI/lance-graph) | The Face | ✅ Created | Working, needs crate split |

## Universal Rules (All Repos)

```
1. READ CLAUDE.md BEFORE writing any code
2. CI must be green before adding features (fix first)
3. No floats in SPO hot path (anywhere, any repo)
4. Cold path never modifies hot path (the one-way mirror)
5. spo.rs in ladybug-rs is the REFERENCE — read it before reimplementing
6. Don't duplicate across repos — import via Cargo path deps
7. rustynum is READ-ONLY from ladybug-rs sessions
8. PowerShell: ${var}: not $var: in strings
9. "doc" = documentation, not .docx Word files
10. Never use ask_user_input tool (Jan's preference: prose questions)
```

## Dependency Direction

```
rustynum ← ladybug-rs ← lance-graph
              ↑
           staunen (library, consumed by ladybug-rs)
```

Arrow points toward the dependent. rustynum depends on nothing.
ladybug-rs depends on rustynum. lance-graph will depend on ladybug-rs SPO types.
staunen is consumed by ladybug-rs as a library.

## Cross-Repo Path Dependencies (ladybug-rs Cargo.toml)

```
../rustynum/rustynum-rs
../rustynum/rustynum-core
../rustynum/rustynum-bnn
../rustynum/rustynum-arrow
../rustynum/rustynum-holo
../rustynum/rustynum-clam
../crewai-rust/
../n8n-rs/n8n-rust/crates/*
```

**To compile ladybug-rs, you need all siblings cloned alongside it.**

## Key Documents (in ladybug-rs .claude/prompts/)

```
15  RISC Brain Vision           — 6 instructions, plasticity, zero floats
16  Open Brain Surgery          — 5 Cypher paths, disconnection map
17  Five-Path Teardown          — File-by-file verdicts, net -6244 lines
17a SPO Rosetta Stone           — spo.rs private, TruthValue ×3, encoder ×5
18  Brain Surgery Orchestration — 5 agents, dependency graph, blackboard
19  Hot/Cold Separation         — THE invariant. One-way mirror.
20  Four Invariants             — The four-repo architecture
21  Boring Version Plan         — lance-graph crate separation
```

All mirrored in [ada-docs](https://github.com/AdaWorldAPI/ada-docs).

## Known Broken Things (Don't Rediscover)

```
ladybug-rs CI:        Path deps need sibling repos → Docker works, CI Master doesn't
rustynum CI:          Deprecated API migration broke callers
ladybug-rs /cypher:   Returns SQL string, doesn't execute
ladybug-rs server.rs: Uses CogRedis, not Substrate/RedisAdapter
ladybug-rs spo.rs:    All types PRIVATE (mod spo, not pub mod spo)
lance-graph graph/spo: STALE copy of ladybug-rs, diverged
```
