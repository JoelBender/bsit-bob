# More Connections

The `>>` operator can also be used to connect a thing to a list of things.
It is common to create graph nodes from a CSV file or some other database
source and then filter them into groups.

For example, assume that `thing1` is the output of an air handling unit that
provides conditioned air to all of the rooms on the first floor of a building.
The application can read in the list of rooms, filter those that are on the
first floor in a `list_of_thing2`, and then connect them to `thing1`.


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

thing1 = Thing1(label="thing1")

list_of_thing2 = [Thing2(label=f"thing{n}") for n in range(10)]

thing1 >> list_of_thing2

dump()
```

This creates a detailed graph of all of the air flows.
