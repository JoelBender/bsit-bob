from pathlib import Path

from bob.connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from bob.core import Junction, bind_model_namespace, dump
from bob.template import SystemFromTemplate, config_from_yaml

from .header import ttl_test_header

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_junction_from_yaml(bob_fixture):
    """We need to be able to create connection point on demand so we can relate to them
    in the template
    """
    yaml_path = Path(__file__).parent / "yaml_templates" / "junction.yaml"
    c = config_from_yaml(str(yaml_path))
    print(c)
    thing = SystemFromTemplate(config=c)

    assert isinstance(thing["MixedAir"], Junction)
    assert isinstance(thing["MixedAir"].returnAir, AirInletConnectionPoint)
    assert isinstance(thing["MixedAir"].outdoorAir, AirInletConnectionPoint)
    assert isinstance(thing["MixedAir"].mixedAir, AirOutletConnectionPoint)


    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
