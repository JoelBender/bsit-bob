from typing import Dict

from bob.properties.states import NormalAlarmStatus

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...core import P223, Equipment
from ...sensor.particle import (
    CoarseParticulateSensor,
    FineParticulateSensor,
    UltraFineParticulateSensor,
)

_namespace = P223


particlecounter_template = {
    "properties": {"alarmStatus": NormalAlarmStatus},
    "sensors": {
        ("label_of_sensor_1", CoarseParticulateSensor): {
            "hasExternalReference": "bacnet://",
            "comment": "Coarse Particles 10.0um or less",
        },
        ("label_of_sensor_2", FineParticulateSensor): {
            "hasExternalReference": "bacnet://",
            "comment": "Fine Particles 2.5um or less",
        },
        ("label_of_sensor_3", UltraFineParticulateSensor): {
            "hasExternalReference": "bacnet://",
            "comment": "Ultra Fine Particles 1.0um or less",
        },
    },
}


class ParticleCounter(Equipment):
    _class_iri = P223.ParticleCounter
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint

    def __init__(self, config: Dict = particlecounter_template, **kwargs):
        config["properties"] = config.get(
            "properties", particlecounter_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
