from typing import Any

from bob.properties.states import OnOffStatus

from ..core import (
    S223,
    PropertyReference,
)
from .sensor import Sensor, split_kwargs

_namespace = S223


class IntrusionSensor(Sensor):
    _class_iri = S223.Sensor
    observes: PropertyReference  # OnOffStatus

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)
        self.observes = OnOffStatus(
            label=f"{self.label}.intrusion_status", **_property_kwargs
        )
