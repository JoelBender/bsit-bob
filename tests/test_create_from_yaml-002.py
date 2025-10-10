from pathlib import Path

from .header import ttl_test_header

from bob.core import bind_model_namespace, dump
from bob.template import (
    EquipmentFromTemplate,
    config_from_yaml,
)

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_create_equipment_from_yaml(bob_fixture):
    yaml_path = Path(__file__).parent / "yaml_templates" / "ahuAsEquipment.yaml"
    c = config_from_yaml(str(yaml_path))

    ahu = EquipmentFromTemplate(config=c) #noqa F841

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
