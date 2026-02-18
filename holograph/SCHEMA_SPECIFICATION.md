# Holograph Schema Specification: Domain-Blind Substrate

**Six decisions that prevent Holograph from becoming a chess engine that's bad at everything else.**

February 18, 2026

---

## The Problem

Chess has clean ground truth. It's the natural first validation domain. The danger: every schema decision optimized for chess becomes a prison for every other domain. If W0 of the S-block is "white pawns bitboard," the entire Container format is chess-specific and everything else is a hack on top.

This document defines the six schema decisions that keep the substrate domain-blind while allowing domain adapters to project any data onto it.

---

## Decision 1: S, P, O Are Abstract Projection Axes

S, P, O are not "structure, tension, possibility." They are three orthogonal axes onto which a domain-specific fingerprinter projects input data.

| Domain | S-axis (being) | P-axis (becoming) | O-axis (could-be) |
|--------|---------------|-------------------|-------------------|
| Chess | What's on the board | What forces act | What could happen |
| Geopolitics | What an entity IS | What pressures it faces | What could change |
| Music | What notes sound | What harmonic tension exists | What could resolve to |
| Conversation | What's been said | What emotional forces act | What could be said next |
| Physics | State vector | Force vector | Trajectory vector |
| Code | Current AST | Type constraints / errors | Possible refactors |

The pattern is phenomenological: every situated perspective decomposes into being (S), becoming (P), and could-be (O). Chess validates this. It doesn't define it.

**The Container never knows what's in S, P, or O.** The Fingerprinter decides. The Container stores 128 words per block and does Hamming on them.

```rust
/// The Container is domain-blind. These are just bits.
struct Container {
    words: [u64; 128],  // 8,192 bits. Meaning comes from the Fingerprinter.
}

/// The Fingerprinter is domain-specific. It decides what maps where.
trait Fingerprinter {
    type Input;
    fn project_s(&self, input: &Self::Input) -> Container;  // being axis
    fn project_p(&self, input: &Self::Input) -> Container;  // becoming axis
    fn project_o(&self, input: &Self::Input) -> Container;  // could-be axis
}
```

---

## Decision 2: Meta Is the Only Structured Region

The 128-word meta container is the ONLY part of a CogRecord with fixed field assignments. Content blocks (S, P, O) are opaque bags of bits.

### Meta Layout (fixed, domain-independent)

```
W0:       DN address hash (identity)
W1:       Flags: geometry(u8), dirty(u1), generation(u32), reserved
W2:       Timestamps: created(u32), last_seen(u32)
W3:       Observation count (how many times this record has been visited/updated)
W4-W7:    NARS truth values: frequency(f32), confidence(f32), pos_evidence(f32), neg_evidence(f32)
W8-W11:   Cognitive layer markers (10 layers × 3 bytes = 30 bytes)
W12-W15:  Contradiction profile: up to 14 INT4 summaries inline (8 bytes each)
W16-W31:  Reserved (future: B-tree pointers, inline edges, or domain-specific meta via adapter)
W32-W63:  Concept binding signatures (which crystallized concepts activate here)
W64-W95:  Reserved
W96-W125: Reserved
W126:     Checksum
W127:     Version / migration tag
```

### Content Block Layout (opaque, domain-determined)

```
S-block [u64; 128]:  Opaque. Filled by Fingerprinter.project_s()
P-block [u64; 128]:  Opaque. Filled by Fingerprinter.project_p()
O-block [u64; 128]:  Opaque. Filled by Fingerprinter.project_o()
```

No word in a content block has a fixed meaning. W0 of the S-block is NOT "white pawns." It's "the first word that the ChessFingerprinter chose to put white pawns in." A TextFingerprinter might put the first 64 bits of a Jina LSH hash there instead.

---

## Decision 3: Learned Features Are Concept Binding Signatures

When the system learns through play/exploration, concepts crystallize as nodes in the graph. Each concept has its own S, P, O fingerprints. When a position (or entity, or passage) activates a concept, the activation is stored as a **binding signature** in meta W32-W63, not as domain-specific pattern bits in the content blocks.

