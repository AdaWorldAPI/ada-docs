# Holograph: Explicit Edge Contract

## The Requirement

If someone draws a graph — any graph — with named nodes, typed directed edges, ports, and wiring, the substrate stores it as CogRecords and the topology is explicit, inspectable, queryable, and Hamming-searchable. No serialization. No JSON blobs. No opaque payloads. The edge IS a CogRecord with source, target, type, direction, and port bindings visible in the meta block. A human can write YAML and get a working graph. An orchestration engine can traverse edges by reading meta fields, not by deserializing anything.

---

## 1. The Two Primitives

There are exactly two things in the substrate: **Nodes** and **Edges**. Both are CogRecords. They differ in exactly one bit: `meta.W1[63]`.

```
meta.W1[63] = 0  →  NODE
meta.W1[63] = 1  →  EDGE
```

That's the only structural distinction. Everything else is codebook-indexed content in the three blocks. But edges have MANDATORY meta fields that nodes don't.

---

## 2. Node Meta Contract

```
NODE CogRecord meta (128 words):

W0:        dn_hash           — content address of this node
W1:        [63]=0 (NODE)     — type bit
           [62:56]=kind      — 0x00=data, 0x01=transform, 0x02=trigger,
                               0x03=condition, 0x04=agent, 0x05=codebook,
                               0x06=concept, 0x07=workflow, 0x08..=domain-specific
           [55:48]=version   — codebook version at encoding time
           [47:32]=port_mask — which ports exist (up to 16 in, 16 out)
           [31:0]=flags      — reserved
W2:        created_at | modified_at   — packed timestamps
W3:        observation_count
W4:        codebook_id[0]    — block_0 language
W5:        codebook_id[1]    — block_1 language
W6:        codebook_id[2]    — block_2 language
W7:        resonance[0:1:2]  — packed u16 × 3
W8-W11:    NARS (f, c, expectation, quality)
W12-W15:   contradiction INT4 tracking

W16-W23:   PORT TABLE (8 words = 8 port descriptors)
           Each word = one port:
             [63:48] = port_name_hash (16-bit hash of port name string)
             [47:32] = port_type_hash (16-bit hash of expected codebook/schema)
             [31:16] = port_direction  (0x0000=IN, 0x0001=OUT, 0x0002=INOUT)
             [15:0]  = port_index     (position for ordering)

W24-W31:   EXECUTION STATE (for orchestration nodes)
           W24:  state         — 0=idle, 1=pending, 2=running, 3=done,
                                 4=failed, 5=timeout, 6=skipped, 7=paused
           W25:  started_at    — execution start timestamp
           W26:  finished_at   — execution end timestamp  
           W27:  error_hash    — DN hash of error record (0 if no error)
           W28:  retry_count   — how many times this node has been retried
           W29:  parent_wf     — DN hash of parent workflow node
           W30:  exec_id       — execution instance identifier
           W31:  reserved

W32-W63:   CONCEPT BINDING SIGNATURES (crystallization, same for nodes and edges)
W64-W95:   LABEL SPACE
           Up to 32 words for human-readable identity:
           W64-W67: node_name_hash (256-bit hash of full name string)
           W68-W71: node_label_hash (256-bit hash of display label)
           W72-W79: tag_hashes (up to 8 tags, 64-bit hash each)
           W80-W95: reserved
W96-W127:  RESERVED (growth headroom)
```

### Port Table Detail

```
A node can have up to 8 ports (W16-W23). Each port is one word:

  port_name_hash:  hash("input"), hash("output"), hash("on_success"), 
                   hash("on_failure"), hash("data_in"), hash("trigger"), etc.
  port_type_hash:  hash of expected content type / codebook
  port_direction:  IN, OUT, or INOUT
  port_index:      ordering (port 0, port 1, ...)

For simple nodes (one in, one out):
  W16 = port("input",  type=any, direction=IN,  index=0)
  W17 = port("output", type=any, direction=OUT, index=0)
  W18-W23 = 0x0000 (unused ports)

For a condition node (one in, two out):
  W16 = port("input",      type=any,  direction=IN,  index=0)
  W17 = port("on_true",    type=any,  direction=OUT, index=0)
  W18 = port("on_false",   type=any,  direction=OUT, index=1)

For a fan-in node (three in, one out):
  W16 = port("input_a",  direction=IN,  index=0)
  W17 = port("input_b",  direction=IN,  index=1)
  W18 = port("input_c",  direction=IN,  index=2)
  W19 = port("output",   direction=OUT, index=0)
```

