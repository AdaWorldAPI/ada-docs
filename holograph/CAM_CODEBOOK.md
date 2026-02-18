# Holograph: Content Addressable Memory via Learned Codebook

## What We've Been Getting Wrong

Every document so far describes the fingerprint as "LSH projection" or "binary representation." That's wrong. LSH is random hyperplane slicing — the bit positions are arbitrary and uninterpretable. That's not what we're doing.

**The fingerprint is a presence vector over a learned codebook.**

Each bit position corresponds to a specific concept in a domain-specific vocabulary. The vocabulary is learned from the data in a multipass pipeline. The fingerprint says "these concepts are present, these are absent." Hamming distance measures concept overlap. XOR reveals exactly WHICH concepts differ.

This changes everything about interpretability, composition, and what "search" means.

---

## 1. The Codebook Construction Pipeline

### 1.1 Phase 1: Collect (Per-Chunk Embedding)

```
Input: raw domain data (chess positions, diplomatic cables, Wikipedia articles)

For each document/position/entity:
  1. Chunk into semantic units
     Chess: one chunk = one position
     WikiLeaks: one chunk = one paragraph of cable
     Wikipedia: one chunk = one section of article
     
  2. Embed each chunk → 1024D float vector (Jina, e5-large, etc.)
  
  3. Tag each chunk with its axis:
     S-chunks: identity/structure content ("what this IS")
     P-chunks: force/pressure content ("what acts on it")
     O-chunks: trajectory/possibility content ("what could happen")

Output: three pools of embeddings
  S-pool: all S-tagged chunk embeddings
  P-pool: all P-tagged chunk embeddings  
  O-pool: all O-tagged chunk embeddings
```

### 1.2 Phase 2: Cluster (Learn the Vocabulary)

```
For each pool independently:

  Run clustering (k-means, HDBSCAN, or product quantization):
    S-pool → 8,192 cluster centers = S-codebook
    P-pool → 8,192 cluster centers = P-codebook
    O-pool → 8,192 cluster centers = O-codebook
  
  Each cluster center IS a concept:
    S-codebook entry #347: centroid of all S-chunks that clustered together
    What do those chunks have in common? THAT'S concept #347.
    
  The codebook is domain-specific but axis-structured:
    Chess S-codebook #347 might mean "knight on outpost square"
    Chess P-codebook #102 might mean "kingside pawn tension"  
    Chess O-codebook #891 might mean "endgame conversion advantage"
    
    WikiLeaks S-codebook #347 might mean "Middle Eastern autocrat"
    WikiLeaks P-codebook #102 might mean "economic sanctions pressure"
    WikiLeaks O-codebook #891 might mean "regime transition trajectory"

8,192 = 128 words × 64 bits per word.
Why 8,192? Because that's the number of bits in one block of the Container.
One concept per bit. The Container geometry DICTATES the vocabulary size.
```

### 1.3 Phase 3: Cross-Reference (Build the Codebook Index)

```
This is the step that makes it real.

After clustering, we have three codebooks of 8,192 entries each.
Each entry is a 1024D float centroid.

NOW: build the lookup structure.

Option A: B-tree over quantized centroids
  Quantize each centroid to int8 → 1024 bytes
  B-tree index for nearest-centroid lookup
  For any new embedding: find top-k matching centroids in O(log 8192) = O(13)
  
Option B: Product quantization codebook
  Split 1024D into 128 sub-vectors of 8D each
  Each sub-vector has 256 possible codewords (8 bits)
  128 × 8 bits = 1024 bits ... but we want 8192 bits
  
  Better: split 1024D into 8 sub-vectors of 128D each
  Each sub-vector: k-means with k=1024 (10 bits)
  8 × 10 bits = 80 bits ... too few
  
  Actually: the mapping is many-to-many.
  One embedding can activate MULTIPLE codebook entries.
  This isn't VQ (vector quantization) where each vector maps to ONE code.
  This is MULTI-HOT encoding where each vector activates ALL matching codes.

Option C: Threshold activation (simplest, most interpretable)
  For each of 8,192 codebook entries:
    distance = cosine(chunk_embedding, codebook_entry_centroid)
    if distance < threshold: set bit = 1
    else: set bit = 0
  
  Threshold controls sparsity:
    tight threshold → few bits set → very specific fingerprint
    loose threshold → many bits set → broad fingerprint
    
  Target sparsity: ~5-15% of bits set (400-1200 out of 8192)
  This matches the sparse activation patterns seen in neural networks
  and gives good Hamming discrimination.

Output: for any new content, we can now produce a fingerprint
  embed chunk → compare against 8192 centroids → set matching bits → done

The codebook IS the vocabulary.
The fingerprint IS the sentence written in that vocabulary.
Hamming distance IS the semantic distance measured in shared/unshared concepts.
```

