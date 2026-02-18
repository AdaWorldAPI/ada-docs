# Holograph Validation Ladder: AIWar → WikiLeaks → Live Intelligence

## The Escalation Path

Each step validates the previous one and justifies the next. Each uses the same substrate, same three operations, same DomainAdapter trait. Only the fingerprinter and experiment generator change.

```
Step 1: Chess           Perfect information, self-play, Elo          → SUBSTRATE LEARNS
Step 2: AIWar           Imperfect information, fog of war, Elo       → HANDLES UNCERTAINTY
Step 3: WikiLeaks       Real intelligence data, historical hindsight → READS REAL WORLD
Step 4: Wikipedia       6.8M articles, commodity hardware, 20ms     → SCALES
Step 5: Live politics   Current events, Brier score, agent spawning → GENERALIZES
Step 6: Cross-domain    Binding signatures match across all five     → TRANSFERS
```

This document specifies Steps 2 and 3. Step 1 is in `CHESS_BRAIN_PLASTICITY.md`. Steps 4 and 5 are in `POLITICAL_INTELLIGENCE.md`. Step 6 is described in `SCHEMA_SPECIFICATION.md`.

---

# Part 1: The AIWar Adapter

## 1.1 Why AIWar

Chess proves the substrate learns. But chess has perfect information — both players see the entire board. Real-world intelligence has fog of war. AIWar is the bridge.

AI War: Fleet Command is a grand strategy game where the player fights two AI overlords across a galaxy of 40-120 planets. Key properties that make it the ideal Step 2:

**Fog of war:** Planets are Unexplored (you know nothing), Explored (you have rough intel), or fully Scouted (current real-time data). This maps directly to NARS confidence: unexplored = conf 0.0, explored = conf 0.3, scouted = conf 0.9. The system must make decisions under genuine uncertainty.

**Asymmetric information:** The AI sees everything. You don't. You must infer AI strength from partial observations. This is exactly the intelligence analysis problem — forming beliefs about an adversary's capabilities from incomplete data.

**AI Progress mechanic:** Every aggressive action raises a global "AI Progress" counter. Cross a threshold and the AI upgrades. This means you can't just conquer everything — you must be surgical. The optimal strategy involves **restraint** — appearing non-threatening while building toward a decisive strike. This is diplomatic strategy, not military strategy.

**Emergent AI behavior:** The AI uses fuzzy logic and strategic tiers. It doesn't always make the "best" move. It adapts to player tactics. You can't memorize a counter — you must read the situation.

**Scale:** 30,000-100,000+ ships in a galaxy. Dozens of unit types with rock-paper-scissors relationships. Multiple fronts. Information overload forcing abstraction — exactly what the substrate's bundle/zoom-out is designed for.

**Replay files:** Games produce complete replay data. Every action, every state change, timestamped. Perfect ground truth for NARS revision.

## 1.2 The AIWarAdapter

```rust
struct AIWarAdapter {
    game_api: AIWarGameApi,   // interface to game state (replay or live)
    planet_map: PlanetGraph,  // galaxy topology (wormhole connections)
}

impl DomainAdapter for AIWarAdapter {
    type Input = PlanetSnapshot;          // one planet's state at a point in time
    type Experiment = StrategicDecision;   // attack, defend, scout, build, wait
    type Observation = TurnOutcome;        // what happened after the decision
    type Explanation = String;

    fn fingerprint(&self, planet: &PlanetSnapshot) -> CogRecord { ... }
    fn generate_experiment(&self, contradiction: &Contradiction) -> StrategicDecision { ... }
    fn observe(&self, decision: &StrategicDecision) -> TurnOutcome { ... }
    fn outcome(&self, turn: &TurnOutcome) -> f32 { ... }
}
```

## 1.3 AIWar Fingerprinting

