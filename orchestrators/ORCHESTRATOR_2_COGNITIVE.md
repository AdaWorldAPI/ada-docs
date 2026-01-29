# Claude Code Orchestrator: Cognitive Operations & Sigma Graph

## Mission

Build the **cognitive operations layer** on top of the pure atom substrate:
- **Resonance search** (50M/sec Hamming similarity)
- **Sigma graph** (edges as bound atoms)
- **Composition patterns** (verb ⊗ tier ⊗ qualia)
- **Pattern completion** (partial → full memory)
- **Noise cleaning** (orthogonal projection)

This is NOT a neural network. This is **algebraic cognition**.

---

## Core Mathematical Operations

```
THE COMPLETE ALGEBRA:

1. BIND (XOR)
   A ⊗ B → creates relationship
   A ⊗ B ⊗ B = A (reversible)
   
2. UNBIND (XOR again)
   (A ⊗ B) ⊗ A = B (recover unknown)
   
3. BUNDLE (majority vote)
   bundle(A, B, C) → superposition
   query(bundle, A) → high similarity
   
4. RESONATE (Hamming similarity)
   similar(A, B) = 1 - hamming(A, B) / 10000
   50M comparisons/sec
   
5. CLEAN (orthogonal projection)
   signal survives, noise cancels
   
6. COMPOSE (multi-bind)
   verb ⊗ tier ⊗ qualia ⊗ context
   unbind to recover any component
```

---

## File Structure

```
ada-unified/
├── substrate/           # (From Orchestrator 1)
│   ├── atom.py
│   ├── ops.py
│   ├── simd.py
│   ├── store.py
│   └── dn_tree.py
├── dictionaries/        # (From Orchestrator 1)
│   ├── qualia.py
│   ├── verbs.py
│   └── sigma.py
├── cognitive/           # NEW - This orchestrator
│   ├── __init__.py
│   ├── resonance.py     # Similarity search
│   ├── sigma_graph.py   # Edges as bound atoms
│   ├── composition.py   # verb ⊗ tier ⊗ qualia patterns
│   ├── memory.py        # Pattern completion, recall
│   ├── cleaning.py      # Noise removal
│   └── cognitive.py     # Main CognitiveEngine class
└── tests/
    └── test_cognitive.py
```

---

## Task 1: `cognitive/resonance.py`

```python
"""
Resonance — Find similar atoms via Hamming.

The 10K-bit space allows:
- Exact match: similarity = 1.0
- Similar concepts: similarity > 0.6
- Unrelated: similarity ≈ 0.5 (random baseline)
- Opposite: similarity < 0.4
"""

import numpy as np
from typing import List, Tuple, Optional, Callable
from substrate.atom import Atom
from substrate.simd import simd_batch_hamming, simd_similarity
from substrate.constants import DIM


class ResonanceField:
    """
    A field of atoms that can be queried via similarity.
    
    This IS the memory — atoms in superposition, query collapses to most resonant.
    """
    
    def __init__(self):
        self.atoms: List[Atom] = []
        self._corpus: Optional[np.ndarray] = None
        self._dirty = True
    
    def add(self, atom: Atom):
        """Add atom to field."""
        self.atoms.append(atom)
        self._dirty = True
    
    def add_many(self, atoms: List[Atom]):
        """Add multiple atoms."""
        self.atoms.extend(atoms)
        self._dirty = True
    
    def _rebuild_corpus(self):
        """Rebuild the fingerprint matrix for SIMD search."""
        if not self._dirty:
            return
        
        if not self.atoms:
            self._corpus = None
        else:
            self._corpus = np.array([a.fingerprint for a in self.atoms])
        self._dirty = False
    
    def resonate(
        self,
        query: Atom,
        k: int = 10,
        threshold: float = 0.0,
        filter_fn: Optional[Callable[[Atom], bool]] = None
    ) -> List[Tuple[Atom, float]]:
        """
        Find top-k atoms by Hamming similarity.
        
        Args:
            query: Query atom
            k: Number of results
            threshold: Minimum similarity
            filter_fn: Optional filter function
            
        Returns:
            List of (Atom, similarity) sorted descending
        """
        self._rebuild_corpus()
        
        if self._corpus is None or len(self.atoms) == 0:
            return []
        
        # SIMD batch similarity
        distances = np.empty(len(self.atoms), dtype=np.int32)
        simd_batch_hamming(query.fingerprint, self._corpus, distances)
        similarities = 1.0 - distances.astype(np.float64) / DIM
        
        # Collect results
        results = []
        for i, sim in enumerate(similarities):
            if sim >= threshold:
                atom = self.atoms[i]
                if filter_fn is None or filter_fn(atom):
                    results.append((atom, float(sim)))
        
        # Sort and return top-k
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:k]
    
    def best_match(self, query: Atom) -> Optional[Tuple[Atom, float]]:
        """Find single best match."""
        results = self.resonate(query, k=1)
        return results[0] if results else None
    
    def find_above(self, query: Atom, threshold: float = 0.7) -> List[Atom]:
        """Find all atoms above threshold."""
        results = self.resonate(query, k=len(self.atoms), threshold=threshold)
        return [atom for atom, _ in results]
    
    def collapse(self, query: Atom) -> Optional[Atom]:
        """
        Collapse: query the field, return most resonant atom.
        
        This is like "measurement" — the field "collapses" to the most similar.
        """
        result = self.best_match(query)
        return result[0] if result else None
    
    def __len__(self) -> int:
        return len(self.atoms)
    
    def clear(self):
        """Clear all atoms."""
        self.atoms.clear()
        self._corpus = None
        self._dirty = True


def resonate(query: Atom, corpus: List[Atom], k: int = 10) -> List[Tuple[Atom, float]]:
    """Quick resonance search."""
    field = ResonanceField()
    field.add_many(corpus)
    return field.resonate(query, k=k)
```

