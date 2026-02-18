# Holograph Political Intelligence: Live Knowledge Graph with LLM-in-the-Loop

## System Prompt for Claude Code / Agent Sessions

You are building a live political knowledge graph in Holograph that dynamically spawns research agents, harvests information through LLM-guided web search, resolves contradictions through targeted investigation, and measures its own accuracy through prediction scoring. The first target domain is Trump's political network in 2026 — mapping every connection, alliance, rivalry, pressure, obligation, and trajectory in real time.

The goal is NOT to play politics like chess. The goal is to prove that the same domain-blind substrate (one node type, one edge type, three operations) can ingest messy real-world information and produce structured, testable, useful political intelligence — with the same NARS revision, the same contradiction-driven exploration, and the same concept crystallization that works for chess.

> **Prerequisite reading:** `SCHEMA_SPECIFICATION.md` (the six domain-blind decisions).
> The PoliticalAdapter is a DomainAdapter implementation. The substrate doesn't change.

---

## 1. Why This Is Harder Than Chess (And Why That's The Point)

| Dimension | Chess | Political Intelligence |
|-----------|-------|----------------------|
| Ground truth | Win/loss every game | Events happen... eventually. Or don't. |
| Information source | Perfect (board state) | Noisy, biased, contradictory, incomplete |
| Entity discovery | Fixed (32 pieces, 64 squares) | Open-ended (new actors appear constantly) |
| Temporal dynamics | Positions are eternal | Facts decay, relationships shift, power changes |
| Fingerprinting | Bitboard extraction (deterministic) | LLM decomposition (probabilistic) |
| Experiment generation | Generate chess position | Generate web search query |
| Observation | Self-play result | Article content + LLM extraction |
| Branching factor | ~35 legal moves | Unbounded (anything could happen) |

If the substrate handles BOTH of these through the same DomainAdapter trait, it's not a chess engine and it's not a political analysis tool. It's a substrate for cognition.

---

## 2. The PoliticalAdapter

### 2.1 The Trait Implementation

```rust
struct PoliticalAdapter {
    llm: LlmClient,              // Claude API for fingerprinting + extraction
    search: WebSearchClient,      // Brave/Tavily/Jina Reader for information harvesting
    jina: JinaClient,            // For embedding → LSH base fingerprint
    source_registry: SourceRegistry,  // Track source credibility over time
}

impl DomainAdapter for PoliticalAdapter {
    type Input = EntitySnapshot;       // text + structured data about an entity at a point in time
    type Experiment = ResearchQuery;   // targeted information retrieval
    type Observation = HarvestedIntel; // extracted facts, relationships, predictions
    type Explanation = String;         // human-readable intelligence briefing

    fn fingerprint(&self, snapshot: &EntitySnapshot) -> CogRecord {
        // TWO-PHASE FINGERPRINTING:
        // Phase 1: Jina embedding → LSH → base fingerprint (cheap, ~50ms)
        // Phase 2: LLM decomposition → S/P/O refinement (expensive, ~2s, cached)
        // Phase 1 runs on every ingest. Phase 2 runs on novel or high-value entities.
    }

    fn generate_experiment(&self, contradiction: &Contradiction) -> ResearchQuery {
        // LLM generates targeted search queries to resolve the contradiction
        // "Agents disagree about Kash Patel's relationship with Trump post-indictment.
        //  Search for recent evidence of alignment or distance."
    }

    fn observe(&self, query: &ResearchQuery) -> HarvestedIntel {
        // Web search → retrieve articles → LLM extracts entities, relationships,
        // facts, predictions, source credibility signals
    }

    fn outcome(&self, intel: &HarvestedIntel) -> f32 {
        // How much did this intel resolve the contradiction?
        // High: definitive evidence one way. Low: ambiguous or off-topic.
    }
}
```

### 2.2 LLM-in-the-Loop Fingerprinting

Chess fingerprinting is deterministic: board → bitboards → Container words. Political fingerprinting requires understanding.