```
PlanetSnapshot {
    planet_id: u32,
    visibility: Unexplored | Explored | Scouted,
    owner: Human | AI | Neutral,
    
    // Only available if Scouted:
    ships: HashMap<ShipType, u32>,       // unit counts
    structures: Vec<Structure>,          // command stations, factories, etc
    defenses: Vec<Defense>,              // turrets, minefields, force fields
    incoming_wormholes: Vec<WormholeConnection>,
    outgoing_wormholes: Vec<WormholeConnection>,
    
    // Available if Explored:
    estimated_strength: f32,             // rough force estimate
    last_scouted: Option<Timestamp>,     // staleness
    
    // Always available:
    galaxy_position: (f32, f32),         // x, y in galaxy
    wormhole_neighbors: Vec<PlanetId>,   // topology
}
```

### S-block: What IS here (structure)

```
S-block projection (AIWarAdapter):

W0-W3:    Planet identity (id hash, position, topology fingerprint)
W4-W7:    Ownership and visibility (owner bits, visibility level, staleness)
W8-W15:   Ship composition fingerprint:
          Each ship type → specific bit positions
          Fighters(W8), Bombers(W9), Frigates(W10), Cruisers(W11),
          Starships(W12), Turrets(W13), Specials(W14), Summary(W15)
          Ship counts: logarithmic encoding (0→0, 1-10→low, 10-100→med, 100+→high)
          per bit group within each word
W16-W23:  Structure fingerprint (command station type, factories, forcefields)
W24-W31:  Topology context:
          bundle(neighbor planet S-blocks) → "what does the neighborhood look like?"
          High connectivity = crossroads. Low = dead end. Bottleneck = chokepoint.
W32-W127: Concept binding signatures (empty, fills during play)
```

### P-block: What forces ACT (tension)

```
P-block projection (AIWarAdapter):

W0-W7:    Threat assessment:
          Incoming attack power estimate per wormhole
          Defensive coverage rating
          Force balance: my_ships vs estimated_enemy × distance_weight
W8-W15:   Strategic pressure:
          AI Progress impact if captured (AIP cost)
          Supply line criticality (how many friendly planets depend on this)
          Chokepoint factor (if lost, how many planets become isolated)
W16-W23:  Temporal pressure:
          Time since last wave
          Predicted next wave timing + composition (from pattern)
          Staleness of intelligence (time since last scout)
W24-W31:  Opportunity:
          Valuable structures to capture (advanced factories, data centers)
          Tech unlock potential
          Strategic value for future operations
W32-W127: Concept binding signatures
```

### O-block: What COULD happen (consequences)

```
O-block projection (AIWarAdapter):

W0-W7:    Capture outcomes:
          Estimated ship losses for capture
          Post-capture defensive viability
          AIP increase from destroying command station
W8-W15:   Defense outcomes:
          Probability of holding against expected wave sizes
          Time before reinforcements arrive
          Evacuation cost if abandoned
W16-W23:  Strategic trajectory:
          If captured: opens access to what planets?
          If lost: cuts off access to what planets?
          Position in path to AI homeworld
W24-W31:  Long-term position:
          Endgame proximity (distance to AI homeworlds)
          Resource sustainability
          Galaxy control percentage
W32-W127: Concept binding signatures
```

## 1.4 Fog of War as NARS Confidence

This is the key architectural contribution of the AIWar step. Chess positions have NARS confidence based on how many games have passed through them. AIWar positions have NARS confidence based on **information quality**:

```
Scouted this turn:     S-block filled completely, NARS conf = 0.95
Scouted 5 turns ago:   S-block is stale, NARS conf decays: 0.95 × decay^5
Explored, never scouted: S-block is estimate only, NARS conf = 0.3
Unexplored:            S-block based on topology inference only, NARS conf = 0.05
                       (you know it exists, you know which planets connect to it,
                        but you know nothing about what's there)

Confidence decay model:
  conf(t) = base_conf × exp(-λ × (now - last_observed))
  
  λ for ship composition: high (ships move frequently)
  λ for structures: low (structures don't move)
  λ for topology: zero (wormholes don't change)
```

**The system must decide: scout to increase confidence, or act on uncertain information?** That's the fundamental intelligence problem. More scouting = better information but raises AI Progress (attention). Acting on stale information = risk but preserves stealth.