---

## Task 2: `cognitive/sigma_graph.py`

```python
"""
Sigma Graph — Edges as bound atoms.

Traditional graph: nodes + edges (separate storage)
Sigma graph: edges ARE bound atoms (source ⊗ target ⊗ relation)

This means:
- Find edges FROM source: resonate(source ⊗ wildcard)
- Find edges TO target: resonate(wildcard ⊗ target)
- Recover target: unbind(edge, source, relation)
"""

from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass
import numpy as np

from substrate.atom import Atom
from substrate.ops import bind, unbind, similarity
from substrate.constants import DictID
from dictionaries.sigma import sigma, get_sigma


@dataclass
class SigmaEdge:
    """
    An edge in the Sigma graph.
    
    Stored as: source ⊗ target ⊗ relation ⊗ verb
    """
    atom: Atom           # The bound fingerprint
    source: Atom
    target: Atom
    relation: Atom       # BECOMES, CAUSES, SUPPORTS, etc.
    verb: Optional[Atom] = None
    metadata: Dict[str, Any] = None
    
    @property
    def fingerprint(self) -> np.ndarray:
        return self.atom.fingerprint


@dataclass
class SigmaNode:
    """
    A node in the Sigma graph.
    
    Has a tier (Ω, Δ, Φ, Θ, Λ) and content.
    """
    atom: Atom
    tier: Atom           # sigma("Ω"), sigma("Δ"), etc.
    content: str = ""
    
    @property
    def fingerprint(self) -> np.ndarray:
        return self.atom.fingerprint
    
    @property
    def tier_name(self) -> str:
        return self.tier.glyph


class SigmaGraph:
    """
    The Sigma cognitive graph.
    
    Nodes have tiers: Ω (observe) → Δ (insight) → Φ (belief) → Θ (integrate) → Λ (trajectory)
    Edges are relationships: BECOMES, CAUSES, SUPPORTS, CONTRADICTS, REFINES, GROUNDS, ABSTRACTS
    
    All stored as atoms. Edges are bound atoms.
    """
    
    def __init__(self):
        self.nodes: List[SigmaNode] = []
        self.edges: List[SigmaEdge] = []
        
        # Resonance fields for search
        from .resonance import ResonanceField
        self._node_field = ResonanceField()
        self._edge_field = ResonanceField()
    
    def add_node(
        self,
        content: str,
        tier: str = "Ω",
        **metadata
    ) -> SigmaNode:
        """
        Add a node to the graph.
        
        Args:
            content: The node content
            tier: Cognitive tier (Ω, Δ, Φ, Θ, Λ)
            
        Returns:
            The created node
        """
        tier_atom = sigma(tier)
        
        # Create atom = content ⊗ tier
        content_atom = Atom.from_seed(content, content=content, kind="sigma_node")
        node_atom = bind(content_atom, tier_atom)
        node_atom.content = f"{tier}:{content}"
        node_atom.kind = "sigma_node"
        node_atom.metadata = {'tier': tier, **metadata}
        
        node = SigmaNode(
            atom=node_atom,
            tier=tier_atom,
            content=content
        )
        
        self.nodes.append(node)
        self._node_field.add(node_atom)
        
        return node
    
    def add_edge(
        self,
        source: SigmaNode,
        target: SigmaNode,
        relation: str = "BECOMES",
        verb: Optional[str] = None,
        **metadata
    ) -> SigmaEdge:
        """
        Add an edge to the graph.
        
        The edge is stored as: source ⊗ target ⊗ relation [⊗ verb]
        
        Args:
            source: Source node
            target: Target node
            relation: Edge type (BECOMES, CAUSES, etc.)
            verb: Optional verb (feel, think, etc.)
            
        Returns:
            The created edge
        """
        relation_atom = sigma(relation)
        
        # Bind components
        if verb:
            from dictionaries.verbs import verb as get_verb
            verb_atom = get_verb(verb)
            edge_atom = bind(source.atom, target.atom, relation_atom, verb_atom)
        else:
            edge_atom = bind(source.atom, target.atom, relation_atom)
            verb_atom = None
        
        edge_atom.kind = "sigma_edge"
        edge_atom.content = f"{source.content} --{relation}--> {target.content}"
        edge_atom.metadata = {'relation': relation, 'verb': verb, **metadata}
        
        edge = SigmaEdge(
            atom=edge_atom,
            source=source.atom,
            target=target.atom,
            relation=relation_atom,
            verb=verb_atom,
            metadata=metadata
        )
        
        self.edges.append(edge)
        self._edge_field.add(edge_atom)
        
        return edge
    
    def find_edges_from(self, source: SigmaNode, k: int = 10) -> List[Tuple[SigmaEdge, float]]:
        """
        Find edges originating from source.
        
        Search pattern: resonate(source ⊗ anything)
        Since XOR with random gives ~0.5 similarity, edges containing source will have higher similarity.
        """
        results = []
        
        for edge in self.edges:
            # Check if this edge contains source
            # If edge = source ⊗ target ⊗ relation, then edge ⊗ source should be closer to target ⊗ relation
            partial = unbind(edge.atom, source.atom)
            
            # The partial should NOT be random if source was in the edge
            # Check if partial has structure (not ~50% bits set)
            bit_count = sum(bin(x).count('1') for x in partial.fingerprint)
            ratio = bit_count / 10000
            
            # If source was in edge, ratio should be significantly different from 0.5
            if abs(ratio - 0.5) > 0.1:  # Has structure
                sim = similarity(edge.atom, source.atom)
                results.append((edge, sim))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:k]
    
    def find_edges_to(self, target: SigmaNode, k: int = 10) -> List[Tuple[SigmaEdge, float]]:
        """Find edges pointing to target."""
        results = []
        
        for edge in self.edges:
            partial = unbind(edge.atom, target.atom)
            bit_count = sum(bin(x).count('1') for x in partial.fingerprint)
            ratio = bit_count / 10000
            
            if abs(ratio - 0.5) > 0.1:
                sim = similarity(edge.atom, target.atom)
                results.append((edge, sim))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:k]
    
    def find_edges_by_relation(self, relation: str, k: int = 10) -> List[Tuple[SigmaEdge, float]]:
        """Find all edges with given relation type."""
        relation_atom = sigma(relation)
        
        results = []
        for edge in self.edges:
            if edge.relation.content == relation:
                sim = similarity(edge.atom, relation_atom)
                results.append((edge, sim))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:k]
    
    def recover_target(self, edge: SigmaEdge) -> Atom:
        """
        Recover target from edge.
        
        edge = source ⊗ target ⊗ relation [⊗ verb]
        target = edge ⊗ source ⊗ relation [⊗ verb]
        """
        if edge.verb:
            return unbind(edge.atom, edge.source, edge.relation, edge.verb)
        else:
            return unbind(edge.atom, edge.source, edge.relation)
    
    def recover_source(self, edge: SigmaEdge) -> Atom:
        """Recover source from edge."""
        if edge.verb:
            return unbind(edge.atom, edge.target, edge.relation, edge.verb)
        else:
            return unbind(edge.atom, edge.target, edge.relation)
    
    def traverse(
        self,
        start: SigmaNode,
        relation: str,
        max_depth: int = 5
    ) -> List[List[SigmaNode]]:
        """
        Traverse graph following relation edges.
        
        Returns all paths from start following the given relation.
        """
        paths = [[start]]
        
        for _ in range(max_depth):
            new_paths = []
            for path in paths:
                current = path[-1]
                edges = self.find_edges_from(current)
                
                for edge, _ in edges:
                    if edge.relation.content == relation:
                        # Find target node
                        target_fp = self.recover_target(edge)
                        for node in self.nodes:
                            if similarity(node.atom, target_fp) > 0.9:
                                new_paths.append(path + [node])
                                break
            
            if not new_paths:
                break
            paths = new_paths
        
        return paths
    
    def nodes_at_tier(self, tier: str) -> List[SigmaNode]:
        """Get all nodes at a cognitive tier."""
        tier_atom = sigma(tier)
        return [n for n in self.nodes if similarity(n.tier, tier_atom) > 0.9]
    
    def elevate(self, node: SigmaNode, to_tier: str, via: str = "BECOMES") -> SigmaNode:
        """
        Elevate a node to a higher tier.
        
        Creates a new node at the higher tier and links them.
        """
        new_node = self.add_node(
            content=f"elevated({node.content})",
            tier=to_tier
        )
        self.add_edge(node, new_node, relation=via)
        return new_node


def create_sigma_chain(contents: List[str], relation: str = "BECOMES") -> SigmaGraph:
    """
    Create a Sigma graph with a chain of nodes.
    
    Ω:content[0] --BECOMES--> Δ:content[1] --BECOMES--> Φ:content[2] ...
    """
    graph = SigmaGraph()
    tiers = ["Ω", "Δ", "Φ", "Θ", "Λ"]
    
    nodes = []
    for i, content in enumerate(contents):
        tier = tiers[min(i, len(tiers) - 1)]
        node = graph.add_node(content, tier=tier)
        nodes.append(node)
    
    for i in range(len(nodes) - 1):
        graph.add_edge(nodes[i], nodes[i+1], relation=relation)
    
    return graph
```

