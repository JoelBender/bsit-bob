from pathlib import Path

from .header import ttl_test_header

from bob import core
from bob.core import (
    Connection,
    Equipment,
    OutletConnectionPoint,
    bind_model_namespace,
    dump,
)
from bob.enum import Air

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")
core.INCLUDE_INVERSE = True


def test_connect_from(bob_fixture):
    d1 = Equipment(label="d1")
    cp1 = OutletConnectionPoint(d1, hasMedium=Air)

    c = Connection(hasMedium=Air)
    cp1 >> c

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
