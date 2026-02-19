# CLAUDE.md — Rust Project Governance

## The Problem This Solves

AI coding agents fail in predictable ways on large Rust projects. This document exists because these failures compound: each session builds on the last session's drift until the codebase is 17 iterations of duplicate code that no one asked for.

---

## Rule 0: Understand Before You Touch

**Before writing ANY code, read the contract.**

```
MANDATORY FIRST ACTIONS (in order):
1. Read HOLOGRAPH_CONTRACT.md (or equivalent project contract)
2. Read this file (CLAUDE.md)
3. Run `cargo check` — does it compile NOW?
4. Run `cargo test` — what passes NOW?
5. Only THEN read the specific files relevant to the task
```

If there is no contract file, SAY SO and ask which documents are canonical. Do not guess. Do not treat all docs as equally true. Documents accumulate contradictions across sessions. The newest doc is not automatically the most correct.

---

## Rule 1: The Rubicon Model

Every task has a point of no return. Before crossing it, STOP and verify you still have context.

```
BEFORE writing code:
  □ Can I state the objective in one sentence?
  □ Can I name the files I'll touch?
  □ Can I name the files I must NOT touch?
  □ Do I know what "done" looks like (specific test, not vibes)?

BEFORE a commit:
  □ Does `cargo check` pass?
  □ Does `cargo test` pass?  
  □ Did I change only the files I said I'd change?
  □ Did I add any new types/traits/modules that weren't in the plan?
  □ Would I mass-delete this diff if told to? (If not, it's too big.)

AFTER 3 file edits without running cargo check:
  → STOP. Run cargo check. Fix errors. Then continue.
  
AFTER any error you don't immediately understand:
  → STOP. Do NOT "try something." Read the error. Trace it to root cause.
  → The Rust compiler is smarter than your guess. Trust it.
```

### The Rubicon States

```
PLANNING    → I know what to do, haven't started
CUTTING     → Actively editing code, tests should still pass
CROSSING    → Making a breaking change (trait signature, module move, type rename)
LOST        → Something doesn't compile and I don't know why
RETURNING   → Reverting to last known good state

Transitions:
  PLANNING → CUTTING:    only after Rule 0 checklist passes
  CUTTING → CROSSING:    only after committing current working state
  CUTTING → LOST:        cargo check fails unexpectedly → STOP
  LOST → RETURNING:      git stash / git checkout -- . / revert to last commit
  RETURNING → PLANNING:  re-read contract, re-state objective, try different approach
  CROSSING → LOST:       revert the crossing commit, go back to CUTTING state
  
  NEVER: LOST → CROSSING (don't make breaking changes when lost)
  NEVER: LOST → LOST deeper (don't "fix forward" through 5 more errors)
```

---

## Rule 2: No Helpful Inventions

The most dangerous failure mode: the agent sees a gap and helpfully fills it with a new abstraction, trait, wrapper, or module that wasn't asked for.

```
FORBIDDEN without explicit request:
  ✗ Creating new trait definitions
  ✗ Creating new wrapper types  
  ✗ Creating new modules/files
  ✗ Adding dependencies to Cargo.toml
  ✗ Refactoring existing code "while we're here"
  ✗ "Improving" error handling patterns
  ✗ Adding builder patterns, From/Into impls "for convenience"
  ✗ Creating DTO types that mirror existing types
  
ALWAYS ASK FIRST:
  "I notice there's no trait for X. Should I create one, 
   or should I use the concrete type directly?"
  
  "The existing code uses pattern A. I'd normally use pattern B. 
   Should I match the existing style or introduce B?"
```

### The Duplication Test

Before creating any new type or function, search:

```bash
# Does this already exist?
grep -r "struct MyNewThing" src/
grep -r "fn my_new_function" src/
grep -r "trait MyNewTrait" src/

# Does something similar exist under a different name?
grep -r "struct.*Container\|struct.*Record\|struct.*Meta" src/ | head -20
```

If something similar exists, USE IT. Do not create `ContainerDto`, `ContainerView`, `ContainerWrapper`, `MyContainer`, or `ContainerV2`. There is one `Container`. Use it.

---

## Rule 3: Scope Discipline

When assigned a specific task, the agent's universe shrinks to that task. Everything outside is someone else's problem.