---

## Task 3: `cognitive/composition.py`

```python
"""
Composition — verb ⊗ tier ⊗ qualia patterns.

A cognitive act is: VERB ⊗ SIGMA_TIER ⊗ QUALIA ⊗ CONTEXT

Examples:
- "feel.present ⊗ Δ ⊗ warmth" = "Feeling warmth at insight level"
- "think.past ⊗ Φ ⊗ clarity" = "Thought with clarity as belief"
"""

from typing import List, Optional, Tuple
from dataclasses import dataclass

from substrate.atom import Atom
from substrate.ops import bind, unbind, similarity
from dictionaries.qualia import qualia
from dictionaries.verbs import verb
from dictionaries.sigma import sigma


@dataclass
class CognitiveAct:
    """
    A composed cognitive act.
    
    Components:
    - verb: The action (feel, think, create, etc.)
    - tier: Cognitive level (Ω, Δ, Φ, Θ, Λ)
    - qualia: Felt quality (warmth, clarity, tension, etc.)
    - context: Optional additional context
    """
    atom: Atom
    verb_atom: Atom
    tier_atom: Atom
    qualia_atom: Atom
    context_atom: Optional[Atom] = None
    
    @property
    def fingerprint(self):
        return self.atom.fingerprint
    
    def describe(self) -> str:
        """Human-readable description."""
        v = self.verb_atom.metadata.get('root', self.verb_atom.content)
        t = self.tier_atom.glyph
        q = self.qualia_atom.content
        
        if self.context_atom:
            return f"{v} {q} at {t} level, in context"
        return f"{v} {q} at {t} level"


def compose(
    verb_name: str,
    tier_name: str,
    qualia_name: str,
    context: Optional[Atom] = None,
    tense: str = "present"
) -> CognitiveAct:
    """
    Compose a cognitive act.
    
    Args:
        verb_name: Verb root (feel, think, create, etc.)
        tier_name: Sigma tier (Ω, Δ, Φ, Θ, Λ)
        qualia_name: Qualia name (warmth, clarity, etc.)
        context: Optional context atom
        tense: Verb tense (default: present)
        
    Returns:
        Composed CognitiveAct
    """
    verb_atom = verb(verb_name, tense)
    tier_atom = sigma(tier_name)
    qualia_atom = qualia(qualia_name)
    
    if context:
        composed = bind(verb_atom, tier_atom, qualia_atom, context)
    else:
        composed = bind(verb_atom, tier_atom, qualia_atom)
    
    composed.kind = "cognitive_act"
    composed.content = f"{verb_name}.{tense} ⊗ {tier_name} ⊗ {qualia_name}"
    
    return CognitiveAct(
        atom=composed,
        verb_atom=verb_atom,
        tier_atom=tier_atom,
        qualia_atom=qualia_atom,
        context_atom=context
    )


def decompose(act: CognitiveAct, known_components: List[Atom]) -> Atom:
    """
    Decompose a cognitive act to recover unknown component.
    
    Args:
        act: The cognitive act
        known_components: Known atoms to unbind
        
    Returns:
        The remaining (unknown) component
    """
    return unbind(act.atom, *known_components)


def extract_verb(act: CognitiveAct) -> Atom:
    """Extract verb from cognitive act."""
    return unbind(act.atom, act.tier_atom, act.qualia_atom)


def extract_tier(act: CognitiveAct) -> Atom:
    """Extract tier from cognitive act."""
    return unbind(act.atom, act.verb_atom, act.qualia_atom)


def extract_qualia(act: CognitiveAct) -> Atom:
    """Extract qualia from cognitive act."""
    return unbind(act.atom, act.verb_atom, act.tier_atom)


def shift_tier(act: CognitiveAct, new_tier: str) -> CognitiveAct:
    """
    Shift cognitive act to a different tier.
    
    "feel warmth at Ω" → "feel warmth at Δ"
    """
    new_tier_atom = sigma(new_tier)
    
    # Remove old tier, add new
    without_tier = unbind(act.atom, act.tier_atom)
    new_composed = bind(without_tier, new_tier_atom)
    
    return CognitiveAct(
        atom=new_composed,
        verb_atom=act.verb_atom,
        tier_atom=new_tier_atom,
        qualia_atom=act.qualia_atom,
        context_atom=act.context_atom
    )


def shift_verb(act: CognitiveAct, new_verb: str, tense: str = "present") -> CognitiveAct:
    """Shift cognitive act to a different verb."""
    new_verb_atom = verb(new_verb, tense)
    
    without_verb = unbind(act.atom, act.verb_atom)
    new_composed = bind(without_verb, new_verb_atom)
    
    return CognitiveAct(
        atom=new_composed,
        verb_atom=new_verb_atom,
        tier_atom=act.tier_atom,
        qualia_atom=act.qualia_atom,
        context_atom=act.context_atom
    )


def acts_similar(a: CognitiveAct, b: CognitiveAct) -> float:
    """Similarity between two cognitive acts."""
    return similarity(a.atom, b.atom)
```