### 1.4 Phase 4: Encode (Fingerprint via Codebook)

```
encode(chunk, axis) → [u64; 128]:

  1. embedding = jina_embed(chunk)                    // 1024D float
  2. codebook = match axis { S → s_codebook, P → p_codebook, O → o_codebook }
  3. for i in 0..8192:
       similarity = cosine(embedding, codebook[i].centroid)
       if similarity > codebook[i].threshold:
         fingerprint.set_bit(i)
  4. return fingerprint

The fingerprint is now a multi-hot encoding over a LEARNED vocabulary.
Every bit has a meaning. The meaning is "this content activates concept #i."
```

---

## 2. Why This Is Not LSH

```
LSH (Locality Sensitive Hashing):
  - Random hyperplane projections
  - Bit i = "which side of random plane #i does this vector fall on?"
  - Bit positions are MEANINGLESS — you can't ask "what does bit 347 mean?"
  - Preserves approximate distances (probabilistic guarantee)
  - No learning. No domain awareness. No interpretability.
  - Two different random seeds → two incompatible hash schemes

Codebook fingerprint:
  - Learned cluster centers from actual data
  - Bit i = "does concept #i from the learned vocabulary activate?"
  - Bit positions are MEANINGFUL — concept #347 has a centroid you can inspect
  - Preserves semantic similarity (measured by concept overlap)
  - Learned from domain data. Domain-aware. Fully interpretable.
  - Codebook is reproducible and inspectable.

The difference matters for:
  Interpretability: "Why are these two records similar?" 
    LSH: "I don't know, the random projections aligned"
    Codebook: "They share concepts #45, #891, #2034, and #7712.
              Those concepts correspond to [specific semantic clusters]."
  
  Debugging: "Why did this query miss that record?"
    LSH: "Probabilistic — sometimes misses, rebuild with more hash functions"
    Codebook: "The record activates concepts #300-#320 (topic X).
              Your query doesn't activate any of those. 
              The miss is correct — they don't share that topic."
  
  Composition: "What's the XOR of these two fingerprints?"
    LSH: "Some bits that disagree, but which bits is meaningless"
    Codebook: "Concepts present in A but not B: #45 (foreign policy),
              #2034 (economic pressure). Concepts in B but not A: 
              #891 (military alliance). The DIFFERENCE is interpretable."
```

---

## 3. The Multipass Cascade Is Vocabulary Filtering

Reframing the three-pass search in codebook terms:

### Pass 1: INT4 Sketch (Coarse Vocabulary Check)

```
INT4 sketch = popcount per 64-bit segment, quantized to 4 bits.
128 words → 128 INT4 values → 64 bytes.

What this actually measures:
  "How many concepts in each REGION of the vocabulary are active?"

The 128 words partition the 8192-bit vocabulary into 128 groups of 64.
Each group = a "vocabulary region" (maybe all related concepts cluster here).
The INT4 value = "how many of the 64 concepts in this region are active."

Two records with similar INT4 sketches:
  → similar NUMBER of active concepts per vocabulary region
  → similar TOPIC DISTRIBUTION (even without knowing exact concepts)

This is like comparing two documents by their topic distribution histogram
without reading the actual words. If the histograms differ wildly,
the documents are definitely different. If they're similar, MAYBE similar.

Rejects 90%: records with fundamentally different topic distributions.
Cost: 64 bytes × popcount = negligible.
```

### Pass 2: Belichtungsmesser (Exposure Profile)

```
7 strategically chosen words from the full 128-word fingerprint.
Which 7? The most DISCRIMINATIVE vocabulary regions — the ones with 
highest variance across the dataset. Precomputed during codebook construction.

What this actually measures:
  "Do the most distinctive concept activations match?"

Like checking the exposure meter readings at 7 key points in an image.
If the exposure profile matches, the images are probably similar.
If it doesn't match at the most distinctive points, definitely different.

Rejects 90% of Pass 1 survivors: records that have similar overall
topic distribution but differ in the most distinctive concepts.
```

