from pathlib import Path

from header import ttl_test_header

from bob.core import Equipment, Junction, bind_model_namespace, dump
from bob.connections.air import AirInletConnectionPoint, AirOutletConnectionPoint

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class InletThing(Equipment):
    airInlet: AirInletConnectionPoint


class OutletThing(Equipment):
    airOutlet: AirOutletConnectionPoint


def test_junction_connections(bob_fixture):
    """
    Create a thing `x` with an outlet connection point and two things `y` and
    `z` with inlets.  Connect the outlet of `x` to the junction with one
    connection and the junction to both inlets each with their own connection.
    """
    x = OutletThing(label="x")
    y = InletThing(label="y")
    z = InletThing(label="z")

    j = Junction(label="j")
    x >> j
    j >> y
    j >> z

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
