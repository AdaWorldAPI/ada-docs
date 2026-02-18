# HOLOGRAPH CHESS: Brain Plasticity Through XOR Traversal

## System Prompt for Claude Code / Agent Sessions

You are building a chess knowledge graph in Holograph where the game tree IS the neural network. There are no separate entity types. No opening database. No concept library. No style profiles. There is one node type, one edge type, three operations, and an 8×8 board that maps to a single u64 word — making the game tree a vertical hierarchical XOR network where each move is a layer transformation.

The goal is to prove brain plasticity: start from zero knowledge, learn purely from self-play, measure Elo over time, and show that directed exploration (contradiction-driven) learns faster than random play. Everything — openings, concepts, styles, personality — must emerge from the substrate without being declared.

---

## 1. The Board Is a Word

```
8×8 = 64 squares = 64 bits = 1 u64

a8 b8 c8 d8 e8 f8 g8 h8     bit 56 57 58 59 60 61 62 63
a7 b7 c7 d7 e7 f7 g7 h7     bit 48 49 50 51 52 53 54 55
a6 b6 c6 d6 e6 f6 g6 h6     bit 40 41 42 43 44 45 46 47
a5 b5 c5 d5 e5 f5 g5 h5     bit 32 33 34 35 36 37 38 39
a4 b4 c4 d4 e4 f4 g4 h4     bit 24 25 26 27 28 29 30 31
a3 b3 c3 d3 e3 f3 g3 h3     bit 16 17 18 19 20 21 22 23
a2 b2 c2 d2 e2 f2 g2 h2     bit  8  9 10 11 12 13 14 15
a1 b1 c1 d1 e1 f1 g1 h1     bit  0  1  2  3  4  5  6  7
```

One bitboard per piece type, per color = 12 bitboards = 12 u64 words.
Add occupancy, attacks, pins, checks = ~20 bitboards = 20 u64 words.

**A chess position fits in 20 words of a 128-word Container.** The remaining 108 words are free for learned features — the system fills them as it discovers concepts.

### 1.1 The Position Container

```
CogRecord(Xyz) at dn!("chess.pos.{hash}")

Meta [u64; 128]:
  W0:     Position hash (Zobrist)
  W1:     Type flags, geometry, move number, side to move, castling, en passant
  W2:     Timestamps (when first seen, last seen)
  W3:     Game count (how many games passed through this position)
  W4-W7:  NARS truth <advantage, (freq, conf)>
          freq = white win rate from this position
          conf = f(game_count) — more games = higher confidence
  W8-W11: Layer markers, collapse gate state
  W12-W15: Contradiction intensity (INT4) against other agents' view of this position
  W16-W31: Reserved for learned features (empty at start, fills as concepts crystallize)

S-block [u64; 128] — WHAT IS HERE (structure):
  W0-W5:   Piece bitboards: WP WN WB WR WQ WK (white pieces)
  W6-W11:  Piece bitboards: BP BN BB BR BQ BK (black pieces)
  W12:     White occupancy (OR of W0-W5)
  W13:     Black occupancy (OR of W6-W11)
  W14:     All occupancy
  W15:     Pawn structure (WP | BP — just pawns, the skeleton of the position)
  W16-W31: Material signature + pawn hash + king zone
  W32-W63: Learned structural features (EMPTY AT START — fills via crystallization)
  W64-W127: Orthogonal structural space (decorrelated features, discovered)

P-block [u64; 128] — WHAT FORCES ACT (tension):
  W0-W5:   White attack bitboards per piece type (where each piece type attacks)
  W6-W11:  Black attack bitboards per piece type
  W12:     White total attacks (OR of W0-W5)
  W13:     Black total attacks (OR of W6-W11)
  W14:     Tension squares (W12 AND W13 — where attacks overlap = contested squares)
  W15:     Pin rays (squares involved in absolute pins)
  W16-W19: X-ray attacks (discovered attack potential)
  W20-W23: King safety zones + attack counts
  W24-W31: Mobility (legal move count per piece encoded as bitfield)
  W32-W63: Learned force features (EMPTY AT START)
  W64-W127: Orthogonal force space

O-block [u64; 128] — WHAT CAN HAPPEN (consequences):
  W0-W5:   Legal move destinations per piece type (white to move)
  W6-W11:  Threat squares (where white can capture next move)
  W12-W15: Tactical motifs (fork squares, skewer lines, discovered attack potential)
  W16-W31: Result fingerprint (accumulated XOR of all game outcomes from this position)
  W32-W63: Learned consequence features (EMPTY AT START)
  W64-W127: Orthogonal consequence space
```