---

## 3. Edge Meta Contract

```
EDGE CogRecord meta (128 words):

W0:        dn_hash           — content address of this edge
W1:        [63]=1 (EDGE)     — type bit
           [62:56]=kind      — 0x00=semantic, 0x01=structural, 0x02=dataflow,
                               0x03=control, 0x04=orchestration, 0x05=causal,
                               0x06=temporal, 0x07=inhibitory, 0x08..=domain-specific
           [55:48]=version
           [47:32]=reserved
           [31:0]=flags      — [0]=directed, [1]=weighted, [2]=conditional,
                               [3]=buffered, [4]=idempotent, [5]=ordered
W2:        created_at | modified_at
W3:        observation_count
W4:        codebook_id[0]
W5:        codebook_id[1]
W6:        codebook_id[2]
W7:        resonance[0:1:2]
W8-W11:    NARS

W12-W15:   TOPOLOGY (the core of the edge contract)
           W12:  source_dn     — DN hash of source node
           W13:  target_dn     — DN hash of target node
           W14:  source_port   — port_name_hash on source (which OUT port)
           W15:  target_port   — port_name_hash on target (which IN port)

W16-W19:   EDGE TYPE IDENTITY
           W16:  type_dn       — DN hash of edge type definition
           W17:  type_name_hash — hash of human-readable type name
           W18:  weight         — f64 edge weight (or 0x3FF0000000000000 = 1.0 default)
           W19:  priority       — u64 execution priority (lower = sooner)

W20-W23:   EXECUTION STATE (for orchestration edges)
           W20:  state         — 0=idle, 1=armed, 2=fired, 3=delivered,
                                 4=failed, 5=timeout, 6=retrying
           W21:  fired_at      — timestamp of last fire
           W22:  exec_id       — execution instance (matches source node exec_id)
           W23:  payload_dn    — DN hash of payload record (0 if no payload)
                                 payload is ANOTHER CogRecord (node), not inline

W24-W27:   CONDITION (for conditional edges)
           W24:  condition_type — 0=always, 1=on_success, 2=on_failure,
                                  3=on_match, 4=on_timeout, 5=expression
           W25:  condition_dn  — DN hash of condition expression record (if type=5)
           W26:  match_codebook — codebook_id to match against (if type=3)
           W27:  match_threshold — Hamming threshold for match (u64 packed)

W28-W31:   DELIVERY GUARANTEES
           W28:  semantics     — 0=at_most_once, 1=at_least_once, 2=exactly_once
           W29:  timeout_ms    — milliseconds before edge times out (0=infinite)
           W30:  max_retries   — retry count before failure (0=no retry)
           W31:  buffer_size   — how many pending fires to queue (0=unbuffered)

W32-W63:   CONCEPT BINDING SIGNATURES
W64-W95:   LABEL SPACE (same layout as node: name_hash, label_hash, tags)
W96-W127:  RESERVED
```

### Topology Is Always Explicit

```
W12 = source_dn
W13 = target_dn
W14 = source_port (which port on the source)
W15 = target_port (which port on the target)

This is ALWAYS populated for edges. There is no implicit edge.
There is no edge without a source and target.
There is no edge without port binding.

If an edge is undirected (rare, only semantic edges):
  flag[0] = 0 (undirected)
  Convention: source_dn < target_dn (canonical ordering)
  Searching "edges from node X": check both W12 and W13 for X

If an edge is directed (everything else):
  flag[0] = 1 (directed)
  source_dn → target_dn is the only valid traversal direction
```

---

## 4. Content Blocks for Edges

The three content blocks on an edge CogRecord aren't S/P/O. They encode ABOUT the edge:

