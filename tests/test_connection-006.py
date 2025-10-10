from pathlib import Path

from header import ttl_test_header

from bob.connections import ChilledWaterConnection
from bob.core import bind_model_namespace, dump
from bob.equipment.hvac.coil import ChilledWaterCoil
from bob.equipment.hvac.fan import Fan

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_connect_chilled_water_coil(bob_fixture):
    # there is a chilled water connection, we don't know where the chilled
    # is coming from
    c = ChilledWaterConnection()

    # there is a chilled water coil (itself a system) that is a subsystem
    # of a larger context
    coil1 = ChilledWaterCoil(label="CW-Coil-1")

    # the coil gets its chilled water from the connection
    c >> coil1.chilledWaterInlet

    # there is a fan, and the air output of the fan goes into the coil
    f = Fan(label="F")
    f >> coil1.airInlet
    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
