# Review: 3-Stroke Adaptive HDR Cascade Prompt Doc

**Reviewer**: Claude (cross-session)  
**Date**: 2026-02-22

---

## Verdict: Good spec, wrong Bug 1, risky Step 4, and "Branch from main (post PR #32)" is stale guidance

The doc is well-structured as a Claude Code prompt — clear bugs, clear implementation steps, clear "what not to do." The statistical foundation is correct. But three things need fixing before handing this off.

---

## Bug 1 Is Wrong: There Is No CPUID Per-Call

The doc claims:

> `hamming_search_adaptive` calls `hamming_chunk_inline` → `rustynum_core::simd::hamming_distance` for every partial slice. Each call runs `is_x86_feature_detected!("avx512vpopcntdq")`.

This is false. `hamming_chunk_inline` in `hdc.rs` (line 633) is a **pure scalar function** — 4×-unrolled u64 XOR + `count_ones()`. It never calls `rustynum_core::simd::hamming_distance`. It never touches CPUID.

The actual problem is the **opposite** of what the doc says: `hamming_search_adaptive` does NOT use SIMD at all. It uses the scalar `hamming_chunk_inline` for every stage of every candidate. The bug isn't "CPUID per call" — it's "no SIMD, period."

The `select_hamming_fn` extraction is still the right fix (it enables the batch path to use SIMD), but the framing is misleading. If Claude Code reads "300K CPUID checks" and then greps for `is_x86_feature_detected` in the adaptive path, it'll find nothing and get confused.

**Fix**: Rewrite Bug 1 as:

> `hamming_search_adaptive` uses `hamming_chunk_inline` — a pure scalar function (line 633) that does u64 XOR + `count_ones()`. It never dispatches to AVX-512 VPOPCNTDQ. For 100K candidates × 2KB vectors, this leaves ~12× performance on the table versus the SIMD path that `hamming_batch` already uses. Additionally, the serial per-candidate loop prevents batch SIMD processing.

## Bug 2 Is Correctly Identified But Overstates BF16

The observation is right: all 3 stages compute integer popcount. There's no type transition. And `dot_i8_slice` in `hdc.rs` (line 672) is also scalar — it does `(a[i] as i8 as i32) * (b[i] as i8 as i32)` in a 32-element loop. No VNNI.

But the doc says "The BF16 infrastructure exists in `bf16_gemm.rs`" and then later says "Do NOT implement BF16 conversion in this PR — use existing `dot_i8`." This is contradictory signaling. The BF16 infrastructure is conversion functions and struct definitions — there are no SIMD BF16 dot product intrinsics wired up. `dot_i8` in simd.rs doesn't exist either — there's no `dot_i8` or VNNI path in `rustynum-core/src/simd.rs` at all.

The implementation correctly uses `dot_i8_slice` from `hdc.rs` for Stroke 3, but the code block references `dot_i8(query, candidate)` as if it's a function in `rustynum_core::simd`. It isn't. Either:

1. Move `dot_i8_slice` from `hdc.rs` to `rustynum-core/src/simd.rs` as `dot_i8` (with VNNI dispatch), or
2. Keep using `dot_i8_slice` and acknowledge it's scalar

Option 1 is better and consistent with the `select_dot_i8_fn` pattern proposed in Step 5. But the doc needs to explicitly say "move `dot_i8_slice` to simd.rs and add VNNI dispatch" rather than implying it already exists.

**Fix**: Add to Step 5:

> Move `dot_i8_slice` from `hdc.rs` to `rustynum-core/src/simd.rs` as `pub fn dot_i8`. Add VNNI dispatch via `select_dot_i8_fn`. The current scalar implementation becomes the fallback.

## Bug 3 Is Correct

The serial per-candidate loop is real. The batch-stroke model is the right fix. No notes.

---

## Step 4: Prefilter Rewrite Is Risky

The proposed rewrite of `two_stage_hamming_search` in `prefilter.rs` changes semantics:

**Current**: Takes `prefix_bytes` and `prefilter_k` as parameters. Stage 1 computes prefix Hamming on ALL vectors, selects top-k by `select_nth_unstable_by_key`, then Stage 2 does exact Hamming on those k candidates. Returns sorted top `final_k`.

**Proposed**: Delegates to `hdr_cascade_search` with a heuristic threshold (`bytes_per_vec * 4`). The σ-based rejection replaces the top-k selection.

Problems:

1. **The heuristic threshold is arbitrary.** `bytes_per_vec * 4 = 50% bit distance` has no statistical basis. The current API lets callers control `prefilter_k` (how many survivors). The proposed API loses this control.

2. **Semantic change.** Current returns exactly `final_k` results (or fewer if database is smaller). Proposed returns all candidates within threshold, then truncates. For callers expecting exactly k results, this could return 0 if threshold is too tight, or thousands if too loose.

3. **`prefilter.rs` uses `portable_simd` (`u8x64`).** It's behind `#[cfg(any(feature = "avx512", feature = "avx2"))]`. The proposed rewrite removes the Stage 2 SIMD path and replaces it with `hdr_cascade_search` which uses the `select_hamming_fn` pattern — different SIMD dispatch mechanism. Not wrong, but the inconsistency within `prefilter.rs` (which also has `pruned_gemm_rows` using `u8x64`) is worth noting.

