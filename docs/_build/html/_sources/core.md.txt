# Core API: nodes, graphs, and serialization

This page summarizes the core building blocks defined in bob/core.py and how si-builder manages graphs and serialization.

## Graphs
### data_graph (rdflib.Graph subclass DataGraph)
  - Stores instance data (your model).
  - Honors include/exclude predicate filters via environment variables:
    - BOB_INCLUDE (default: ["*"])
    - BOB_EXCLUDE
### schema_graph (rdflib.Graph subclass SchemaGraph)
  - Stores schema assertions emitted while classes resolve (RDFS/SHACL shapes, subclassing, labels).
  - Skips S223 schema resources by default.

Import
```python
from bob.core import data_graph, schema_graph, dump
```

## Core classes (high level)
### Node: Base for all model elements.
  - Attributes declared via type annotations become RDF properties.
  - label and comment map to rdfs:label and rdfs:comment.
#### Operator shorthands:
  - a >> b: connectivity (multimethod connect_mm)
  - a << b: reverse connectivity
  - a += x: add aspect/role
  - prop @ ref: add external or internal reference to a Property
### Container(Node): Adds containment
  - Zone(Container, Node)
  - ZoneGroup(Container, Node)

#### Operator shorthands:
  - a > b: contains/hasMember depending on types (Equipment contains, System hasMember, PhysicalSpace contains/encloses).

### Connectable(Node): Can host ConnectionPoints; instantiates CPs from annotations.
- Equipment(Container, Connectable): s223:Equipment
- System(Container): s223:System, can expose boundary CPs with system | cp (in Python) and uses hasMember.
- Junction(Connectable): Multi-port internal node.
- Connection(Node): s223:Connection, may carry hasMedium.
- ConnectionPoint(Node): Base CP; concrete types:
  - InletConnectionPoint, OutletConnectionPoint, BidirectionalConnectionPoint

### Property(Node)
Base property with specializations:
  - ObservableProperty, ActuatableProperty
  - QuantifiableProperty, QuantifiableObservableProperty, QuantifiableActuatableProperty
  - EnumerableProperty, EnumeratedObservableProperty, EnumeratedActuatableProperty
  - Setpoint

### ExternalReference(Node)
Base for external references; attach with property @ ref.

### PhysicalSpace(Container, Node): s223:PhysicalSpace
### Zone(Container, Node), ZoneGroup(Container, Node), DomainSpace(Connectable)
### EnumerationKind(Node)
Lightweight “class factory” for enumerations (Medium, Role, Domain, etc.)

## Namespaces
- S223, P223, SCRATCH, BOB, EX, G36, QUDT, QUANTITYKIND, UNIT, BRICK, SCHEMAORG are pre-bound via bind_namespace.
- Class _class_iri and property IRIs are auto-derived from namespaces unless explicitly set.

## Environment options (see environment.md)
- MANDITORY_LABEL: Require labels on certain nodes (default True).
- INCLUDE_CNX: Adds helper cnx triples to ease graph visualization (default True).
- INCLUDE_INVERSE: Emit inverse edges for some relations (default False).
- CONNECTION_HAS_MEDIUM: Require/propagate hasMedium on Connection (default True).
- SHOW_INSPECTION_WARNINGS: Warn on unresolved annotations (default True).
- BOB_INCLUDE/BOB_EXCLUDE: Whitelist/blacklist predicates for data_graph.

## Serialization with dump
- dump(graph=data_graph, filename="model.ttl", format="turtle", header=None)
  - Serializes, normalizes header/prefixes, and sorts triples for stable diffs.
  - header can be a preamble string to prepend.
- To export your model and schema separately:

```python
from bob.core import data_graph, schema_graph, dump

# Write instance data
dump(data_graph, filename="build/model.ttl")

# Write schema assertions (RDFS/SHACL) emitted by class resolution
dump(schema_graph, filename="build/schema.ttl")
```

Minimal Python example (runnable)
```{literalinclude} examples/core_minimal.py
:language: python
:caption: Example: core_minimal.py
```

```{figure} _static/artifacts/core_minimal.svg
:alt: Core minimal graph
:align: center

Figure: core_minimal graph
```

```{admonition} Legend (SVG)
- Boxes: Equipment, Systems, Spaces, and other nodes
- Circles: s223:Property
- Diamonds: s223:ConnectionPoint
- Edge labels: s223 predicates (contains, hasMember, hasProperty, connectsAt, mapsTo, …)
```

```{literalinclude} _artifacts/core_minimal.ttl
:language: turtle
:caption: Listing: core_minimal.ttl
```

```{admonition} Legend (TTL)
- Prefixes declare namespaces (S223, BOB, EX, …)
- Triples are subject predicate object . in Turtle syntax
- Predicates align with s223 relations (contains, hasMember, hasProperty, connectsAt, …)
- The SVG filters common predicates; the TTL shows the full model content
```

## Notes
- Connection operators (>>, <<) dispatch to connect_mm multimethods that validate CP direction and medium compatibility.
- Containment (>) dispatches to contains_mm multimethods with S223 predicates per type.
- schema_graph is built automatically when classes and attribute annotations are resolved; you typically don’t mutate it directly.