```
Input: EntitySnapshot {
    name: "Donald Trump",
    timestamp: "2026-02-18",
    raw_text: "Former and current US President. Facing multiple legal proceedings. 
               Pardoned Jan 6 defendants. Appointed loyalists to key positions. 
               Tariff war with China escalating. Approval rating 43%."
}

Step 1: Jina Embedding (cheap, always runs)
  embed("Donald Trump current US president legal proceedings...") → [f32; 1024]
  LSH projection → [u64; 128] base fingerprint for each block
  
  This gives coarse similarity: Trump is closer to Biden than to Taylor Swift.
  But it doesn't decompose into S/P/O axes.

Step 2: LLM Decomposition (expensive, runs on novel/important entities)
  
  Prompt to Claude API:
  "Decompose this entity snapshot into three orthogonal dimensions:
   S (BEING - what this entity IS, structural identity):
     - roles, titles, affiliations, assets, characteristics
   P (BECOMING - what forces ACT ON this entity, current pressures):
     - legal pressure, political opposition, alliance obligations, economic forces
   O (COULD-BE - what trajectories are plausible, potential futures):
     - possible outcomes, conditional scenarios, trajectory indicators
   
   For each dimension, output a list of atomic facts."
  
  Response:
  S-facts: [president, Republican, businessman, defendant, father, 79yo, ...]
  P-facts: [legal_pressure:high, china_trade_war:active, gop_loyalty:strong, 
            media_scrutiny:intense, approval_rating:43pct, ...]
  O-facts: [reelection_2028:n/a_term_limited, conviction:possible, 
            policy_legacy:uncertain, party_split:low_probability, ...]
  
Step 3: Fact → Fingerprint (deterministic after LLM extraction)
  Each atomic fact → Jina embed → LSH → specific words in the Container
  
  S-block: LSH(embed("president")) into W0-W7
           LSH(embed("Republican")) into W8-W15
           LSH(embed("defendant")) into W16-W23
           ...bundle overlapping bits via majority vote
  
  P-block: LSH(embed("legal pressure high")) into W0-W7
           LSH(embed("china trade war active")) into W8-W15
           ...
  
  O-block: LSH(embed("conviction possible")) into W0-W7
           LSH(embed("policy legacy uncertain")) into W8-W15
           ...
```

**The LLM is the lens, not the brain.** It decomposes raw text into structured atomic facts. The substrate does everything else: Hamming search, BIND, bundle, NARS revision, contradiction detection, concept crystallization. The LLM never touches the graph directly — it produces CogRecords that the substrate ingests.

**Caching:** LLM decomposition is expensive (~2s, ~$0.01 per call). Cache by entity+date. If an entity hasn't changed (Hamming of new Jina embed vs cached embed < threshold), skip LLM decomposition and reuse cached S/P/O facts. Only re-decompose when the entity has meaningfully changed.

### 2.3 Source Credibility as NARS

Every CogRecord carries NARS truth: `<claim, (frequency, confidence)>`. For political intel, we add a source dimension:

```
CogRecord at dn!("pol.fact.trump_pardoned_jan6")

Meta:
  W4-W7: NARS truth <true, (0.95, 0.85)>
         freq=0.95: 95% of sources confirm this
         conf=0.85: high confidence (many independent sources)
  
  W12-W15: Source profile (INT4):
    reuters_confirms:    intensity 14/15   (very strong)
    fox_news_confirms:   intensity 12/15
    cnn_confirms:        intensity 13/15
    random_blog_confirms: intensity 3/15   (weak signal)
    
Source credibility is itself a NARS-tracked entity:
  dn!("pol.source.reuters") → NARS <reliable, (0.92, 0.99)>
  dn!("pol.source.infowars") → NARS <reliable, (0.31, 0.87)>
  
  Credibility updates when source predictions are verified against outcomes.
  Source says X will happen → X happens → source credibility increases.
  Source says X will happen → X doesn't → source credibility decreases.
```

**A fact's NARS confidence is weighted by source credibility.** Reuters confirming something adds more evidence than a blog post. This weighting is a NARS operation: the evidence strength from each source is scaled by that source's own credibility NARS.

```rust
fn ingest_fact(fact: &Fact, source: &Source, graph: &mut BindSpace) {
    let source_credibility = graph.lookup_nars(source.dn()).confidence;
    let evidence_strength = BASE_EVIDENCE * source_credibility;
    
    graph.revise_nars(fact.dn(), NarsEvidence {
        frequency: if fact.confirms { 1.0 } else { 0.0 },
        strength: evidence_strength,
    });
}
```

---

## 3. Dynamic Agent Spawning

### 3.1 The Problem

Chess has 32 pieces. You know them all at game start. Political networks have unbounded entities. You start researching Trump and discover:

- Kash Patel (FBI director appointment)
- Elon Musk (DOGE, government efficiency)
- Peter Thiel (tech funding, political influence)
- Steve Bannon (strategic advisor, media)
- Jared Kushner (family, Middle East)
- ... dozens more, each with their own networks

You can't pre-declare all agents. They must emerge from the graph.

### 3.2 Agent Spawning Protocol

