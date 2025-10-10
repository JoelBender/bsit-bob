from pathlib import Path
from typing import Dict
from header import ttl_test_header

from bob.core import bind_model_namespace, dump, Equipment, SCRATCH

from bob.sensor.particle import (
    CoarseParticulateSensor,
    FineParticulateSensor,
    UltraFineParticulateSensor,
)
from bob.connections.air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
)
from bob.template import template_update, configure_relations

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class ParticleCounter(Equipment):
    """
    This Equipment is normally defined in Scratch and duplicated here for testing purposes.
    It represents a particle counter that measures particulate matter in the air.
    """
    _class_iri = SCRATCH.ParticleCounter
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _relations)

def test_create_particle_counter(bob_fixture):
    particlecounter_config = {
        "properties": {},
        "sensors": {
            ("coarse_sensor", CoarseParticulateSensor): {
                # "hasExternalReference": "bacnet://1/analog-value,1/present-value",
            },
            ("fine_sensor", FineParticulateSensor): {
                # "hasExternalReference": "bacnet://1/analog-input,2/present-value",
            },
            ("ultrafine_sensor", UltraFineParticulateSensor): {
                # "hasExternalReference": "bacnet://1/analog-input,3/present-value",
            },
        },
    }

    pm = ParticleCounter( #noqa F841
        label="PM-1",
        comment="Particulate Measurement Station AKA particle counter",
        config=particlecounter_config,
    )

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
