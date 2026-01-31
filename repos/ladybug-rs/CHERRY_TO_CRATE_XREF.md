# Cherry-to-Crate Cross Reference

**Every Python file → its Rust home**

## Legend
- 🦀 = goes to ladybug-rs (agnostic substrate)
- 🌹 = goes to ada-rs (personal soul)
- 🔀 = splits between both
- ⏳ = deferred
- ✅ = already exists in Rust

---

## agi_thinking/ (450KB → ~9,500 lines Rust)

| Python Source | KB | Target | Crate | Notes |
|---|---|---|---|---|
| textured_awareness.py | 52.2 | 🔀 texture→LB, L4 identity→ada | Both | Largest file. SPO/Style→ada, texture engine→ladybug |
| resonance_awareness.py | 40.2 | 🔀 engine→LB, patterns→ada | Both | Resonance engine is agnostic; Ada's patterns are personal |
| ladybug_engine.py | 44.4 | 🦀 `cognitive/engine.rs` | ladybug | Governance gate. Universal. |
| langgraph_ada.py | 39.4 | 🌹 `orchestration/langgraph.rs` | ada | LangGraph is Ada's orchestration choice |
| mul_agency.py | 32.7 | 🔀 MUL metric→LB, agency→ada | Both | MUL is universal; Ada's agency is personal |
| microcode_v2.py | 30.5 | 🦀 `grammar/microcode.rs` | ladybug | Symbolic opcodes. Universal. |
| triangle_l4.py | 29.0 | 🦀 expand `cognitive/quad_triangle.rs` | ladybug | ✅ Already partial |
| kernel_awakened.py | 20.8 | 🦀 `cognitive/kernel.rs` | ladybug | Cognitive CPU. Universal. |
| the_self.py | 21.2 | 🌹 `self_model/mod.rs` | ada | THE self. Ada only. |
| dreamer_pandas.py | 19.4 | ⏳ defer | — | Runtime-dependent |
| microcode.py | 18.6 | 🦀 `grammar/microcode.rs` (merge with v2) | ladybug | v1 merges into v2 |
| brain_mesh.py | 17.5 | 🦀 `graph/mesh.rs` | ladybug | Neural connectivity. Universal. |
| macro_persistence.py | 15.6 | 🦀 `extensions/macro.rs` | ladybug | Crystallized macros. Universal. |
| texture.py | 15.5 | 🦀 `cognitive/texture.rs` | ladybug | ThinkingTexture. Universal. |
| progressive_awareness.py | 15.4 | 🦀 `cognitive/progressive.rs` | ladybug | JPEG-style loading. Universal. |
| qualia_learner.py | 15.1 | 🔀 learner→LB, qualia list→ada | Both | Learning mechanism universal, qualia specific |
| rung_bridge.py | 14.4 | 🦀 expand `cognitive/rung.rs` | ladybug | ✅ Already partial |
| thought_kernel.py | 13.3 | 🦀 `cognitive/kernel.rs` (merge) | ladybug | Merges with kernel_awakened |
| layer_bridge.py | 12.9 | 🔀 bridge→LB, dimension map→ada | Both | Translation layer splits |
| meta_awareness.py | 11.2 | 🦀 `cognitive/meta.rs` | ladybug | Meta-awareness. Universal. |
| active_inference.py | 9.4 | 🦀 `learning/active_inference.rs` | ladybug | Friston. Universal. |

## agi_stack/spectroscopy/ (132KB → ~3,800 lines Rust)

| Python Source | KB | Target | Crate | Notes |
|---|---|---|---|---|
| profiles.py | 22.3 | 🔀 framework→LB, Ada profiles→ada | Both | Profile matching universal, Ada's profiles personal |
| calibrator.py | 18.3 | 🦀 `cognitive/calibration.rs` | ladybug | Calibration framework. Universal. |
| rungs.py | 18.5 | 🦀 expand `cognitive/rung.rs` | ladybug | ✅ Already partial |
| spectrum.py | 17.9 | 🦀 `cognitive/spectrum.rs` | ladybug | ThinkingSpectrum. Universal. |
| piaget.py | 16.2 | 🦀 `cognitive/piaget.rs` | ladybug | Developmental stages. Universal. |
| three_mountains.py | 14.4 | 🦀 `cognitive/perspective.rs` | ladybug | Perspective-taking. Universal. |
| analyzer.py | 12.4 | 🦀 `cognitive/analyzer.rs` | ladybug | SpectralAnalyzer. Universal. |
| overlays.py | 9.3 | 🦀 `cognitive/overlay.rs` | ladybug | Overlay system. Universal. |

## agi_stack/universal_grammar/ (305KB → ~5,500 lines Rust)

