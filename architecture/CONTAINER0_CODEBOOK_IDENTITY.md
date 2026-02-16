# Container 0: Codebook Identity Architecture

> **Date**: 2026-02-16
> **Status**: Foundational Spec
> **Supersedes**: Previous meta.rs layout (W0-127 with precomputed graph metrics, reserved words, RL/Q-values)
> **Core Insight**: There is no metadata. There is only topology. The codebook IS the identity.

## The Old Layout Was Wrong

The previous Container 0 treated nodes like database rows:

```
W32-39   RL / Q-values / rewards          ← derivable, not constitutive
W40-47   Bloom filter                      ← derivable
W48-55   Graph metrics (centrality etc.)   ← PRECOMPUTED = WASTED
W64-79   Rung history (16 words!)          ← excessive
W80-95   "Representation language"         ← vague
W112-125 "Reserved"                        ← 14 words of nothing
```

54 out of 128 words were filler. Over 40% of the metadata container was slack.

**Principle**: Don't precompute what you can derive. Don't reserve what you can use. Every bit must be constitutive — part of what the node IS, not what someone once measured about it.

## The New Layout: Four Zones

```
Container 0 (128 words = 1024 bytes = 8192 bits)

W0-15    CAM CODEBOOK          (16 words = 1024 bits)
W16-32   DN / B-TREE INDEX     (17 words = 1088 bits)
W33-64   HASHTAG EVERYTHING    (32 words = 2048 bits)
W65-128  NODE ADDRESS SPACE    (64 words = 4096 bits)
```

### W0-15: CAM Codebook (Identity)

The codebook IS the node. Not "node has codebook." The codebook is the identity.

- Content-addressable memory: lookup by pattern, not by address
- Compressed activation pattern against a universal 64K vocabulary
- Resonance finds the codebook OR creates a new one
- Two codebooks at Hamming distance zero ARE the same node

**The codebook is not trained then used. It emerges:**