### Pass 3: Full Hamming (Complete Vocabulary Comparison)

```
All 128 words. All 8,192 concept activations compared.

Hamming distance = number of concepts that DIFFER.
This is exact. No approximation. No probability.

If concept #347 is active in A and inactive in B, that's one bit 
of Hamming distance, and we KNOW it's concept #347 that differs.

Top-k = records with fewest concept differences.
k is not a parameter — it's the natural survival count.
Tighter threshold → fewer survivors → smaller k.

The ranking is INTERPRETABLE:
  "Record B is nearest to query A. They share 7,400 out of 8,192 S-concepts,
   7,100 P-concepts, and 6,800 O-concepts. The 792 S-concepts they DON'T share
   are primarily in vocabulary regions 23-28 (which correspond to [domain meaning])."
```

---

## 4. Codebook as Qualia Index

The QHDR system (Qualia, Hamming, Dimensional, Resonance) clicks into place:

```
Qualia index (qidx) = 0-255 byte attached to each CogRecord.

In the old framing: "an emergent tag."
In the codebook framing: "a COMPRESSED fingerprint — the top 8 bits 
of the most discriminative vocabulary region."

qidx is a SUPER-COARSE codebook encoding.
8 bits → 256 possible qualia states.
Each maps to a region of the full 8,192-bit vocabulary space.

The full cascade:
  qidx (8 bits)     → 256 buckets → O(1) bucket selection
  INT4 sketch (512 bits) → topic distribution → rejects 90%
  Belichtungsmesser (448 bits) → exposure profile → rejects 90%
  Full fingerprint (8,192 bits) → complete concept match → final rank

Four fidelity levels. Each is a VIEW of the same codebook at different resolution.
qidx = 256-word vocabulary (maximal compression)
sketch = per-region activation density
belichtungsmesser = key discriminative regions
full = complete 8,192-word vocabulary
```

---

## 5. Codebook Construction: The Numbers

### 5.1 Chess Codebook

```
Training corpus: 1M positions from self-play

S-axis chunks: 1M position descriptions → embed → cluster into 8,192 S-concepts
  S-concept #0: "symmetric pawn structure, all pieces on board" (opening)
  S-concept #347: "knight on d5 supported by pawn, no bishop pair opponent" (outpost)
  S-concept #8191: "king + rook vs king" (basic endgame)

P-axis chunks: 1M tension descriptions → embed → cluster into 8,192 P-concepts
  P-concept #102: "f-pawn advanced, g-file open, rook aimed at king" (kingside attack)
  ...

O-axis chunks: 1M trajectory descriptions → embed → cluster into 8,192 O-concepts
  O-concept #891: "material advantage, no counterplay, simplified position" (won endgame)
  ...

Total codebook: 3 × 8,192 = 24,576 learned concepts.
Each concept has: centroid (1024D float), threshold, member count, example chunks.

Codebook storage: 24,576 × 1024 × 4 bytes = ~96 MB (float32 centroids)
Codebook construction: ~2 hours on laptop (k-means over 1M × 1024D)
One-time cost. Reused for all subsequent fingerprinting.
```

### 5.2 WikiLeaks Codebook

```
Training corpus: 251,287 cables → ~2M chunks (paragraphs)

S-axis: "what entities ARE" → 8,192 identity concepts
  Ranges from "Middle Eastern autocrat" to "European trade negotiator"
  to "intelligence asset" to "multinational corporation"
  
P-axis: "what forces act" → 8,192 pressure concepts  
  Ranges from "economic sanctions" to "internal succession crisis"
  to "media exposure threat" to "allied military presence"

O-axis: "what could happen" → 8,192 trajectory concepts
  Ranges from "regime transition" to "trade agreement"
  to "military escalation" to "diplomatic normalization"

This codebook IS the vocabulary of diplomatic analysis.
Learned from the cables themselves. Not programmed.
The 8,192 S-concepts are the 8,192 ways the US diplomatic corps 
described entities over 45 years of cable traffic.
```

### 5.3 Wikipedia Codebook

