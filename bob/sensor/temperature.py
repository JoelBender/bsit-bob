from typing import Any, Dict

from rdflib import URIRef

from ..core import (
    BOB,
    QUANTITYKIND,
    S223,
    UNIT,
    PropertyReference,
    Setpoint,
)
from ..enum import Air, Water
from ..properties import Temperature
from .sensor import Sensor, split_kwargs

_namespace = BOB


class TemperatureSetpoint(Setpoint):
    _class_iri = S223.Setpoint
    hasQuantityKind: URIRef = QUANTITYKIND.Temperature
    hasUnit: URIRef


class TemperatureSensor(Sensor):
    _class_iri = S223.TemperatureSensor
    observes: PropertyReference  # Temperature

    def __init__(self, config: dict[str, Any] = {}, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        if "hasUnit" not in _property_kwargs:
            _sensor_kwargs["hasUnit"] = UNIT.DEG_C
            #raise ValueError(
            #    "You must provide hasUnit when defining a temperature sensor"
            #)
        if "ofMedium" not in _property_kwargs:
            raise ValueError(
                "You must provide ofMedium when defining a temperature sensor",
            )

        observed_prop = Temperature(
            # isObservedBy=self,
            label="observed_property",
            **_property_kwargs,
        )

        _sensor_kwargs["observed_property"] = observed_prop

        super().__init__(config=config, **_sensor_kwargs)


class AirTemperatureSensor(TemperatureSensor):
    def __init__(self, config: dict[str, Any] = {},**kwargs):
        super().__init__(config=config, ofMedium=Air, **kwargs)


class WaterTemperatureSensor(TemperatureSensor):
    def __init__(self, config: dict[str, Any] = {}, **kwargs):
        super().__init__(config=config,ofMedium=Water, **kwargs)