```
Block 0 (codebook[W4]):  RELATIONSHIP CONTENT
  What does this edge MEAN?
  Encoded against whatever codebook best describes the relationship.
  
  Semantic edge: CODEBOOK_POLITICAL → "pressures", "allies_with", "opposes"
  Orchestration edge: CODEBOOK_WORKFLOW → "triggers_after", "gates_on", "feeds_data"
  Causal edge: CODEBOOK_CAUSAL → "causes", "prevents", "enables"

Block 1 (codebook[W5]):  CONTEXT
  Under what CONDITIONS does this edge apply?
  
  Semantic: CODEBOOK_TEMPORAL → "during_2009", "since_cold_war"
  Orchestration: CODEBOOK_EXECUTION → "when_queue_empty", "if_payload_valid"
  Causal: CODEBOOK_EVIDENCE → "observed_experimentally", "theorized"

Block 2 (codebook[W6]):  SIGNATURE
  What is the STRUCTURAL PATTERN of this edge?
  
  This is XOR(source.block_0, target.block_0) — the content delta.
  The Hamming distance of this block measures how DIFFERENT source and 
  target are. Bundling many edge block_2s gives the prototype "shape" 
  of edges in a workflow or network.
```

### Why Block 2 as XOR Delta Matters

```
In an n8n workflow:
  SendEmail → ParseResponse:  XOR delta = difference between email-sending 
                               and response-parsing concepts
  ParseResponse → StoreDB:    XOR delta = difference between parsing 
                               and storage concepts

bundle(all edge deltas in workflow) = the workflow's TRANSFORMATION SIGNATURE
  "This workflow transforms email-like content into database-like content"

Search: "find workflows with similar transformation signature"
  → Hamming scan over bundled edge deltas
  → finds structurally similar workflows even if they use different nodes
  → "SendEmail→Parse→Store" matches "CallAPI→Extract→Archive" because 
     the transformation shape is the same: fetch→parse→persist
```

---

## 5. YAML Mapping

The entire point: someone writes YAML, it maps to CogRecords.

```yaml
# workflow: daily_report.yaml

workflow:
  name: "Daily Report Pipeline"
  
nodes:
  - id: fetch_data
    kind: transform
    label: "Fetch Sales Data"
    codebooks: [data_pipeline, business_logic]
    ports:
      - name: trigger
        direction: in
      - name: output
        direction: out
        
  - id: process
    kind: transform
    label: "Aggregate by Region"
    codebooks: [data_pipeline, analytics]
    ports:
      - name: input
        direction: in
      - name: output
        direction: out
      - name: on_error
        direction: out

  - id: send_report
    kind: transform
    label: "Email Report"
    codebooks: [data_pipeline, communication]
    ports:
      - name: input
        direction: in
      - name: on_success
        direction: out
      - name: on_failure
        direction: out

  - id: alert
    kind: transform
    label: "Slack Alert"
    codebooks: [communication, alerting]
    ports:
      - name: input
        direction: in

edges:
  - source: fetch_data.output
    target: process.input
    kind: dataflow
    condition: always
    delivery: exactly_once
    
  - source: process.output
    target: send_report.input
    kind: orchestration
    condition: on_success
    delivery: at_least_once
    timeout_ms: 30000
    
  - source: process.on_error
    target: alert.input
    kind: control
    condition: on_failure
    delivery: at_least_once
    
  - source: send_report.on_failure
    target: alert.input
    kind: control
    condition: on_failure
    delivery: at_least_once
```

### YAML → CogRecord Mapping

```
Node "fetch_data" becomes:

  CogRecord {
    meta: {
      W0:  dn_hash("daily_report.fetch_data"),
      W1:  type=NODE, kind=TRANSFORM, port_mask=0b_0000_0010_0000_0001,
      W4:  CODEBOOK_DATA_PIPELINE,
      W5:  CODEBOOK_BUSINESS_LOGIC,
      W6:  0 (no third codebook),
      W16: port("trigger", direction=IN,  index=0),
      W17: port("output",  direction=OUT, index=0),
      W64: name_hash("fetch_data"),
      W68: label_hash("Fetch Sales Data"),
    },
    block_0: fingerprint("Fetch Sales Data" against CODEBOOK_DATA_PIPELINE),
    block_1: fingerprint("Fetch Sales Data" against CODEBOOK_BUSINESS_LOGIC),
    block_2: [0; 128],  // no third codebook
  }


Edge "fetch_data.output → process.input" becomes:

  CogRecord {
    meta: {
      W0:  dn_hash("daily_report.edge.fetch_data.output→process.input"),
      W1:  type=EDGE, kind=DATAFLOW, flags=[directed, idempotent],
      W12: dn_hash("daily_report.fetch_data"),    // source
      W13: dn_hash("daily_report.process"),        // target
      W14: port_hash("output"),                    // source port
      W15: port_hash("input"),                     // target port
      W24: condition=ALWAYS,
      W28: semantics=EXACTLY_ONCE,
      W29: timeout_ms=0,
    },
    block_0: fingerprint("dataflow fetch_data→process" against CODEBOOK_WORKFLOW),
    block_1: fingerprint(context against relevant codebook),
    block_2: XOR(fetch_data.block_0, process.block_0),  // transformation delta
  }
```

