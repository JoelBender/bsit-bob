# Properties

Python classes in **Bob** are like other classes, they can have attributes
and methods that do not have an impact on the generated graph.

```python
from pathlib import Path
from bob import Node, dump
from bob.core import Property, bind_model_namespace

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex1", f"urn:{model_name}/")

class Thing(Node):
    someAttr: int

x = Thing(label="x")
x.someAttr = 12

dump()
```

Results in this graph:

```turtle
@prefix ex1: <urn:property-01/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex1:00001 a ex1:Thing ;
    rdfs:label "x" .
```

## Special Attributes

Through annotations, Python classes in **Bob** can reference special types
of classes in **ASHRAE 223**. One of those is the `Property` class:

```python
from pathlib import Path
from bob import Node, dump
from bob.core import Property, bind_model_namespace

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex2", f"urn:{model_name}/")

class Thing(Node):
    someAttr: Property

x = Thing(label="x")
x.someAttr = 12

dump()
```

In the resulting graph note that the `ex2:someAttr` is a sub-property of
`s223:hasProperty`, both predicates reference the same object of type
`s223:Property` which references the value.  The integer value in the
application has been turned into the equivalent literal in the graph:

```turtle
@prefix ex2: <urn:property-02/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix s223: <http://data.ashrae.org/standard223#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex2:00001 a ex1:Thing ;
    rdfs:label "x" ;
    s223:hasProperty ex1:00002 ;
    ex2:someAttr ex2:00002 .

ex2:00002 a s223:Property ;
    s223:hasValue 12 .
```

## Properties by Reference

There are modeling situations where two different things refer to the
same property (usually with two different attributes/predicates) and
**Bob** will associate the two references to the same object:

```python
from pathlib import Path
from bob import Node, dump
from bob.core import Property, bind_model_namespace

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex2", f"urn:{model_name}/")

class Thing(Node):
    someAttr: Property

x = Thing(label="x")
x.someAttr = 12

y = Thing(label="y")
y.someAttr = x.someAttr

dump()
```

Results in the following graph:

```turtle
@prefix ex2: <urn:property-03/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix s223: <http://data.ashrae.org/standard223#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex2:00001 a ex2:Thing ;
    rdfs:label "x" ;
    s223:hasProperty ex2:00002 ;
    ex2:someAttr ex2:00002 .

ex2:00002 a s223:Property ;
    s223:hasValue 12 .

ex2:00003 a ex2:Thing ;
    rdfs:label "y" ;
    s223:hasProperty ex2:00002 ;
    ex2:someAttr ex2:00002 .
```

While `y` was created after `x`, the intermediate `Property` object was also
created, so `y` has the IRI `ex2:00003`.

## Predefined Properties

**Bob** has a number of predefined properties that can be used directly or as
an example of how to define model specific properties.  For example, `HP` is
a class for horsepower that is defined in [QUDT](https://qudt.org/vocab/unit/HP.html):

```python
from pathlib import Path
from bob import Node, dump
from bob.core import Equipment, bind_model_namespace
from bob.properties.force import HP

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex4", f"urn:{model_name}/")

class Thing(Equipment):
    hp: HP

x = Thing(label="x")
x.hp = 100.0

dump()
```

In the following graph note that the `Property` instance is not just an
`223:QuantifiableObservableProperty` but also an instance of `bob:HP`
which shows that the `HP` type is defined in **Bob**:

```turtle
@prefix bob: <http://data.ashrae.org/standard223/si-builder#> .
@prefix ex4: <urn:property-04/> .
@prefix qudt: <http://qudt.org/schema/qudt/> .
@prefix qudtqk: <http://qudt.org/vocab/quantitykind/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix s223: <http://data.ashrae.org/standard223#> .
@prefix unit: <http://qudt.org/vocab/unit/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex4:00001 a s223:Connectable,
        s223:Equipment,
        ex4:Thing ;
    rdfs:label "x" ;
    s223:hasProperty ex4:00002 ;
    ex4:hp ex4:00002 .

ex4:00002 a s223:ObservableProperty,
        s223:Property,
        s223:QuantifiableObservableProperty,
        s223:QuantifiableProperty,
        bob:HP ;
    s223:hasValue 100.0 ;
    qudt:hasQuantityKind qudtqk:Power ;
    qudt:hasUnit unit:HP .
```