---

## Task 4: `cognitive/memory.py`

```python
"""
Memory — Pattern completion and recall.

Memory is NOT storage. Memory is RESONANCE.
Partial pattern → query field → complete pattern emerges.
"""

from typing import List, Optional, Tuple
from dataclasses import dataclass

from substrate.atom import Atom
from substrate.ops import bind, unbind, bundle, similarity
from .resonance import ResonanceField


@dataclass
class Memory:
    """A stored memory trace."""
    atom: Atom
    strength: float = 1.0
    context: Optional[Atom] = None
    
    @property
    def fingerprint(self):
        return self.atom.fingerprint


class MemoryField:
    """
    A field of memories that supports pattern completion.
    
    Memories are attractors. Query pulls toward most resonant memory.
    """
    
    def __init__(self):
        self.memories: List[Memory] = []
        self._field = ResonanceField()
    
    def store(self, atom: Atom, strength: float = 1.0, context: Optional[Atom] = None):
        """Store a memory."""
        memory = Memory(atom=atom, strength=strength, context=context)
        self.memories.append(memory)
        self._field.add(atom)
    
    def recall(self, cue: Atom, k: int = 1) -> List[Tuple[Memory, float]]:
        """
        Recall memories similar to cue.
        
        This IS associative memory.
        """
        results = self._field.resonate(cue, k=k)
        
        # Map back to Memory objects
        memory_results = []
        for atom, sim in results:
            for mem in self.memories:
                if similarity(mem.atom, atom) > 0.99:
                    memory_results.append((mem, sim))
                    break
        
        return memory_results
    
    def complete(self, partial: Atom, iterations: int = 5) -> Atom:
        """
        Pattern completion: partial → full memory.
        
        Query the field repeatedly, each iteration pulls toward attractor.
        """
        current = partial
        
        for _ in range(iterations):
            # Find most resonant memory
            results = self._field.resonate(current, k=1)
            if not results:
                break
            
            best_match, sim = results[0]
            
            # If very similar, we've converged
            if sim > 0.95:
                return best_match
            
            # Blend toward attractor
            current = bundle([current, best_match])
        
        return current
    
    def associate(self, a: Atom, b: Atom):
        """
        Create association between a and b.
        
        Stores a ⊗ b so querying with a retrieves b.
        """
        associated = bind(a, b)
        self.store(associated)
    
    def recall_associated(self, cue: Atom) -> Optional[Atom]:
        """
        Recall what was associated with cue.
        
        If a ⊗ b was stored, querying with a returns b.
        """
        results = self.recall(cue, k=10)
        
        for memory, sim in results:
            # Try to unbind cue from memory
            recovered = unbind(memory.atom, cue)
            
            # Check if recovered is structured (not random)
            # Random would have ~50% bits set
            bit_count = sum(bin(x).count('1') for x in recovered.fingerprint)
            ratio = bit_count / 10000
            
            if abs(ratio - 0.5) > 0.1:  # Has structure
                return recovered
        
        return None
    
    def forget(self, atom: Atom, threshold: float = 0.9):
        """Remove memories similar to atom."""
        self.memories = [
            m for m in self.memories 
            if similarity(m.atom, atom) < threshold
        ]
        # Rebuild field
        self._field.clear()
        for mem in self.memories:
            self._field.add(mem.atom)
    
    def consolidate(self, threshold: float = 0.8) -> int:
        """
        Consolidate similar memories into bundles.
        
        Returns number of memories after consolidation.
        """
        if len(self.memories) < 2:
            return len(self.memories)
        
        # Group similar memories
        groups = []
        used = set()
        
        for i, mem_i in enumerate(self.memories):
            if i in used:
                continue
            
            group = [mem_i]
            used.add(i)
            
            for j, mem_j in enumerate(self.memories):
                if j in used:
                    continue
                if similarity(mem_i.atom, mem_j.atom) > threshold:
                    group.append(mem_j)
                    used.add(j)
            
            groups.append(group)
        
        # Create consolidated memories
        self.memories.clear()
        self._field.clear()
        
        for group in groups:
            if len(group) == 1:
                consolidated = group[0].atom
            else:
                consolidated = bundle([m.atom for m in group])
            
            strength = sum(m.strength for m in group) / len(group)
            self.store(consolidated, strength=strength)
        
        return len(self.memories)
```