---

## 6. Traversal Primitives

An orchestration engine needs exactly these operations. All work directly on meta fields. No deserialization.

```rust
// Find all edges FROM a node
fn edges_from(source_dn: u64) -> Vec<&CogRecord> {
    // Scan receptor index: filter where meta.W1[63]==1 AND meta.W12 == source_dn
    receptor_index.scan(|meta| meta.is_edge() && meta.source_dn() == source_dn)
}

// Find all edges TO a node  
fn edges_to(target_dn: u64) -> Vec<&CogRecord> {
    receptor_index.scan(|meta| meta.is_edge() && meta.target_dn() == target_dn)
}

// Find all edges FROM a specific port
fn edges_from_port(source_dn: u64, port_name_hash: u16) -> Vec<&CogRecord> {
    receptor_index.scan(|meta| 
        meta.is_edge() && 
        meta.source_dn() == source_dn && 
        meta.source_port() == port_name_hash
    )
}

// Find all edges of a specific type
fn edges_of_type(type_name_hash: u64) -> Vec<&CogRecord> {
    receptor_index.scan(|meta| meta.is_edge() && meta.type_name_hash() == type_name_hash)
}

// Find all nodes reachable from a node (BFS/DFS over explicit edges)
fn reachable_from(start_dn: u64) -> Vec<u64> {
    let mut visited = HashSet::new();
    let mut queue = VecDeque::new();
    queue.push_back(start_dn);
    
    while let Some(current) = queue.pop_front() {
        if visited.insert(current) {
            for edge in edges_from(current) {
                queue.push_back(edge.meta.target_dn());
            }
        }
    }
    visited.into_iter().collect()
}

// Topological sort (for execution ordering)
fn topo_sort(workflow_dn: u64) -> Vec<u64> {
    let nodes = children_of(workflow_dn);     // all nodes in this workflow
    let edges = edges_within(workflow_dn);     // all edges between them
    
    // Standard Kahn's algorithm, reading source_dn/target_dn from meta
    kahns_algorithm(nodes, edges, |e| e.meta.source_dn(), |e| e.meta.target_dn())
}

// Next nodes to execute (orchestration)
fn next_executable(workflow_dn: u64, exec_id: u64) -> Vec<u64> {
    topo_sort(workflow_dn)
        .into_iter()
        .filter(|node_dn| {
            let node = load(node_dn);
            // Node is idle AND all incoming edges are in state DELIVERED
            node.meta.exec_state() == IDLE &&
            edges_to(*node_dn).iter().all(|e| 
                e.meta.exec_id() == exec_id && 
                e.meta.edge_state() == DELIVERED
            )
        })
        .collect()
}
```

### Performance

```
Edge traversal via receptor scan:

Receptor has source_dn at byte offset 96 (W12 position in meta).
To find edges from node X: scan all receptors where W1[63]==1 AND W12==X.

For 6.8M records, ~10% are edges = 680K edges.
680K × 8 bytes (W12 check) = 5.4 MB scan → <0.2 ms.

For a workflow with 50 nodes and 60 edges:
  All traversals are over 60 edges. Sub-microsecond.

Topological sort: O(V+E) = O(50+60) = negligible.

The orchestration engine never touches content blocks for traversal.
It reads meta fields only. Content blocks are for Hamming search 
(find similar edges, find similar workflows). Traversal is pure meta.
```

---

## 7. Secondary Index: Adjacency Receptor

For high-frequency traversal (orchestration hot path), maintain a secondary index:

```
struct AdjacencyReceptor {
    node_dn: u64,                              // 8 bytes
    outgoing_edges: SmallVec<[EdgeRef; 8]>,    // up to 8 outgoing, inline
    incoming_edges: SmallVec<[EdgeRef; 8]>,    // up to 8 incoming, inline
}

struct EdgeRef {
    edge_dn: u64,       // 8 bytes — DN of the edge CogRecord
    target_dn: u64,     // 8 bytes — DN of the other end
    port: u16,          // 2 bytes — which port
    kind: u8,           // 1 byte  — edge kind
    condition: u8,      // 1 byte  — condition type
    state: u8,          // 1 byte  — current execution state
    _pad: [u8; 3],      // 3 bytes — alignment
}
// EdgeRef = 24 bytes

// AdjacencyReceptor for typical node (4 in, 4 out):
//   8 + (8 × 24) + (8 × 24) = 392 bytes per node

// For 10K workflow nodes: 10K × 392 = 3.8 MB
// Fits in L2 cache. Traversal is cache-hot.
```

