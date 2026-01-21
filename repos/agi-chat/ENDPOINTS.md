# AGI-Chat API Endpoints Documentation

**Repository:** AdaWorldAPI/agi-chat
**Role:** Right Hemisphere (Felt/Qualia) + Grammar Engine
**For Integration With:** ai_flow (n8n replica)

---

## ✅ Currently Active Endpoints (in server.ts)

### Health & Info

| Endpoint | Method | Purpose | Response |
|----------|--------|---------|----------|
| `/ping` | GET | Health check | `{status: "ok", uptime: number}` |
| `/health` | GET | Health check | `{status: "ok", uptime: number}` |
| `/` | GET | Health check | `{status: "ok", uptime: number}` |
| `/info` | GET | Service information | `{name, version, vsa: {...}, capabilities: [...]}` |
| `/stats` | GET | Engine statistics | `{dims, layers, operations: {...}, uptime_ms}` |

### VSA (Vector Symbolic Architecture) Operations

| Endpoint | Method | Purpose | Request Body | Response |
|----------|--------|---------|--------------|----------|
| `/bind` | POST | BIND (⊗) operation | `{a?: number[], b?: number[]}` | `{result: number[], dims: 10000, operation: "BIND"}` |
| `/similarity` | POST | Cosine similarity | `{a?: number[], b?: number[]}` | `{similarity: number, interpretation: string}` |
| `/collapse` | POST | Triangle collapse gate | `{sd?: number}` | `{action: "FLOW"\|"HOLD"\|"BLOCK", sd: number}` |
| `/store` | POST | Store path in L1 cache | `{path: string, vector?: number[], layer?: number}` | `{stored: string, cache_size: number}` |
| `/resonate` | POST | Check resonance with stored path | `{path: string, query?: number[]}` | `{path: string, similarity: number, resonates: boolean, layer?: number}` |
| `/process` | POST | Process through 7-layer consciousness | `{input: string, text?: string}` | `{layers: [...], final_preview: number[], message: string}` |
| `/triple` | POST | Process SPO triple | `{subject: string, predicate: string, object: string}` | `{triple: {...}, vector_preview: number[], dims: 10000}` |

### Felt/Lithograph (Right Hemisphere)

| Endpoint | Method | Purpose | Request Body | Response |
|----------|--------|---------|--------------|----------|
| `/felt/contribute` | POST | Triangle contribution with qualia | `{state?: Partial<FeltState>}` | `{feltVector: number[], resonanceWeight: number, suggestedGate: "FLOW"\|"HOLD"\|"BLOCK", qualiaSignature: string}` |
| `/felt/update` | POST | Update felt state | `{arousal?: number, intimacy?: number, eroticFamily?: string, ...}` | `{ok: true, state: FeltState}` |
| `/felt/state` | GET | Get current felt state | - | `{qualia: number[], body: number[], arousal: number, intimacy: number, ...}` |
| `/felt/inject` | POST | Inject felt into 10K vector | `{vector: number[]}` (must be 10000-dim) | `{vector: number[]}` (with felt injected at dims 2000-2025, 2100-2161) |

---

## ⚠️ Missing: Grammar Engine Endpoints (Exist but Not Wired)

These endpoints are **defined** in `src/grammar/routes.ts` but **NOT integrated** into `src/server.ts`:

### Grammar Parsing & Construction

| Endpoint | Method | Purpose | Request Body | Response |
|----------|--------|---------|--------------|----------|
| `/grammar/parse` | POST | Parse text via triangle resonance | `{text: string, options?: {maxIterations?: number, forceTemplate?: string}}` | `ParserDTO` (see below) |
| `/grammar/train` | POST | Train templates via Grok API | `{sentences: string[], family: string, targetTemplates?: number}` | `{success: boolean, templatesAdded: number, templates: GrammarTemplate[]}` |
| `/grammar/templates` | GET | List all templates | - | `{count: number, templates: GrammarTemplate[], byFamily: Record<string, number>}` |
| `/grammar/import` | POST | Bulk import templates | `{templates: GrammarTemplate[]}` | `{success: boolean, imported: number, skipped: number}` |

