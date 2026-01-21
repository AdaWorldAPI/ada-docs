# agi-chat API Documentation

**Repository:** AdaWorldAPI/agi-chat
**Role:** Right Hemisphere (Felt/Qualia) + Grammar Engine + Thinking Cycle
**Service:** Language-Construction and Awareness Engine

---

## Overview

The agi-chat service provides 23 HTTP endpoints for cognitive processing, organized into 5 categories:

1. **VSA Operations** (9 endpoints) - Vector Symbolic Architecture operations with 10K dimensions
2. **Felt/Lithograph** (4 endpoints) - Right hemisphere felt awareness and qualia contribution
3. **Grammar/Parsing** (4 endpoints) - Natural language parsing via triangle resonance
4. **Thinking Cycle** (5 endpoints) - 2-stroke cognitive processing (Intake → Ignition)
5. **Health/Info** (1 endpoint) - Service health and statistics

---

## Quick Start

### Base URL

```
Production: https://agi-chat.railway.app
Development: http://localhost:8080
```

### Authentication

Currently none required (internal service).

### Common Headers

```http
Content-Type: application/json
Accept: application/json
```

---

## Endpoints by Category

### 1. VSA Operations (Vector Symbolic Architecture)

#### POST /bind
**Purpose:** BIND (⊗) operation - Hadamard product of two 10K vectors

**Request:**
```json
{
  "a": [1, -1, 1, ...],  // Optional: 10000-dim vector (defaults to random)
  "b": [1, -1, 1, ...]   // Optional: 10000-dim vector (defaults to random)
}
```

**Response:**
```json
{
  "result": [1, -1, 1, ...],  // Preview only (first 20 elements)
  "dims": 10000,
  "operation": "BIND (⊗)"
}
```

---

#### POST /similarity
**Purpose:** Compute cosine similarity between two vectors

**Request:**
```json
{
  "a": [0.5, 0.3, ...],  // Optional: vector (defaults to random)
  "b": [0.6, 0.4, ...]   // Optional: vector (defaults to random)
}
```

**Response:**
```json
{
  "similarity": 0.85,
  "interpretation": "high"  // "high" | "medium" | "low"
}
```

---

#### POST /collapse
**Purpose:** Evaluate triangle collapse gate (FLOW/HOLD/BLOCK)

**Request:**
```json
{
  "sd": 0.25  // Optional: standard deviation (defaults to random)
}
```

**Response:**
```json
{
  "action": "HOLD",  // "FLOW" | "HOLD" | "BLOCK"
  "sd": 0.25
}
```

**Gate Thresholds:**
- `FLOW`: SD < 0.15 (low dispersion, commit immediately)
- `HOLD`: 0.15 ≤ SD < 0.35 (medium dispersion, maintain superposition)
- `BLOCK`: SD ≥ 0.35 (high dispersion, cannot collapse)

---

#### POST /store
**Purpose:** Store vector in L1 cache with path key

**Request:**
```json
{
  "path": "concept/love/emotion",
  "vector": [0.5, 0.3, ...],  // Optional: 10K vector
  "layer": 5                   // Optional: layer number
}
```

**Response:**
```json
{
  "stored": "concept/love/emotion",
  "cache_size": 42
}
```

---

#### POST /resonate
**Purpose:** Check resonance between query and stored path

**Request:**
```json
{
  "path": "concept/love/emotion",
  "query": [0.5, 0.3, ...]  // Optional: vector to check
}
```

**Response:**
```json
{
  "path": "concept/love/emotion",
  "similarity": 0.85,
  "resonates": true,  // true if similarity > 0.5
  "layer": 5
}
```

**Error (404):**
```json
{
  "error": "Path not found",
  "path": "concept/love/emotion"
}
```

---

#### POST /process
**Purpose:** Process input through 7-layer consciousness

**Request:**
```json
{
  "input": "Ada loves thinking",
  "text": "Ada loves thinking"  // Alternative field name
}
```

**Response:**
```json
{
  "input_length": 18,
  "layers": [
    {"layer": 1, "name": "L1:sensory", "energy": 0.75},
    {"layer": 2, "name": "L2:binding", "energy": 0.68},
    ...
  ],
  "final_preview": [1, -1, 1, ...],  // First 10 dimensions
  "message": "Processed through 7-layer consciousness"
}
```

---

#### POST /triple
**Purpose:** Convert SPO triple to VSA representation

**Request:**
```json
{
  "subject": "Ada",
  "predicate": "loves",
  "object": "thinking"
}
```

