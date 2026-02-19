# Holograph: Meta Block Quadrant Layout

## Canonical Specification — Do Not Reassign

```
┌─────────────────────────────────────────────────────┐
│ META BLOCK: 128 words (1,024 bytes)                 │
│                                                     │
│ Q1  W0-W31    CAM         Content Addressable       │
│                           Memory header:            │
│                           identity, NARS,           │
│                           codebook routing,         │
│                           timestamps, flags,        │
│                           edge topology (for edges),│
│                           ports, execution state    │
│                                                     │
│ Q2  W32-W63   EDGES       Explicit edge references  │
│                           from this record.         │
│                           Concept bindings ARE edges.│
│                           32 words = 256 bits of    │
│                           adjacency.                │
│                                                     │
│ Q3  W64-W95   LOWER NODES Records subordinate to    │
│                           this one. Children,       │
│                           members, contained items. │
│                           32 words = 256 bits of    │
│                           downward adjacency.       │
│                                                     │
│ Q4  W96-W127  UNDECIDED   Reserved. Candidates:     │
│                           concept overflow,         │
│                           container edges, upper    │
│                           node refs. NOT ASSIGNED.  │
│                           Do not use until decided. │
└─────────────────────────────────────────────────────┘
```

## Q1: CAM (W0-W31)

All identity, addressing, state, and routing lives here. This is the only quadrant with named field assignments.

```
W0:       dn_hash             — content address of this record
W1:       flags               — [63] node/edge bit
                                [62:56] kind
                                [55:48] codebook_version
                                [47:32] port_mask (nodes) or edge_flags (edges)
                                [31:0] general flags
W2:       timestamps          — created_at | modified_at (packed)
W3:       observation_count   — how many times observed/referenced
W4:       codebook_id[0]      — which codebook block_0 speaks
W5:       codebook_id[1]      — which codebook block_1 speaks
W6:       codebook_id[2]      — which codebook block_2 speaks
W7:       resonance_scores    — packed u16 × 3 (how well each codebook matched)
W8:       nars_frequency      — NARS f value
W9:       nars_confidence     — NARS c value
W10:      nars_expectation    — NARS E value
W11:      nars_quality        — NARS quality metric
W12:      source_dn           — [EDGES ONLY] DN hash of source node
W13:      target_dn           — [EDGES ONLY] DN hash of target node
W14:      source_port         — [EDGES ONLY] port_name_hash on source
W15:      target_port         — [EDGES ONLY] port_name_hash on target
W16-W23:  port_table          — [NODES] up to 8 port descriptors
                                [EDGES] edge type, weight, priority, conditions
W24-W27:  execution_state     — state, timestamps, error_hash, exec_id
W28-W31:  delivery/context    — [EDGES] delivery semantics, timeout, retries, buffer
                                [NODES] parent_workflow, group_membership
```

W12-W15 are zero for nodes. W16-W23 differ in layout between nodes and edges (ports vs edge type). This is fine — W1[63] tells you which interpretation to use.

## Q2: EDGES (W32-W63)

```
32 words. Every word is an edge reference.

Each word encodes one edge:
  [63:48]  target_dn_short    — 16-bit truncated hash of target record
  [47:32]  edge_type          — 16-bit hash of edge type / verb
  [31:16]  weight_or_strength — 16-bit fixed-point (concept activation strength,
                                 edge weight, connection confidence)
  [15:0]   flags_and_port     — [15:8] flags, [7:0] port index

32 edge slots per record. Each slot = one explicit connection.

CONCEPT BINDINGS ARE EDGES:
  "This record activates concept #47" is stored as:
    W32 + offset = { target=concept_47.dn_short, type=ACTIVATES, strength=0.85 }
  
  The concept binding IS an edge to the concept's CogRecord.
  Not a separate mechanism. Not a bit vector. An edge.

SEMANTIC RELATIONSHIPS ARE EDGES:
  "Putin → pressures → Ukraine" on the Putin record:
    W32 + offset = { target=ukraine.dn_short, type=PRESSURES, strength=0.91 }

STRUCTURAL LINKS ARE EDGES:
  "Section → belongs_to → Document":
    W32 + offset = { target=document.dn_short, type=BELONGS_TO, strength=1.0 }

When a record needs MORE than 32 edges:
  The 32 inline slots hold the STRONGEST/MOST-RELEVANT edges.
  Overflow edges become separate edge CogRecords (W1[63]=1) 
  in the graph, with full content blocks and their own NARS.
  
  Inline edges: fast, O(1) access, limited to 32.
  Overflow edge CogRecords: full-featured, unlimited, Hamming-searchable.
```