This is an OPTIONAL acceleration structure. The substrate truth is always in the CogRecords. The adjacency receptor is derived, rebuilt on startup or when edges change. It's a materialized view, not source of truth.

---

## 8. Execution Protocol

How an orchestration engine (n8n, ada-n8n, or anything else) runs a workflow using only these primitives:

```
EXECUTE(workflow_dn, input_payload_dn):

1. TOPO_SORT
   nodes = topo_sort(workflow_dn)
   // Deterministic execution order from explicit edge topology.
   // No ambiguity. Edges in meta.W12/W13 define the graph.

2. INITIALIZE
   exec_id = new_unique_id()
   for node in nodes:
     node.meta.W24 = IDLE        // state = idle
     node.meta.W30 = exec_id     // bind to this execution
   for edge in edges_within(workflow_dn):
     edge.meta.W20 = IDLE        // state = idle
     edge.meta.W22 = exec_id     // bind to this execution

3. ARM ENTRY EDGES
   for edge in edges_to(nodes[0]):  // edges into first node
     edge.meta.W20 = ARMED
     edge.meta.W23 = input_payload_dn  // attach input payload

4. EXECUTION LOOP
   while any node has state != DONE and state != FAILED and state != SKIPPED:
     
     // Find nodes ready to execute
     ready = next_executable(workflow_dn, exec_id)
     
     for node_dn in ready:
       // Collect input payloads from incoming edges
       inputs = edges_to(node_dn)
         .filter(|e| e.meta.W22 == exec_id && e.meta.W20 == DELIVERED)
         .map(|e| e.meta.W23)  // payload_dn from each incoming edge
       
       // Execute the node
       node.meta.W24 = RUNNING
       node.meta.W25 = now()
       
       result = execute_node(node_dn, inputs)  // domain-specific execution
       
       match result {
         Ok(output_payload_dn) => {
           node.meta.W24 = DONE
           node.meta.W26 = now()
           
           // Fire outgoing edges
           for edge in edges_from(node_dn):
             if edge.meta.condition_matches(DONE):
               edge.meta.W20 = FIRED
               edge.meta.W21 = now()
               edge.meta.W23 = output_payload_dn
               
               // Deliver to target (check delivery semantics)
               deliver(edge)  // sets edge state to DELIVERED
         }
         
         Err(error_dn) => {
           node.meta.W24 = FAILED
           node.meta.W27 = error_dn
           
           // Fire error edges
           for edge in edges_from(node_dn):
             if edge.meta.condition_matches(FAILED):
               edge.meta.W20 = FIRED
               edge.meta.W23 = error_dn
               deliver(edge)
         }
       }

5. COMPLETION
   workflow_node.meta.W24 = if all_nodes_done { DONE } else { FAILED }
   workflow_node.meta.W26 = now()
```

### Delivery Guarantees

```
fn deliver(edge: &mut CogRecord) {
    match edge.meta.delivery_semantics() {
        AT_MOST_ONCE => {
            edge.meta.W20 = DELIVERED;
            // Fire and forget. If target never reads it, lost.
        }
        AT_LEAST_ONCE => {
            edge.meta.W20 = DELIVERED;
            // If target fails to acknowledge within timeout_ms:
            //   edge.meta.W20 = RETRYING
            //   edge.meta.W28 (retry_count) += 1
            //   if retry_count > max_retries: edge.meta.W20 = FAILED
        }
        EXACTLY_ONCE => {
            // Check idempotency key (exec_id + edge_dn)
            // If already delivered for this exec_id: skip
            // Otherwise: deliver, mark, never deliver again for this exec_id
            edge.meta.W20 = DELIVERED;
        }
    }
}
```

---

## 9. Payloads Are Nodes, Not Inline

