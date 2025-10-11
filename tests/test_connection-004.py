from pathlib import Path

from bob import core
from bob.core import (
    Connection,
    Equipment,
    InletConnectionPoint,
    OutletConnectionPoint,
    bind_model_namespace,
    dump,
)
from bob.enum import Air

from .header import ttl_test_header

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")
core.INCLUDE_INVERSE = True


def test_connection_with_direction(bob_fixture):
    d1 = Equipment(label="d1")
    cp1 = OutletConnectionPoint(d1, label="d1.out", hasMedium=Air)

    d2 = Equipment(label="d2")
    cp2 = InletConnectionPoint(d2, label="d2.in", hasMedium=Air)

    c = Connection(hasMedium=Air)
    cp1 >> c >> cp2
    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
