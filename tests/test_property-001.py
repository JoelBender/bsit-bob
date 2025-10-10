from pathlib import Path

from header import ttl_test_header

from bob.core import (
    bind_model_namespace,
    dump,
    ActuatableProperty,
    ObservableProperty,
    Property,
    QuantifiableProperty,
)

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_create_properties(bob_fixture):
    p1 = Property(1) #noqa F841

    p2 = ActuatableProperty(2) #noqa F841

    p3 = ObservableProperty("green") #noqa F841
 
    from bob.core import QUDT

    p4 = QuantifiableProperty(4.5, hasUnit=QUDT.DEG_F) #noqa F841

    p6 = ObservableProperty("green", label="color") #noqa F841

    class TestProperty1(Property):
        pass

    p7 = TestProperty1(7) #noqa F841

    class TestProperty2(Property):
        label = "test 2"

    p8 = TestProperty2(8) #noqa F841

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