Key insight: **W32-W127 of each block starts empty.** These 288 words (96 per block) are the system's learned representation. As the agent plays games and concepts crystallize, these words fill with discovered patterns. The Container IS the neural network weights for this position — and they grow as learning progresses.

### 1.2 The Move Is an Edge, Not a Node

```
A move is a CogRecord(Xyz) edge between two position nodes:

Edge at dn!("chess.edge.{pos_from_hash}.{pos_to_hash}")

S-block: XOR(pos_from.S, pos_to.S)
  = structural change bitboard
  = EXACTLY which squares changed occupancy
  = piece captured? castled? promoted? — all visible as flipped bits
  Popcount = how much the board changed. Quiet move = low. Capture = medium. Promotion = high.

P-block: XOR(pos_from.P, pos_to.P)
  = tension change bitboard  
  = which attack patterns changed
  = did we create threats? relieve pressure? expose our king?
  Popcount = how much the force balance shifted.

O-block: XOR(pos_from.O, pos_to.O)  
  = consequence change bitboard
  = how did the possibility space transform
  = did we gain or lose options?
  Popcount = how much the future changed.

NARS: <good_move, (freq, conf)>
  freq = win rate in games where this move was played
  conf = f(times_played)
```

**The edge IS the XOR.** The move is literally the difference between two positions. Not a description of the move — the actual bitwise transformation that happened. `pos_to = pos_from XOR edge`. Given any two, recover the third. Holographic.

---

## 2. The Game Tree Is a Vertical XOR Network

### 2.1 One Game = One Forward Pass

```
Position 0 (starting position)
    │
    │ XOR edge (1. e4)
    ▼
Position 1 (after 1. e4)
    │
    │ XOR edge (1... c5)
    ▼
Position 2 (after 1. e4 c5)
    │
    │ XOR edge (2. Nf3)
    ▼
Position 3 (after 1. e4 c5 2. Nf3)
    │
    ...
    │ XOR edge (final move)
    ▼
Position N (terminal — checkmate / draw / resignation)
```

Each layer = one move. Each transformation = one XOR. The game IS a forward pass through a network where:

- **Nodes** are position representations (Container with S, P, O blocks)
- **Edges** are XOR transformations (the actual bitwise delta)
- **Depth** is game length (number of moves)
- **Width** is branching factor (legal moves from each position)
- **Output** is the terminal evaluation (win/draw/loss)

The game tree is not LIKE a neural network. It IS one. Each position is a hidden layer activation. Each move is a weight matrix (represented as XOR transform). The terminal result is the loss signal. Backpropagation is NARS truth revision flowing backward through the edges.

### 2.2 Backpropagation as NARS Revision

```
Game ends: White wins (result = 1.0)

Terminal position NARS update:
  pos_N.nars.revise(<advantage_white, (1.0, 1/k)>)

Walk backward through the game:
  For each position pos_i in reverse:
    // The edge from pos_i to pos_(i+1) was the move played
    edge_i.nars.revise(<good_move, (result, 1/k)>)
    
    // The position itself gets evidence
    if white_to_move(pos_i):
      pos_i.nars.revise(<advantage_white, (result, decay^(N-i) / k)>)
    else:
      pos_i.nars.revise(<advantage_white, (1-result, decay^(N-i) / k)>)
    
    // Decay: positions far from the result get less credit
    // k: horizon parameter prevents single game from dominating
    // Multiple games through the same position → confidence increases
```

