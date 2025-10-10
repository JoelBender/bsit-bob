# Subclasses

Creating a subclass of `Node` implies that instances of the subclass are
instances of an `rdfs:Class` of that type.

## Simple Subclass

This is a sample application that subclasses `Node`, and then creates an
additional subclass to refine the parent class.  This uses the default
'example' namespace for definitions of the `Thing1` and `Thing2` classes:

```python
from bob import Node, dump

class Thing1(Node):
    pass

class Thing2(Thing1):
    pass

x = Thing1(label="x")
y = Thing2(label="y")

dump()
```

Results in this graph:

```turtle
@prefix ex: <http://example/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

[] a ex:Thing1 ;
    rdfs:label "x" .

[] a ex:Thing1,
        ex:Thing2 ;
    rdfs:label "y" .
```

## Equipment Subclasses

The classes defined in `Bob` are the most basic versions of the
classes in `ASHRAE 223` and are designed to be extended to be
more opinionated versions.  For example, subclassing `Equipment`
would create a special sub-type of equipment with its own attributes:

```python
from bob import Equipment, dump

class Thing1(Equipment):
    pass

class Thing2(Thing1):
    pass

x = Thing1(label="x")
y = Thing2(label="y")

dump()
```

Results in this graph:

```turtle
@prefix ex: <http://example/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix s223: <http://data.ashrae.org/standard223#> .

[] a s223:Connectable,
        s223:Equipment,
        ex:Thing1 ;
    rdfs:label "x" .

[] a s223:Connectable,
        s223:Equipment,
        ex:Thing1,
        ex:Thing2 ;
    rdfs:label "y" .
```

This shows that [s223:Equipment](https://defs.open223.info/#s223:Equipment)
is a subclass of
[s223:Connectable](<https://defs.open223.info/#s223:Connectable>) and
any subclass of `s223:Equipment` is therefore also "connectable".
