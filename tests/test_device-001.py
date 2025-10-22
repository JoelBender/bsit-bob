from pathlib import Path

from bob.core import Equipment, Property, bind_model_namespace, dump

from .header import ttl_test_header

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_create_Equipment(bob_fixture):
    d1 = Equipment(label="d1")

    class TestEquipment2(Equipment):
        pass

    d2 = TestEquipment2(label="d2")

    class TestProperty(Property):
        pass

    class TestEquipment3(Equipment):
        prop: TestProperty

    d3 = TestEquipment3(label="d3")

    d3.prop = TestProperty(1)

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
