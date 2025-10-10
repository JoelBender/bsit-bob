from pathlib import Path

from .header import ttl_test_header

from bob.core import bind_model_namespace, dump
from bob.template import (
    SystemFromTemplate,
    config_from_yaml,
)

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_open_yaml(bob_fixture):
    yaml_path = Path(__file__).parent / "yaml_templates" / "ahuAsSystem.yaml"
    c = config_from_yaml(str(yaml_path))
    assert c is not None
    assert isinstance(c, dict)
    assert c["params"]["label"] == "AHU"
    assert c["params"]["comment"] == "AHU delivering air to 2 VAV boxes"


def test_create_system_from_yaml(bob_fixture):
    yaml_path = Path(__file__).parent / "yaml_templates" / "ahuAsSystem.yaml"
    c = config_from_yaml(str(yaml_path))

    ahu = SystemFromTemplate(config=c)

    assert len(ahu._junctions) == 4
    assert len(ahu._equipment) == 9
    assert len(ahu._sensors) == 1

    assert ahu["SA-T"].hasObservationLocation == ahu["SupplyAirDuct"].supplyAir

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
