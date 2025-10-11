from typing import Any, Dict

from ..core import (
    BOB,
    S223,
    PropertyReference,
)
from ..enum import Electricity
from ..properties import Amps, OnOffStatus, Volts
from .sensor import Sensor, split_kwargs

_namespace = BOB


class VoltageSensor(Sensor):
    _class_iri = S223.Sensor
    observes: PropertyReference  # type: ignore[assignment]
    hasMinRange: PropertyReference  # type: ignore[assignment]
    hasMaxRange: PropertyReference  # type: ignore[assignment]

    def __init__(self, config: dict[str, Any] = {}, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        if "ofMedium" not in _property_kwargs:
            # raise ValueError(
            #    "You must provide ofMedium when defining a Voltage Sensor"
            # )
            _property_kwargs["ofMedium"] = Electricity

        observed_prop = Volts(
            label="observed_property",
            **_property_kwargs,
        )
        _sensor_kwargs["observed_property"] = observed_prop

        super().__init__(config=config, **_sensor_kwargs)


class CurrentSensor(Sensor):
    _class_iri = S223.Sensor
    observes: PropertyReference  # type: ignore[assignment]
    hasMinRange: PropertyReference  # type: ignore[assignment]
    hasMaxRange: PropertyReference  # type: ignore[assignment]

    def __init__(self, config: dict[str, Any] = {}, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        if "ofMedium" not in _property_kwargs:
            _property_kwargs["ofMedium"] = Electricity

        observed_prop = Amps(
            label="observed_property",
            **_property_kwargs,
        )
        _sensor_kwargs["observed_property"] = observed_prop

        super().__init__(config=config, **_sensor_kwargs)

class DryContactSensor(Sensor):
    _class_iri = S223.Sensor
    observes: PropertyReference

    def __init__(self, config: dict[str, Any] = {}, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        if "ofMedium" not in _property_kwargs:
            _property_kwargs["ofMedium"] = Electricity

        observed_prop = OnOffStatus(
            label="observed_property",
            **_property_kwargs,
        )
        _sensor_kwargs["observed_property"] = observed_prop

        super().__init__(config=config, **_sensor_kwargs)