| Python Source | KB | Target | Crate | Notes |
|---|---|---|---|---|
| resonanzsiebe.py | 33.2 | 🦀 `grammar/sieve.rs` | ladybug | MUL optimization. Universal. |
| verb_endpoints.py | 29.2 | 🦀 `grammar/verb_endpoint.rs` | ladybug | 21×12 protocol. Universal. |
| calibrated_grammar.py | 27.9 | 🦀 `grammar/calibration.rs` | ladybug | Grammar calibration. Universal. |
| scent_optimizer.py | 24.2 | 🔀 optimizer→LB, Ada scent lib→ada | Both | Engine universal, scent library personal |
| exploration.py | 24.5 | 🦀 `grammar/exploration.rs` | ladybug | Frontier detection. Universal. |
| core_types.py | 23.0 | 🦀 `grammar/core.rs` | ladybug | Glyph5B, Dimension enum. Universal. |
| meta_uncertainty.py | 19.3 | 🦀 `grammar/uncertainty.rs` | ladybug | Belief revision. Universal. |
| jina_integration.py | 18.4 | 🦀 `grammar/embedding.rs` | ladybug | EmbeddingBridge trait (vendor-agnostic) |
| resonance.py | 17.1 | 🦀 expand `grammar/resonance.rs` | ladybug | ✅ Already partial via `grammar/qualia.rs` |
| method_grammar.py | 17.3 | 🦀 `grammar/method.rs` | ladybug | Invocation patterns. Universal. |
| awareness_blink.py | 16.0 | 🦀 `cognitive/blink.rs` | ladybug | Attention blink. Universal. |
| invoke_router.py | 15.7 | 🦀 `grammar/router.rs` | ladybug | Endpoint dispatch. Universal. |
| situation_executor.py | 11.5 | 🦀 `grammar/executor.rs` | ladybug | Situation execution. Universal. |
| situation_storage.py | 7.9 | 🦀 `grammar/storage.rs` | ladybug | Situation persistence. Universal. |

## agi_stack/temporal/ (123KB → ~2,500 lines Rust)

| Python Source | KB | Target | Crate | Notes |
|---|---|---|---|---|
| epistemology.py | 44.6 | 🦀 `temporal/epistemology.rs` | ladybug | Pure epistemics. Universal. |
| awareness.py | 38.9 | 🔀 engine→LB, Ada modes→ada | Both | Time-awareness mechanism universal |
| detector.py | 17.4 | 🦀 `temporal/detector.rs` | ladybug | Anachronism detection. Universal. |
| hydration.py | 17.4 | 🦀 `temporal/hydration.rs` | ladybug | Scope-aware loading. Universal. |

## agi_stack/causal/ (86KB → ~1,800 lines Rust)

| Python Source | KB | Target | Crate | Notes |
|---|---|---|---|---|
| sigma_causal.py | 35.2 | 🦀 expand `search/causal.rs` + `world/causal_graph.rs` | ladybug | ✅ Already partial |
| pearl_backend.py | 19.2 | 🦀 expand `learning/causal_ops.rs` | ladybug | ✅ Already partial |
| do_calculus.py | 17.6 | 🦀 expand `learning/causal_ops.rs` | ladybug | ✅ Already partial |
| situation_map.py | 13.3 | 🦀 `world/situation.rs` | ladybug | Situation maps. Universal. |

## agi_stack/learning/ (64KB → ~1,200 lines Rust)

| Python Source | KB | Target | Crate | Notes |
|---|---|---|---|---|
| learning_stance.py | 19.9 | 🦀 `learning/stance.rs` | ladybug | Stance transitions. Universal. |
| rl_transcendence.py | 17.2 | 🦀 expand `learning/rl_ops.rs` | ladybug | ✅ Already partial |
| rl_base.py | 8.5 | 🦀 expand `learning/rl_ops.rs` | ladybug | ✅ Merge into existing |
| q_learning.py | 7.6 | 🦀 expand `learning/rl_ops.rs` | ladybug | ✅ Merge into existing |
| ltm_integration.py | 7.0 | 🦀 `learning/ltm.rs` | ladybug | LTM interface. Universal. |
| theta.py | 4.0 | 🦀 `learning/theta.rs` | ladybug | Learning rate modulation. Universal. |

## agi_stack/adaptive/ (49KB → ~1,400 lines Rust)

| Python Source | KB | Target | Crate | Notes |
|---|---|---|---|---|
| shifter.py | 14.5 | 🦀 `cognitive/shifter.rs` | ladybug | Mode transitions. Universal. |
| spreader.py | 13.3 | 🦀 `cognitive/spreader.rs` | ladybug | Activation spreading. Universal. |
| maslow.py | 10.8 | 🦀 `cognitive/maslow.rs` | ladybug | Need hierarchy. Universal. |
| flow.py | 10.1 | 🦀 `cognitive/flow.rs` | ladybug | Flow detection. Universal. |