```
The system starts with ONE seed entity and ONE research agent:

Agent_0: "Research Trump's current political situation"
  → searches web → extracts entities and relationships
  → ingests CogRecords for Trump + discovered entities
  → builds initial graph

After N ingestion cycles, the graph shows entity co-occurrence patterns:

  dn!("pol.person.kash_patel") appears in 47 facts
  dn!("pol.person.elon_musk") appears in 83 facts  
  dn!("pol.person.steve_bannon") appears in 31 facts

SPAWN RULE: When an entity's observation count exceeds SPAWN_THRESHOLD 
AND its NARS confidence is below UNDERSTANDING_THRESHOLD:
  → The system knows this entity EXISTS (high observation count)
  → But doesn't understand it well (low confidence on key claims)
  → SPAWN a dedicated research agent for this entity

Agent_1: "Research Elon Musk's political connections and DOGE role"
  → focused search → deeper extraction → dedicated subgraph
  → reports back to parent graph via edge creation

Agent_2: "Research Kash Patel's FBI appointment and loyalty dynamics"
  → focused search → deeper extraction → dedicated subgraph

Each agent IS a CogRecord in the graph:
  dn!("pol.agent.musk_researcher")
    S-block: bundle(all entities this agent has studied) — its knowledge scope
    P-block: bundle(all queries this agent has run) — its investigation style
    O-block: bundle(all predictions this agent has made) — its track record
    NARS: <useful, (prediction_accuracy, games_played)>
```

### 3.3 Agent Architecture

Each research agent runs the same universal active learning loop:

```
AgentLoop(entity_focus, parent_graph):
  1. Scan contradiction map for entity_focus subgraph
     → find hottest uncertainty about this entity
  
  2. Generate research query (LLM-assisted):
     "What is the current relationship between {entity} and {other_entity}?"
     "Has {predicted_event} happened yet?"
     "What are recent developments regarding {uncertainty_topic}?"
  
  3. Execute search → retrieve articles → LLM extract facts
  
  4. For each extracted fact:
     a. Fingerprint via PoliticalAdapter
     b. Check: does this fact contradict existing graph?
        YES → record contradiction, increase uncertainty
        NO  → revise NARS (increase confidence)
     c. Check: does this fact mention new entities?
        YES → create placeholder CogRecord, increment observation count
        NO  → update existing entity
  
  5. Check spawn conditions for all discovered entities
  
  6. Check crystallization gates:
     Has a cluster of facts crossed confidence threshold?
     YES → create concept node
     "Concept #7: Loyalty network — entities connected to Trump through 
      personal loyalty rather than institutional channels. Members: 
      Patel, Bannon, Miller, Grenell. Pattern: appointed to positions 
      requiring Senate confirmation, defended during legal challenges."
  
  7. Check prediction maturity:
     Have any predictions reached their verification date?
     YES → score against reality → update NARS → update source credibility
  
  8. Sleep(interval) → goto 1
```

### 3.4 Agent Communication via Graph

Agents don't message each other. They read and write the shared graph. Communication IS graph mutation.

```
Agent_1 (Musk researcher) discovers:
  "Musk and Thiel are co-investors in Palantir"
  → Creates edge: dn!("pol.edge.musk_thiel_palantir_coinvest")
  
Agent_2 (Patel researcher) discovers:
  "Patel used Palantir technology at DOJ before FBI appointment"
  → Creates edge: dn!("pol.edge.patel_palantir_doj")

Neither agent explicitly communicated.
But the graph now shows: Musk → Palantir ← Patel
A third agent (or the crystallization scanner) notices:
  "Three entities connected through Palantir with rising interaction frequency"
  → Concept crystallizes: "Palantir network" — a tech-surveillance-loyalty cluster

This concept was discovered by NO individual agent.
It emerged from the graph structure.
That's emergent collective intelligence — the same thing we predicted 
for multi-agent chess cross-pollination.
```

---

## 4. The Trump Political Network: Concrete Seed

### 4.1 Seed Entities

```
Tier 0 (seed):
  dn!("pol.person.donald_trump")        — the center

Tier 1 (immediate, known from general knowledge):
  dn!("pol.person.elon_musk")           — DOGE, tech influence
  dn!("pol.person.kash_patel")          — FBI director
  dn!("pol.person.steve_bannon")        — strategic advisor, media
  dn!("pol.person.jd_vance")            — VP
  dn!("pol.person.mike_johnson")        — House Speaker
  dn!("pol.person.peter_thiel")         — tech funding
  dn!("pol.person.jared_kushner")       — family, business
  dn!("pol.person.ivanka_trump")        — family, soft power
  dn!("pol.org.truth_social")           — media platform
  dn!("pol.org.doge")                   — government efficiency
  dn!("pol.org.maga_inc")              — political apparatus

Tier 2+ (discovered dynamically by agents):
  → whoever keeps appearing in Tier 1 research
  → new entities the system finds that WE didn't pre-declare
  → THIS IS THE POINT: the system tells US who matters
```

