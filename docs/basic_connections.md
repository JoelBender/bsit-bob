# Connections

Many types of things in **ASHRAE 223** are "connectable" which means that the
output of one thing is associated with the input of something else.  These
connections specified in semantic layers.  Starting with this simple model:

```python
from pathlib import Path
from bob import Equipment, dump
from bob.core import bind_model_namespace
from bob.connections.air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
)

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex1", f"urn:{model_name}/")

class Thing1(Equipment):
    airOut: AirOutletConnectionPoint

class Thing2(Equipment):
    airIn: AirInletConnectionPoint

Thing1(label="thing1") >> Thing2(label="thing2")

dump()
```

There are two things, `thing1` has air going out and `thing2` has air coming
in.  The `>>` operator is an instruction for **Bob** to inspect the two nodes,
find an unconnected outlet connection point of some medium, find an unconnected
inlet connection point with the same medium, and connect the two together.

Starting at the highest level of abstraction, this just describes that they
are connected in some way:

```turtle
ex1:00001 a ex1:Thing1 ;
    rdfs:label "thing1" ;
    s223:connected ex1:00003 .

ex1:00003 a ex1:Thing2 ;
    rdfs:label "thing2" ;
    s223:connected ex1:00001 .
```

```{mermaid}
graph LR
    thing1 -- connected --> thing2
    thing2 -- connected --> thing1
```

The next layer down is more specific and uses relations (predicataes) that
describe the direction of the "flow" of something:

```turtle
ex1:00001 a ex1:Thing1 ;
    s223:connectedTo ex1:00003 .

ex1:00003 a ex1:Thing2 ;
    s223:connectedFrom ex1:00001 .
```

```{mermaid}
graph LR
    thing1 -- connectedTo --> thing2
    thing2 -- connectedFrom --> thing1
```

The next semantic layer down describes the connection in more detail.  More
than two things can be connected together, e.g. the output of a pump can go
to multiple heat exchangers, or the outputs of a primary and secondary pump
can go to a distribution system.  In this case the medium is `s223:Fluid-Air`:

```turtle
ex1:00001 a ex1:Thing1 ;
    s223:connectedThrough ex1:00005 .

ex1:00003 a ex1:Thing2 ;
    s223:connectedThrough ex1:00005 .

ex1:00005 a s223:Connection ;
    s223:connectsFrom ex1:00001 ;
    s223:connectsTo ex1:00003 ;
    s223:hasMedium s223:Fluid-Air .
```

```{mermaid}
graph LR
    thing1 -- connectedThrough --> connection
    connection -- connectsFrom --> thing1
    thing2 -- connectedThrough --> connection
    connection -- connectsTo --> thing2
    connection -- hasMedium --> Fluid-Air
```

The next semantic layer down has more details about the relationship between
`thing1` and the connection, its `s223:ConnectionPoint`.  The model definition
shows that `ex1:airOut` is a specific connection point which is not only
defined using **ASHRAE 223** concepts but also the `bob:AirConnectionPoint`
that has the medium `s223:Fluid-Air`:

```turtle
ex1:00001 a ex1:Thing1 ;
    s223:hasConnectionPoint ex1:00002 ;
    ex1:airOut ex1:00002 .

ex1:00002 a s223:ConnectionPoint,
        s223:OutletConnectionPoint,
        bob:AirConnectionPoint ;
    rdfs:label "thing1.airOut" ;
    s223:connectsThrough ex1:00005 ;
    s223:hasMedium s223:Fluid-Air ;
    s223:isConnectionPointOf ex1:00001 .
```

```{mermaid}
graph LR
    thing1 -- hasConnectionPoint --> thing1.airOut
    thing1 -- ex1:airOut --> thing1.airOut
    thing1.airOut -- isConnectionPointOf --> thing1
    thing1.airOut -- connectsThrough --> connection
    thing1.airOut -- hasMedium --> Fluid-Air
```

A similar set of RDF statements are added to the model about `thing2`.