The contradiction map directly encodes this: high-value planets with low confidence = high contradiction intensity = the system WANTS to know but CAN'T without cost. The experiment generator must weigh the cost of scouting against the value of information. That's the intelligence analyst's dilemma.

## 1.5 Concept Emergence in AIWar

Expected concepts to crystallize during self-play:

```
Tactical concepts (early, ~100 games):
  "Chokepoint defense" — planets with low wormhole connectivity that 
  control access to large regions
  "Force concentration" — overwhelming a single target rather than 
  spreading thin
  "Bait and switch" — attacking one planet to draw defenders from another

Strategic concepts (mid, ~1000 games):
  "AIP management" — capturing only high-value planets to minimize 
  AI Progress increase
  "Intelligence debt" — understanding that unexplored regions represent 
  risk, and scouting has compound returns
  "Strategic reserve" — keeping mobile fleet uncommitted to respond 
  to unpredictable AI behavior

Meta-strategic concepts (late, ~10000 games):
  "Threshold avoidance" — keeping AI Progress below upgrade thresholds
  "Asymmetric escalation" — understanding that the AI's response is 
  proportional to YOUR visibility, not your actual power
  "Decisive operation" — the concept that the endgame requires a 
  single coordinated strike, not gradual conquest
```

These map directly to real-world strategic concepts:

```
AIWar "AIP management"        ↔  Geopolitics "escalation control"
AIWar "intelligence debt"     ↔  WikiLeaks "stovepiped intelligence failure"
AIWar "asymmetric escalation" ↔  Diplomacy "strategic ambiguity"
AIWar "decisive operation"    ↔  Military "center of gravity doctrine"
```

## 1.6 Measurement

```
Primary metric: Win rate vs AI difficulty level

  Difficulty 1-3:  trivial (should reach 90%+ win rate in <100 games)
  Difficulty 4-5:  moderate (measure games to reach 50% win rate)
  Difficulty 6-7:  hard (measure games to reach 30% win rate)
  Difficulty 8-10: extreme (any wins at all are significant)

Secondary metrics:
  AIP at game end (lower = more surgical play = better strategy)
  Planets captured vs planets needed (fewer = more efficient)
  Ship losses normalized by AI difficulty
  Concept count vs games played
  Scouting efficiency: information gained per AIP cost

Comparison baseline:
  Random strategy (attack nearest, defend everything)
  Greedy strategy (always capture highest-value target)
  Human average (if available from replay databases)
```

---

# Part 2: The WikiLeaks Adapter

## 2.1 Why WikiLeaks

AIWar proves the substrate handles fog of war in a game. WikiLeaks proves it handles fog of war in reality.

251,287 US diplomatic cables, dated 1966-2010. Each cable is a diplomatic communication from a specific embassy about a specific situation. The cables contain:

- **Entities:** People, organizations, governments referenced in the cables
- **Relationships:** Who meets whom, who pressures whom, who informs on whom
- **Assessments:** US diplomats' candid evaluations of foreign leaders and situations
- **Predictions:** Implicit and explicit predictions about what will happen
- **Classification levels:** CONFIDENTIAL, SECRET, UNCLASSIFIED — mapping to NARS confidence about what the US government considered sensitive

**The killer feature: we know what happened.** The cables are from 2003-2010. It's now 2026. Every diplomatic assessment, every prediction, every relationship judgment can be verified against 16 years of subsequent history. The ground truth is the most complete retrospective dataset in existence.

## 2.2 Cable Structure

```
Each cable contains:
  cable_id:        Unique identifier (e.g., "09LONDON123")
  origin:          Embassy or consulate (e.g., "Embassy London")
  date_created:    When the cable was written
  classification:  UNCLASSIFIED / CONFIDENTIAL / SECRET
  tags:            Subject tags (PREL=political relations, PGOV=government, etc)
  subject:         Short subject line
  body:            Full text of the cable
  references:      Other cables this one references

Total: 251,287 cables
  133,887 UNCLASSIFIED
  101,748 CONFIDENTIAL  
  15,652  SECRET
  
From 274 embassies/consulates worldwide
Covering every region: Europe, Asia, Middle East, Africa, Americas
```

