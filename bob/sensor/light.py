from typing import Any


from bob.properties.states import DaylightDetected

from ..core import (
    BOB,
    S223,
    PropertyReference,
)
from .sensor import Sensor, split_kwargs
from ..enum import Light

_namespace = BOB


class DaylightSensor(Sensor):
    _class_iri = S223.Sensor
    # measuresMedium: Medium = Light
    observes: PropertyReference  # visible light level -- units?

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)

        self.observes = DaylightDetected(
            # isObservedBy=self,
            label=f"{self.label}.Daylight",
            ofMedium=Light.Visible,
            **_property_kwargs,
        )