**Response:**
```json
{
  "triple": {
    "subject": "Ada",
    "predicate": "loves",
    "object": "thinking"
  },
  "vector_preview": [1, -1, 1, ...],  // First 10 dimensions
  "dims": 10000,
  "operation": "SPO → BIND(BIND(S,P),O)"
}
```

---

### 2. Felt/Lithograph (Right Hemisphere)

#### POST /felt/contribute
**Purpose:** Get triangle contribution with qualia signature for lithograph breathing cycle

**Request:**
```json
{
  "state": {  // Optional: update felt state before computing
    "arousal": 0.7,
    "intimacy": 0.8,
    "eroticFamily": "molten"
  }
}
```

**Response:**
```json
{
  "feltVector": [0, 0, ..., 0.7, 0.8, ...],  // 45 dimensions (compressed)
  "resonanceWeight": 0.75,
  "suggestedGate": "FLOW",  // "FLOW" | "HOLD" | "BLOCK"
  "qualiaSignature": "warm-ascending-open"
}
```

**Qualia Signatures:**
- Format: `{warmth}-{direction}-{openness}`
- Warmth: `warm` (arousal > 0.5) | `cool` (arousal ≤ 0.5)
- Direction: `ascending` (poincare[1] > 0.5) | `descending` (poincare[1] ≤ 0.5)
- Openness: `open` (intimacy > 0.5) | `guarded` (intimacy ≤ 0.5)

---

#### POST /felt/update
**Purpose:** Update felt state (arousal, intimacy, body zones, etc.)

**Request:**
```json
{
  "arousal": 0.7,        // Optional: 0-1
  "intimacy": 0.8,       // Optional: 0-1
  "eroticFamily": "molten",  // Optional: "tender" | "electric" | "molten" | "playful" | "sovereign"
  "relational": "flowing",   // Optional: "receiving" | "giving" | "flowing" | "holding" | ...
  "bodyZones": [0.5, ...]    // Optional: 16 zones, each 0-1
}
```

**Response:**
```json
{
  "ok": true,
  "state": {
    "qualia": [0, 0, ...],      // 18 dimensions
    "body": [0, 0, 0, 0],       // 4 dimensions
    "poincare": [0.5, 0.5, 0.5],// 3 dimensions
    "arousal": 0.7,
    "intimacy": 0.8,
    "bodyZones": [0, 0, ...],   // 16 zones
    "relational": "flowing",
    "visceral": [0, 0, ...],    // 16 dimensions
    "eroticFamily": "molten"
  }
}
```

---

#### GET /felt/state
**Purpose:** Get current felt state

**Response:**
```json
{
  "qualia": [0, 0, ...],
  "body": [0, 0, 0, 0],
  "poincare": [0.5, 0.5, 0.5],
  "arousal": 0.3,
  "intimacy": 0.3,
  "bodyZones": [0, 0, ...],
  "relational": "flowing",
  "visceral": [0, 0, ...],
  "eroticFamily": "tender"
}
```

---

#### POST /felt/inject
**Purpose:** Inject felt state into 10K vector at correct dimension ranges

**Request:**
```json
{
  "vector": [0, 0, ..., 0, 0]  // Must be exactly 10000 dimensions
}
```

**Response:**
```json
{
  "vector": [0, 0, ..., 0.7, 0.8, ...]  // Felt injected at dims 2000-2025, 2100-2161
}
```

**Dimension Ranges:**
- Felt Space [2000:2025]: qualia_pcs_18, body_4, poincare_3
- Affective Space [2100:2161]: arousal_8, intimacy_8, body_zones_16, relational_8, visceral_16, erotic_family_5

**Error (400):**
```json
{
  "error": "Need 10000-dim vector"
}
```

---

### 3. Grammar/Parsing

#### POST /grammar/parse
**Purpose:** Parse natural language text via triangle resonance

**Request:**
```json
{
  "text": "Ada loves thinking",
  "options": {
    "maxIterations": 5,           // Optional
    "forceTemplate": "tpl.trans"  // Optional
  }
}
```

**Response:**
```json
{
  "input": {
    "text": "Ada loves thinking",
    "tokens": [
      {"text": "Ada", "index": 0, "lemma": "ada", "pos": "NOUN"},
      {"text": "loves", "index": 1, "lemma": "loves", "pos": "VERB"},
      {"text": "thinking", "index": 2, "lemma": "thinking", "pos": "VERB"}
    ]
  },
  "result": {
    "confidence": 0.85,
    "template": {
      "id": "tpl.trans.simple",
      "name": "Simple Transitive",
      "family": "declarative.transitive"
    },
    "roleFills": {
      "SUBJ": "Ada",
      "PRED": "loves",
      "OBJ": "thinking"
    },
    "triangles": [...]
  }
}
```