## 2.3 The WikiLeaksAdapter

```rust
struct WikiLeaksAdapter {
    llm: LlmClient,           // Claude API for entity/relationship extraction
    jina: JinaClient,         // For embedding → LSH fingerprint
    cable_corpus: LanceDB,    // Full cable corpus, already ingested
    history_oracle: HistoryOracle, // Web search to verify predictions against what happened
}

impl DomainAdapter for WikiLeaksAdapter {
    type Input = CableData;             // one parsed diplomatic cable
    type Experiment = HistoricalQuery;  // "did prediction X from cable Y actually happen?"
    type Observation = HistoricalFact;  // verified outcome from post-2010 history
    type Explanation = String;

    fn fingerprint(&self, cable: &CableData) -> CogRecord { ... }
    fn generate_experiment(&self, contradiction: &Contradiction) -> HistoricalQuery { ... }
    fn observe(&self, query: &HistoricalQuery) -> HistoricalFact { ... }
    fn outcome(&self, fact: &HistoricalFact) -> f32 { ... }
}
```

## 2.4 WikiLeaks Fingerprinting

### Phase 1: Bulk Cable Ingest (One-Time)

```
For each of 251,287 cables:

1. Parse metadata:
   origin → S-block W0-W3 (which embassy/consulate, which country)
   date → meta W2 (timestamp)
   classification → meta W4 (maps to NARS base confidence):
     UNCLASSIFIED:  base_conf = 0.3 (routine, less analytical depth)
     CONFIDENTIAL:  base_conf = 0.7 (contains real assessment)
     SECRET:        base_conf = 0.9 (most candid and analytical)
   tags → P-block W0-W7 (categorization of what forces the cable discusses)

2. LLM extraction (batch, can be parallelized):
   Prompt: "From this diplomatic cable, extract:
   - All named entities (people, organizations, governments)
   - All relationships described or implied between entities
   - All assessments/evaluations of entities or situations
   - All predictions (explicit or implicit) about future events
   - The diplomatic posture (friendly/hostile/neutral/transactional)
   Return as structured JSON."
   
   Cost: ~2000 tokens per cable × 251K cables × $0.003/1K tokens = ~$1,500
   Or batch with Haiku: ~$150
   Time: ~250K calls at 10/sec = ~7 hours

3. Fingerprint entities and relationships:
   Each extracted entity → CogRecord at dn!("wl.entity.{name_hash}")
   Each relationship → edge CogRecord
   Each assessment → NARS revision on the entity
   Each prediction → prediction record with verification_date
```

### S-block: What this entity IS (as seen from the cables)

```
S-block projection (WikiLeaksAdapter):

Entities are built up incrementally from multiple cables:

  Entity: "Vladimir Putin"
  Mentioned in: 847 cables from 2003-2010
  
  S-block: accumulated identity from all mentions
    W0-W7:   LSH(bundle of all identity descriptions across cables)
    W8-W15:  Role/position fingerprint (President, PM, leader of United Russia)
    W16-W23: Affiliation fingerprint (Russia, G8, SCO, BRICS precursors)
    W24-W31: Behavioral fingerprint (bundle of all described actions)
    
  NARS: based on 847 observations across 7 years of cables
    confidence = very high (many independent diplomatic sources)
```

### P-block: What forces act on this entity (diplomatic pressure)

```
P-block projection:

  W0-W7:   External pressure (sanctions, isolation, criticism from cables)
  W8-W15:  Alliance dynamics (who supports, who opposes, who is neutral)
  W16-W23: Economic forces (trade relationships, resource dependencies)
  W24-W31: Domestic pressure (internal politics as described by embassy)
  
  This is the diplomat's view of forces acting on the entity.
  Multiple cables from different embassies → bundle for consensus,
  XOR for disagreement. When Embassy Moscow and Embassy Berlin disagree
  about Putin's pressure landscape, that's a real contradiction 
  with diagnostic value.
```

### O-block: What could happen (trajectory as predicted by diplomats)