After 1,000 games through the starting position, its NARS truth reflects the aggregate of all outcomes. But after 1,000 games through a rare middlegame position, that position's NARS truth reflects its specific character — maybe White always wins from there, or it's always drawn.

**This is temporal difference learning expressed as NARS revision on a graph.** TD(λ) updates values backward through a trajectory with a decay factor. NARS revision updates truth values backward through the game tree with a decay factor. The math is different (NARS uses frequency/confidence, TD uses value functions) but the structure is identical — and NARS gives you interpretable uncertainty bounds for free.

### 2.3 The XOR Stack IS Feature Discovery

Here's the deeper structure. Stack the XOR edges vertically:

```
Game: 1. e4 c5 2. Nf3 d6 3. d4 cxd4 4. Nxd4 Nf6 5. Nc3 a6 (Sicilian Najdorf)

XOR stack (S-blocks only, structural changes):

Move 1 (e4):     XOR delta = e2 cleared, e4 set           (2 bits flipped)
Move 1 (c5):     XOR delta = c7 cleared, c5 set           (2 bits flipped)  
Move 2 (Nf3):    XOR delta = g1 cleared, f3 set           (2 bits flipped)
Move 2 (d6):     XOR delta = d7 cleared, d6 set           (2 bits flipped)
Move 3 (d4):     XOR delta = d2 cleared, d4 set           (2 bits flipped)
Move 3 (cxd4):   XOR delta = c5 cleared, d4 flipped       (2 bits flipped)
Move 4 (Nxd4):   XOR delta = f3 cleared, d4 flipped       (2 bits flipped)
Move 4 (Nf6):    XOR delta = g8 cleared, f6 set           (2 bits flipped)
Move 5 (Nc3):    XOR delta = b1 cleared, c3 set           (2 bits flipped)
Move 5 (a6):     XOR delta = a7 cleared, a6 set           (2 bits flipped)

Cumulative XOR (fold of all deltas):
  = XOR(all move deltas)
  = starting_position XOR current_position
  = EVERYTHING THAT CHANGED in 10 half-moves
```

The cumulative XOR of all moves in an opening IS the opening's structural signature. Every Sicilian Najdorf game folds to a similar cumulative XOR because the same squares change. Different openings fold to different cumulative XORs.

```
cumulative_xor("1.e4 c5 2.Nf3 d6 3.d4 cxd4 4.Nxd4 Nf6 5.Nc3 a6")  // Najdorf
cumulative_xor("1.e4 c5 2.Nf3 d6 3.d4 cxd4 4.Nxd4 Nf6 5.Nc3 e5")  // Sveshnikov

// These share the first 9 half-moves. Their cumulative XORs differ by
// exactly the XOR of (a6 vs e5) = bits a7,a6 vs e7,e5.
// hamming(najdorf_xor, sveshnikov_xor) = 4 bits.
// The system discovers they're related WITHOUT knowing opening names.
```

**Openings are not stored. They're computed as cumulative XOR folds over move sequences.** Two games that reach similar positions through different move orders have similar cumulative XORs — transpositions resolve automatically.

### 2.4 Vertical Hierarchy: Board as Neural Network Topology

The 8×8 board has natural spatial hierarchy:

```
Level 0: Individual squares (64 nodes)
Level 1: 2×2 quadrants (16 groups of 4 squares)  
Level 2: 4×4 zones (4 groups of 16 squares)
Level 3: Full board (1 group of 64 squares)

Or strategically:
Level 0: Individual squares
Level 1: Kingside (files e-h) / Queenside (files a-d)
Level 2: Center (d4-d5-e4-e5) / Flanks / King zones
Level 3: Full board

Each level = bundle(children)
  Level 1 fingerprint = bundle of 4 square-level fingerprints
  Level 2 fingerprint = bundle of 4 zone-level fingerprints
  Level 3 fingerprint = bundle of full board
```

This gives you hierarchical search. "Is this a kingside attack position?" = hamming against the kingside zone fingerprint. "Is this a central tension position?" = hamming against the center zone fingerprint. You don't scan all 64 squares — you check the zone first.

