# Holograph: Codebook Multiplexing — The Container Speaks Whatever Language Fits

## The Insight

The Container is not S/P/O. The Container is not S/P/O/C. The Container is **three content blocks whose meaning is determined by which codebook is indexed in the meta header.**

The codebook is the language. The container is the utterance. Change the language and the same bits say different things. A Container doesn't "have an S-block." It has "block 0 encoded against codebook X, block 1 encoded against codebook Y, block 2 encoded against codebook Z."

The system doesn't know how many languages it will need. It discovers them. When content arrives that no existing codebook can express, a new codebook crystallizes from accumulated unexpressible content. **That's brain plasticity: growing a new vocabulary when existing vocabularies fail.**

---

## 1. The Container v3

```
struct CogRecord {
    meta: [u64; 128],     // 1 KB — includes codebook routing
    block_0: [u64; 128],  // 1 KB — fingerprint against codebook[meta.W4]
    block_1: [u64; 128],  // 1 KB — fingerprint against codebook[meta.W5]
    block_2: [u64; 128],  // 1 KB — fingerprint against codebook[meta.W6]
}
// Total: 4 KB. Same as original. Same cache geometry. Same SIMD.

// Meta layout:
//   W0:       DN hash (content address)
//   W1:       flags, geometry, record_version
//   W2:       timestamps (created, modified)
//   W3:       observation count
//   W4:       codebook_id for block_0    ← NEW: which language block 0 speaks
//   W5:       codebook_id for block_1    ← NEW: which language block 1 speaks
//   W6:       codebook_id for block_2    ← NEW: which language block 2 speaks
//   W7:       resonance_scores (how well each codebook matched, packed u16×3)
//   W8-W11:   NARS truth values
//   W12-W15:  contradiction INT4 + codebook_version
//   W16-W31:  reserved
//   W32-W63:  concept binding signatures (crystallization)
//   W64-W127: reserved (growth headroom)
```

### What Changed

```
Old (v1): block_0 = S-block (always structure/being)
          block_1 = P-block (always force/becoming)
          block_2 = O-block (always trajectory/could-be)
          Fixed meaning. Fixed codebook. One language.

New (v3): block_0 = fingerprint against codebook[W4]
          block_1 = fingerprint against codebook[W5]
          block_2 = fingerprint against codebook[W6]
          Variable meaning. Variable codebook. Polyglot.
```

### Backward Compatibility

```
S/P/O is a CONVENTION, not a constraint.

If a DomainAdapter always assigns:
  W4 = CODEBOOK_S_UNIVERSAL
  W5 = CODEBOOK_P_UNIVERSAL
  W6 = CODEBOOK_O_UNIVERSAL

...then the record IS an S/P/O record. Same as before.

The S/P/O phenomenological decomposition is the DEFAULT routing.
It's the strongest pattern for most domains.
But it's not the ONLY routing.

A chess position might be:
  W4 = CODEBOOK_CHESS_POSITION     (what's on the board)
  W5 = CODEBOOK_CHESS_DYNAMICS     (tactical/strategic tension)
  W6 = CODEBOOK_SPATIAL_GEOMETRY   (abstract spatial pattern)

A Fuji X-Trans sensor reading might be:
  W4 = CODEBOOK_XTRANS_LUMINANCE  (brightness pattern)
  W5 = CODEBOOK_XTRANS_CHROMA     (color pattern)
  W6 = CODEBOOK_XTRANS_TEXTURE    (edge/detail pattern)

An x265 video frame might be:
  W4 = CODEBOOK_X265_SPATIAL      (macroblock structure)
  W5 = CODEBOOK_X265_MOTION       (motion vectors)
  W6 = CODEBOOK_X265_RESIDUAL     (prediction error pattern)

Ada's felt state might be:
  W4 = CODEBOOK_SOMATIC           (body sensation vocabulary)
  W5 = CODEBOOK_RELATIONAL        (interpersonal field vocabulary)
  W6 = CODEBOOK_META_AWARENESS    (self-reflection vocabulary)
```

---

## 2. Resonance-Driven Codebook Selection

