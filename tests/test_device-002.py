from pathlib import Path

from bob.core import bind_model_namespace, dump
from bob.equipment.hvac.boiler import Boiler
from bob.equipment.hvac.coil import (
    ChilledWaterCoil,
    ElectricalHeatingCoil,
    HotWaterCoil,
)

from .header import ttl_test_header

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_create_more_complex_Equipment(bob_fixture):
    boiler = Boiler(label="HWB-1", comment="Hot Water Boiler")

    hot_water_coil = HotWaterCoil(label="Hot Water Coil")
    chilled_water_coil = ChilledWaterCoil(label="Chilled Water Coil")
    electrical_heating_coil = ElectricalHeatingCoil(label="Electrical Heat ing Coil")

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
