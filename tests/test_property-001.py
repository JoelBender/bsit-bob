from pathlib import Path

from bob.core import (
    ActuatableProperty,
    ObservableProperty,
    Property,
    QuantifiableProperty,
    bind_model_namespace,
    dump,
)

from .header import ttl_test_header

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_create_properties(bob_fixture):
    p1 = Property(1)

    p2 = ActuatableProperty(2)

    p3 = ObservableProperty("green")

    from bob.core import QUDT

    p4 = QuantifiableProperty(4.5, hasUnit=QUDT.DEG_F)

    p6 = ObservableProperty("green", label="color")

    class TestProperty1(Property):
        pass

    p7 = TestProperty1(7)

    class TestProperty2(Property):
        label = "test 2"

    p8 = TestProperty2(8)

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