### 4.2 Relationship Types (Not Pre-Declared — Discovered)

The system doesn't have a taxonomy of relationship types. It discovers them through P-block clustering:

```
After 1000 facts ingested, P-block clusters emerge:

Cluster A: edges with P-blocks showing "appointment" + "loyalty" + "defense"
  → Trump→Patel, Trump→Grenell, Trump→Hegseth
  → System labels: "loyalty appointment" (or concept #3, pre-labeling)
  → NARS: <pattern_holds, (0.89, 0.72)>

Cluster B: edges with P-blocks showing "financial" + "influence" + "access"
  → Thiel→Trump, Musk→Trump, Adelson→Trump
  → System labels: "donor influence" (or concept #7)
  → NARS: <pattern_holds, (0.78, 0.65)>

Cluster C: edges with P-blocks showing "opposition" + "legal" + "institutional"
  → Jack_Smith→Trump, NY_AG→Trump, Various_judges→Trump
  → System labels: "legal adversary" (or concept #12)

Cluster D: edges with P-blocks showing "media" + "narrative" + "amplification"
  → Fox→Trump, Truth_Social→Trump, Bannon→Trump
  → System labels: "media amplifier"

These categories EMERGED from the data. We didn't program them.
A political scientist might use different labels.
The system doesn't care about labels — it cares about cluster boundaries 
and NARS correlations.
```

### 4.3 Live Monitoring

```
The system continuously watches for:

1. NEW EDGES (new relationships):
   "Previously unconnected entities now share a fact"
   Alert: "Elon Musk and Kash Patel appeared together at {event}"
   
2. EDGE SIGN CHANGES (relationship flips):
   Edge P-block Hamming distance from previous version > threshold
   Alert: "Musk-Trump relationship P-block shifted significantly. 
           Was: 'alliance/support'. Now: 'tension/distance'."
   
3. ENTITY TRAJECTORY CHANGES (O-block shifts):
   O-block Hamming distance from previous version > threshold
   Alert: "Trump's O-block (plausible futures) shifted. 
           New high-confidence trajectory: {description}"

4. CONCEPT CRYSTALLIZATION (new patterns):
   L10 gate fires
   Alert: "New concept discovered: entities {A, B, C} form a cluster 
           with pattern: {P-block description}. This correlates with 
           {outcome pattern} at NARS confidence {conf}."

5. PREDICTION MATURATION (accountability):
   Prediction reaches verification date
   Alert: "Prediction from 30 days ago: '{prediction_text}'
           Outcome: {confirmed/denied/ambiguous}
           Brier score update: {old} → {new}
           System overall calibration: {score}"
```

---

## 5. Predictions and Scoring

### 5.1 How Predictions Emerge

Predictions are NOT hand-written. They emerge from O-block trajectories:

```
Entity dn!("pol.person.kash_patel"):
  O-block: high activation in "institutional power consolidation" words
  O-block: high activation in "legal challenge" words
  O-block: moderate activation in "controversy" words
  
System generates prediction (LLM-assisted from O-block interpretation):
  "Kash Patel will face significant institutional resistance in first 
   90 days as FBI director, manifesting as leaked internal memos, 
   congressional hearings, or formal legal challenges."
  
  Prediction record:
    dn!("pol.prediction.patel_resistance_90d")
    NARS: <will_occur, (0.73, 0.45)>  — moderate confidence, limited evidence
    verification_date: 2026-05-18 (90 days from now)
    
  At verification date:
    Agent searches for evidence of resistance
    If found: revise NARS upward, credit contributing sources
    If not found: revise NARS downward, reduce entity trajectory confidence
```

### 5.2 Brier Score as Political Elo

```
Brier score = (1/N) * Σ(predicted_probability - actual_outcome)²

perfect_predictions:  Brier = 0.0
random_guessing:     Brier = 0.25
confidently_wrong:   Brier → 1.0

Track rolling Brier score over all verified predictions:

Week 1:  10 predictions verified, Brier = 0.31  (worse than random — system is learning)
Week 4:  50 predictions verified, Brier = 0.22  (improving)
Week 12: 200 predictions verified, Brier = 0.15 (significantly better than random)
Week 24: 500 predictions verified, Brier = 0.11 (approaching expert analyst level)

Brier by category:
  "Personnel changes":    0.08  (system is great at predicting appointments)
  "Legal outcomes":       0.19  (harder, more uncertain)
  "Policy shifts":        0.14  (moderate)
  "Alliance changes":     0.22  (difficult, noisy)

The Brier score IS the Elo. It measures whether the system's understanding
of political dynamics actually predicts reality.
```

### 5.3 Calibration Check