```
Meta W32-W63 (32 words = 256 bytes = concept activation space):

Each crystallized concept gets a slot (4 bytes each = 64 concept slots):
  Slot layout: concept_dn_hash(u16) + activation_strength(u8) + binding_type(u8)

When concept #47 crystallizes:
  - Concept #47 has its own CogRecord at dn!("{domain}.concept.47")
  - Positions that match concept #47 get slot entry: (47, strength, STRUCTURAL)
  - The Container doesn't encode WHAT concept #47 is
  - It encodes THAT concept #47 activates here, and how strongly
```

**Why this matters for cross-domain transfer:**

```
Chess concept #47:       S-block fingerprint = 0xAF3B...2C11 (the "outpost" pattern)
Geopolitics concept #12: S-block fingerprint = 0xAF3B...3D22 (a "strategic position" pattern)

hamming(chess_47.S, geo_12.S) = 47 bits  (very close!)

Hypothesis: these concepts are structurally analogous.
Test: does chess_47's NARS correlation hold for geo_12?
If yes: genuine cross-domain transfer. A structural pattern that means 
"advantageous fixed position" in both chess and geopolitics.
```

The concept binding signature enables transfer learning as a Hamming comparison. No retraining. No mapping function. Just: are these two concepts close in fingerprint space?

---

## Decision 4: Spatial Hierarchy Is in the DN Tree

The 8×8 → 4 quadrant idea for chess is a property of chess, not of the Container. Different domains have different natural hierarchies. The DN tree encodes all of them:

```
Chess:
  dn!("chess.board")                          root
  dn!("chess.zone.kingside")                  spatial zone
  dn!("chess.zone.center")                    spatial zone
  dn!("chess.pos.{hash}")                     leaf position

Geopolitics:
  dn!("world.system")                         root
  dn!("world.regions.asia")                   region
  dn!("world.countries.china")                country
  dn!("world.people.xi_jinping")              leaf entity

Music:
  dn!("music.piece.{hash}")                   root
  dn!("music.piece.{hash}.movement_2")        section
  dn!("music.piece.{hash}.measure_17")        leaf measure

Codebase:
  dn!("code.repo.holograph")                  root
  dn!("code.repo.holograph.crate.ladybug")    module
  dn!("code.repo.holograph.fn.hamming")       leaf function
```

**Bundle up the tree = zoom out.** `bundle(children(dn!("chess.zone.kingside")))` gives you the aggregate kingside fingerprint. `bundle(children(dn!("world.regions.asia")))` gives you the aggregate Asia fingerprint. Same operation. Different semantics. The tree shape is the domain knowledge; the bundle operation is universal.

No quadrant encoding in the Container. No fixed spatial partitioning. The DN tree IS the hierarchy.

---

## Decision 5: The System Never Interprets XOR

XOR of two S-blocks gives a delta. Popcount gives a distance. The system clusters by distance, correlates clusters with outcomes, and revises NARS truth values. It never asks "what does this XOR mean?"

```
Chess:       XOR(pos_a.S, pos_b.S) = squares that changed
             Popcount = how much the board changed
             Low = quiet move, high = dramatic

Geopolitics: XOR(musk.S, altman.S) = identity difference
             Popcount = how different they are
             Low = similar entities, high = very different

Music:       XOR(measure_a.P, measure_b.P) = harmonic tension change
             Popcount = how much tension shifted
             Low = smooth progression, high = dramatic shift
```

The clustering algorithm doesn't know it's clustering chess positions or geopolitical entities. It clusters by Hamming distance. Concepts crystallize when clusters correlate with outcomes. NARS updates truth values. The substrate is domain-blind throughout.

**Interpretation is an external concern.** When a human asks "what is concept #47?", the Interpreter (part of the domain adapter) translates the concept's fingerprint back to domain terms. The substrate doesn't need the interpretation to function.