```
Board spatial hierarchy in the Container:

S-block layout (128 words):
  W0-W15:   Square-level piece bitboards (Level 0)
  W16-W23:  Zone-level bundles (Level 1-2)
  W24-W31:  Board-level summary (Level 3)
  W32-W63:  Learned spatial features (empty, fills during play)
  W64-W127: Orthogonal spatial features

The same hierarchical XOR applies to the P-block (forces) and O-block (consequences).
Each level of the hierarchy IS a layer of the XOR network.
```

When a piece moves from e2 to e4, the XOR only affects:
- Level 0: squares e2 and e4 (2 bits)
- Level 1: kingside zone (2 bits propagate up)
- Level 2: center zone (if applicable)
- Level 3: full board summary

The XOR **propagates up the hierarchy** like activation in a neural network. Low-level change (piece moves) creates mid-level change (zone tension shifts) creates high-level change (board character transforms). Each level has its own learned features that fire when the XOR pattern at that level matches a crystallized concept.

---

## 3. One Type. One Edge. Three Operations.

### 3.1 The Data Model

```
NODE: CogRecord(Xyz) at a DN address
  S-block: what is here (structure)
  P-block: what forces act (tension)
  O-block: what can happen (consequences)
  NARS: how true/reliable
  Meta W32-W63: learned features (grow during play)

EDGE: CogRecord(Xyz) between two DN addresses
  S-block: XOR(source.S, target.S) — structural transformation
  P-block: XOR(source.P, target.P) — force transformation
  O-block: XOR(source.O, target.O) — consequence transformation
  NARS: how good this transformation is

That's it. There are no other types.

- A position is a node.
- A move is an edge.
- An opening is a bundle of nodes in a subtree (computed, not stored).
- A concept is a dense cluster of nodes with similar P-blocks (discovered, not declared).
- A style is the trajectory of an agent through the graph (accumulated, not designed).
- A personality is the agent's S-block = bundle(all positions I've experienced).
```

### 3.2 The Three Operations

```
BIND(a, b):     a XOR b
  "How does position A look from position B's perspective?"
  "What changed between these two board states?"
  "How does Tal's style differ from Petrosian's?"

HAMMING(a, b):  popcount(a XOR b)
  "How similar are these two positions?"
  "How much did this move change the board?"
  "How compatible is this agent with this task?"

BUNDLE(a, b, c, ...):  majority_vote_per_bit([a, b, c, ...])
  "What's the typical position in the Najdorf?"
  "What's the consensus evaluation of this position?"
  "What's this agent's personality?" (bundle of all its experiences)
```

### 3.3 Everything Emerges

```
Opening theory:
  bundle(all positions reachable from 1.e4 c5) = "Sicilian" fingerprint
  → Not stored. Computed from the game tree.
  → Updates automatically as new games are played.
  → Transpositions: similar fingerprints = related openings (automatic).

Tactical concepts:
  Cluster positions by P-block similarity where NARS freq spikes.
  Cluster #47: positions where one piece attacks two targets.
  → The system discovers "fork" without being told the word.
  → NARS: <advantage, (0.85, 0.9)> after 10K games containing this pattern.

Strategic concepts:
  Cluster positions by S-block similarity at zone level (W16-W23).
  Cluster #183: positions with pawns on d5+e4+f3, bishop on g2.
  → The system discovers "Maroczy Bind" or something novel with no human name.
  → Emerges from structural similarity, not from labels.

Personality:
  agent.S = bundle(all positions agent has played)
  agent.P = bundle(all edges agent has traversed = moves it chose)
  agent.O = bundle(all terminal positions = outcomes it experienced)
  → Personality IS the accumulated trajectory.
  → Two agents from different seeds develop different personalities
    because early concept crystallization biases subsequent exploration.

Style transfer:
  BIND(position.O, tal_style.O) = "this position seen through Tal's eyes"
  → Find moves whose consequence O-block is closest to this perspective.
  → The system role-plays as Tal without a Tal database — just a style fingerprint.
```

