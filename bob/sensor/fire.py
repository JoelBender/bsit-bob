from typing import Any


from ..connections.controlsignal import OnOffSignalOutletConnectionPoint
from ..core import (
    BOB,
    S223,
    PropertyReference,
)
from ..enum import Air
from ..properties import SmokePresence
from .sensor import Sensor, split_kwargs

_namespace = BOB


class SmokeDetectionSensor(Sensor):
    _class_iri = S223.Sensor
    observes: PropertyReference  # Temperature
    dryContactOutlet: OnOffSignalOutletConnectionPoint

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        if "hasUnit" not in _property_kwargs:
            raise ValueError(
                "You must provide hasUnit when defining a smoke detection sensor"
            )
        if "ofMedium" not in _property_kwargs:
            raise ValueError(
                "You must provide ofMedium when defining a smoke detection sensor"
            )

        super().__init__(**_sensor_kwargs)

        self.observes = SmokePresence(
            # isObservedBy=self,
            label=f"{self.label}.SmokeDetection",
            ofMedium=Air,
            **_property_kwargs,
        )
