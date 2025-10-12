# Schema Graph

In addition to creating data graphs, `Bob` will also describe the model
being designed and built in a schema graph.  The schema graph can be used
to validate instances of a data graph.

```python
from bob import Node, schema_graph, dump

class Thing1(Node):
    pass

class Thing2(Thing1):
    pass

x = Thing1(label="x")
y = Thing2(label="y")

dump(schema_graph)
```

Results in this graph, note that the label names include the name of
the module that defined the class which is useful for debugging:

```turtle
@prefix ex: <http://example/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex:Thing1 a rdfs:Class ;
    rdfs:label "__main__.Thing1" .

ex:Thing2 a rdfs:Class ;
    rdfs:label "__main__.Thing2" ;
    rdfs:subClassOf ex:Thing1 .
```