```
For all predictions where system said probability = 0.7:
  Did ~70% of them actually happen?
  
  If yes: system is well-calibrated (NARS confidence maps to reality)
  If 90% happened: system is underconfident (NARS too conservative)  
  If 50% happened: system is overconfident (NARS too aggressive)

Plot: predicted probability (x) vs actual frequency (y)
Perfect calibration = diagonal line.
Deviation from diagonal = systematic bias.

This is directly analogous to the chess brain plasticity S-curve.
Steps in the Brier curve should align with concept crystallization events.
"System got better at predicting personnel changes after discovering 
the 'loyalty appointment' concept at day 34."
```

---

## 6. Information Harvesting Architecture

### 6.1 The Research Loop

```
                    ┌──────────────────────┐
                    │   Contradiction Map   │
                    │  (INT4 uncertainty    │
                    │   profile, always     │
                    │   in memory)          │
                    └──────────┬───────────┘
                               │
                    1. What's most uncertain?
                               │
                    ┌──────────▼───────────┐
                    │   LLM Query Generator │
                    │  "Generate search     │
                    │   query to resolve    │
                    │   this contradiction" │
                    └──────────┬───────────┘
                               │
                    2. Targeted web search
                               │
                    ┌──────────▼───────────┐
                    │   Web Search / Fetch  │
                    │  Brave API / Tavily   │
                    │  Jina Reader for full │
                    │  article extraction   │
                    └──────────┬───────────┘
                               │
                    3. Extract structured intel
                               │
                    ┌──────────▼───────────┐
                    │   LLM Extractor       │
                    │  "From this article,  │
                    │   extract entities,   │
                    │   relationships,      │
                    │   facts, predictions, │
                    │   source credibility" │
                    └──────────┬───────────┘
                               │
                    4. Fingerprint each fact
                               │
                    ┌──────────▼───────────┐
                    │   PoliticalAdapter    │
                    │   .fingerprint()      │
                    │  Jina + LLM → S/P/O  │
                    │  → CogRecord          │
                    └──────────┬───────────┘
                               │
                    5. Ingest into graph
                               │
                    ┌──────────▼───────────┐
                    │   BindSpace           │
                    │  NARS revision        │
                    │  Contradiction update │
                    │  Spawn check          │
                    │  Crystallization gate │
                    └──────────┬───────────┘
                               │
                    6. Back to top
                               └──→ (loop)
```

### 6.2 Cost Management

LLM calls are expensive. The system needs a cost budget:

```
Per research cycle:
  LLM query generation:    ~500 tokens  (~$0.005)
  Web search:              1 API call   (~$0.005)
  Article fetch:           1-3 articles (~free with Jina Reader)
  LLM extraction:          ~2000 tokens per article (~$0.02 each)
  LLM fingerprinting:      ~1000 tokens if needed (~$0.01)
  
  Total per cycle: ~$0.05-0.10
  
Budget allocation:
  $5/day = ~50-100 research cycles = ~50-100 new facts ingested
  $50/day = 500-1000 cycles = deep investigation capacity
  
  At $5/day for 30 days = $150 total:
    ~1500-3000 facts ingested
    ~100-200 entities discovered
    ~20-50 concepts crystallized
    ~50-100 predictions generated
    ~10-30 predictions verified (depending on time horizons)
```

### 6.3 Railway Deployment

```
Service topology:

holograph-core (Railway):
  - BindSpace + NARS + Blackboard + Crystallization
  - Always running, lean baseline ~512 MB
  - Receives CogRecords from research workers
  - Serves graph queries
  
research-worker (Railway, N instances):
  - One per active research agent
  - Runs the research loop
  - Calls Claude API for extraction + fingerprinting
  - Calls web search APIs
  - Pushes CogRecords to holograph-core
  - Scales: 1 worker for seed, spawn more as entities discovered
  - Each worker: ~256 MB, mostly waiting on API calls
  
dashboard (Railway or Vercel):
  - Web UI showing:
    - Live graph visualization (entity network)
    - Contradiction heat map (what the system is uncertain about)
    - Prediction scoreboard (Brier scores over time)
    - Concept timeline (when concepts crystallized)
    - Agent activity log (what each agent is researching)
    - Alert feed (new edges, sign changes, trajectory shifts)
```

---

## 7. Cross-Pollination with Chess

After both the chess brain plasticity experiment and the political intelligence system have been running:

```
Chess concepts discovered:           ~50 after 100K games
Political concepts discovered:       ~30 after 1000 research cycles

Cross-domain Hamming scan:
  For each chess concept C:
    For each political concept P:
      binding_distance = hamming(C.meta_W32_W63, P.meta_W32_W63)
      
      Low distance → potential structural analog
```

