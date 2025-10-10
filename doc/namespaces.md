# Namespaces

When creating graph nodes it is customary to use blank nodes for subjects and
objects unless the output is intended for human consumption, it which case the
URI is a hint to the context of the node in the graph.

## Blank Nodes

This is a sample application that just creates a `Node`:

```python
from bob import Node, dump

x = Node(label="x")

dump()
```

And the generated identifier is a blank node:

```turtle
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

[] rdfs:label "x" .
```

## Namespace Nodes

The `bob.core` module has a function `bind_model_namespace` that will use
the provided namespace for new nodes with a simple sequence number for
each node that is created.

```python
from bob import Node, dump
from bob.core import bind_model_namespace

EX = bind_model_namespace("ex", "http://example.com/")

x = Node(label="x")

dump()
```

Results in this graph:

```turtle
@prefix ex1: <http://example.com/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex1:00001 rdfs:label "x" .
```

## Explicit Node IRIs 

Any subclass of `Node` can provide an explicit IRI for the node.

```python
from bob import Node, dump
from bob.core import bind_model_namespace

EX = bind_model_namespace("ex", "http://example.com/")

x = Node(_node_iri=EX.x, label="x")

dump()
```

Results in this graph:

```turtle
@prefix ex1: <http://example.com/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex1:x rdfs:label "x" .
```

## Application Name Nodes

It's handy to using the application name in some part of the
namespace, particularly when combining a series of graphs
together into a larger graph.  Each application can then
create minor variations of a particular pattern so you can
run pattern matching queries.

```python
from pathlib import Path
from bob import Node, dump
from bob.core import bind_model_namespace

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:{model_name}/")

x = Node(label="x")

dump()
```

Results in this graph:

```turtle
@prefix ex1: <urn:sample-04/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex1:00001 rdfs:label "x" .
```