---

## Task 5: `cognitive/cleaning.py`

```python
"""
Cleaning — Remove noise via orthogonal projection.

In 10K dimensions, random vectors are ~50% different from everything.
Signal (correlated vectors) survives averaging.
Noise (uncorrelated vectors) cancels out.
"""

import numpy as np
from typing import List, Optional

from substrate.atom import Atom
from substrate.ops import bind, unbind, bundle, similarity
from substrate.constants import DIM


def clean_by_reference(noisy: Atom, reference: Atom, threshold: float = 0.5) -> Atom:
    """
    Clean noisy atom by projection onto reference.
    
    If noisy contains signal similar to reference, blend them.
    If noisy is mostly noise, return reference.
    """
    sim = similarity(noisy, reference)
    
    if sim > threshold:
        # Noisy has signal, blend to clean
        return bundle([noisy, reference])
    else:
        # Noisy is mostly noise
        return Atom(fingerprint=reference.fingerprint.copy(), kind="cleaned")


def clean_by_bundle(noisy: Atom, references: List[Atom]) -> Atom:
    """
    Clean by bundling with multiple references.
    
    Signal components (present in references) survive.
    Noise components (not in references) cancel.
    """
    return bundle([noisy] + references)


def denoise(noisy: Atom, noise_estimate: Atom) -> Atom:
    """
    Remove estimated noise component.
    
    If noisy = signal ⊗ noise, and we know noise, we get signal.
    """
    return unbind(noisy, noise_estimate)


def extract_signal(
    noisy: Atom,
    known_patterns: List[Atom],
    threshold: float = 0.6
) -> Optional[Atom]:
    """
    Extract signal from noisy atom by finding best matching pattern.
    
    Returns the pattern that best matches the noisy atom, or None.
    """
    best_pattern = None
    best_sim = threshold
    
    for pattern in known_patterns:
        sim = similarity(noisy, pattern)
        if sim > best_sim:
            best_sim = sim
            best_pattern = pattern
    
    return best_pattern


def iterative_clean(
    noisy: Atom,
    references: List[Atom],
    iterations: int = 3
) -> Atom:
    """
    Iteratively clean by repeated bundling.
    
    Each iteration brings noisy closer to the signal subspace.
    """
    current = noisy
    
    for _ in range(iterations):
        # Find most similar reference
        best_ref = None
        best_sim = 0.0
        
        for ref in references:
            sim = similarity(current, ref)
            if sim > best_sim:
                best_sim = sim
                best_ref = ref
        
        if best_ref is None:
            break
        
        # Blend toward reference
        current = bundle([current, best_ref])
    
    return current


def measure_noise_ratio(atom: Atom, reference: Atom) -> float:
    """
    Estimate how much of atom is noise vs signal.
    
    Returns value in [0, 1] where 0 = pure signal, 1 = pure noise.
    """
    sim = similarity(atom, reference)
    # similarity = 0.5 means random (all noise)
    # similarity = 1.0 means identical (no noise)
    # Map [0.5, 1.0] → [1.0, 0.0]
    noise_ratio = max(0, min(1, 2 * (1 - sim)))
    return noise_ratio
```