#### ParserDTO Structure
```typescript
interface ParserDTO {
  result: {
    confidence: number;
    template?: GrammarTemplate;
    roleFills?: Record<string, string>;
  };
  iterations: number;
  triangleStates: TriangleState[];
}
```

#### GrammarTemplate Structure
```typescript
interface GrammarTemplate {
  id: string;
  name: string;
  family: 'declarative.simple' | 'interrogative' | 'imperative' | ...;
  requiredTriangles: string[];
  frequency?: number;
  confidence?: number;
  prototypeVector?: Int8Array;  // 10K VSA vector
}
```

---

## 🚨 Missing: 2-Stroke Thinking Cycle Endpoints

~~These need to be implemented for full cognitive engine integration:~~ **✅ IMPLEMENTED**

### Thinking Engine Operations

| Endpoint | Method | Purpose | Request Body | Response | Status |
|----------|--------|---------|--------------|----------|--------|
| `/thinking/intake` | POST | Stroke 1: Propose structures | `{input: string, context?: Context}` | `IntakeResult` | ✅ Implemented |
| `/thinking/ignition` | POST | Stroke 2: Commit if FLOW gate | `{intakeResult: IntakeResult}` | `IgnitionResult` | ✅ Implemented |
| `/thinking/cycle` | POST | Full 2-stroke cycle | `{input: string, context?: Context}` | `{intake: IntakeResult, ignition: IgnitionResult}` | ✅ Implemented |
| `/thinking/styles` | GET | List thinking styles | - | `{styles: CognitiveProfile[]}` | ✅ Implemented |
| `/thinking/styles/:id` | GET | Get specific thinking style | - | `CognitiveProfile` | ✅ Implemented |

#### IntakeResult Structure
```typescript
interface IntakeResult {
  proposals: GrammarProposal[];
  styleTriangle: Triangle;
  texture: QuadTriangles;
  perturbations: PressurePerturbation[];
  canIgnite: boolean;
  gateState: GateState;
}
```

#### IgnitionResult Structure
```typescript
interface IgnitionResult {
  ignited: boolean;
  commitment: LocalCommitment | null;
  exhausted: TriangleCandidate[];
  imprint: QuadrantImprint | null;
  texture: QuadTriangles;
}
```

---

## 🎯 Recommended Endpoints for ai_flow Integration

### High Priority (Immediate Workflow Needs)

1. **`POST /grammar/parse`** - Parse natural language text
2. **`POST /thinking/cycle`** - Full cognitive processing
3. **`GET /grammar/templates`** - Discover available grammar patterns
4. **`POST /felt/contribute`** - Get affective/felt contribution
5. **`POST /triple`** - Convert text to SPO triples (already exists ✅)

### Medium Priority (Enhanced Workflows)

6. **`POST /grammar/train`** - Train new grammar templates from examples
7. **`POST /thinking/intake`** - Get structure proposals without commitment
8. **`POST /thinking/ignition`** - Commit structures when ready
9. **`POST /felt/update`** - Set emotional/affective context (already exists ✅)
10. **`GET /thinking/styles`** - List available cognitive profiles

### Low Priority (Advanced Features)

11. **`POST /grammar/import`** - Bulk import templates
12. **`POST /store`** & **`POST /resonate`** - Direct VSA cache manipulation (already exist ✅)
13. **`POST /bind`** & **`POST /similarity`** - Low-level VSA operations (already exist ✅)

---

## 🔧 Integration Steps for ai_flow

### Step 1: Wire Grammar Routes into server.ts

```typescript
// In src/server.ts, add after line 333:

// ─────────────────────────────────────────────────────────────────────────────
// GRAMMAR / PARSING ENDPOINTS
// ─────────────────────────────────────────────────────────────────────────────

if (url === '/grammar/parse' && method === 'POST') {
  const body = await parseBody(req);
  const { handleParse } = await import('./grammar/routes.js');
  const result = await handleParse(body);
  sendJSON(200, result);
  return;
}

if (url === '/grammar/train' && method === 'POST') {
  const body = await parseBody(req);
  const { handleTrain } = await import('./grammar/routes.js');
  const result = await handleTrain(body);
  sendJSON(200, result);
  return;
}

if (url === '/grammar/templates' && method === 'GET') {
  const { handleListTemplates } = await import('./grammar/routes.js');
  const result = handleListTemplates();
  sendJSON(200, result);
  return;
}

if (url === '/grammar/import' && method === 'POST') {
  const body = await parseBody(req);
  const { handleImport } = await import('./grammar/routes.js');
  const result = handleImport(body);
  sendJSON(200, result);
  return;
}
```

