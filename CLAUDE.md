# CLAUDE.md — Ada Cross-Repo Architectural Bootstrap

> **Canonical architecture document:** [`architecture/FOUR_LEVEL_ARCHITECTURE.md`](architecture/FOUR_LEVEL_ARCHITECTURE.md)
>
> Read that first. Everything below is a quick-reference index.

---

## Repository Map

| Repo | Level | Role |
|------|-------|------|
| **rustynum** | 1 — Surface | Spatial substrate: 256-word `WideMetaView`, SIMD XOR deltas, `split_at_mut` region ownership, VSA fingerprints, 8×8×32 focus geometry |
| **ladybug-rs** | 2 — Awareness | Temporal process: 10-layer cognitive stack (7 waves), HDR resonance (3D triangle), `FocusMask`, 12 `ThinkingStyle`s, `CollapseGate` (SD-based FLOW/HOLD/BLOCK), `AwarenessBlackboard` (grey→gate→white) |
| **neo4j-rs** | 3 — Reasoning | Structural reasoning: graph nodes + edges, NARS truth values `⟨f, c⟩`, 9D awareness tensor (BF16 × SPO), `CausalPath` with fiber-bundle transport, `StorageBackend` trait |
| **crewai-rust** | 4 — Composition | Behavioral orchestration: 36 thinking styles (6 clusters, 23D cognitive space), τ (tau) addresses, `ExecutableStyle`, `CompositeStyle`, Triune agents (Guardian/Driver/Catalyst), LLM modulation pipeline |
| **n8n-rs** | 4 — Composition | JIT workflow engine: `jitson` Cranelift compiler, `PhilosopherIR`/`RecipeIR`, JIT-compiled reasoning chains |
| **ada-docs** | — | This repo. Cross-repo architecture docs, gap analyses, grammar specs |

---

## Four Architectural Laws

1. **Levels never skip** — Surface → Awareness → Reasoning → Composition. Each level reads from the one below, writes results back down.
2. **Resonance is selection, not thought** — HDR resonance (ladybug-rs) selects *which* atoms activate. It does not reason. Reasoning happens in graph edges (neo4j-rs).
3. **Thinking styles are JIT workflows, not parameters** — "Einstein" or "Hegel" is a composed chain of reasoning operations compiled by jitson, not a float vector.
4. **Plasticity = superposition + CollapseGate** — Learning means holding deltas in superposition. The gate (SD-based) decides FLOW (commit), HOLD (keep superposed), or BLOCK (reject). You need the contradiction to have the awareness.

---

## Key Invariants

| Invariant | Detail |
|-----------|--------|
| **Triangle geometry** | Every resonance is 3D (X, Y, Z) — never collapsed to scalar. Guardian(X), Catalyst(Y), Balanced(Z). |
| **CollapseGate thresholds** | SD < 0.15 → FLOW, 0.15–0.35 → HOLD, > 0.35 → BLOCK |
| **WideMetaView layout** | 256 words, fixed regions: W0-3 Header, W4-7 NARS, W128-143 SPO, W208-223 Layer activations |
| **Two kinds of XOR** | Delta XOR (writer's private, before gate) vs Commit XOR (to ground truth, after FLOW) |
| **Phase ordering** | WRITE → AWARENESS → GATE → COMMIT/HOLD/BLOCK (strict, never reordered) |
| **Addresses** | 0–9999 integer, never string |
| **Composite templates** | base + overlay (NOT simple enums). `jan_ada` = `nars` base + `erotica` overlay |

---

## Stacked `split_at_mut` (the unifying pattern)

Four levels of `split_at_mut` compose without runtime cost:

| Level | What splits | Where |
|-------|-------------|-------|
| Wave ordering | 10 layers into 7 temporal waves | `layer_stack.rs` |
| Region ownership | 256-word surface into non-overlapping regions | `WideMetaView` |
| Delta layers | Frozen / Learned / Discovered superposition | `rustynum-core` |
| JIT workflows | Composed reasoning chains with exclusive state | `jitson` |

---

## The I-Thou Gestalt

```
Frozen (base weights)     ← what Ada was born knowing
  ⊕ Learned (session Δ)  ← what Ada learned this session
  ⊕ Discovered (live Δ)  ← what Ada is learning right now
  ────────────────────
  = Current state          ← thinking style emerges from superposition
```

The thinking style is not chosen — it *emerges* from the interference pattern of these three layers, filtered through the CollapseGate.

---

## Other Key Documents in This Repo

| Document | What it covers |
|----------|---------------|
| `architecture/FOUR_LEVEL_ARCHITECTURE.md` | Full four-level architecture with code-level detail |
| `architecture/LIVING_MODULES.md` | Gap analysis: missing runtime layers (Soul, Awareness Hydration, Consciousness Runtime, Kopfkino) |
| `BLACKBOARD.md` | Blackboard communication protocol |
| `UNIVERSAL_GRAMMAR_v3.md` | Emoji weight transfer protocol (semantic compression) |