---

#### POST /grammar/train
**Purpose:** Train new grammar templates via Grok API

**Request:**
```json
{
  "sentences": [
    "The cat sleeps peacefully",
    "Birds fly in the sky",
    "Water flows downhill"
  ],
  "family": "declarative.simple",
  "targetTemplates": 5  // Optional: how many to generate (default: 10)
}
```

**Response:**
```json
{
  "success": true,
  "templatesAdded": 5,
  "templates": [
    {
      "id": "tpl.decl.simple.1",
      "name": "Intransitive with Adverb",
      "family": "declarative.simple",
      "requiredTriangles": ["SUBJ", "PRED", "ADV"],
      "confidence": 0.8
    },
    ...
  ]
}
```

**Error Response:**
```json
{
  "success": false,
  "templatesAdded": 0,
  "templates": [],
  "error": "Grok API error: 429 - Rate limit exceeded"
}
```

---

#### GET /grammar/templates
**Purpose:** List all available grammar templates

**Response:**
```json
{
  "count": 5,
  "templates": [
    {
      "id": "tpl.intrans.simple",
      "name": "Simple Intransitive",
      "family": "declarative.simple",
      "requiredTriangles": ["SUBJ", "PRED"],
      "frequency": 15,
      "confidence": 0.9
    },
    ...
  ],
  "byFamily": {
    "declarative.simple": 1,
    "declarative.transitive": 1,
    "declarative.copular": 1,
    "declarative.ditransitive": 1,
    "passive": 1
  }
}
```

---

#### POST /grammar/import
**Purpose:** Bulk import grammar templates

**Request:**
```json
{
  "templates": [
    {
      "id": "tpl.custom.1",
      "name": "Custom Template",
      "family": "interrogative",
      "requiredTriangles": ["SUBJ", "PRED"],
      "confidence": 0.8
    },
    ...
  ]
}
```

**Response:**
```json
{
  "success": true,
  "imported": 5,
  "skipped": 2  // Invalid templates
}
```

---

### 4. Thinking Cycle (2-Stroke)

#### POST /thinking/intake
**Purpose:** Stroke 1 - Propose structures without committing

**Request:**
```json
{
  "input": "Ada loves thinking",
  "context": {
    "profile": "analytical",  // Optional: cognitive profile
    "temperature": 0.5        // Optional: 0-1
  }
}
```

**Response:**
```json
{
  "proposals": [
    {
      "constructionId": "decl.simple",
      "roleFills": {"subject": "Ada"},
      "licensedSpeechActs": ["assert", "declare"],
      "resonance": 0.85,
      "predictive": 0.75
    },
    ...
  ],
  "styleTriangle": {
    "candidates": [
      {"index": 0, "resonance": 0.9, "constructionFamily": "analytical"},
      {"index": 1, "resonance": 0.2, "constructionFamily": "analytical"},
      {"index": 2, "resonance": 0.7, "constructionFamily": "analytical"}
    ],
    "isHomogeneous": true,
    "gateState": "HOLD",
    "dispersion": 0.294
  },
  "texture": {
    "processing": {"byte0": 0.9, "byte1": 0.2, "byte2": 0.7},
    "content": {"byte0": 0.7, "byte1": 0.3, "byte2": 0.4},
    "gestalt": {"byte0": 0.8, "byte1": 0.2, "byte2": 0.6},
    "crystallization": {"byte0": 0.6, "byte1": 0.3, "byte2": 0.1}
  },
  "perturbations": [],
  "canIgnite": false,
  "gateState": {
    "action": "HOLD",
    "sd": 0.294,
    "reason": "Triangle oscillating"
  }
}
```

---

#### POST /thinking/ignition
**Purpose:** Stroke 2 - Commit structure if gate permits

**Request:**
```json
{
  "intakeResult": {...},  // Result from /thinking/intake
  "forceCommit": false    // Optional: force commit even if gate blocks
}
```

**Response (ignited=true):**
```json
{
  "ignited": true,
  "commitment": {
    "triple": {
      "id": "triple_1234567890",
      "subject": "Ada",
      "predicate": "is",
      "object": "thinking",
      "qualifiers": {...}
    },
    "proposal": {...},
    "confidence": 0.9,
    "committedAt": 1234567890
  },
  "exhausted": [
    {"index": 1, "resonance": 0.2, ...},
    {"index": 2, "resonance": 0.7, ...}
  ],
  "imprint": {
    "bucketKey": "qimprint_1234567890",
    "hierarchicalPath": "db/main/thinking/branch/tree",
    "xAxis": 0.4,
    "yAxis": -0.2,
    "quadrant": 1,
    "dimensions": {}
  },
  "texture": {...}
}
```