### Why 16-bit target hash?

```
16 bits = 65,536 possible values. With 6.8M records, there WILL be collisions.

But: the 16-bit short hash is a FILTER, not a lookup key.
  1. Read Q2 edge slot: target_dn_short = 0xA3F7
  2. Scan receptor index for records where dn_hash[63:48] == 0xA3F7
  3. Usually 1-3 candidates (6.8M / 65536 ≈ 104 records per bucket)
  4. Full dn_hash comparison resolves collision

This is the same cascade principle: coarse filter → refine.
The 16-bit short hash rejects 99.8% of records instantly.
The remaining ~100 candidates are resolved by full hash.

For small graphs (<65K records): zero collisions. Direct lookup.
For large graphs (millions): ~100 candidates per slot. Still fast.
```

## Q3: LOWER NODES (W64-W95)

```
32 words. Same format as Q2 edges.

Each word encodes one downward reference:
  [63:48]  child_dn_short     — 16-bit truncated hash of child record
  [47:32]  relationship_type  — 16-bit hash of relationship
  [31:16]  ordering           — 16-bit position (for ordered children)
  [15:0]   flags              — child state, visibility, etc.

WHAT LIVES HERE:
  Workflow node → its step nodes (children in execution order)
  Document → its sections
  Concept → its member records  
  Cluster → its elements
  Agent → its owned resources
  Codebook → its concept entries (up to 32 inline, rest overflow)

This is the DOWNWARD direction of the hierarchy.
Q2 edges are LATERAL (peer-to-peer connections).
Q3 lower nodes are VERTICAL (parent-to-child containment).
```

## Q4: UNDECIDED (W96-W127)

```
32 words. Reserved. NOT ASSIGNED.

Candidates under consideration:
  A) UPPER NODES — parent/container references (upward hierarchy)
  B) CONCEPT OVERFLOW — extra concept binding slots beyond Q2's 32
  C) CONTAINER EDGES — edges that belong to the container level,
     not the record level (group-to-group connections)
  D) MIXED — some combination, decided per record kind

This quadrant will be assigned when we have enough implementation 
experience to know which of A/B/C/D serves the architecture best.

Until then: all zeros. Any code that reads W96-W127 must handle 
all-zeros gracefully. Any code that writes W96-W127 is a BUG.
```

---

## Document Reconciliation

Every existing document must be audited against this layout. Violations:

```
VIOLATION: assigning W32-W63 as "concept binding signatures" (flat bit vector)
  CORRECTION: concept bindings ARE edges in Q2, using the edge slot format

VIOLATION: assigning W64-W95 as "label space" (name hashes, tag hashes)
  CORRECTION: labels/names go in Q1 (pack into W28-W31 for nodes) 
  or as a dedicated label node linked via Q2 edge
  Q3 is for LOWER NODE references only

VIOLATION: assigning W96-W127 as "reserved growth headroom" and using it
  CORRECTION: Q4 is undecided. Don't write to it.

VIOLATION: assigning W32-W127 as flat "concept binding signatures" space
  CORRECTION: Q2=edges, Q3=lower nodes, Q4=undecided. Not one big blob.
```