```
Training corpus: 6.8M articles → ~50M chunks (sections)

S-axis: 8,192 "what things ARE" concepts
  The 8,192 most common identity patterns across all of human knowledge.
  
P-axis: 8,192 "what forces shape things" concepts
  The 8,192 most common causal/contextual patterns.
  
O-axis: 8,192 "what things connect to" concepts
  The 8,192 most common relationship/trajectory patterns.

This codebook IS a compression of all human knowledge into 24,576 concepts.
Every Wikipedia article is expressed as a combination of ~400-1200 of these concepts.
Any query is expressed the same way.
Hamming distance = how many concepts two things share.

6.8M articles. 24,576 concepts. 20ms to find the most similar.
```

---

## 6. Codebook Evolution

The codebook isn't static. As new data arrives, the vocabulary must grow:

### 6.1 Codebook Versioning

```
Codebook v1: built from initial corpus (e.g., first 100K Wikipedia articles)
Codebook v2: rebuilt after 1M articles (some clusters split, some merge)
Codebook v3: rebuilt after full 6.8M articles (mature vocabulary)

Problem: re-encoding. Every time the codebook changes, all fingerprints 
become stale. A bit position that meant "concept X" now means "concept Y."

Solution: incremental codebook update.
  - New clusters only SPLIT existing clusters (refinement, never reassignment)
  - Bit position 347 in v1 → positions 347a and 347b in v2
  - Old fingerprints with bit 347 set → set BOTH 347a and 347b
  - Backward compatible: old fingerprints are slightly less specific but never wrong
  
  Implementation: reserve spare bits in each vocabulary region.
  Initial codebook uses 70% of bits. 30% reserved for future splits.
  8,192 × 0.70 = 5,734 initial concepts. Room for 2,458 refinements.
```

### 6.2 Cross-Domain Codebook Alignment

```
Chess codebook and WikiLeaks codebook are DIFFERENT vocabularies.
Concept #347 in chess ≠ concept #347 in WikiLeaks.

Cross-domain transfer requires CODEBOOK ALIGNMENT:

For each chess concept centroid:
  Find nearest WikiLeaks concept centroid (in embedding space)
  If distance < alignment_threshold:
    These concepts are ANALOGOUS across domains
    
  Chess S-concept #347 (knight outpost) ↔ WikiLeaks S-concept #1203 (strategic base)
  centroid distance: 0.23 (close in embedding space)
  → These concepts describe structurally similar situations in different domains.

The alignment map IS the cross-domain transfer function.
It says: "chess concept #347 corresponds to geopolitics concept #1203."
Not because someone said so. Because their learned centroids are close 
in the shared embedding space (Jina embeds both chess descriptions and 
diplomatic text into the same 1024D space).
```

---

## 7. What "Search" Means Now

### 7.1 Traditional Query

```sql
-- SQL: syntactic match
SELECT * FROM entities WHERE name LIKE '%Putin%'

-- Vector DB: similarity in embedding space
SELECT * FROM entities ORDER BY cosine(embedding, query_embedding) LIMIT 10

-- Holograph codebook: concept overlap
"Which entities activate the same concepts as this query?"

The query is fingerprinted using the codebook.
Every entity in the database has a fingerprint.
Hamming scan finds entities with maximum concept overlap.

But we can do something NO other system can:

"Which entities share S-concepts with Putin but have DIFFERENT P-concepts?"
  = Hamming(S-blocks) < threshold AND Hamming(P-blocks) > threshold
  = "Entities that ARE similar to Putin but face different forces"
  = "Other autocrats under different kinds of pressure"
  
"Which entities have O-blocks similar to pre-Arab-Spring Egypt?"
  = "Who else might undergo regime change?"
  = Direct structural query over trajectory concepts
  
These aren't text queries. They're CONCEPT ALGEBRA:
  S-match AND P-diverge → structural analog under different conditions
  O-match across time → entities on similar trajectories
  XOR(A.P, B.P) → exact concepts that differ between two entities' pressure profiles
```

### 7.2 Composition via Codebook

```
bundle(entity_A.S, entity_B.S, entity_C.S) → majority vote per bit
  = "which S-concepts are shared by at least 2 of 3 entities?"
  = the PROTOTYPE of this group

XOR(entity_A.S, entity_B.S) → bits that differ
  = "which concepts are present in A but not B, and vice versa?"
  = the DIFFERENCE between two entities

AND(entity_A.P, query.P) → bits set in both
  = "which pressure concepts does this entity share with my query?"
  = the OVERLAP

These are all O(1) operations on 128-word vectors. No re-embedding.
No LLM call. No neural network forward pass. Just bitwise operations
on codebook-indexed fingerprints. The codebook gives them MEANING.
XOR without codebook = "some bits differ." 
XOR with codebook = "concepts #45, #891, and #2034 differ, 
and those correspond to [specific semantic meanings]."
```