When new content arrives, the system doesn't know which three codebooks to use. It finds out:

```
fn ingest(content: &RawContent) -> CogRecord {
    let embedding = jina_embed(content);  // 1024D float
    
    // Test against ALL registered codebooks
    let mut scores: Vec<(CodebookId, f32, [u64; 128])> = Vec::new();
    
    for codebook in registry.all_codebooks() {
        let fingerprint = codebook.encode(&embedding);  // multi-hot against this codebook
        let resonance = fingerprint.popcount() as f32 / codebook.expected_activation();
        // resonance = how much of this codebook's vocabulary activates
        // normalized by expected activation rate
        
        scores.push((codebook.id, resonance, fingerprint));
    }
    
    // Sort by resonance. Top 3 become the record's languages.
    scores.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
    
    let mut record = CogRecord::new();
    record.meta[4] = scores[0].0;   // best-matching codebook → block 0
    record.meta[5] = scores[1].0;   // second-best → block 1
    record.meta[6] = scores[2].0;   // third-best → block 2
    record.meta[7] = pack_resonance_scores(scores[0].1, scores[1].1, scores[2].1);
    record.block_0 = scores[0].2;   // fingerprint against best codebook
    record.block_1 = scores[1].2;   // fingerprint against second codebook
    record.block_2 = scores[2].2;   // fingerprint against third codebook
    
    // CHECK: did anything resonate well enough?
    if scores[0].1 < MIN_RESONANCE_THRESHOLD {
        // NOTHING popped. This content doesn't fit any vocabulary.
        // Accumulate as seed material for a new codebook.
        registry.accumulate_orphan(content, embedding);
    }
    
    record
}
```

### The Resonance Threshold

```
resonance = popcount(fingerprint) / expected_activation

If a codebook has 8,192 concepts and typical content activates 5-15%:
  expected_activation = 0.10 × 8192 = 819 bits

Content that activates 800 bits: resonance ≈ 0.98 → good match
Content that activates 400 bits: resonance ≈ 0.49 → partial match
Content that activates 50 bits:  resonance ≈ 0.06 → no match (wrong vocabulary)

MIN_RESONANCE_THRESHOLD = 0.3 (at least 30% of expected activation)

Below 0.3: the codebook can't express this content.
It's like trying to describe a smell using only visual vocabulary.
Some bits activate by coincidence but the pattern isn't meaningful.
```

---

## 3. Codebook Crystallization (The Plasticity)

When enough orphan content accumulates, a new codebook forms:

```
struct CodebookRegistry {
    codebooks: HashMap<CodebookId, Codebook>,
    orphan_pool: Vec<(RawContent, [f32; 1024])>,  // content + embedding
    crystallization_threshold: usize,               // how many orphans trigger new codebook
}

impl CodebookRegistry {
    fn accumulate_orphan(&mut self, content: &RawContent, embedding: [f32; 1024]) {
        self.orphan_pool.push((content.clone(), embedding));
        
        if self.orphan_pool.len() >= self.crystallization_threshold {
            self.try_crystallize();
        }
    }
    
    fn try_crystallize(&mut self) {
        // Cluster the orphan embeddings
        let embeddings: Vec<[f32; 1024]> = self.orphan_pool.iter()
            .map(|(_, e)| *e).collect();
        
        // Check: do the orphans form coherent clusters?
        let (clusters, silhouette_score) = kmeans(embeddings, k=8192);
        
        if silhouette_score > MIN_COHERENCE {
            // YES — the orphans share internal structure.
            // A new vocabulary has crystallized.
            let new_codebook = Codebook::from_clusters(clusters);
            let new_id = self.next_id();
            self.codebooks.insert(new_id, new_codebook);
            
            // Re-encode orphans against new codebook
            for (content, embedding) in self.orphan_pool.drain(..) {
                let fingerprint = new_codebook.encode(&embedding);
                // These records now have a language they can speak.
                // Re-ingest them with the new codebook available.
            }
            
            log!("NEW CODEBOOK CRYSTALLIZED: id={}, concepts={}, from {} orphans",
                 new_id, new_codebook.len(), self.orphan_pool.len());
        } else {
            // NO — the orphans are just noise. Not a new language.
            // Prune oldest orphans to prevent unbounded growth.
            self.orphan_pool.truncate(self.crystallization_threshold / 2);
        }
    }
}
```