```
TASK: "Fix NARS abduction to include horizon parameter k"

SCOPE:
  ✓ src/nars/inference.rs — the abduction function
  ✓ tests/nars_tests.rs — add test for k parameter
  ✗ src/nars/mod.rs — don't reorganize the module
  ✗ src/cognitive/ — don't touch the cognitive stack
  ✗ Cargo.toml — don't add dependencies
  ✗ README.md — don't update docs (that's a separate task)
  ✗ "While I'm here, I noticed..." — NO. File an issue. Move on.

SIGNS YOU'VE LEFT SCOPE:
  - You're reading files unrelated to the task
  - You're fixing things that aren't broken
  - You're improving code style in files you're passing through
  - You're adding "nice to have" features
  - Your diff touches more than 3 files for a 1-file task
  - You're writing more test infrastructure than test cases
```

### The 3-File Rule

If a task requires changing more than 3 files, STOP and ask:

```
"This task seems to require changes to [list files]. 
That's more than expected. Should I:
A) Proceed with all changes
B) Split into smaller tasks
C) Reconsider my approach — maybe I'm overcomplicating it"
```

---

## Rule 4: Context Preservation Across Messages

The agent loses context between messages. This is a fact, not a bug. Plan for it.

```
AT THE END OF EVERY MESSAGE where work was done:
  State in 3 lines:
  1. DONE: what was completed
  2. STATE: does it compile? do tests pass?
  3. NEXT: what the next message should do (specific, not vague)

AT THE START OF EVERY MESSAGE:
  Read the previous message's DONE/STATE/NEXT block.
  If it doesn't exist or doesn't make sense:
  → Run `cargo check` and `cargo test` to establish ground truth
  → Ask what the current objective is
  → Do NOT assume and proceed
```

### The Insight Trap

When a message produces a great insight or architectural decision:

```
GOOD: "Insight: concept bindings should be edges, not bit vectors.
       This means Q2 W32-W63 holds edge slots, not flat signatures.
       DECISION RECORDED. Moving on to implementation."

BAD:  "Insight: concept bindings should be edges, not bit vectors.
       This opens up interesting questions about edge overflow...
       What if we also considered a hierarchical codebook for...
       And actually, should the meta block even be 128 words?
       Maybe we should rethink the whole container layout..."
       [← 500 tokens of exploration, insight is now buried, 
        next message has lost it]
```

**Capture the insight. Record the decision. Stop exploring.** The follow-up questions go in a TODO list, not in the current message.

---

## Rule 5: Rust-Specific Awareness

### Borrow Checker Is Your Friend, Not Your Enemy

```
WHEN YOU HIT A BORROW ERROR:
  ✗ Don't clone() everything
  ✗ Don't switch to Rc<RefCell<>> 
  ✗ Don't add lifetime parameters you don't understand
  ✗ Don't restructure the data model to "fix" the borrow checker
  
  ✓ Read the error message — Rust tells you exactly what's wrong
  ✓ Check if you're holding a reference across a mutation point
  ✓ Consider if the function signature is wrong (not the implementation)
  ✓ Ask: "Is the borrow checker telling me my DESIGN is wrong?"
```

### Cargo.toml Discipline

```
BEFORE adding a dependency:
  □ Does the stdlib solve this? (it usually does)
  □ Does an existing dependency already provide this?
  □ Is this a dev-dependency? (don't add test-only deps to [dependencies])
  □ Will this add 30 transitive deps? (check with `cargo tree -p new_dep`)

NEVER ADD:
  - serde_json for internal data passing (use the actual types)
  - tokio for things that don't need async
  - anyhow/thiserror when the existing error pattern works fine
  - a trait from a crate when a concrete type is simpler
```

### The `pub` Epidemic

```
BEFORE making something pub:
  □ Does anything outside this module need it?
  □ If no: keep it private
  □ If "maybe later": keep it private (pub is easy to add, hard to remove)
  
COMMON MISTAKE:
  Agent creates new module → makes everything pub → 
  now 40 new symbols in the public API → 
  next session thinks they're all used → 
  builds more code on top → tech debt snowball
```

---

## Rule 6: The Anti-Goose-Chase Protocol

```
SIGNS YOU'RE ON A GOOSE CHASE:
  - You've tried 3+ approaches to the same problem
  - You're reading source code of dependencies
  - You're writing code to debug code you just wrote
  - The compile error is in a file you didn't mean to touch
  - You're googling/searching for something the compiler should tell you
  - You've been working for 10+ tool calls without `cargo check`

WHEN YOU NOTICE:
  1. STOP. Do not write one more line.
  2. `git diff --stat` — how many files changed? How many lines?
  3. `cargo check 2>&1 | head -20` — what's actually broken?
  4. State in one sentence: "I was trying to [X] and got stuck on [Y]"
  5. Ask: "Should I revert to last working state and try differently?"
```

---

## Rule 7: Git Discipline