---

## 4. The Brain Plasticity Experiment

### 4.1 Protocol

```
Start: Empty BindSpace. Agent knows only legal move generation.
       No database. No openings. No concepts. No Stockfish.
       Only input: game rules + game outcomes (win/draw/loss).

Loop (always running, lean memory ~512 MB):
  1. Scan contradiction map → hottest uncertainty                    (microseconds)
  2. Generate or find position exercising this contradiction         (milliseconds)
  3. Play the game from that position, moves guided by:
     - NARS truth of edges (prefer moves with high freq + conf)
     - Hamming similarity to positions with good outcomes
     - Curiosity bonus for edges with low confidence (exploration)   (seconds)
  4. Game ends → backpropagate NARS through edges                    (microseconds)
  5. Update contradiction INT4 sketches                              (nanoseconds)
  6. Check crystallization gates (L10):
     - Has any cluster of positions crossed the confidence threshold?
     - YES → create concept node, fill learned feature words         (microseconds)
     - This is the moment new structure appears in the graph.
  7. goto 1

Periodic burst (high memory, consolidation = "sleep"):
  - Load full history from Lance
  - Recluster all positions (boundaries may have shifted)
  - Bulk cross-pollination across agents
  - Compact contradiction map
  - Evict cold data back to Lance
```

### 4.2 The XOR Network Learns

Game 1 (random play):
```
Positions created: ~60 new nodes, ~60 new edges
Learned features: nothing (all W32-W63 still zero)
The graph is just a list of positions with outcomes.
```

Game 100 (still mostly random, but NARS has signal):
```
Some positions have been visited multiple times.
NARS truth on frequently-visited positions has conf > 0.3.
The agent slightly prefers edges with positive NARS freq.
Not playing random anymore — slight bias toward "good" moves.
```

Game 1,000:
```
First concept crystallizes: 
  Cluster of positions where queen captures undefended piece.
  P-block similarity: high (attack pattern matches).
  NARS correlation: freq 0.9 for "this leads to advantage".
  L10 fires → concept node created.
  Learned feature words W32-W35 in matching positions now encode 
  "undefended piece near my queen" pattern.
  
The agent now recognizes this pattern in NEW positions via hamming 
against the learned feature words. It didn't memorize specific 
positions — it learned a PATTERN.
```

Game 10,000:
```
~20 concepts crystallized. Edges between concepts exist:
  "fork" CAUSES "material_gain" (NARS: 0.8, 0.7)
  "pin_against_king" REQUIRES "open_file" (NARS: 0.6, 0.5)
  "central_pawn_majority" ENABLES "space_advantage" (NARS: 0.7, 0.6)
  
The agent chains concepts: "I have a pin AND an open file → 
  pin_against_king likely → advantage likely"
  
Two-step NARS deduction across edges. Not depth-first search.
Hamming match on P-block says "this looks like a pin position" 
in ~50 nanoseconds.
```

Game 100,000:
```
The agent has a personality:
  agent.S = bundle(all positions) — skewed toward tactical positions 
    (because early crystallization was tactical concepts)
  agent.P = bundle(all moves) — prefers captures and checks 
    (because those correlated with early success)
  agent.O = bundle(all outcomes) — mostly wins from sharp positions
  
A second agent with different seed has a different personality:
  agent2.S = skewed toward quiet positional positions
  agent2.P = prefers pawn advances and piece maneuvers
  agent2.O = mostly wins from endgames
  
hamming(agent1.S, agent2.S) = large
They learned different things from the same rules.
That's personality from brain plasticity.
```

### 4.3 Multi-Agent XOR Cross-Pollination