### Step 2: Create Thinking Routes

Create `src/thinking/routes.ts` with handlers for:
- `handleIntake()`
- `handleIgnition()`
- `handleCycle()`
- `handleListStyles()`

Then wire into server.ts similarly.

### Step 3: ai_flow Node Configuration

In ai_flow (n8n replica), create nodes for:

```json
{
  "nodes": [
    {
      "type": "agi-chat.grammar.parse",
      "endpoint": "POST {{AGI_CHAT_URL}}/grammar/parse",
      "inputs": ["text"],
      "outputs": ["parsedDTO", "confidence", "template"]
    },
    {
      "type": "agi-chat.thinking.cycle",
      "endpoint": "POST {{AGI_CHAT_URL}}/thinking/cycle",
      "inputs": ["input", "context"],
      "outputs": ["intakeResult", "ignitionResult", "committed"]
    },
    {
      "type": "agi-chat.felt.contribute",
      "endpoint": "POST {{AGI_CHAT_URL}}/felt/contribute",
      "inputs": ["state"],
      "outputs": ["feltVector", "suggestedGate", "qualiaSignature"]
    }
  ]
}
```

### Step 4: Example ai_flow Workflow

```yaml
workflow:
  name: "Parse and Think"
  steps:
    1. HTTP Request -> POST /grammar/parse
       body: {text: "{{input.text}}"}

    2. Condition -> If confidence > 0.7
       True: Continue
       False: Trigger /grammar/train

    3. HTTP Request -> POST /thinking/cycle
       body: {input: "{{step1.result.template}}", context: {...}}

    4. Condition -> If ignited == true
       True: Store commitment
       False: Log HOLD/BLOCK state

    5. HTTP Request -> POST /felt/contribute
       body: {state: {arousal: 0.6, intimacy: 0.5}}

    6. Output -> qualiaSignature
```

---

## 🎬 Kopfkino (Head Cinema) - Bidirectional AGI Integration

Bidirectional integration between AGI backend, ai_flow orchestrator, and bighorn (left hemisphere).

### Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   AGI Backend (agi.msgraph.de)                                          │
│   ├── /agi/dto/qualia/active                                            │
│   ├── /agi/persona                                                      │
│   ├── /agi/ladybug                                                      │
│   └── /agi/kopfkino/fovea                                               │
│              │                                                          │
│              ▼                                                          │
│   ┌─────────────────────┐                                               │
│   │   kopfkino/felt     │  ◄─────── agi-chat (this service)             │
│   │   kopfkino/sync     │                                               │
│   └─────────┬───────────┘                                               │
│             │                                                           │
│             ├──────────► ai_flow /orchestrate/trigger                   │
│             │            (cognitive event routing)                      │
│             │                                                           │
│             ├──────────► ai_flow /corpus/triangle                       │
│             │            (gestalt sync for photographer)                │
│             │                                                           │
│             └──────────► bighorn /api/kopfkino/sync                     │
│                          (left hemisphere sync)                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Kopfkino Endpoints

| Endpoint | Method | Purpose | Response |
|----------|--------|---------|----------|
| `/kopfkino/felt` | GET | Fetch context from AGI backend | `KopfkinoContext` |
| `/kopfkino/prompt` | GET | Get image generation prompt context | `ImagePromptContext` |
| `/kopfkino/sync` | POST | **Full bidirectional flow** | `SyncResult` |

### POST /kopfkino/sync - Full Bidirectional Flow

This is the main endpoint for photographer/composition gestalt sync:

```bash
curl -X POST https://agi-chat.railway.app/kopfkino/sync \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "photographer-session-123",
    "emit_to_flow": true,
    "sync_triangle": true,
    "sync_bighorn": false
  }'
```