---

## 8. The Full Architecture Name

Not "binary knowledge graph."
Not "Hamming-searchable vector store."
Not "LSH-projected embedding database."

```
CONTENT ADDRESSABLE MEMORY
  with learned domain-specific codebook (8,192 concepts per axis)
  multipass fidelity cascade (qidx → sketch → belichtungsmesser → full)
  where top-k = survival count at chosen threshold
  fingerprint size = vocabulary size = 8,192 concepts per axis
  the address IS the content (presence vector over learned vocabulary)
  composition IS bitwise logic (XOR = difference, AND = overlap, bundle = prototype)
  every bit is interpretable (maps to specific codebook entry)
  cross-domain transfer IS codebook alignment in shared embedding space
```

That's what Holograph actually is. Everything else — the DomainAdapter, the NARS, the contradiction map, the crystallization gates, the agent spawning — runs ON TOP of this CAM substrate. The CAM is the foundation. The codebook is the vocabulary. The fingerprint is the sentence. Hamming is the grammar.

---

## 9. Comparison Table

```
System          | Index Type     | Interpretable? | Composition | Cross-Domain | Hardware
----------------|---------------|----------------|-------------|-------------|----------
Neo4j           | B-tree/labels | Yes (schema)   | Cypher joins| Manual schema| Server
Pinecone        | HNSW (float)  | No             | Re-embed    | Re-embed    | Cloud
Weaviate        | HNSW (float)  | No             | Re-embed    | Re-embed    | Cloud
ChromaDB        | HNSW (float)  | No             | Re-embed    | Re-embed    | Local
Binary LSH      | Random planes | No             | XOR (noise) | Incompatible| CPU
Holograph (old) | LSH project   | No             | XOR (okay)  | Unclear     | CPU
Holograph (CAM) | Learned codebk| YES            | XOR=concept | Alignment   | CPU/RPi

The codebook is what makes XOR interpretable and cross-domain transfer possible.
Without it, XOR is "some bits differ." With it, XOR is "these specific concepts differ."
Without it, cross-domain is "hope the random projections align." 
With it, cross-domain is "find which concepts have similar centroids."
```

---

## 10. Implementation Notes

### 10.1 Codebook Construction Cost

```
k-means with k=8192 over N embeddings of D=1024:

Wikipedia (N=50M chunks):
  faiss.Kmeans on GPU: ~2 hours
  scikit-learn on CPU: ~12 hours
  One-time cost. Codebook stored as 8192 × 1024 × 4 = 32 MB per axis.
  Total: 96 MB for S+P+O codebooks.

WikiLeaks (N=2M chunks):
  ~15 minutes on CPU. Trivial.

Chess (N=1M positions):
  ~8 minutes on CPU. Trivial.
```

### 10.2 Encoding Cost (Per Record)

```
Fingerprint one new record:
  1. Embed content: ~50ms (Jina API) or ~5ms (local model)
  2. Compare against 8192 centroids: 
     Naive: 8192 × cosine(1024D) = ~8M float ops = ~2ms on CPU
     With SIMD: <0.5ms
     With precomputed norms: <0.3ms
  3. Threshold → set bits: negligible
  
  Total encoding time: ~50ms (API) or ~6ms (local)
  
  For Wikipedia bulk ingest (6.8M articles):
    Local embeddings: 6.8M × 6ms = ~11 hours
    With batching + GPU: ~3 hours
    Jina API: 6.8M × 50ms = ~94 hours (but parallelizable to ~10 hours)
```

### 10.3 Codebook Storage and Loading

```
Per axis:
  8,192 centroids × 1024 dimensions × 4 bytes = 32 MB
  8,192 thresholds × 4 bytes = 32 KB
  8,192 concept labels (optional) = ~500 KB
  
Three axes: ~96 MB total codebook

Loaded into RAM at startup. Never touches disk during query.
The codebook IS the vocabulary. It must be in memory to encode or decode.
96 MB. Fits easily alongside the 654 MB sketch index.

Total hot footprint:
  Codebook: 96 MB
  Sketch index: 654 MB
  Total: 750 MB

Still fits on a Raspberry Pi 5.
```