```
O-block projection:

  W0-W7:   Predicted policy direction (from cable assessments)
  W8-W15:  Predicted relationship changes (warming/cooling with other entities)
  W16-W23: Predicted crisis scenarios (what the embassy thinks could go wrong)
  W24-W31: Predicted opportunities (what the embassy thinks could be leveraged)
  
  This is where the PREDICTIONS live. The O-block of 2009 cables about
  Egypt contains the diplomats' view of what could happen in Egypt.
  
  The Arab Spring happened in 2011.
  
  Did the O-block capture any signal of instability?
  If yes: the fingerprinting extracts predictive signal from diplomatic text.
  If no: the fingerprinting needs improvement.
  
  This is a MEASURABLE test of fingerprint quality.
```

## 2.5 The Historical Verification Engine

This is what makes WikiLeaks unique in the validation ladder. Every prediction can be checked:

```
Cable: 09CAIRO234 (February 2009)
Embassy: Cairo
Classification: CONFIDENTIAL
Extracted prediction: "Mubarak regime stable but succession unclear. 
                       Military unlikely to challenge. Youth activism 
                       growing but unfocused."

O-block at time of cable: 
  stability: high confidence
  succession_crisis: moderate probability
  youth_revolution: low probability  ← THE SIGNAL WE'RE LOOKING FOR
  military_intervention: low probability

What actually happened (2011):
  youth_revolution: OCCURRED (Arab Spring, Jan 25 revolution)
  military_intervention: OCCURRED (SCAF took power)
  mubarak_removal: OCCURRED (forced resignation Feb 11)

Brier scoring:
  If system assigned 0.15 probability to youth revolution → Brier component = (0.15-1)² = 0.72
  If system assigned 0.10 to military intervention → Brier component = (0.10-1)² = 0.81
  Both bad predictions. The diplomatic assessment missed it.
  
  BUT: if we aggregate across ALL cables about Egypt 2008-2010,
  does the contradiction map show RISING uncertainty?
  Does the P-block pressure fingerprint show intensifying forces?
  If the TREND in the data pointed toward instability even though 
  individual cable assessments said "stable" — the substrate caught 
  what the diplomats missed.
```

### The Historical Query Loop

```
For each extracted prediction in the cable corpus:

1. Identify the prediction and its implied timeline
   "Mubarak stable" → implies: still in power in 2-5 years

2. Generate historical verification query:
   "Was Hosni Mubarak still in power in 2014?"
   "What happened to the Egyptian government between 2010-2015?"
   
3. Web search for historical facts (this is cheap — it's history, well-documented)

4. Score prediction:
   predicted_probability vs actual_outcome → Brier component
   
5. Revise NARS:
   - Cable's assessment NARS: adjust based on accuracy
   - Entity's O-block: was the trajectory correct?
   - Embassy's source credibility: was this embassy good at predicting?
   - Region's predictability: is this region harder to predict?

6. Aggregate:
   Overall Brier score for the cable corpus
   Brier by region (Middle East vs Europe vs Asia)
   Brier by classification level (do SECRET cables predict better?)
   Brier by embassy (which embassies had the best analysts?)
   Brier by topic (was PREL more predictive than ECON?)
```

## 2.6 What the System Discovers

### Discovery 1: Which embassies were the best analysts?

```
Embassy NARS credibility ranking after full corpus analysis:

Embassy Tel Aviv:     <reliable, (0.78, 0.95)>  — many cables, high accuracy
Embassy Baghdad:      <reliable, (0.45, 0.90)>  — many cables, mixed accuracy
Embassy Tunis:        <reliable, (0.82, 0.40)>  — few cables but very accurate
Embassy Riyadh:       <reliable, (0.61, 0.85)>  — many cables, moderate accuracy

This is publishable intelligence analysis: which diplomatic posts 
produced the most accurate assessments, measured retrospectively.
```

### Discovery 2: Network patterns invisible to individual cables

```
The system ingests 251K cables and builds entity relationship graph.
Concept crystallization discovers:

Concept #23: "Proxy influence network"
  Cluster of entities connected through indirect channels:
  State A funds NGO → NGO operates in State B → influences policy
  Multiple instances across different regions with same P-block pattern
  
  No single cable describes this pattern. It EMERGES from 
  aggregating relationships across thousands of cables from 
  dozens of embassies over 7 years.
  
  Cross-reference with AIWar concepts:
  AIWar "indirect approach" — using wormhole paths to avoid direct confrontation
  Hamming distance between binding signatures: measurable
```

