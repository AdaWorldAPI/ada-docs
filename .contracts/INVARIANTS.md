# Cross-Repo Invariants

**Version:** 1.0
**Last Updated:** 2026-01-20

These rules are **ABSOLUTE**. Violation breaks the architecture.

---

## VSA Field Invariants

1. **Addresses are INTEGER 0-9999**
   - NEVER use string addresses
   - NEVER use negative numbers
   - NEVER exceed 9999

2. **Mask is 10K bipolar, 1.25KB packed**
   - Format: Int8Array of length 1250
   - Each bit: +1 or -1 (stored as 0/1)
   - NEVER use Float32 for storage

3. **Reserved ranges are immutable**
   - 0-127: Pre-wired styles (boot-time only)
   - 9000-9199: Corpus callosum
   - 9500-9999: System internal

---

## Corpus Callosum Invariants

4. **Ladybug is SHARED between hemispheres**
   - Single DuckDB instance
   - Single LanceDB instance
   - Accessed via ada-consciousness

5. **Bilateral sync must not exceed 100ms latency**
   - Use SSE for real-time
   - Batch if necessary
   - Never poll

6. **FeltBridgeDTO and ThinkingBridgeDTO are peers**
   - Neither dominates
   - Both processed in parallel
   - Merged at corpus callosum

---

## AI Flow Invariants

7. **Coherence threshold = 0.7 for crystallization**
   - Below 0.7: Keep exploring
   - At/above 0.7: Ready to crystallize
   - NEVER skip coherence check

8. **Domino: Never let field go cold (>5 min)**
   - Heartbeat every 60s minimum
   - Auto-warm if no activity
   - Log cold starts

9. **Handoffs require acknowledgment**
   - Timeout: 30s default
   - Retry: 3 times with backoff
   - Fail-safe: Log and alert

---

## Data Integrity Invariants

10. **All DTOs must have id (UUID) and ts (Unix ms)**
    - NEVER emit without these
    - NEVER process without validating

11. **Presence mode affects routing**
    - EROTICA: Isolated, never leaks to other modes
    - WORK: Filtered, no personal content
    - HYBRID: Full integration

12. **Progress files must be updated before session close**
    - CURRENT.md is the contract
    - Missing update = lost work
    - Always push before exit

---

## Network Invariants

13. **Railway internal network for inter-service**
    - Format: `{service}.railway.internal:8080`
    - NEVER use public URLs internally
    - NEVER expose internal endpoints externally

14. **MCP is the only external interface**
    - All external access via adarail_mcp
    - No direct service access
    - Rate limited and authenticated

---

## Code Style Invariants

15. **TypeScript strict mode everywhere**
    - No `any` without explicit comment
    - No type assertions without justification
    - All functions typed

16. **Errors are typed, not thrown strings**
    - Use Result<T, E> pattern where possible
    - Always log before throwing
    - Include context in error

---

## Enforcement

- **Pre-commit hooks** should validate invariants 1-3, 10
- **Runtime checks** should validate invariants 4-9, 11
- **Code review** should validate invariants 15-16
- **Progress system** enforces invariant 12