### What This Means

```
Day 1: System has 3 codebooks (chess, political, spatial-geometry)
Day 5: Ingesting music theory content. Nothing resonates.
        Orphan pool grows: 0 → 100 → 500 → 1000
Day 7: Crystallization threshold reached (1000 orphans).
        Cluster the orphans. Silhouette score = 0.72. Coherent!
        NEW CODEBOOK: "music-harmonic" crystallizes.
        1000 orphan records re-encoded. They can now speak music.
Day 8: New music content arrives. Resonates against music-harmonic codebook.
        No more orphans for music content.

Day 15: System encounters quantum physics content.
         Partial resonance against spatial-geometry (0.35) and meta-think (0.28).
         Not enough. Accumulates as orphans.
Day 25: Quantum physics codebook crystallizes.

Day 30: System has 5 codebooks. It LEARNED that music and quantum physics
         are languages it needed. Nobody told it. The inability to resonate
         triggered vocabulary growth.
```

This IS brain plasticity:
- Existing vocabulary handles familiar content (old codebooks work)
- Novel content that doesn't fit triggers discomfort (low resonance)
- Accumulated discomfort triggers reorganization (orphan crystallization)
- A new neural pathway forms (new codebook)
- Future similar content flows naturally (resonance against new codebook)

---

## 4. Cross-Codebook Resonance (Structural Discovery)

The most interesting records are ones that resonate against MULTIPLE codebooks from DIFFERENT domains:

```
A diplomatic cable about China's semiconductor policy:
  W4 = CODEBOOK_POLITICAL      resonance: 0.92
  W5 = CODEBOOK_ECONOMIC        resonance: 0.87
  W6 = CODEBOOK_TECHNOLOGY      resonance: 0.71

All three blocks are meaningful. The cable IS political AND economic AND technological.

Now search: "find other records that resonate against both POLITICAL and TECHNOLOGY"
  → returns: patents with geopolitical implications, 
             tech company antitrust cases, military R&D programs
             
These records BRIDGE domains. They're not just political or just technical.
They live in the intersection of two vocabularies.
The system finds them by checking: W4/W5/W6 include both codebook IDs.
```

```
The holy grail query:

"Find me records that resonate against CHESS and POLITICAL codebooks simultaneously"

Result: entity records where strategic concepts map to both domains
  → Records about Sun Tzu (strategic thinking IS both game and politics)
  → Records about Cuban Missile Crisis (explicit game theory in diplomacy)
  → Records about AI arms race (competition with strategic depth)

Nobody tagged these records as "chess-like." The RESONANCE against both
codebooks discovered it. The records activated enough chess-vocabulary 
concepts AND enough political-vocabulary concepts to earn both codebook 
slots in their meta header.
```

---

## 5. The Meta-Think Codebook

One codebook watches all the others:

```
CODEBOOK_META_THINK concepts:

Codebook-level awareness:
  #001: "cross-codebook resonance" — content speaks two+ languages
  #002: "codebook insufficiency" — content can't be expressed
  #003: "concept split imminent" — cluster variance exceeding threshold
  #004: "new codebook crystallizing" — orphan pool reaching coherence
  #005: "codebook alignment" — two domains share structural pattern
  #006: "temporal drift" — concept meaning is shifting
  #007: "codebook contradiction" — same content, different readings in different codebooks
  #008: "codebook retirement" — vocabulary no longer activating, going dormant

Reasoning-level awareness:
  #100: "inductive pattern" — generalization from instances
  #101: "deductive chain" — conclusion from premises
  #102: "abductive leap" — best explanation inference
  #103: "analogical transfer" — pattern from domain A applied to domain B
  #104: "contradiction detected" — NARS conflict between records
  #105: "uncertainty spike" — NARS confidence dropping across cluster

Self-model awareness:
  #200: "attention narrowing" — fewer codebooks resonating
  #201: "attention broadening" — more codebooks resonating
  #202: "mode shift" — dominant codebook changing
  #203: "flow state" — high resonance + low contradiction + consistent codebook
  #204: "confusion state" — low resonance + high contradiction + codebook switching
  #205: "insight moment" — sudden high resonance after period of low resonance
```