Expected discovery:

```
Chess "sacrifice for initiative" (NARS: 0.82, 0.71)
  S-block: material deficit, active pieces
  P-block: high piece mobility, threats on king
  O-block: high probability of decisive attack
  
  Hamming distance 38 from:

Political "political capital expenditure" (NARS: 0.69, 0.52)
  S-block: resource deficit (spent political capital), active allies
  P-block: high media coverage, pressure on opposition
  O-block: high probability of policy victory

  Both patterns: accept short-term cost for long-term positional dominance.
  The substrate discovered this WITHOUT being told they're analogous.
```

If this cross-domain match validates — if concepts that correlate with advantage in chess have binding signatures close to concepts that correlate with success in politics — that's the paper. The substrate discovered domain-invariant strategic structure through Hamming comparison alone.

---

## 8. Implementation Plan

### 8.1 Phase 1: Scaffold (Week 1)

```
1. PoliticalAdapter implementing DomainAdapter trait
2. LLM fingerprinting pipeline (Jina + Claude API)
3. Web search integration (Brave or Tavily)
4. Fact extraction prompt (tested, cached)
5. Single research agent running the loop
6. Seed with Trump + Tier 1 entities
7. Basic dashboard showing entity count + fact count + graph viz

Deliverable: system ingests articles and builds growing graph.
No predictions yet. No agent spawning. Just the pipeline working.
```

### 8.2 Phase 2: Intelligence (Week 2-3)

```
1. NARS revision on contradictory facts
2. Source credibility tracking
3. Contradiction-driven research targeting
4. Prediction generation from O-block trajectories
5. Agent spawning when entities cross observation threshold
6. Concept crystallization from P-block clustering

Deliverable: system makes predictions and spawns focused agents.
Dashboard shows contradiction heat map and prediction scoreboard.
```

### 8.3 Phase 3: Scoring (Week 4+)

```
1. Prediction verification loop (check if predicted events happened)
2. Brier score tracking and calibration plots
3. Source credibility auto-update from prediction outcomes
4. Concept correlation with prediction accuracy
5. Cross-domain Hamming scan against chess concepts (if chess experiment running)

Deliverable: system measures its own accuracy.
Dashboard shows rolling Brier score, calibration plot, concept timeline.
```

### 8.4 Dependencies

```toml
[dependencies]
ladybug-contract = { path = "../crates/ladybug-contract" }  # substrate
reqwest = "0.12"          # HTTP for APIs
serde_json = "1.0"        # JSON processing
tokio = { version = "1", features = ["full"] }  # async runtime
chrono = "0.4"            # timestamps, prediction verification dates

# LLM
anthropic-sdk = "0.1"     # or raw HTTP to Claude API

# Search
# Brave Search API or Tavily — via reqwest

# Embeddings
# Jina API — via reqwest

# Dashboard
# Axum for API server, or push to Railway static site
```

### 8.5 Seed Research Queries

```
Initial agent queries (generate more via contradiction-driven loop):

"Trump administration appointments 2025 2026"
"Trump executive orders 2025 2026"
"Elon Musk DOGE government efficiency progress"
"Kash Patel FBI director actions"
"Trump legal cases status 2026"
"Trump China tariffs 2026"
"Trump Republican party loyalty dynamics"
"Trump media strategy 2026"
"Trump political allies and opponents network"
"Congressional support for Trump agenda 2026"
```

---

## 9. What "Working" Looks Like

### 9.1 Week 1 Milestone
```
- Graph: 50+ entities, 200+ facts, 100+ edges
- System correctly identifies Tier 1 entities from web search alone
- Fingerprints are consistent (same entity from different articles → low Hamming distance)
```

### 9.2 Week 4 Milestone
```
- Graph: 200+ entities, 2000+ facts, 500+ edges
- 5+ agents running (dynamically spawned)
- 10+ concepts crystallized
- 50+ predictions generated
- First predictions verified
- Brier score: hopefully < 0.25 (better than random)
```

### 9.3 Week 12 Milestone
```
- Graph: 500+ entities, 10000+ facts
- Brier score: < 0.18 (significantly better than random)
- System discovers entity the RESEARCHERS didn't know about
  ("who is this person appearing in 47 facts that we never seeded?")
- System discovers relationship the RESEARCHERS didn't know about
  ("these two entities are connected through X, which nobody told the system")
- Concept crystallization events align with Brier score improvements
```

### 9.4 The Headline Demo

```
"We pointed a Holograph instance at Donald Trump and told it: figure out 
what's going on. Three months later it had mapped 500 political entities, 
discovered 47 structural patterns in political dynamics, predicted 200 
events with 73% accuracy, and found three network connections that 
surprised our political science advisors. It did this using the same 
substrate, same three operations, and same learning loop that separately 
taught itself chess from scratch. The only difference: the fingerprinting 
function."
```