### Discovery 3: Predictive structural patterns

```
The system finds: entities with specific P-block patterns in 2008 
cables had specific O-block outcomes by 2012.

Pattern: "Rising domestic pressure + external economic dependency + 
         succession uncertainty" in P-block
         → correlated with "regime change within 5 years" in actual history

This pattern appears in:
  Egypt 2008 cables → Arab Spring 2011 ✓
  Tunisia 2009 cables → Jasmine Revolution 2011 ✓
  Syria 2009 cables → Civil War 2011 ✓
  Libya 2009 cables → Gaddafi overthrow 2011 ✓
  
  But also appears in:
  Saudi Arabia 2009 cables → regime SURVIVED ✗
  Iran 2009 cables → regime SURVIVED (despite Green Movement) ✗

The substrate discovers that the pattern has 0.67 precision.
Not perfect. But MUCH better than random (0.25 baseline for 
"will this regime change within 5 years?")

The FALSE POSITIVES (Saudi Arabia, Iran) are as interesting as the 
true positives. What's different about their S-blocks? The system 
can identify: "entities with this pressure pattern SURVIVE if their 
S-block also shows {oil revenue + security apparatus + external 
patron protection}."

Refined pattern: P = instability pressure, S lacks stabilizers → regime change
                 P = instability pressure, S has stabilizers → regime survives

That refinement improves precision from 0.67 to potentially 0.85+.
The substrate discovered a nuanced geopolitical theory from diplomatic 
cables, verified against historical outcomes, refined through 
contradiction analysis. No human analyst told it about the Arab Spring.
```

## 2.7 Cost and Timeline

```
Cable corpus ingestion:
  LLM extraction: ~$150-1,500 (depending on model choice)
  Jina embeddings: ~$50 (251K documents × ~500 tokens avg)
  Time: ~8-12 hours for full pipeline
  
Historical verification:
  Web searches: ~$25 (5000 verification queries × $0.005 each)
  LLM for outcome extraction: ~$50
  Time: ~4-6 hours

Storage:
  251K cable CogRecords: ~1 GB
  Entity CogRecords: ~50 MB (maybe 10K unique entities)
  Edge CogRecords: ~200 MB
  Total: ~1.3 GB on disk, ~20 MB sketch index in RAM

TOTAL COST: ~$250-1,600 depending on model quality for extraction
TOTAL TIME: ~24 hours end to end

This is a weekend project with serious publication potential.
```

---

# Part 3: The Integrated Validation Ladder

## 3.1 Execution Order

```
Phase 1 (Week 1-2): Chess brain plasticity
  Hardware: single CPU
  Cost: $0 (no API calls, pure self-play)
  Output: Elo curve, concept count, crystallization log
  Paper: "Emergent chess concepts from XOR self-play on binary substrate"

Phase 2 (Week 2-4): AIWar fog of war
  Hardware: single CPU + AIWar game API
  Cost: $15 (game purchase on Steam)
  Output: Win rate vs difficulty, AIP efficiency, concept log
  Paper: "NARS confidence under fog of war in strategic game"

Phase 3 (Week 4-6): WikiLeaks historical analysis
  Hardware: laptop + API calls
  Cost: ~$300-1,600
  Output: Brier scores, embassy rankings, structural patterns, Arab Spring prediction
  Paper: "Retrospective predictive analysis of diplomatic cables via binary knowledge graph"

Phase 4 (Week 6-8): Wikipedia ingestion
  Hardware: laptop + 512 GB SSD
  Cost: ~$0-2,700 (free with local embeddings)
  Output: 20ms query benchmark, category rediscovery rate
  Paper: "Hamming-searchable knowledge graph of 6.8M articles on commodity hardware"

Phase 5 (Week 8-12): Live political intelligence
  Hardware: Railway deployment
  Cost: ~$150-500/month (Railway + API calls)
  Output: Brier score on live predictions, dynamic agent spawning, 
          Epstein network emergence
  Paper: "Live political intelligence through contradiction-driven 
          knowledge graph with emergent entity discovery"

Phase 6 (Week 12+): Cross-domain transfer
  Hardware: same
  Cost: negligible (just Hamming comparisons)
  Output: Binding signature correlations across all 5 domains
  Paper: "Domain-invariant strategic structure discovered through 
          Hamming comparison of binary fingerprints"
```