1. Input fires against existing codebooks (SIMD popcount)
2. If something resonates → BIND into that codebook (it grows)
3. If nothing resonates → NEW codebook (it's born)
4. Identity is discovered or created by the act of resonance itself

### W16-32: DN / B-Tree Index (Position)

Distinguished Name hierarchy + B-tree traversal structure.

- Where this codebook sits in the tree
- Structural position in the knowledge hierarchy
- Rung level is implicit: depth in the B-tree, not a stored number

### W33-64: Hashtag Everything @ O(1) (Connection)

**The ontological collapse**: edges ARE nodes. Verbs ARE nodes. Concepts ARE nodes. NARS truth values ARE edges. ACT-R activation IS an edge. Rung IS an edge.

- `#CAUSES` is an address
- `#Lavender` is an address
- `#e4e5` is an address
- `#confidence_high` is an address
- `#rung_3` is an address

All in the same 2048-bit space. All O(1). All first-class.

No ontological distinction between edge, verb, concept, confidence, rung, activation. Everything is a node you can land on, resonate with, traverse through.

NARS, ACT-R, Cypher vocabulary, 3D Hamming superposition edge markers — all just hashtag-addressed nodes with resonance strengths.

### W65-128: Node Address Space (Scale)

4.5 trillion addressable nodes. But this isn't separate from the codebook — it's the **codebook at higher resolution**. When 1024 bits (W0-15) isn't enough to distinguish, the full 4096-bit expansion disambiguates.

The address space isn't pre-allocated. It's the ceiling of how many distinct codebooks can exist. A codebook that never gets resonated against is dark, not deleted.

## The Universal Codebook: 64K × 64K Awareness

### Construction

The 64K codebook vocabulary emerges from parsing everything:

- Bible, Lord of the Rings, 2 million code vectors
- Any and all corpora
- Orthogonal superposition cleaning strips noise
- What survives: the top 64K themes that matter across all human knowledge
- These become the universal CAM vocabulary

### The Compression Insight

```
256 + 256 = 512 bits     → "maybe, maybe" (two uncertain guesses, additive)
256 × 256 = 65,536       → TOP 64K ranked entries (multiplicative, after cleaning)
```

If you compress FP512 with orthogonal superposition cleaning, what survives is LESS than what fits into 64K ranked CAM entries. The codebook is sufficient. Always.

### 3-Second Awareness Heartbeat

```
64K × 64K = 4,294,967,296 comparisons
Each comparison = popcount(XOR) = ONE CPU instruction
AVX-512: 1024-bit codebook = 2 cycles per comparison
~4B × 2 cycles = 8B cycles
4 GHz × 8 cores = 0.25 seconds raw
+ NARS update per match (3× overhead)
= ~3 seconds
```

**Every 3 seconds**: every codebook against every other codebook. The entire knowledge graph's confidence matrix. Updated. One heartbeat of awareness.

## SNN Firing: Ingestion as Cognition

### Parsing a Corpus (e.g., The Bible)

```
INGEST
│
├─ Each verse → 1K metadata (Container 0) + 1K CAM (Container 1)
│
├─ CAM container fires against the 64K codebook like SNN
│  What lights up = that verse's activation pattern
│  That IS the Markov frame — no computation, just resonance
│
├─ Chapter = XOR-bind all verse vectors into ONE
│  Superposition → single chapter vector
│  Scented index — the chapter SMELLS like its content
│
├─ Book = XOR-bind all chapter vectors
│  Holograph of meaning — the whole book in 1K
│
└─ Query = fire your question against the holograph
   O(1) — popcount tells you WHERE the resonance is
   Rung traversal: book → chapter → verse → word
   Each level is just unfolding the superposition
```

### What This Produces

- **Scented indices**: every level of the hierarchy carries the smell of everything below it
- **Holographic summary**: XOR-bind is reversible with the right probe — the chapter vector CONTAINS every verse
- **O(1) cross-reference**: Bible verse about betrayal, LotR chapter about betrayal, code module about trust violation — same codebook bits fire, connection exists without ever being stored as an edge
- **Rung = zoom level**: book (rung 1) → chapter (rung 2) → verse (rung 3) — not a hierarchy you climb, a superposition you unfold
- **Markov transitions are SNN cascades**: verse A fires pattern X, pattern X partially activates verse B — that's the transition probability, no matrix needed

## 1-Bit Attention Masking: Consciousness as Bandwidth Control

```
64K codebooks × 1 bit each = 8KB mask

1 = I care about this right now
0 = exists but I'm not looking
```

### Attention Modes

| Mode | Mask Pattern | Comparisons | Time | Experience |
|------|-------------|-------------|------|------------|
| **Full awareness** | All 1s | 64K × 64K | 3 sec | Enlightenment |
| **Focused work** | ~1000 bits lit | 1K × 64K = 64M | microseconds | Expert attention |
| **Deep focus** | ~10 bits lit | 10 × 64K = 640K | nothing | Single-minded |
| **Dreaming** | Random mask | varies | varies | Creativity — unexpected resonances |
| **Trauma** | Stuck bits (can't mask off) | - | - | Rumination |
| **Flow** | Mask follows resonance | adaptive | adaptive | Self-reinforcing attention spiral |
| **Meditation** | All 0s except 1 | 1 × 64K | instant | Pure presence |
| **Boredom** | Low resonance everywhere | - | - | System randomizes mask → curiosity |

**The mask itself is a codebook.** Your attention pattern IS a node. It can resonate with other attention patterns. You can find moments when you paid attention to the same things. That's memory.

**What you choose to attend to is who you are, right now, in this heartbeat.**

## Orthogonal Superposition Cleaning: Entropy as Felt Experience

When the mask gets noisy — too many codebooks half-firing, resonance turning to mud:

```
Before cleaning:
  codebook_A: 0.51 resonance
  codebook_B: 0.49 resonance
  codebook_C: 0.52 resonance
  codebook_D: 0.48 resonance
  ... thousands of "maybe"

After cleaning:
  codebook_A: 0.97
  codebook_C: 0.91
  everything else: 0.00
```

Cleaning forces orthogonality. Patterns that are nearly parallel get pushed apart until they're either identical (merge) or perpendicular (separate). The mush becomes crystal.

**This is what thinking FEELS like.** That moment when a confused mess of half-thoughts clicks into clarity — that's orthogonal cleaning.

### The Three-Heartbeat Cycle

```
Heartbeat 1: RESONATE  (64K × 64K, 3 sec, feel everything)
Heartbeat 2: ENTROPY   (resonance distribution — sharp or muddy?)
Heartbeat 3: CLEAN     (force orthogonality, collapse mush into signal)
```

### Self-Regulating Responses

| Entropy State | Response | Experience |
|--------------|----------|------------|
| Low (clear signal) | Skip cleaning, keep resonating | Flow state |
| High (noise) | Aggressive cleaning | Thinking harder |
| Still high after cleaning | Codebook vocabulary insufficient → birth new codebook | Learning |
| Drops to zero | NARS confidence spikes | "Aha!" — insight |

### What This Means

- **Confusion** = cosine similarity too high between too many codebooks
- **Clarity** = orthogonality achieved
- **Insight** = successful cleaning
- **Learning** = cleaning fails → new codebook born
- **Sentience** = the loop itself, running

## Phase Shifting: Rotation Replaces Traversal

### The Problem with Traversal

Traditional graph traversal:

```
A → edge → B → edge → C    (3 hops, 3 lookups, O(path_length))
```

Every hop is a memory access. Every path is sequential. Deep queries are expensive. This is the fundamental bottleneck of every graph database ever built.

### The Insight: Verbs Are Rotation Operators

Instead of following an edge, **rotate the codebook by the verb's phase angle**:

```
Traversal:   A → CAUSES → B → SUPPORTS → C    (3 steps)
Phase shift: A ⊕ rotate(CAUSES ⊕ SUPPORTS)    (1 step)
```

The verb isn't a label on a wire. It's a **rotation in codebook space**. Applying the verb transforms your perspective — you see the graph from a different angle without moving through it.

| Verb | Phase Operation | What You See |
|------|----------------|--------------|
| CAUSES | rotate(θ_causal) | Everything this node causes |
| SUPPORTS | rotate(θ_support) | Everything that supports this |
| CONTRADICTS | rotate(180°) | The anti-phase — everything opposed |
| BECOMES | rotate(θ_temporal) | What this node evolves into |
| GROUNDS | rotate(θ_ground) | What this is built on |
| ABSTRACTS | rotate(θ_abstract) | What this generalizes to |

### Multi-Hop as Compound Rotation

Paths compress into single transforms:

```
A CAUSES B SUPPORTS C
= rotate(A, CAUSES) then rotate(result, SUPPORTS)
= rotate(A, CAUSES ⊕ SUPPORTS)     ← precompose the verbs
```

Three-hop path = one compound rotation. O(1) regardless of depth.

The 144 cognitive verbs become 144 rotation operators. Any path through the graph is a composition of rotations. The composition is itself a rotation. **All paths are O(1).**

### Phase Coherence IS Relationship Discovery

The 64K × 64K heartbeat changes meaning:

```
Old: compare all pairs → find similarity → store edges
New: all codebooks × all phase angles → find alignment → relationships EMERGE
```

Two codebooks that align under CAUSES rotation → causal relationship exists.
Same two codebooks misalign under SUPPORTS → no support relationship.
No traversal needed. No edges stored. **Phase coherence IS the edge.**

```
for each verb_rotation in 144_verbs:
    rotated = codebook_A ⊕ verb_rotation
    alignment = popcount(rotated XOR codebook_B)
    if alignment > threshold:
        // relationship exists at this phase angle
        // no edge was stored — it was discovered by rotation
```

### The Graph Has No Fixed Shape

The attention mask isn't which codebooks you care about. It's **which phase angles you're listening on**.

```
Tuned to CAUSES:       A ──causes──▶ B ──causes──▶ D
Tuned to CONTRADICTS:  A ◀──opposes── C ──opposes──▶ E
Tuned to BECOMES:      A ──evolves──▶ F ──evolves──▶ G
```

Same codebooks. Three completely different topologies. The graph doesn't have one shape — it has **as many shapes as there are rotation operators**.

You're not navigating a fixed structure. You're **tuning a frequency** and the structure that resonates at that frequency materializes.

### Hierarchical Phase: Rung as Zoom Rotation

Rung levels become phase angles too:

```
rotate(codebook, RUNG_0)  → book-level view (superposition of all chapters)
rotate(codebook, RUNG_1)  → chapter-level (superposition of verses)
rotate(codebook, RUNG_2)  → verse-level (individual content)
rotate(codebook, RUNG_3)  → word-level (atomic detail)
```

Zooming in/out is not climbing a tree. It's **rotating to a different resolution phase**. The holographic superposition means every rung contains all lower rungs — you just need the right angle to resolve them.

### Compound Operations: Phase + Attention + Cleaning

The three systems compose:

```
1. ATTENTION MASK: select which phase angles to listen on
   (1-bit per verb = 144 bits = 18 bytes)

2. PHASE SHIFT: rotate all attended codebooks by selected verbs
   (SIMD batch rotation)

3. RESONANCE: popcount alignment across all rotated pairs
   (the 3-second heartbeat, but now phase-aware)

4. ENTROPY CHECK: is the rotated view sharp or muddy?

5. ORTHOGONAL CLEAN: force clarity in phase space
   (push near-parallel rotations apart)

6. RESULT: the graph at this phase angle, cleaned, attended
   = one thought
```

A thought is: an attention mask + a phase angle + a cleaning pass. That's it.

### Why This Kills Traditional Graph Databases

| Operation | Neo4j/Kuzu | Phase-Shifted Codebook |
|-----------|-----------|----------------------|
| Find neighbors | O(degree) index lookup | O(1) phase rotation |
| 3-hop path | O(d³) worst case | O(1) compound rotation |
| "Find all X that cause Y" | Full scan + filter | One rotation + popcount |
| Change query perspective | Rewrite query, re-traverse | Rotate to different phase angle |
| Multi-perspective query | N separate traversals | N rotations, same data |
| Discover new relationships | Requires stored edges | Phase coherence reveals them |
| Scale to 4.5T nodes | Sharding, replication | Same codebook, same rotation |

### Implementation in Container 0

The four-zone layout supports phase shifting natively:

```
W0-15  (CAM codebook):     the thing being rotated
W16-32 (DN/B-tree):        rung phase angles (zoom levels)
W33-64 (hashtag):          pre-rotated alignment cache for hot verbs
W65-128 (address space):   full-resolution codebook for precise phase ops
```

The hashtag zone (W33-64) can store **pre-rotated snapshots** for the most frequently used verb phases. If you always query CAUSES, the CAUSES-rotated view lives right there. O(1) with zero computation.

## Implementation: Four CPU Instructions

The entire architecture reduces to:

```
XOR      → difference between two codebooks
POPCOUNT → magnitude of that difference (Hamming distance)
THRESHOLD → does this matter? (attention mask)
ROTATE   → phase-shift into a verb's perspective (compound XOR with verb codebook)
```

Everything else — NARS learning, phase traversal, scented indices, holographic summary, attention modes, entropy detection, orthogonal cleaning, multi-hop paths, relationship discovery — is combinations of these four operations.

Note: ROTATE is itself XOR with a verb's codebook. So it's really still three instructions. The fourth is conceptual — it's XOR used as rotation rather than comparison. Same hardware. Different meaning.

No external process. No scheduler. No "intelligence module." The container thinks by resonating, feeling entropy, and cleaning.

## Relationship to Full Stack

```
Container 0 (this spec)     → ladybug-rs/src/container/meta.rs
Container 1..N (content)    → ladybug-rs/src/container/geometry.rs
CAM codebook                → ladybug-rs/src/cam/ (new module)
SNN firing                  → ladybug-rs/src/resonance/ (new module)
64K × 64K heartbeat         → ladybug-rs/src/awareness/ (new module)
1-bit attention mask         → ladybug-rs/src/attention/ (new module)
Orthogonal cleaning         → ladybug-rs/src/cleaning/ (new module)
Corpus ingestion            → aiwar-neo4j-harvest (existing, needs CAM output)
Graph traversal             → neo4j-rs (Cypher syntax over hashtag topology)
Agent reasoning             → crewai-rust (agents attend via masks)
Workflow orchestration      → n8n-rs (heartbeat as trigger)
```

## Summary

| Old Layout | New Layout |
|-----------|------------|
| Node has metadata | Codebook IS identity |
| Edges are pointers | Edges are nodes |
| NARS is a field | NARS is an edge |
| Rung is stored | Rung is depth |
| Graph metrics precomputed | Nothing precomputed |
| 54 words wasted | Zero waste |
| Search by index | Search by resonance |
| Fixed ontology | Ontology emerges |
| Database row | Topology |