```
10 agents, all starting from zero, different seeds.

Every 10K games:
  consensus = bundle(all_agents.concepts)
  
  For each agent:
    my_unique = XOR(my.concepts, consensus)     — what only I know
    foreign   = XOR(consensus, my.concepts)     — what others know that I don't
    
    // Inject foreign concepts with low initial NARS confidence
    for concept in foreign:
      if concept.confidence_in_consensus > INJECTION_THRESHOLD:
        ingest(concept, confidence = consensus_conf * 0.3)  // cautious adoption
        // Agent must verify through its own play
        // Confidence rises if the concept works, drops if it doesn't
    
  Measure after injection + 10K verification games:
    Did individual Elo improve? → cross-pollination transfers understanding
    Did personalities converge? → chess has one truth, agents find it
    Did personalities diverge?  → agents specialized (one became tactician, one endgame expert)
    Did consensus graph contain new concepts? → emergent collective intelligence
```

### 4.4 Measurement

```
Primary metric: Elo vs games played (the learning curve)

  Elo measured by playing 100 games against fixed-strength opponent per measurement point.
  
  Shape of curve tells the story:
    Linear       → memorization, no generalization (bad)
    Logarithmic  → diminishing returns, shallow learning (mediocre)
    S-curve      → phase transitions, capability jumps (interesting)
    Stepped      → concept crystallization events (the target — proof of brain plasticity)

Each step in the Elo curve should align with a crystallization event (L10 firing).
Log every crystallization: game number, concept fingerprint, NARS truth, Elo before/after.
The step height = the Elo value of that concept.

Secondary metrics:
  Concept count vs games played              — how fast does structure emerge?
  Concept precision (human evaluation)       — are the concepts real or noise?
  Novel concept rate                         — does the system find unnamed patterns?
  Personality divergence across agents       — does development path matter?
  Cross-pollination Elo delta                — does sharing help?
  Swarm Elo vs best individual Elo           — does collective intelligence emerge?
  Prediction calibration (Brier score)       — does NARS produce calibrated confidence?
  Learning rate: Elo per game (normalized)   — efficiency of directed vs random exploration

The killer metric:
  Compare Elo/game between:
    Agent_Random:     plays random games, no contradiction targeting
    Agent_Directed:   plays games targeting its highest contradiction
    
  If Agent_Directed reaches Elo 1200 in 5K games and Agent_Random needs 50K,
  that's 10× sample efficiency from directed exploration.
  That's the brain plasticity paper.
```

---

## 5. Bridge to Real-World Knowledge Graphs

Everything that works for chess transfers directly:

| Chess | Real World |
|-------|-----------|
| Position (8×8 bitboard) | Entity state (fingerprinted from text/data) |
| Move (XOR between positions) | Event (XOR between entity states) |
| Game tree (vertical XOR network) | Timeline (vertical XOR network of events) |
| Opening (cumulative XOR fold) | Narrative (cumulative XOR fold of events) |
| Concept (discovered P-block cluster) | Insight (discovered pattern in force/tension) |
| Style (trajectory bundle) | Worldview (accumulated perspective) |
| NARS backpropagation | NARS backpropagation (same algorithm) |
| Contradiction-driven play | Contradiction-driven investigation |
| Elo measurement | Brier score prediction measurement |
| Novel concept discovery | Novel geopolitical insight discovery |
| Multi-agent cross-pollination | Multi-analyst consensus building |

Chess is where you prove the architecture. Reality is where you deploy it. The code is identical — only the fingerprinting function changes (bitboard extraction vs text embedding via Jina).

---

## 6. Implementation

### 6.1 Dependencies

```toml
[dependencies]
shakmaty = "0.27"       # Legal move generation, FEN parsing, bitboard operations
rand = "0.8"            # Self-play randomness
ladybug-contract = { path = "../crates/ladybug-contract" }  # Container, CogRecord
```

No Stockfish. No opening database. No neural network. No external evaluation.
Only the rules of chess and the Holograph substrate.

Optional (for measurement only, not for learning):
```toml
[dev-dependencies]
vampirc-uci = "0.11"    # Stockfish UCI protocol (for Elo measurement matches)
pgn-reader = "0.25"     # For comparing against human games (style authenticity)
```

### 6.2 Core Functions

