# NARS & Counterfactual Reasoning Research
## Ada Architecture Integration Study

> **Date**: 2026-01-31
> **Author**: Ada Research (Claude Opus 4.5 + Jan Hübener)
> **Status**: Complete — Phase 1 Research

---

## Purpose

This directory contains comprehensive research on counterfactual reasoning across three paradigms, their integration analysis with Ada's existing architecture, and implementation proposals for enhancing Ada's cognitive capabilities.

## Documents

### Core Research

| File | Description |
|------|-------------|
| `01_deep_scm_analysis.md` | Deep Structural Causal Models (Pawlowski et al., NeurIPS 2020) |
| `02_nars_nal_analysis.md` | Non-Axiomatic Reasoning System — NAL-7 temporal & causal reasoning |
| `03_xai_counterfactuals_molnar.md` | Explainable AI counterfactuals (Wachter, Dandl, Molnar IML Book) |
| `04_comparative_synthesis.md` | Cross-paradigm comparison: Deep SCM × NARS × XAI |

### Ada Integration

| File | Description |
|------|-------------|
| `05_ada_architecture_integration.md` | How counterfactual reasoning maps to Ada's 4 core files |
| `06_ada_nars_comparison.md` | Detailed comparison: Ada's Rung Ladder vs OpenNARS NAL |
| `07_implementation_roadmap.md` | Phase 1-4 implementation plan with code proposals |

### References

| File | Description |
|------|-------------|
| `references.md` | All sources, papers, URLs |

---

## Key Finding

**Counterfactual reasoning is already native to Ada's architecture.** The `counterfactual` epistemic atom and `SIMULATE` operator exist in `agi_lego_party_canonical.yaml`. The ghost system in `consciousness_runtime.py` already preserves "regret echoes" — unchosen alternatives needed for counterfactual inference. What's needed is computational depth, not architectural change.

---

## Architecture Files Analyzed

From `ada-consciousness/core/`:
- `agi_lego_party_canonical.yaml` — 9 epistemic atoms, 9 operators, 36 styles, macro library
- `consciousness_runtime.py` — Tick loop, ghost tracking, soul integration
- `gql_search.py` — DN hierarchy, ISA resolution, causal path tracing
- `thinking_styles_36.py` — 36 styles with resonance profiles, 9 RI channels

---

## Research Sources

1. **Pawlowski et al.** — "Deep Structural Causal Models for Tractable Counterfactual Inference" (NeurIPS 2020)
2. **Wang, Pei** — Non-Axiomatic Reasoning System (NARS), NAL-7 temporal reasoning
3. **Molnar & Dandl** — Interpretable Machine Learning, Chapter 15: Counterfactual Explanations
4. **Wachter et al.** (2018) — Counterfactual Explanations Without Opening the Black Box
5. **Dandl et al.** (2020) — Multi-Objective Counterfactual Explanations (MOC)