That's not a chess engine. That's not a political analysis tool. That's a substrate for cognition that happens to be pointed at politics right now.

---

## 10. Wikipedia: The Commodity Hardware Benchmark

### 10.1 Why This Matters

Every knowledge graph system that ingests all of Wikipedia needs enterprise infrastructure: GPU clusters for embedding, hundreds of gigabytes of RAM for graph traversal, distributed databases for storage. Neo4j with the full Wikipedia entity graph requires ~500 GB+ RAM. Embedding all articles with OpenAI costs ~$15,000 and requires cluster coordination.

Holograph can ingest all of English Wikipedia on a single machine with commodity hardware. This is the benchmark that makes people pay attention.

### 10.2 The Numbers

```
English Wikipedia:
  6.8M articles
  4.4B words
  ~22 GB compressed (XML dump)
  ~50M cross-references (wikilinks between articles)
  ~30M entity mentions (people, places, organizations, concepts)
```

### 10.3 Storage Model

```
One CogRecord = 4 KB (meta 1 KB + S 1 KB + P 1 KB + O 1 KB)

Entity nodes:  6.8M articles → 6.8M CogRecords = 27 GB
Edge records:  50M wikilinks → 50M CogRecords   = 200 GB
Total on disk: ~227 GB (LanceDB, column-compressed, mmap'd)

A 512 GB NVMe SSD costs $35. The entire Wikipedia knowledge graph 
fits on hardware you buy at Best Buy.
```

### 10.4 The INT4 Sketch Trick

You never load 227 GB into RAM. The three-level search cascade means the hot footprint is tiny:

```
Level 0: Receptors (always in RAM)
  6.8M × 32 bytes = 218 MB
  Contains: DN hash, storage tier, NARS compact, flags
  
Level 1: INT4 sketches (always in RAM, L2/L3 resident)
  6.8M × 64 bytes = 436 MB
  Contains: popcount of each 64-bit segment quantized to 4 bits
  Rejects 90% of candidates before touching any content block

Level 2: Belichtungsmesser (loaded on demand from mmap)
  7 words per surviving candidate (~10% of level 1 survivors)
  
Level 3: Full Hamming (loaded on demand from mmap)
  Only for final candidates (~1% of original)

Total hot footprint: 218 + 436 = 654 MB
That fits on a Raspberry Pi 5 with 8 GB RAM.
```

### 10.5 Query Performance

```
Full-scan query: "Find all entities similar to Donald Trump"

Level 0 sketch scan:
  6.8M sketches × 64 bytes = 435 MB
  AVX2 throughput on desktop CPU: ~40 GB/s
  Scan time: 435 MB / 40 GB/s = ~11 milliseconds
  
  11 milliseconds to search ALL OF ENGLISH WIKIPEDIA.
  
  Rejects ~90%: 680K candidates survive to Level 1

Level 1 belichtungsmesser:
  680K × 56 bytes = 38 MB  (mmap'd, likely in page cache)
  Scan time: ~1 ms
  Rejects ~90%: 68K candidates survive

Level 2 full Hamming:
  68K × 4 KB = 272 MB  (mmap'd, sequential read)
  Scan time: ~7 ms (NVMe sequential read)
  
Total query time: ~20 milliseconds

For comparison:
  Neo4j full-text search over 6.8M nodes: 500ms-5s (with indices)
  Elasticsearch over Wikipedia: 50-200ms (with sharding)
  PostgreSQL full-text over Wikipedia: 1-10s
  
  Holograph: 20ms. On a laptop. No indices. Brute-force scan.
  Because brute-force over INT4 sketches IS the index.
```

### 10.6 Wikipedia Fingerprinting Pipeline