```
CRITICAL: Edge payloads are NOT stored in the edge.

Edge meta.W23 = payload_dn → DN hash pointing to ANOTHER CogRecord.

The payload is a regular node CogRecord:
  - It has its own DN hash
  - It's fingerprinted against appropriate codebooks
  - It's Hamming-searchable ("find all payloads similar to this one")
  - It has NARS truth values
  - It can carry any domain content in its 3 blocks

Why not inline?
  1. Edge is 4 KB. Payload could be any size concept.
  2. Payload might be shared by multiple edges (fan-out).
  3. Payload needs to be searchable independently.
  4. No serialization. Payload IS a CogRecord. Always was.

The ONLY reference is the DN hash in W23. O(1) lookup.
If you need the payload, load the record at that DN.
If you don't need it (just traversing topology), never touch it.
```

---

## 10. Cypher-like Query Language

For the Neo4j people who need to FEEL the graph:

```cypher
-- Find all nodes in a workflow
MATCH (n)-[]-() WHERE n.parent_wf = workflow_dn RETURN n

-- Translates to: scan receptors where W29 == workflow_dn

-- Find path between two nodes
MATCH path = (a)-[*]->(b) 
WHERE a.dn = source_dn AND b.dn = target_dn
RETURN path

-- Translates to: BFS from source_dn to target_dn over explicit edges

-- Find similar edges (Hamming search!)
MATCH ()-[e]->() 
WHERE hamming(e.block_0, query_fingerprint) < 500
RETURN e ORDER BY hamming(e.block_0, query_fingerprint)

-- Translates to: codebook-filtered cascade scan over edge records

-- Find workflows with similar transformation shape
MATCH (wf:workflow)
WHERE hamming(bundle(edges_within(wf).block_2), query_shape) < 1000
RETURN wf

-- Translates to: bundle all edge deltas per workflow, Hamming against query

-- Create a node (YAML equivalent)
CREATE (n:transform {
  name: "Process Data",
  codebooks: [data_pipeline, analytics],
  ports: [{name: "input", dir: IN}, {name: "output", dir: OUT}]
})

-- Translates to: construct CogRecord with meta fields populated per contract

-- Create an edge
CREATE (a)-[:dataflow {
  condition: always,
  delivery: exactly_once,
  source_port: "output",
  target_port: "input"
}]->(b)

-- Translates to: construct edge CogRecord with W12=a.dn, W13=b.dn, 
--                W14=hash("output"), W15=hash("input"), etc.
```

---

## 11. Contract Summary

```
CONTRACT E1: Two primitives only
  Everything is a CogRecord. W1[63] distinguishes node from edge.
  No other structural types exist.

CONTRACT E2: Edges have explicit topology
  W12 = source_dn, W13 = target_dn, W14 = source_port, W15 = target_port.
  ALWAYS populated. ALWAYS inspectable. No implicit edges.

CONTRACT E3: Ports are declared in node meta
  W16-W23 port table. Up to 8 ports per node.
  Each port has: name_hash, type_hash, direction, index.

CONTRACT E4: Edge kind determines mandatory fields
  Semantic edges: W12-W15 only (topology).
  Dataflow edges: + W28-W31 (delivery guarantees).
  Control edges: + W24-W27 (conditions).
  Orchestration edges: all fields populated.

CONTRACT E5: Payloads are nodes, referenced by DN
  Edge.W23 = DN hash of payload CogRecord.
  Never inline. Never serialized. Always a first-class record.

CONTRACT E6: Execution state is in meta, not external
  Node state in W24-W31. Edge state in W20-W23.
  Orchestration engine reads/writes meta directly.
  No external state machine. The graph IS the state.

CONTRACT E7: Traversal is meta-only
  Finding edges from/to a node: scan W12/W13.
  Topo sort: Kahn's over W12/W13.
  Never touch content blocks for graph traversal.
  Content blocks are for Hamming search (similarity), not navigation.

CONTRACT E8: Content blocks on edges are searchable
  Block 0 = relationship meaning (codebook-indexed).
  Block 2 = XOR delta of source and target (transformation signature).
  bundle(all edge block_2s) = workflow's transformation shape.
  Hamming search over edge blocks finds structurally similar relationships.

CONTRACT E9: YAML in, CogRecords out
  Every field in the YAML maps to a specific meta word.
  No JSON serialization. No opaque blobs. 
  What you write is what gets stored.

CONTRACT E10: Adjacency receptor is optional acceleration
  Derived from CogRecords. Not source of truth.
  Rebuilt on startup. Enables sub-microsecond traversal for hot paths.
```
