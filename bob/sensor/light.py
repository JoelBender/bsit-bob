from typing import Any, Dict

from bob.properties.states import DaylightDetected

from ..core import (
    BOB,
    S223,
    PropertyReference,
)
from ..enum import Light
from .sensor import Sensor, split_kwargs

_namespace = BOB


class DaylightSensor(Sensor):
    _class_iri = S223.Sensor
    # measuresMedium: Medium = Light
    observes: PropertyReference  # visible light level -- units?

    def __init__(self, config: dict[str, Any] = {}, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        observed_property = DaylightDetected(
            label="observed_property",  # needs more focus
            ofMedium=Light.Visible,
            **_property_kwargs,
        )
        _sensor_kwargs["observed_property"] = observed_property

        super().__init__(config=config, **_sensor_kwargs)
