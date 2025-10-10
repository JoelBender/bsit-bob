from pathlib import Path

from .header import ttl_test_header
from rdflib import Literal

from bob.connections.electricity import (
    Electricity_600VLL_3Ph_60HzInletConnectionPoint,
    Electricity_600VLL_3Ph_60HzOutletConnectionPoint,
)
from bob.core import bind_model_namespace, dump
from bob.equipment.electricity.vfd import VFD
from bob.properties import (
    RPM,
)
from bob.properties.states import NormalAlarmStatus

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_create_vfd_from_template(bob_fixture):
    vfd_template = {
        "params": {"label": "MyVFD", "comment": "A VFD for a Big Fan"},
        "cp": {
            "electricalInlet": Electricity_600VLL_3Ph_60HzInletConnectionPoint,
            "electricalOutlet": Electricity_600VLL_3Ph_60HzOutletConnectionPoint,
        },
        "properties": {
            ("rpm", RPM): {},
            ("alarm_status", NormalAlarmStatus): {},
        },
    }
    v = VFD(config=vfd_template)
    assert type(v["rpm"]) is RPM
    assert type(v["alarm_status"]) is NormalAlarmStatus
    assert v.label == Literal("MyVFD")
    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
