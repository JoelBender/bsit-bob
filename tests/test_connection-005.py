from pathlib import Path

import pytest
from .header import ttl_test_header

from bob.core import (
    Connection,
    Equipment,
    InletConnectionPoint,
    OutletConnectionPoint,
    bind_model_namespace,
    dump,
)

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_wrong_direction(bob_fixture):
    d1 = Equipment(label="d1")
    cp1 = OutletConnectionPoint(d1, label="d1.out")

    d2 = Equipment(label="d2")
    cp2 = InletConnectionPoint(d2, label="d2.in")

    c = Connection()

    with pytest.raises(TypeError):
        c >> cp1

    with pytest.raises(TypeError):
        cp2 >> c

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
