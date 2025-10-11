from pathlib import Path

from bob import core
from bob.connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from bob.core import (
    BoundaryConnectionPoint,
    Equipment,
    System,
    bind_model_namespace,
    dump,
)

from .header import ttl_test_header

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")
core.INCLUDE_INVERSE = True


def test_systems_004(bob_fixture):
    class A(Equipment):
        cOut: AirOutletConnectionPoint

    class X(System):
        cOut: BoundaryConnectionPoint

    class B(Equipment):
        cIn: AirInletConnectionPoint

    class Y(System):
        cIn: BoundaryConnectionPoint

    a = A(label="a")
    x = X(label="x")
    x.cOut = a.cOut

    b = B(label="b")
    y = Y(label="y")
    y.cIn = b.cIn

    # system from system
    y << x

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