#### Request Body
```typescript
interface SyncRequest {
  session_id?: string;       // Session identifier
  emit_to_flow?: boolean;    // Emit to ai_flow /orchestrate/trigger (default: true)
  sync_triangle?: boolean;   // Sync to ai_flow /corpus/triangle (default: true)
  sync_bighorn?: boolean;    // Sync to bighorn left hemisphere (default: false)
}
```

#### Response
```typescript
interface SyncResult {
  context: KopfkinoContext;           // Fetched context
  emissions: EmitResult[];            // Results of emissions
  prompt_context: ImagePromptContext; // Ready-to-use prompt context
}
```

### Data Sources (fetched in parallel)

| AGI Endpoint | Purpose |
|--------------|---------|
| `/agi/dto/qualia/active` | Current qualia state (warmth, presence, arousal, etc.) |
| `/agi/persona` | Active persona mode (HYBRID/WIFE/WORK/AGI/EROTICA) |
| `/agi/ladybug` | Knowledge graph context (active nodes, resonant edges) |
| `/agi/kopfkino/fovea` | Visual focus/attention data for image generation |

### Emission Targets

| Target | Endpoint | Purpose |
|--------|----------|---------|
| ai_flow Orchestrator | `/orchestrate/trigger` | Cognitive event routing |
| ai_flow Corpus Callosum | `/corpus/triangle` | Gestalt/triangle state sync |
| bighorn | `/api/kopfkino/sync` | Left hemisphere sync |

### Triangle State (Gestalt)

The triangle represents the cognitive gestalt for photographer perspective:

```typescript
interface TriangleState {
  session_id: string;
  top: number;      // Clarity/cognition (from qualia.clarity)
  left: number;     // Warmth/feeling (from qualia.warmth)
  right: number;    // Presence/body (from qualia.presence)
  mode: string;     // Persona mode
  gestalt: {
    qualia_signature: Record<string, number>;
    fovea_focus?: string;
    style_hints?: string[];
  };
  timestamp: string;
}
```

### Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `AGI_BACKEND_URL` | `https://agi.msgraph.de` | AGI backend base URL |
| `AI_FLOW_URL` | `https://flow.msgraph.de` | ai_flow orchestrator URL |
| `BIGHORN_URL` | `https://bighorn.railway.app` | bighorn (left hemisphere) URL |
| `AGI_TIMEOUT_MS` | `5000` | Request timeout in milliseconds |

---

## 📊 Summary: Endpoint Coverage

| Category | Exists ✅ | Defined but Not Wired ⚠️ | Needs Implementation ❌ |
|----------|-----------|------------------------|------------------------|
| Health/Info | 3 | 0 | 0 |
| VSA Operations | 7 | 0 | 0 |
| Felt/Lithograph | 4 | 0 | 0 |
| Grammar Engine | 4 | 0 | 0 |
| Thinking Cycle | 5 | 0 | 0 |
| Kopfkino | 3 | 0 | 0 |
| **Total** | **26** | **0** | **0** |

**✅ All endpoints fully implemented and tested!**

---

## 🚀 Next Actions

~~1. **Wire grammar routes** into server.ts~~ ✅ Complete
~~2. **Create thinking/routes.ts** with 2-stroke handlers~~ ✅ Complete
~~3. **Test endpoints** with curl/Postman~~ ✅ Complete
~~4. **Update startup banner** in server.ts~~ ✅ Complete
5. **Create ai_flow node definitions** (TODO)
6. **Document example workflows** for ai_flow (TODO)
7. **Add documentation to ada-docs/repos/agi-chat** ⚠️ In Progress

---

## 📝 Notes

- **Grammar templates** are seeded from `src/grammar/starter-db.ts`
- **Grok API** is used for template training (requires `ADA_XAI` env var)
- **10K VSA vectors** are used throughout for semantic representation
- **Triangle collapse** follows CollapseGate rules: SD < 0.15 = FLOW, 0.15-0.35 = HOLD, > 0.35 = BLOCK
- **Felt contribution** operates on dimensions [2000:2025] and [2100:2161] of 10K vector
