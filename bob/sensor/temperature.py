from typing import Any

from rdflib import URIRef

from ..core import (
    BOB,
    QUANTITYKIND,
    S223,
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

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        if "hasUnit" not in _property_kwargs:
            raise ValueError(
                "You must provide hasUnit when defining a temperature sensor"
            )
        if "ofMedium" not in _property_kwargs:
            raise ValueError(
                "You must provide ofMedium when defining a temperature sensor"
            )

        super().__init__(**_sensor_kwargs)

        self.observes = Temperature(
            # isObservedBy=self,
            label=f"{self.label}.Temperature",
            **_property_kwargs,
        )


class AirTemperatureSensor(TemperatureSensor):
    def __init__(self, **kwargs):
        super().__init__(ofMedium=Air, **kwargs)


class WaterTemperatureSensor(TemperatureSensor):
    def __init__(self, **kwargs):
        super().__init__(ofMedium=Water, **kwargs)