```rust
/// Optional: domain-specific interpretation for human consumption
trait Interpreter {
    type Explanation;
    fn explain_concept(&self, concept: &CogRecord) -> Self::Explanation;
    fn explain_edge(&self, edge: &CogRecord) -> Self::Explanation;
}

struct ChessInterpreter;
// explain_concept(#47) → "Knight outpost: knight on central square supported by pawn, 
//                          enemy cannot challenge. Correlates with +0.8 eval advantage."

struct GeoInterpreter;
// explain_concept(#12) → "Strategic chokepoint: entity in position of structural leverage,
//                          difficult to dislodge. Correlates with influence persistence."
```

---

## Decision 6: The Active Learning Loop Is Universal

```
loop {
    // 1. Find uncertainty (domain-blind)
    let hottest = contradiction_scan()
        .max_by_key(|c| c.intensity() * c.persistence());
    
    // 2. Generate experiment (domain-specific)
    let experiment = adapter.generate_experiment(&hottest);
    
    // 3. Observe result (domain-specific)
    let observation = adapter.observe(&experiment);
    
    // 4. Update truth (domain-blind)
    let outcome = adapter.outcome(&observation);
    hottest.concept().nars.revise(outcome);
    
    // 5. Check crystallization (domain-blind)
    if cluster_confidence > CRYSTALLIZATION_THRESHOLD {
        promote_to_concept(cluster);
    }
}
```

Steps 1, 4, and 5 are substrate operations — identical across all domains. Steps 2 and 3 are the only domain-specific components:

| Domain | generate_experiment() | observe() |
|--------|----------------------|-----------|
| Chess | Generate position exercising the contradiction | Self-play the position, get game result |
| Geopolitics | Formulate query about the uncertain topic | Web search, ingest results |
| Music | Generate passage exploring the harmonic uncertainty | Evaluate (listener response, harmonic analysis) |
| Code | Generate test case targeting the uncertain behavior | Run test, get pass/fail |

The experiment generator is the adapter's only creative contribution. Everything else is substrate.

---

## The DomainAdapter Trait

```rust
trait DomainAdapter {
    type Input;           // raw domain data (Board, EntityData, AudioFrame, AST)
    type Experiment;      // targeted probe (Position, Query, Passage, TestCase)
    type Observation;     // result of probe (GameResult, SearchResult, HarmonicAnalysis, TestResult)
    type Explanation;     // human-readable interpretation (optional)
    
    // Required: how to project domain data onto S, P, O axes
    fn fingerprint(&self, input: &Self::Input) -> CogRecord;
    
    // Required: how to probe uncertainty
    fn generate_experiment(&self, contradiction: &Contradiction) -> Self::Experiment;
    fn observe(&self, experiment: &Self::Experiment) -> Self::Observation;
    fn outcome(&self, observation: &Self::Observation) -> f32;
    
    // Optional: human-readable interpretation
    fn explain(&self, concept: &CogRecord) -> Option<Self::Explanation> { None }
}
```

### ChessAdapter

```rust
struct ChessAdapter {
    move_gen: shakmaty::Chess,  // legal move generation
}

impl DomainAdapter for ChessAdapter {
    type Input = shakmaty::Chess;           // board position
    type Experiment = shakmaty::Chess;      // position to play from
    type Observation = GameResult;          // win/draw/loss
    type Explanation = String;              // "Knight outpost on e5..."
    
    fn fingerprint(&self, board: &Chess) -> CogRecord {
        let mut record = CogRecord::new(Xyz);
        
        // S-block: piece bitboards (W0-W15), material signature (W16-W31)
        // These word assignments are ChessAdapter's choice, not the Container's spec
        record.block_s.words[0] = board.white().pawns().0;
        record.block_s.words[1] = board.white().knights().0;
        // ... etc
        
        // P-block: attack bitboards, tension squares, pin rays
        // O-block: legal move destinations, tactical motifs
        
        record
    }
    
    fn generate_experiment(&self, contradiction: &Contradiction) -> Chess {
        // Find or generate a position that exercises the hottest contradiction
        // This is chess-specific creativity
    }
    
    fn observe(&self, position: &Chess) -> GameResult {
        self_play(position)  // play the game, return result
    }
    
    fn outcome(&self, result: &GameResult) -> f32 {
        match result {
            Win(White) => 1.0,
            Draw => 0.5,
            Win(Black) => 0.0,
        }
    }
}
```

