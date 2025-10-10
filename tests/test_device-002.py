from pathlib import Path

from header import ttl_test_header

from bob.core import bind_model_namespace, dump
from bob.equipment.hvac.boiler import Boiler
from bob.equipment.hvac.coil import (
    ChilledWaterCoil,
    ElectricalHeatingCoil,
    HotWaterCoil,
)

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_create_more_complex_Equipment(bob_fixture):
    boiler = Boiler(label="HWB-1", comment="Hot Water Boiler") #noqa F841

    hot_water_coil = HotWaterCoil(label="Hot Water Coil") #noqa F841
    chilled_water_coil = ChilledWaterCoil(label="Chilled Water Coil") #noqa F841
    electrical_heating_coil = ElectricalHeatingCoil(label="Electrical Heat ing Coil") #noqa F841

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