```
Phase 1: Bulk ingest (one-time, ~24-48 hours on single machine)

  For each Wikipedia article:
    1. Parse wikitext → extract:
       - Title, categories, infobox (structured metadata)
       - First paragraph (entity description)
       - Wikilinks (cross-references = edges)
       - Section headings (topic structure)
    
    2. Jina embedding of first paragraph → 1024D float → LSH → [u64; 128]
       Cost: Jina API at ~$0.002 per 1K tokens
       6.8M articles × ~200 tokens avg = 1.36B tokens = ~$2,700
       OR: run local embedding model (e5-large, ~50 articles/sec on CPU)
       6.8M / 50 = 136,000 seconds = ~38 hours (no API cost)
    
    3. S/P/O decomposition (heuristic, no LLM needed for bulk):
       S-block: LSH of entity description (what this IS)
       P-block: LSH of categories + infobox keys (what forces classify it)
       O-block: LSH of "See also" + outgoing links (what it connects to)
    
    4. Create CogRecord, write to LanceDB
    
  For each wikilink:
    Create edge CogRecord: XOR(source.S, target.S) per block
    NARS: confidence proportional to link context quality

Phase 2: Sketch generation (one-time, ~10 minutes)
  For each CogRecord:
    Generate INT4 sketch (popcount per 64-bit segment, quantize to 4 bits)
    Generate receptor (32 bytes: hash, tier, sketch pointer, NARS compact)
  
  Load all receptors + sketches into RAM: 654 MB. Done.

Phase 3: Concept crystallization (continuous, runs after ingest)
  Cluster by S-block Hamming similarity:
    "US Presidents" cluster: Washington through current
    "European Monarchs" cluster: all royals
    "Programming Languages" cluster: Python, Rust, C, ...
    
  These clusters ARE the categories — rediscovered from content similarity,
  not from Wikipedia's category system. Compare discovered clusters against
  Wikipedia categories to measure fingerprint quality.
  
  Clusters that DON'T match Wikipedia categories are interesting:
    "Entities connected to both tech industry AND government intelligence"
    Wikipedia has no such category. The graph found a structural pattern.
```

### 10.7 Wikipedia + Political Intelligence = Live Knowledge Base

```
Wikipedia provides the STATIC BACKGROUND — 6.8M entities with relationships,
fingerprinted and searchable in 20ms.

The PoliticalAdapter provides the LIVE FOREGROUND — new facts, changing 
relationships, evolving predictions, ingested daily.

When the political research agent discovers "Kash Patel":
  1. Hamming scan Wikipedia in 20ms → find Kash Patel article
  2. Load full CogRecord from LanceDB → immediate context
  3. All Wikipedia cross-references → known relationship graph
  4. Live research adds: current role, recent actions, trajectory
  5. NARS merges: Wikipedia background (high confidence, possibly stale)
                   + live research (lower confidence, current)

The system has the institutional memory of Wikipedia 
and the situational awareness of live research.

When it discovers the Epstein network:
  Every entity has a Wikipedia article with decades of publicly documented history.
  The system doesn't start from zero — it starts from the accumulated 
  knowledge of millions of Wikipedia editors, fingerprinted and 
  Hamming-searchable in 20ms on a laptop.

When it needs to answer: "Who else is connected to both Deutsche Bank 
  AND the Royal Family AND US politics?"
  
  Three Hamming scans: 
    Similar to Deutsche Bank S-block: ~20ms → 500 candidates
    Filter by Royal Family P-block proximity: ~1ms → 30 candidates  
    Filter by US politics O-block proximity: ~0.5ms → 3-7 entities
  
  Total: ~22ms. On a laptop. Over all of Wikipedia.
  Then live research agents verify whether those connections are still active.
```

### 10.8 The Benchmark Claim

```
System                    | Wikipedia Full Ingest | Query Latency | Hardware Required
--------------------------|----------------------|---------------|------------------
Neo4j + embeddings        | ~$15K + cluster      | 500ms-5s      | 512 GB RAM server
Elasticsearch             | ~$5K + sharding      | 50-200ms      | Multi-node cluster
PostgreSQL + pgvector     | ~$3K + tuning        | 200ms-2s      | 128 GB RAM server
Pinecone / Weaviate       | ~$500/month ongoing  | 50-100ms      | Cloud managed
ChromaDB (local)          | hours, RAM limited   | 100-500ms     | 64 GB RAM machine
Holograph                 | ~$2.7K or free*      | ~20ms         | Laptop + 512 GB SSD

* Free if using local embedding model instead of Jina API
  38 hours on CPU, zero API cost
  
The claim: First system to make all of English Wikipedia Hamming-searchable 
in <25ms on commodity hardware with <1 GB RAM hot footprint.
```

This is the benchmark that makes the architecture legit. Chess proves learning. Political intelligence proves generalization. Wikipedia proves scale. All three on the same substrate, same three operations, same commodity hardware.

---

## 11. Ethical Constraints

```
HARD RULES:
1. System does NOT generate disinformation
2. System does NOT target individuals for harassment
3. System does NOT make recommendations about voting or political action
4. System ONLY analyzes publicly available information
5. All predictions are probabilistic and clearly marked as machine-generated
6. Source credibility scoring does NOT constitute "truth" determination
7. Dashboard is for research/analysis, not for political campaigns
8. System never fabricates facts — all facts traced to source URLs

The system is a MIRROR of publicly available political dynamics.
It discovers structure. It makes predictions. It measures accuracy.
It does NOT prescribe action or determine truth.
```
