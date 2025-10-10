from pathlib import Path

from .header import ttl_test_header

from bob.core import Equipment, Junction, bind_model_namespace, dump
from bob.connections.air import AirInletConnectionPoint

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class Thing(Equipment):
    airInlet: AirInletConnectionPoint


def test_junction_mapsTo_many(bob_fixture):
    """
    Make a thing `x` that has two component things `y` and `z` that have their
    inputs coming from a junction via a single connection, the junction is
    mapped to the container `x` input.
    """
    x = Thing(label="x")
    y = Thing(label="y")
    x > y
    z = Thing(label="z")
    x > z
    j = Junction(label="j")
    x > j

    # junction connected to the two components
    j >> [y, z]

    # make an additional connection point for the junction and map it to
    # the container
    j.maps_to(x.airInlet)

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