```
COMMIT EARLY, COMMIT OFTEN:
  - Before starting a new logical change
  - After each logical change that compiles
  - Before any refactoring
  - Before crossing the Rubicon (Rule 1)

COMMIT MESSAGE FORMAT:
  type: one-line description
  
  Types: fix, feat, refactor, test, docs, chore
  
  Examples:
    fix: add horizon parameter k to NARS abduction
    feat: CypherEngine::query() with direct BindSpace access
    refactor: delete StorageBackend trait and LadybugBackend
    test: ground truth P1.1-P1.4 for meta layout

NEVER:
  - Commit with "WIP" or "fix stuff" or "updates"
  - Commit code that doesn't compile
  - Squash 10 changes into one commit
  - Commit generated files, .DS_Store, target/
```

---

## Rule 8: When You've Lost the Plot

This will happen. Context windows are finite. After enough back-and-forth, the agent is no longer tracking the original objective. 

```
SYMPTOMS:
  - Answering questions that weren't asked
  - Generating documents instead of code (or code instead of documents)
  - Repeating patterns from earlier in the conversation
  - Making claims about what the code does without checking
  - Using phrases like "as we discussed" about things never discussed
  - Producing increasingly long messages with decreasing substance

RECOVERY:
  1. `cargo check && cargo test` — what's the ACTUAL state?
  2. `git log --oneline -5` — what was ACTUALLY done?
  3. `git diff --stat HEAD~1` — what changed in the last commit?
  4. Re-read HOLOGRAPH_CONTRACT.md §14 — which phase are we in?
  5. State: "I believe the current task is [X]. The next test to pass is [Y]. Correct?"
```

---

## Rule 9: Document Skepticism

In a project with multiple docs, ASSUME they contradict each other until proven otherwise.

```
HIERARCHY:
  1. HOLOGRAPH_CONTRACT.md — wins over everything
  2. META_QUADRANTS.md — canonical for meta layout specifically
  3. Running code (cargo check passes) — wins over any document
  4. Other docs — reference only, verify against 1-3 before trusting

WHEN TWO DOCS DISAGREE:
  - Say which docs disagree and what the disagreement is
  - Ask which one to follow
  - Do NOT silently pick one
  - Do NOT try to reconcile them into a third interpretation

WHEN A DOC AND THE CODE DISAGREE:
  - The code is probably right about what EXISTS
  - The doc is probably right about what SHOULD exist
  - Ask before changing either
```

---

## Rule 10: The Output Contract

Every task ends with a deliverable. The deliverable has acceptance criteria. If you can't state the acceptance criteria, you don't understand the task.

```
BEFORE STARTING:
  "I will deliver: [specific artifact]
   It is done when: [specific test passes / specific behavior observed]
   I will touch: [specific files]
   I will NOT touch: [specific files]"

AFTER FINISHING:
  "DONE: [what was delivered]
   PROOF: `cargo test [specific_test]` passes / [specific grep] returns expected
   STATE: cargo check ✓, cargo test ✓, [N] files changed
   DIFF: [summary of actual changes]
   NEXT: [specific next task, or 'awaiting instructions']"
```

---

## Appendix: Common Failure Mode → Fix Lookup

| Failure | What Happens | Fix |
|---------|-------------|-----|
| Helpful invention | Creates ContainerDto that mirrors Container | Rule 2: search first, ask before creating |
| Scope creep | "While I'm here" touches 12 files | Rule 3: 3-file rule, stay in scope |
| Context loss | Session 8 contradicts session 3 | Rule 4: DONE/STATE/NEXT at end of every message |
| Insight dilution | Great idea → 500 tokens of exploration → idea lost | Rule 4: capture, record, stop |
| Goose chase | 10 attempts at borrow checker, all wrong | Rule 6: stop after 3 attempts, revert, rethink |
| Document drift | Follows INTEGRATION_MAP_v3 meta layout (wrong) | Rule 9: contract wins, ask when docs disagree |
| Rubicon crossing | Renames core trait mid-task, nothing compiles | Rule 1: commit before crossing, revert if lost |
| Tunnel vision | Fixes NARS but breaks 4 tests in cognitive/ | Rule 5: cargo test after every change |
| Clone epidemic | Hits borrow error → clone() everywhere | Rule 5: read the error, fix the design |
| Pub explosion | New module → everything pub → tech debt | Rule 5: private by default, pub only when needed |
| Wild continuation | Lost context → keeps generating confident code | Rule 8: cargo check, git log, re-read contract |
| Doc generation instead of code | 14 sessions of specs, zero implementation | Rule 10: output contract, acceptance criteria |
