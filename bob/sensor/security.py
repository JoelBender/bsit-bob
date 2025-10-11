from typing import Any, Dict

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

    def __init__(self, config: dict[str, Any] = {}, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        observed_prop = OnOffStatus(
            label="observed_property", **_property_kwargs,
        )

        _sensor_kwargs["observed_property"] = observed_prop
        super().__init__(config=config, **_sensor_kwargs)
