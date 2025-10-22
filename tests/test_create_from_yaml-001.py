from pathlib import Path

from bob.core import bind_model_namespace, dump
from bob.template import (
    EquipmentFromTemplate,
    config_from_yaml,
)

from .header import ttl_test_header

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_create_equipment_with_junction_from_yaml(bob_fixture):
    yaml_path = Path(__file__).parent / "yaml_templates" / "equipmentWithJunction.yaml"
    c = config_from_yaml(str(yaml_path))

    ahu = EquipmentFromTemplate(config=c)

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
