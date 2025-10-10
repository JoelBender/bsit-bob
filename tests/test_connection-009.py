from pathlib import Path

from header import ttl_test_header

from bob.core import (
    bind_model_namespace,
    dump,
    data_graph,
    schema_graph,
)
from bob.equipment.network.switch import PoESwitch, EthernetSwitch

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


# Test if I can connect PoE to Ethernet
def test_PoE(bob_fixture):
    switch1 = PoESwitch(label="PoE Switch 1", ports=5, data_rate=1000)
    switch2 = EthernetSwitch(label="Ethernet Switch 1", ports=5, data_rate=1000)

    switch1.port1 >> switch2.port1

    dump(
        data_graph,
        filename=f"tests/ttl/{model_name}.data.ttl",
        header=ttl_test_header(model_name),
    )

    dump(
        schema_graph,
        filename=f"tests/ttl/{model_name}.schema.ttl",
        header=ttl_test_header(model_name),
    )