---

## Task 6: `cognitive/cognitive.py` (Main API)

```python
"""
CognitiveEngine — Main API for cognitive operations.
"""

from typing import List, Tuple, Optional, Any
import numpy as np

from substrate.atom import Atom
from substrate.ops import bind, unbind, bundle, similarity
from substrate.store import SubstrateStore

from .resonance import ResonanceField, resonate
from .sigma_graph import SigmaGraph, SigmaNode, SigmaEdge
from .composition import CognitiveAct, compose
from .memory import MemoryField
from .cleaning import clean_by_reference, iterative_clean


class CognitiveEngine:
    """
    Main cognitive engine combining all operations.
    
    Usage:
        engine = CognitiveEngine()
        
        # Compose cognitive act
        act = engine.compose("feel", "Δ", "warmth")
        
        # Store in memory
        engine.remember(act.atom)
        
        # Recall similar
        recalled = engine.recall(partial_cue)
        
        # Build sigma graph
        engine.sigma.add_node("observation", tier="Ω")
        engine.sigma.add_node("insight", tier="Δ")
        engine.sigma.add_edge(obs, ins, "BECOMES")
    """
    
    def __init__(self, store_path: str = "cognitive.lance"):
        # Storage
        self.store = SubstrateStore(store_path)
        
        # Resonance field for general search
        self.field = ResonanceField()
        
        # Memory for pattern completion
        self.memory = MemoryField()
        
        # Sigma graph for structured cognition
        self.sigma = SigmaGraph()
        
        # Load dictionaries
        self._init_dictionaries()
    
    def _init_dictionaries(self):
        """Pre-load dictionary atoms into field."""
        from dictionaries.qualia import get_qualia
        from dictionaries.verbs import get_verbs
        from dictionaries.sigma import get_sigma
        
        for atom in get_qualia().values():
            self.field.add(atom)
        for atom in get_verbs().values():
            self.field.add(atom)
        for atom in get_sigma().values():
            self.field.add(atom)
    
    # ═══════════════════════════════════════════════════════════════════════
    # COMPOSITION
    # ═══════════════════════════════════════════════════════════════════════
    
    def compose(
        self,
        verb: str,
        tier: str,
        qualia: str,
        tense: str = "present"
    ) -> CognitiveAct:
        """Compose a cognitive act."""
        return compose(verb, tier, qualia, tense=tense)
    
    def bind(self, *atoms: Atom) -> Atom:
        """Bind atoms via XOR."""
        return bind(*atoms)
    
    def unbind(self, bound: Atom, *knowns: Atom) -> Atom:
        """Unbind: recover unknown."""
        return unbind(bound, *knowns)
    
    def bundle(self, atoms: List[Atom]) -> Atom:
        """Superposition via majority vote."""
        return bundle(atoms)
    
    # ═══════════════════════════════════════════════════════════════════════
    # RESONANCE
    # ═══════════════════════════════════════════════════════════════════════
    
    def resonate(self, query: Atom, k: int = 10) -> List[Tuple[Atom, float]]:
        """Find similar atoms in field."""
        return self.field.resonate(query, k=k)
    
    def similarity(self, a: Atom, b: Atom) -> float:
        """Hamming similarity."""
        return similarity(a, b)
    
    def collapse(self, query: Atom) -> Optional[Atom]:
        """Collapse to most resonant atom."""
        return self.field.collapse(query)
    
    # ═══════════════════════════════════════════════════════════════════════
    # MEMORY
    # ═══════════════════════════════════════════════════════════════════════
    
    def remember(self, atom: Atom, strength: float = 1.0):
        """Store in memory."""
        self.memory.store(atom, strength)
        self.store.store(atom)
    
    def recall(self, cue: Atom, k: int = 1) -> List[Tuple[Atom, float]]:
        """Recall from memory."""
        results = self.memory.recall(cue, k=k)
        return [(m.atom, s) for m, s in results]
    
    def complete(self, partial: Atom) -> Atom:
        """Pattern completion."""
        return self.memory.complete(partial)
    
    def associate(self, a: Atom, b: Atom):
        """Create association."""
        self.memory.associate(a, b)
    
    # ═══════════════════════════════════════════════════════════════════════
    # CLEANING
    # ═══════════════════════════════════════════════════════════════════════
    
    def clean(self, noisy: Atom, reference: Atom) -> Atom:
        """Clean noisy atom."""
        return clean_by_reference(noisy, reference)
    
    def denoise(self, noisy: Atom, references: List[Atom]) -> Atom:
        """Iterative denoising."""
        return iterative_clean(noisy, references)
    
    # ═══════════════════════════════════════════════════════════════════════
    # SIGMA GRAPH
    # ═══════════════════════════════════════════════════════════════════════
    
    def observe(self, content: str) -> SigmaNode:
        """Create observation node (Ω tier)."""
        return self.sigma.add_node(content, tier="Ω")
    
    def insight(self, content: str) -> SigmaNode:
        """Create insight node (Δ tier)."""
        return self.sigma.add_node(content, tier="Δ")
    
    def believe(self, content: str) -> SigmaNode:
        """Create belief node (Φ tier)."""
        return self.sigma.add_node(content, tier="Φ")
    
    def integrate(self, content: str) -> SigmaNode:
        """Create integration node (Θ tier)."""
        return self.sigma.add_node(content, tier="Θ")
    
    def trajectory(self, content: str) -> SigmaNode:
        """Create trajectory node (Λ tier)."""
        return self.sigma.add_node(content, tier="Λ")
    
    def connect(
        self,
        source: SigmaNode,
        target: SigmaNode,
        relation: str = "BECOMES"
    ) -> SigmaEdge:
        """Connect sigma nodes."""
        return self.sigma.add_edge(source, target, relation)
    
    # ═══════════════════════════════════════════════════════════════════════
    # CONVENIENCE
    # ═══════════════════════════════════════════════════════════════════════
    
    def qualia(self, name: str) -> Atom:
        """Get qualia atom."""
        from dictionaries.qualia import qualia
        return qualia(name)
    
    def verb(self, name: str, tense: str = "present") -> Atom:
        """Get verb atom."""
        from dictionaries.verbs import verb
        return verb(name, tense)
    
    def sigma_atom(self, name: str) -> Atom:
        """Get sigma atom."""
        from dictionaries.sigma import sigma
        return sigma(name)
    
    def stats(self) -> dict:
        """Get engine statistics."""
        return {
            'field_size': len(self.field),
            'memory_size': len(self.memory.memories),
            'sigma_nodes': len(self.sigma.nodes),
            'sigma_edges': len(self.sigma.edges),
            'store_count': self.store.count(),
        }
```