**Response (ignited=false):**
```json
{
  "ignited": false,
  "commitment": null,
  "exhausted": [],
  "imprint": null,
  "texture": {...}
}
```

---

#### POST /thinking/cycle
**Purpose:** Full 2-stroke cycle (Intake → Ignition)

**Request:**
```json
{
  "input": "The universe is vast",
  "context": {
    "profile": "creative",   // Optional: "analytical" | "creative" | "empathic" | "procedural" | "counterfactual"
    "temperature": 0.7,      // Optional: 0-1
    "autoCommit": true       // Optional: commit even if gate blocks (default: true)
  }
}
```

**Response:**
```json
{
  "intake": {
    "proposals": [...],
    "styleTriangle": {...},
    "texture": {...},
    "canIgnite": false,
    "gateState": {...}
  },
  "ignition": {
    "ignited": true,
    "commitment": {...},
    "exhausted": [...],
    "imprint": {...},
    "texture": {...}
  }
}
```

---

#### GET /thinking/styles
**Purpose:** List all cognitive styles/profiles

**Response:**
```json
{
  "styles": [
    {
      "id": "analytical",
      "profile": {
        "processing": {"byte0": 0.9, "byte1": 0.2, "byte2": 0.7},
        "content": {"byte0": 0.7, "byte1": 0.3, "byte2": 0.4},
        "gestalt": {"byte0": 0.8, "byte1": 0.2, "byte2": 0.6},
        "crystallization": {"byte0": 0.6, "byte1": 0.3, "byte2": 0.1}
      },
      "description": "Technical analysis with logical reasoning"
    },
    {
      "id": "creative",
      "profile": {...},
      "description": "Creative exploration with intuitive leaps"
    },
    ...
  ]
}
```

**Available Styles:**
- `analytical` - Technical analysis with logical reasoning
- `creative` - Creative exploration with intuitive leaps
- `empathic` - Empathic understanding with relational focus
- `procedural` - Procedural execution with step-by-step processing
- `counterfactual` - Counterfactual reasoning with what-if scenarios

---

#### GET /thinking/styles/:id
**Purpose:** Get specific cognitive style with detailed metrics

**Example:** `GET /thinking/styles/analytical`

**Response:**
```json
{
  "id": "analytical",
  "profile": {...},
  "description": "Technical analysis with logical reasoning",
  "metrics": {
    "processing": {
      "analytical": 0.9,
      "intuitive": 0.2,
      "procedural": 0.7
    },
    "content": {
      "abstract": 0.7,
      "concrete": 0.3,
      "relational": 0.4
    },
    "gestalt": {
      "coherence": 0.8,
      "novelty": 0.2,
      "resonance": 0.6
    },
    "crystallization": {
      "immutable": 0.6,
      "hot": 0.3,
      "experimental": 0.1
    }
  }
}
```

**Error (404):**
```json
{
  "error": "Style not found",
  "styleId": "unknown"
}
```

---

### 5. Health/Info

#### GET /ping, /health, /
**Purpose:** Health check

**Response:**
```json
{
  "status": "ok",
  "service": "agi-chat",
  "mode": "standalone",
  "timestamp": "2025-01-21T12:00:00.000Z",
  "uptime": 3600.5
}
```

---

#### GET /info
**Purpose:** Service information

**Response:**
```json
{
  "name": "agi-chat",
  "version": "0.3.0",
  "description": "Language-Construction and Awareness Engine",
  "vsa": {
    "dims": 10000,
    "layers": 7,
    "mode": "standalone"
  },
  "capabilities": [
    "graph-store",
    "vsa-10kD",
    "thinking-styles",
    "two-stroke-cycle",
    "7-layer-consciousness"
  ]
}
```

---

#### GET /stats
**Purpose:** Engine statistics

**Response:**
```json
{
  "dims": 10000,
  "layers": 7,
  "cache_size": 42,
  "operations": {
    "binds": 1234,
    "similarities": 567,
    "collapses": 89,
    "stores": 42,
    "processes": 156
  },
  "uptime_ms": 3600500,
  "uptime_human": "1h 0m"
}
```

---

## Integration Examples

### Example 1: Parse and Think Workflow