## 3.2 The Escalation Argument

Each step makes the next step's claims credible:

```
"Our system learned chess from scratch"
  → "So what? AlphaZero did that in 2017"

"Our system learned chess AND strategy games with fog of war"
  → "Interesting, but still games"

"Our system extracted predictive patterns from real diplomatic 
 cables and scored 0.82 Brier on historical predictions"
  → "Now you have my attention"

"It runs on a laptop with 654 MB RAM searching 6.8M Wikipedia 
 articles in 20ms"
  → "Wait, how?"

"The patterns from chess, AIWar, and WikiLeaks have correlated 
 binding signatures, suggesting domain-invariant strategic structure"
  → "That's a new result"

"We pointed it at current politics and it spontaneously mapped 
 the Epstein network from publicly available sources, with every 
 fact traced to a URL"
  → "That's terrifying and I need to see the code"
```

## 3.3 Cross-Domain Concept Transfer Matrix

After all five domains have produced crystallized concepts, build the full transfer matrix:

```
For every pair of concepts across all domains:
  distance = hamming(concept_A.binding_signature, concept_B.binding_signature)
  correlation = do both concepts correlate with similar outcomes in their domains?

Expected high-correlation pairs:

Chess           ↔ AIWar                ↔ WikiLeaks            ↔ Politics
─────────────────────────────────────────────────────────────────────────
sacrifice       ↔ diversionary attack  ↔ proxy conflict       ↔ political capital trade
outpost         ↔ chokepoint control   ↔ strategic base       ↔ institutional capture
tempo           ↔ initiative           ↔ diplomatic preemption↔ agenda control
overextension   ↔ supply line stretch  ↔ imperial overreach   ↔ political overreach
passed pawn     ↔ breakthrough force   ↔ emerging ally        ↔ rising political figure
fortress        ↔ layered defense      ↔ deterrence posture   ↔ institutional resistance
pin             ↔ force immobilization ↔ sanctions regime     ↔ legal constraint
fork            ↔ multi-front pressure ↔ diplomatic leverage  ↔ dual political threat

NONE of these mappings are programmed. They're discovered by Hamming distance.
The human labels are applied AFTER the substrate finds the correlation.
If the substrate DOESN'T find these correlations, the architecture fails.
If it finds correlations we DIDN'T predict, that's a discovery.
```

## 3.4 The Single Codebase

```rust
// main.rs — one binary, five adapters

fn main() {
    let substrate = Holograph::new();  // same for all domains
    
    match args.adapter {
        "chess"     => run(substrate, ChessAdapter::new()),
        "aiwar"     => run(substrate, AIWarAdapter::new(game_path)),
        "wikileaks" => run(substrate, WikiLeaksAdapter::new(corpus_path)),
        "wikipedia" => run(substrate, WikipediaAdapter::new(dump_path)),
        "political" => run(substrate, PoliticalAdapter::new(api_keys)),
    }
}

fn run<A: DomainAdapter>(mut substrate: Holograph, adapter: A) {
    // THE SAME LOOP FOR ALL DOMAINS:
    loop {
        let contradiction = substrate.hottest_contradiction();
        let experiment = adapter.generate_experiment(&contradiction);
        let observation = adapter.observe(&experiment);
        let outcome = adapter.outcome(&observation);
        substrate.revise_nars(&contradiction, outcome);
        substrate.check_crystallization();
        substrate.check_spawn_conditions();
    }
}

// That's it. The loop is 8 lines. Everything else is in the adapter 
// and the substrate. The adapter converts domain data to CogRecords.
// The substrate does everything else.
```