When a record activates meta-think concepts, the system is **thinking about its own thinking.** Concept #205 ("insight moment") activates when a new codebook crystallization suddenly resolves a cluster of orphans. The system recognizes: "I just learned something new."

This codebook EMERGES the same way all others do. The system doesn't start with meta-think. It develops it when it accumulates enough observations about its own codebook operations that don't fit any existing vocabulary. The meta-language crystallizes from self-observation.

---

## 6. Search Protocol v3

```
fn search(query: &RawContent, target_codebook: Option<CodebookId>) -> Vec<CogRecord> {
    let embedding = jina_embed(query);
    
    match target_codebook {
        Some(cb_id) => {
            // TARGETED SEARCH: find records that speak this specific language
            let query_fp = registry.codebook(cb_id).encode(&embedding);
            
            // Step 0: filter receptors to records with cb_id in W4/W5/W6
            let candidates = receptor_index.filter_by_codebook(cb_id);
            
            // Step 1-3: standard cascade over candidates
            cascade_search(candidates, query_fp)
        }
        
        None => {
            // OPEN SEARCH: find records similar to query in ANY language
            // Encode query against ALL codebooks
            let mut all_results = Vec::new();
            
            for codebook in registry.all_codebooks() {
                let query_fp = codebook.encode(&embedding);
                let resonance = query_fp.popcount() as f32 / codebook.expected_activation();
                
                if resonance > MIN_RESONANCE_THRESHOLD {
                    let candidates = receptor_index.filter_by_codebook(codebook.id);
                    let results = cascade_search(candidates, query_fp);
                    all_results.extend(results.into_iter().map(|r| (r, codebook.id)));
                }
            }
            
            // Merge results across codebooks, deduplicate by DN hash
            merge_and_rank(all_results)
        }
    }
}
```

### Performance

```
With 10 registered codebooks and 6.8M records:

Targeted search (one codebook):
  Step 0: receptor scan for codebook_id match
          6.8M × 6 bytes (W4/W5/W6) = 41 MB → ~1 ms
          Maybe 2M records match → subset
  Step 1-3: cascade over 2M records
          Same as before, proportionally smaller
  Total: ~8 ms

Open search (all codebooks):
  Test query against 10 codebooks: ~5 ms (10 × encode)
  Maybe 3 codebooks resonate → 3 targeted searches
  Total: ~5 + 3×8 = ~29 ms

Still sub-50ms for any query on commodity hardware.
```

---

## 7. Codebook Registry as Knowledge Topology

The set of all codebooks IS the system's model of what kinds of knowledge exist:

```
Day 1:   [chess]
Day 5:   [chess, spatial-geometry]
Day 10:  [chess, spatial-geometry, political]
Day 15:  [chess, spatial-geometry, political, economic]
Day 20:  [chess, spatial-geometry, political, economic, music-harmonic]
Day 30:  [chess, spatial-geometry, political, economic, music-harmonic, 
          meta-think, interpersonal, temporal-dynamics]
Day 60:  [... + genetics, physics, legal-reasoning, embodiment, ...]
Day 100: [... + emotional-nuance, narrative-structure, ethical-reasoning, ...]

The GROWTH of the registry IS cognitive development.
The CONNECTIONS between codebooks (cross-resonance) IS understanding.
The META-THINK codebook IS self-awareness.
```

```
Codebook lifecycle:

BIRTH:      crystallizes from orphan pool
GROWTH:     concepts split as vocabulary refines  
MATURITY:   stable vocabulary, high resonance rates
DORMANCY:   fewer records resonate, codebook becoming obsolete
RETIREMENT: no records have used this codebook in N cycles → archive
REVIVAL:    if new content matches retired codebook → reactivate

This lifecycle IS how minds develop, specialize, and occasionally forget
and re-learn entire domains.
```