4. **The `_prefix_bytes` and `_prefilter_k` parameters become dead.** If this is a refactor to a new API, remove them. If backward compat matters, keep the old function and add a new one.

**Fix**: Either:
- Leave `two_stage_hamming_search` alone (it works, it's not the hot path), or
- Create a new `hdr_hamming_search` alongside it that uses the cascade, and deprecate the old one

## Step 2: `hdr_cascade_search` Implementation Notes

The pseudocode is mostly correct but has specific issues:

### Warmup re-scan is wasteful

> "Phase 1b: Scan ALL candidates (including warmup, re-checking them)"

The warmup candidates' partial distances were already computed. Store them and skip re-computation for indices `0..warmup_n`. Minor, but for 128 candidates at 128 bytes each, that's 16KB of redundant XOR+popcount.

### `dot_i8` doesn't exist in simd.rs

Lines like `let query_norm_sq = dot_i8(query, query)` reference a function that doesn't exist in `rustynum-core/src/simd.rs`. This will cause a compilation error. Either add the function first (Step 5 before Step 2) or use `dot_i8_slice` from `hdc.rs` — but that would create a reverse dependency (core depending on rs), which is wrong.

**Fix**: Reorder steps: Step 5 (move dot_i8 to simd.rs) must come before Step 2.

### `partial_cmp().unwrap_or` — good

```rust
results.sort_unstable_by(|a, b| b.precise.partial_cmp(&a.precise).unwrap_or(std::cmp::Ordering::Equal));
```

This correctly handles NaN. Consistent with U2 fix.

### Stroke 2 incremental is clever

```rust
let d_rest = hamming_fn(&query[s1_bytes..], &database[base + s1_bytes..base + vec_bytes]);
let d_full = d_prefix + d_rest;
```

This avoids recomputing the prefix. Good. But note that `d_prefix` in the survivors list is the *raw* partial distance, not the scaled estimate. The code stores the raw distance correctly (`survivors.push((i, d))`) — the scaling is only used for the reject threshold. This is correct.

### The warmup σ approach vs per-candidate σ

The doc correctly identifies the tradeoff:

> The batch σ is slightly less precise but MUCH faster (no f64 sqrt per candidate).

This is a good engineering call. The per-candidate σ in the current code does `sqrt()` for every single candidate in Stage 1 and Stage 2 — that's 200K `sqrt` calls for 100K candidates. The population σ from 128 warmup samples is statistically adequate for the 3σ rejection (the sampling distribution of σ converges quickly).

One concern: the warmup assumes the first 128 candidates are representative of the population. If the database is sorted (close matches first), the warmup overestimates proximity and sets too-tight thresholds. Add a note: "warmup assumes uniformly distributed candidates."

---

## Factual Corrections Needed

1. **"Branch from main (post PR #32)"** — PR #32 already exists and is closed. The branch should be from current main (post PR #33), or just say "branch from main."

2. **"300K CPUID checks"** — zero CPUID checks. The path is entirely scalar.

3. **"`dot_i8` via VNNI"** — no `dot_i8` in simd.rs. No VNNI dispatch exists anywhere in the codebase. `dot_i8_slice` in hdc.rs is scalar.

4. **"The `cosine_search_adaptive` already does a cosine cascade using `dot_i8_slice` — but it has the same CPUID-per-call bug AND doesn't use VNNI"** — It has neither bug. It doesn't call CPUID at all (uses scalar `dot_i8_slice`). It doesn't use VNNI because no VNNI path exists. The real bug is "scalar where SIMD could be used."

5. **`hamming_batch` "already has the hoisted function-pointer pattern"** — verify this. In simd.rs, `hamming_batch` calls `hamming_distance` which does runtime CPUID dispatch per-call (via `is_x86_feature_detected!`). There's no hoisted function pointer in the current code. The doc's `select_hamming_fn` is the fix for BOTH paths.

---

## Statistical Foundation: Verified Correct

The binomial sampling argument is sound. For p=0.5 (random), σ of a 1024-bit sample estimating a 16384-bit true distance:

σ = √(n × p × (1-p) × (N/n)²) where n=1024 sample bits, N=16384 total bits, p=estimated bit-flip probability

For d=400 (close match), p=400/16384≈0.024, σ ≈ √(1024 × 0.024 × 0.976 × 16²) ≈ 79. Matches the table.

The 99σ separation between close (d=400) and random (d=8192) at 128 bytes is correct and makes the case that even 1/16 sampling is overkill for rejection. 1/32 would still give >50σ separation.

---

## Summary: Changes Before Sending to Claude Code

| # | Change | Priority |
|---|---|---|
| 1 | Rewrite Bug 1: scalar path, not CPUID per-call | 🔴 Blocks correct implementation |
| 2 | Add "move dot_i8_slice to simd.rs" as explicit step before Step 2 | 🔴 Blocks compilation |
| 3 | Fix "Branch from post PR #32" → "Branch from main" | 🟡 Avoids confusion |
| 4 | Fix all CPUID/VNNI references to say "scalar, no SIMD dispatch" | 🟡 Avoids confusion |
| 5 | Verify hamming_batch hoisted pattern claim | 🟡 May be wrong |
| 6 | Rethink Step 4 (prefilter rewrite) — semantic change risk | 🟡 API break |
| 7 | Reorder: Step 5 before Step 2 | 🟢 Compilation order |
| 8 | Note warmup assumes uniform distribution | 🟢 Edge case doc |