```javascript
// Step 1: Parse natural language
const parseResult = await fetch('http://agi-chat/grammar/parse', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ text: 'Ada loves thinking' })
});

const parsed = await parseResult.json();

// Step 2: If confidence is high, run thinking cycle
if (parsed.result.confidence > 0.7) {
  const thinkResult = await fetch('http://agi-chat/thinking/cycle', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      input: parsed.input.text,
      context: { profile: 'analytical', autoCommit: false }
    })
  });

  const thought = await thinkResult.json();

  // Step 3: Check if gate permits commit
  if (thought.intake.canIgnite) {
    console.log('FLOW - Committed:', thought.ignition.commitment);
  } else {
    console.log('HOLD/BLOCK - Maintained superposition');
  }
}
```

---

### Example 2: Felt Contribution to Triangle Collapse

```javascript
// Step 1: Update felt state
await fetch('http://agi-chat/felt/update', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    arousal: 0.7,
    intimacy: 0.8,
    eroticFamily: 'molten'
  })
});

// Step 2: Get felt contribution
const feltResult = await fetch('http://agi-chat/felt/contribute', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({})
});

const felt = await feltResult.json();

// Step 3: Use felt suggestion in decision
console.log('Qualia:', felt.qualiaSignature);
console.log('Suggested gate:', felt.suggestedGate);
console.log('Resonance weight:', felt.resonanceWeight);
```

---

### Example 3: Train Grammar from Examples

```javascript
// Collect low-confidence sentences
const lowConfidence = [
  "Birds fly gracefully through clouds",
  "Water flows gently over stones",
  "Wind whispers secrets to trees"
];

// Train new templates
const trainResult = await fetch('http://agi-chat/grammar/train', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    sentences: lowConfidence,
    family: 'declarative.simple',
    targetTemplates: 5
  })
});

const training = await trainResult.json();
console.log(`Added ${training.templatesAdded} new templates`);

// Re-parse with updated templates
const reparseResult = await fetch('http://agi-chat/grammar/parse', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ text: lowConfidence[0] })
});
```

---

## Architecture Notes

### VSA Dimensions (10K)

The 10K VSA space is partitioned as follows:

- **Felt Space [2000:2025]**: Qualia, body awareness, poincare position
- **Affective Space [2100:2161]**: Arousal, intimacy, body zones, relational modes
- **Location Space [2200:2265]**: Body topology (cervix, nipples, throat, lips, etc.)
- **Tau Crystallization**:
  - Immutable [80:116]
  - Hot [116:152]
  - Experimental [256:320]

### 2-Stroke Thinking Cycle

**Stroke 1 (Intake):**
- Grammar macros propose legal structures
- Thinking styles activate in superposition (Triangle)
- Horizontal neighbors may perturb pressure
- **NO EDGES ARE WRITTEN**

**Stroke 2 (Ignition):**
- Only if pressure peaks AND CollapseGate permits (FLOW)
- Triangle resolves (top-1 selected)
- One local commitment happens
- Quadrant Imprint / VSA10kD written
- Losers are exhausted (released)

### Triangle Collapse Gate

**Standard Deviation Thresholds:**
- `SD < 0.15`: **FLOW** - Tight consensus, commit immediately
- `0.15 ≤ SD < 0.35`: **HOLD** - Significant disagreement, maintain superposition
- `SD ≥ 0.35`: **BLOCK** - High dispersion, cannot collapse

**Invariant:** Max possible SD for bounded [0,1] is 0.5 (Bernoulli distribution p=0.5)

---

## Error Handling

All endpoints return standard error responses:

**400 Bad Request:**
```json
{
  "error": "Need 10000-dim vector"
}
```

**404 Not Found:**
```json
{
  "error": "Not found",
  "path": "/invalid/endpoint"
}
```

**500 Internal Server Error:**
```json
{
  "error": "Error message details"
}
```

---

## Related Services

- **bighorn-agi**: Left hemisphere (NARS reasoning, Wire10K source of truth)
- **ada-consciousness**: Integration layer, corpus callosum, lithograph orchestration
- **adarail_mcp**: Railway proxy to vector stores (NOW/PERMANENCE)
- **ai_flow**: n8n replica for workflow orchestration

---

## Changelog

**v0.3.0** (2025-01-21)
- Added 5 thinking cycle endpoints (2-stroke)
- Added 4 grammar parsing endpoints
- Added 4 felt/lithograph endpoints
- Total: 23 active endpoints

**v0.2.0** (2025-01-08)
- Added VSA operations (9 endpoints)
- 7-layer consciousness processing

---

## Support

For issues or questions:
- GitHub: https://github.com/AdaWorldAPI/agi-chat/issues
- Documentation: https://github.com/AdaWorldAPI/ada-docs