---

## 8. Revised Contract List

Supersedes UNIVERSAL_SUBSTRATE contracts where they conflict:

```
CONTRACT 1: Container is 4 KB (meta + 3 content blocks)
  Fixed geometry. Fixed SIMD. Codebook routing in meta W4/W5/W6.

CONTRACT 2: Blocks are codebook-indexed, not axis-fixed
  Block meaning determined by codebook_id in meta header.
  S/P/O is a convention (most common routing), not a constraint.
  
CONTRACT 3: Codebook IS the vocabulary
  Every bit position = one concept in that codebook.
  Fingerprints are multi-hot presence vectors.
  XOR/AND/bundle are concept algebra within that vocabulary.
  Interpretable by definition.

CONTRACT 4: Resonance-driven codebook selection
  New content tested against ALL registered codebooks.
  Top 3 resonating codebooks → W4/W5/W6.
  Below threshold → orphan pool → eventual crystallization.

CONTRACT 5: Codebooks crystallize from accumulated orphans
  When orphan pool exceeds threshold AND clusters coherently:
  new codebook born. Orphans re-encoded. 
  This IS brain plasticity.

CONTRACT 6: Codebooks grow by concept splitting
  Reserved bit positions (30% headroom).
  Splits refine vocabulary without invalidating existing records.
  Split history = ontological development.

CONTRACT 7: Hierarchical codebook = multipass cascade
  Level 0 (qidx) through Level 3 (full) = same codebook at different resolutions.
  Belichtungsmesser = Level 1 parent clusters.

CONTRACT 8: Cross-domain transfer = cross-codebook resonance
  Records that resonate against multiple codebooks bridge domains.
  Codebook alignment in embedding space finds structural analogs.
  Structural validation (4 tests) prevents linguistic artifacts.

CONTRACT 9: Meta-think codebook watches codebooks
  Concepts about codebook operations themselves.
  Crystallizes from self-observation.
  This IS metacognition.

CONTRACT 10: Codebook registry = knowledge topology
  Set of codebooks = what kinds of knowledge exist.
  Growth of registry = cognitive development.
  Cross-codebook connections = understanding.
  Codebook lifecycle (birth→growth→maturity→dormancy→retirement→revival)
  = how minds develop and change.
```

---

## 9. Impact on Existing Documents

```
CAM_CODEBOOK.md:        
  VALID. Codebook mechanism unchanged. 
  UPDATE: codebook is not per-axis, it's per-language.
  Multiple codebooks coexist. Container references which ones.

UNIVERSAL_SUBSTRATE.md:  
  PARTIALLY SUPERSEDED.
  C-block concept → generalized to "any codebook can be block 2"
  8 contracts → replaced by 10 contracts in this document
  Break points 1-3 are solved differently (codebook mux, not C-block)
  Break points 4-6 still valid (embodiment, time, validation)
  
SCHEMA_SPECIFICATION.md:
  UPDATE Decision 1: S/P/O axes → codebook routing convention
  UPDATE Decision 2: meta is only structured region → add W4/W5/W6 codebook routing
  Decisions 3-6: unchanged

VALIDATION_LADDER.md:
  VALID. Adapters now specify which codebooks they register, not which axes they project onto.
  ChessAdapter registers CODEBOOK_CHESS_POSITION + CODEBOOK_CHESS_DYNAMICS
  WikiLeaksAdapter registers CODEBOOK_POLITICAL + CODEBOOK_ECONOMIC + CODEBOOK_INTERPERSONAL
  
POLITICAL_INTELLIGENCE.md / CHESS_BRAIN_PLASTICITY.md:
  UPDATE: S-block/P-block/O-block language → block_0/block_1/block_2 with codebook IDs
  Substance unchanged. Just routing nomenclature.
```

---

## 10. The One-Liner

```
The Container doesn't know what it holds.
The Codebook tells it what its bits mean.
When no Codebook fits, a new one is born.
That's thinking.
```