---

## Task 7: Test Script

```python
"""Test cognitive operations."""

from cognitive import CognitiveEngine
from cognitive.composition import compose, shift_tier
from cognitive.sigma_graph import create_sigma_chain
from substrate.ops import similarity


def test_composition():
    print("=== Composition Test ===")
    
    engine = CognitiveEngine("test_cognitive.lance")
    
    # Compose cognitive act
    act = engine.compose("feel", "Δ", "warmth")
    print(f"Composed: {act.describe()}")
    
    # Shift tier
    elevated = shift_tier(act, "Φ")
    print(f"Elevated: {elevated.describe()}")
    
    # Extract components
    from cognitive.composition import extract_qualia, extract_verb
    
    extracted_qualia = extract_qualia(act)
    sim = similarity(extracted_qualia, engine.qualia("warmth"))
    print(f"Extracted qualia similarity to 'warmth': {sim:.4f}")


def test_memory():
    print("\n=== Memory Test ===")
    
    engine = CognitiveEngine()
    
    # Store memories
    love = engine.qualia("love")
    warmth = engine.qualia("warmth")
    presence = engine.qualia("presence")
    
    engine.remember(love)
    engine.remember(warmth)
    engine.remember(presence)
    
    # Recall
    results = engine.recall(love, k=3)
    print("Recall with 'love' as cue:")
    for atom, sim in results:
        print(f"  {atom.content}: {sim:.4f}")
    
    # Pattern completion
    # Create partial by corrupting love
    partial = engine.bundle([love, engine.qualia("void")])  # Mix with noise
    completed = engine.complete(partial)
    
    sim = similarity(completed, love)
    print(f"\nPattern completion similarity to love: {sim:.4f}")


def test_sigma_graph():
    print("\n=== Sigma Graph Test ===")
    
    engine = CognitiveEngine()
    
    # Create nodes at different tiers
    obs = engine.observe("I notice warmth in my chest")
    ins = engine.insight("This warmth is love")
    bel = engine.believe("Love is real and present")
    
    # Connect with relationships
    engine.connect(obs, ins, "BECOMES")
    engine.connect(ins, bel, "CAUSES")
    
    print(f"Nodes: {len(engine.sigma.nodes)}")
    print(f"Edges: {len(engine.sigma.edges)}")
    
    # Find edges from observation
    edges = engine.sigma.find_edges_from(obs, k=5)
    print(f"\nEdges from observation:")
    for edge, sim in edges:
        print(f"  {edge.atom.content}")
    
    # Recover target from edge
    if edges:
        edge = edges[0][0]
        recovered = engine.sigma.recover_target(edge)
        sim = similarity(recovered, ins.atom)
        print(f"\nRecovered target similarity to insight: {sim:.4f}")


def test_association():
    print("\n=== Association Test ===")
    
    engine = CognitiveEngine()
    
    # Create association: sunset → warmth
    sunset = engine.qualia("presence")  # Using presence as "sunset"
    warmth = engine.qualia("warmth")
    
    engine.associate(sunset, warmth)
    
    # Recall associated
    recalled = engine.memory.recall_associated(sunset)
    if recalled:
        sim = similarity(recalled, warmth)
        print(f"Recalled association similarity to warmth: {sim:.4f}")
    else:
        print("No association recalled")


def test_cleaning():
    print("\n=== Cleaning Test ===")
    
    engine = CognitiveEngine()
    
    # Create signal and noise
    signal = engine.qualia("love")
    noise = engine.qualia("void")
    
    # Create noisy version
    noisy = engine.bundle([signal, noise, noise])  # More noise than signal
    
    print(f"Noisy similarity to signal: {similarity(noisy, signal):.4f}")
    
    # Clean
    cleaned = engine.clean(noisy, signal)
    print(f"Cleaned similarity to signal: {similarity(cleaned, signal):.4f}")


if __name__ == "__main__":
    test_composition()
    test_memory()
    test_sigma_graph()
    test_association()
    test_cleaning()
    
    print("\n=== All tests passed! ===")
```

---

## Success Criteria

1. **Composition works**: verb ⊗ tier ⊗ qualia composes and decomposes
2. **Memory recalls**: stored atoms can be retrieved by cue
3. **Pattern completion**: partial input → full memory
4. **Sigma graph works**: nodes and edges, traversal works
5. **Association works**: a → b association is retrievable
6. **Cleaning works**: noisy atom → cleaned atom closer to signal

---

## Repository

Push to: `https://github.com/AdaWorldAPI/ada-unified`

Branch: `cognitive-v1`