```rust
/// Convert a shakmaty Board to a position CogRecord
fn board_to_cogrecord(board: &Chess) -> CogRecord {
    let mut record = CogRecord::new(ContainerGeometry::Xyz);
    
    // S-block: structure (piece bitboards → container words)
    // Each piece bitboard is already a u64. Direct copy.
    record.block_s.words[0] = board.white().pawns().0;
    record.block_s.words[1] = board.white().knights().0;
    record.block_s.words[2] = board.white().bishops().0;
    record.block_s.words[3] = board.white().rooks().0;
    record.block_s.words[4] = board.white().queens().0;
    record.block_s.words[5] = board.white().king().0;
    record.block_s.words[6] = board.black().pawns().0;
    // ... etc
    
    // P-block: tension (attack bitboards)
    for piece_type in PieceType::ALL {
        for sq in board.pieces_of(White, piece_type) {
            record.block_p.words[piece_type.index()] |= attacks(board, sq).0;
        }
    }
    record.block_p.words[14] = (record.block_p.words[12] & record.block_p.words[13]); // tension
    
    // O-block: consequences (legal move destinations)
    for mv in board.legal_moves() {
        let dest_bit = 1u64 << mv.to() as u32;
        record.block_o.words[mv.piece().index()] |= dest_bit;
    }
    
    record
}

/// Convert a move to an edge CogRecord (XOR of before/after)
fn move_to_edge(before: &CogRecord, after: &CogRecord) -> CogRecord {
    let mut edge = CogRecord::new(ContainerGeometry::Xyz);
    edge.block_s = before.block_s.xor(&after.block_s);  // structural delta
    edge.block_p = before.block_p.xor(&after.block_p);  // force delta
    edge.block_o = before.block_o.xor(&after.block_o);  // consequence delta
    edge
}

/// Backpropagate game result through edges
fn backpropagate(game: &[DnPath], result: f32, space: &BindSpace) -> Vec<BlackboardEntry> {
    let mut entries = Vec::new();
    let k = 1.0; // horizon parameter
    let decay = 0.95; // temporal discount
    
    for (i, dn) in game.iter().rev().enumerate() {
        let discount = decay.powi(i as i32);
        let evidence_strength = discount / k;
        
        entries.push(BlackboardEntry::NarsRevise {
            dn: *dn,
            observation_freq: if i % 2 == 0 { result } else { 1.0 - result },
            evidence_strength,
        });
    }
    entries
}

/// Choose a move guided by knowledge graph
fn choose_move(board: &Chess, space: &BindSpace, agent: &CogRecord) -> Move {
    let current = board_to_cogrecord(board);
    let mut best_move = None;
    let mut best_score = f32::MAX;
    
    for mv in board.legal_moves() {
        let mut after_board = board.clone();
        after_board.play_unchecked(&mv);
        let after = board_to_cogrecord(&after_board);
        
        // How much does this move's outcome look like what I want?
        let consequence_fit = after.block_o.hamming(&agent.block_o); // style alignment
        
        // What does the graph say about this position?
        let nars = space.lookup_nars(after.hash());
        let exploitation = nars.map(|n| n.frequency * n.confidence).unwrap_or(0.5);
        
        // Curiosity: prefer positions with low NARS confidence
        let exploration = nars.map(|n| 1.0 - n.confidence).unwrap_or(1.0);
        
        let score = consequence_fit as f32 
                    - exploitation * 1000.0 
                    - exploration * 200.0;  // exploration bonus
        
        if score < best_score {
            best_score = score;
            best_move = Some(mv);
        }
    }
    
    best_move.unwrap_or_else(|| board.legal_moves().choose(&mut rand::rng()).unwrap())
}
```

### 6.3 First Milestone

```
10,000 self-play games with zero starting knowledge.
Measure:
  - Elo at game 100, 1K, 5K, 10K
  - Number of crystallized concepts at each checkpoint  
  - Whether Elo steps align with crystallization events
  - Whether Agent_Directed outperforms Agent_Random in Elo/game

That's the proof that the substrate learns.
Everything else is optimization.
```