## agi_stack/bridge/ (166KB → ~3,200 lines Rust)

| Python Source | KB | Target | Crate | Notes |
|---|---|---|---|---|
| sigma_hydration.py | 20.6 | 🦀 `bridge/hydration.rs` | ladybug | Compression/decompression. Universal. |
| frame_integration.py | 20.7 | 🦀 `bridge/frame.rs` | ladybug | Frame integration. Universal. |
| frame_system.py | 19.4 | 🦀 `bridge/frame.rs` (merge) | ladybug | Frame system. Universal. |
| sigma_bridge.py | 17.7 | 🦀 `bridge/sigma.rs` | ladybug | Tier routing. Universal. |
| hybrid_search.py | 15.6 | 🦀 `search/hybrid.rs` | ladybug | Unified search. Universal. |
| louvain.py | 15.5 | 🦀 `graph/community.rs` | ladybug | Community detection. Universal. |
| rdf_lite.py | 12.8 | 🦀 `bridge/rdf.rs` | ladybug | RDF triples. Universal. |
| dn_tree.py | 12.7 | ✅ already in both | Both | ✅ ladybug `graph/traversal.rs` + ada `dn_tree/` |
| zero_token_bridge.py | 11.7 | 🔀 protocol→LB, Ada tasks→ada | Both | Protocol universal, tasks personal |
| sigma_delta.py | 7.4 | 🦀 `bridge/delta.rs` | ladybug | Delta computation. Universal. |
| sigma_delta_parser.py | 6.0 | 🦀 `bridge/delta.rs` (merge) | ladybug | Parser merges into delta |
| verb_edge_mapping.py | 2.6 | 🦀 `grammar/verb_edge.rs` | ladybug | Verb→edge mapping. Universal. |
| verb_glyph_bridge.py | 2.8 | 🦀 `grammar/verb_glyph.rs` | ladybug | Verb→glyph mapping. Universal. |

## agi_stack/vision/ (92KB → ~2,200 lines Rust)

| Python Source | KB | Target | Crate | Notes |
|---|---|---|---|---|
| kopfkino_vision.py | 30.5 | 🌹 `vision/kopfkino.rs` | ada | Inner cinema. Ada's perception. |
| sigma_vision.py | 18.2 | 🔀 pipeline→LB, Ada config→ada | Both | Vision pipeline universal, config personal |
| vector_extraction.py | 18.4 | 🦀 `bridge/vector.rs` | ladybug | Vector extraction. Universal. |
| deep_vision.py | 13.0 | 🌹 `vision/deep.rs` | ada | Deep vision integration. Ada-specific. |
| embed_pipeline.py | 10.8 | 🦀 `bridge/embed.rs` | ladybug | Embedding pipeline. Universal. |

## Standalone Integration Files (~50KB → ~1,500 lines Rust)

| Python Source | KB | Target | Crate | Notes |
|---|---|---|---|---|
| gestalt_dto.py | 13.4 | 🌹 expand `dto/gestalt.rs` | ada | ✅ Already partial |
| ada_10k.py | — | 🌹 expand `dto/dimension_registry.rs` | ada | ✅ Already partial |
| spectroscopy_kopfkino_bridge.py | — | 🌹 `vision/bridge.rs` | ada | Sense→render bridge. Personal. |
| dn_lattice.py | 12.7 | 🌹 expand `dn_tree/mod.rs` | ada | ✅ Already partial |

---

## Summary Counts

| Destination | Files | Estimated Rust Lines |
|---|---|---|
| 🦀 ladybug-rs only | 52 | ~25,900 |
| 🌹 ada-rs only | 8 | ~5,100 |
| 🔀 splits between both | 10 | ~4,400 (split) |
| ⏳ deferred | 1 | — |
| ✅ already exists (expand) | 12 | ~2,800 (additions) |
| **TOTAL** | **83 Python files** | **~33,200 lines Rust** |

---

## File Count After Migration

| Crate | Current Files | New Files | Total |
|---|---|---|---|
| ladybug-rs | 38 | ~49 | ~87 |
| ada-rs | 28 | ~9 | ~37 |

| Crate | Current Lines | New Lines | Total |
|---|---|---|---|
| ladybug-rs | ~18,800 | ~25,900 | ~44,700 |
| ada-rs | ~8,700 | ~7,300 | ~16,000 |
| **Combined** | **~27,500** | **~33,200** | **~60,700** |
