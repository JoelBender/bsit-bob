from typing import Any, Dict


from ..connections.controlsignal import OnOffSignalOutletConnectionPoint
from ..core import (
    BOB,
    S223,
    PropertyReference,
)
from ..properties import SmokePresence
from .sensor import Sensor, split_kwargs

_namespace = BOB


class SmokeDetectionSensor(Sensor):
    _class_iri = S223.Sensor
    observes: PropertyReference  # Temperature
    dryContactOutlet: OnOffSignalOutletConnectionPoint

    def __init__(self, config: Dict[str, Any] = {}, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        if "hasUnit" not in _property_kwargs:
            raise ValueError(
                "You must provide hasUnit when defining a smoke detection sensor"
            )
        if "ofMedium" not in _property_kwargs:
            raise ValueError(
                "You must provide ofMedium when defining a smoke detection sensor"
            )

        observed_prop = SmokePresence(
            label="observed_property",
            **_property_kwargs,
        )
        _sensor_kwargs["observed_property"] = observed_prop

        super().__init__(config=config, **_sensor_kwargs)