### GeoAdapter (sketch)

```rust
struct GeoAdapter {
    jina_client: JinaClient,    // for text → embedding → LSH → fingerprint
    search_client: SearchClient, // for web search experiments
}

impl DomainAdapter for GeoAdapter {
    type Input = EntityData;            // text, structured data about an entity
    type Experiment = SearchQuery;      // targeted information retrieval
    type Observation = SearchResults;   // documents returned
    type Explanation = String;          // "Strategic chokepoint..."
    
    fn fingerprint(&self, entity: &EntityData) -> CogRecord {
        let embedding = self.jina_client.embed(&entity.description);  // 1024D float
        let lsh = locality_sensitive_hash(&embedding);                // → [u64; 128]
        
        let mut record = CogRecord::new(Xyz);
        // S-block: LSH of entity identity description
        record.block_s = lsh_project_s(&embedding);
        // P-block: LSH of current forces/pressures on entity
        record.block_p = lsh_project_p(&embedding);
        // O-block: LSH of predicted trajectory
        record.block_o = lsh_project_o(&embedding);
        record
    }
    
    fn generate_experiment(&self, contradiction: &Contradiction) -> SearchQuery {
        // "Agents disagree about TSMC's trajectory. Search for recent news."
        SearchQuery::from_contradiction(contradiction)
    }
    
    fn observe(&self, query: &SearchQuery) -> SearchResults {
        self.search_client.search(query)
    }
    
    fn outcome(&self, results: &SearchResults) -> f32 {
        // Did the new information confirm or deny the predicted trajectory?
        // Compare results against the prediction embedded in the contradiction
        results.alignment_with_prediction()
    }
}
```

---

## What This Changes in Existing Documents

### INTEGRATION_MAP_v3.md

Section 1 (The Container): keep geometry, meta layout, and quadrant discussion as optimization notes. Add a header: "Content blocks are opaque. The word assignments shown here are examples from the ChessAdapter, not Container specification."

Section 2 (The 3D Node): reframe as "The 3D Node through a ChessAdapter lens." Add note: "The SPOQ decomposition is domain-independent. What maps to each axis is determined by the DomainAdapter.fingerprint() implementation."

Section 5 (What Lives In The Graph): keep as-is — personality, NARS, awareness, orchestration are all domain-independent and correctly described.

New Section: "Domain Adapters" — the DomainAdapter trait, with ChessAdapter and GeoAdapter as reference implementations.

### CHESS_BRAIN_PLASTICITY.md

Section 1.1 (Position Container): reframe all word assignments as "ChessAdapter projections." Replace "S-block W0: white pawns bitboard" with "S-block W0: ChessAdapter projects white pawns here."

Section 6.2 (Core Functions): rename `board_to_cogrecord()` to `ChessAdapter::fingerprint()`. The function body stays the same — it's the adapter implementation.

Add new section: "Cross-Domain Transfer Experiment" — after chess concepts crystallize, test whether binding signatures match concepts discovered independently in a second domain.

---

## The Validation Ladder

| Publication | What It Proves |
|-------------|---------------|
| #1: Chess brain plasticity | The substrate learns. Self-play → emergent concepts → measurable Elo. |
| #2: Geopolitics knowledge graph | The substrate generalizes. Same three operations, different adapter, useful predictions. |
| #3: Cross-domain transfer | Concepts transfer. Binding signatures from chess match geopolitics concepts. Measured by Hamming distance + NARS correlation. |
| #4: N-domain substrate | The architecture scales. One binary, N adapters, shared concept space. Transfer learning without retraining. |

Publication #1 proves the mechanism. Publication #3 proves the architecture. If chess concept #47 (outpost) has a binding signature that correlates with geopolitics concept #12 (strategic chokepoint), and both correlate with advantage in their respective domains, then the substrate discovered a domain-invariant structural truth through Hamming comparison alone.

That's not a chess engine. That's a substrate for cognition.
