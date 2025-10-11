from pathlib import Path

from bob.core import bind_model_namespace, dump
from bob.equipment.hvac.damper import Damper

from .header import ttl_test_header

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_create_damper(bob_fixture):
    d1 = Damper(label="Electrical Proportional Actuated Damper")

    # d2 = ElectricalActuatedOnOffDamper(label="Electrical OnOff Actuated Damper")

    # d3 = PneumaticActuatedOnOffDamper(label="Pneumatic OnOff Actuated Damper")

    # d4 = PneumaticActuatedProportionalDamper(
    #    label="Pneumatic Proportional Actuated Damper"
    # )

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
