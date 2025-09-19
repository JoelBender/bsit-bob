from __future__ import annotations

from typing import Any

from rdflib import URIRef

from ..core import (
    BOB,
    QUANTITYKIND,
    S223,
    UNIT,
    PropertyReference,
    Setpoint,
)
from ..enum import Air
from ..properties import RelativeHumidity
from .sensor import Sensor, split_kwargs

_namespace = BOB


class HumiditySetpoint(Setpoint):
    _class_iri = S223.Setpoint
    hasQuantityKind: URIRef = QUANTITYKIND.RelativeHumidity
    hasUnit: URIRef = UNIT.PERCENT_RH


class HumiditySensor(Sensor):
    _class_iri = S223.HumiditySensor
    observes: PropertyReference  # Temperature

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        if "ofMedium" not in _property_kwargs:
            raise ValueError(
                "You must provide ofMedium when defining a humidity sensor"
            )

        super().__init__(**_sensor_kwargs)

        self.observes = RelativeHumidity(
            # isObservedBy=self,
            label=f"{self.label}.Humidity",
            **_property_kwargs,
        )


class AirHumiditySensor(HumiditySensor):
    """
    Air humidity sensor. Can model room sensor or duct sensor.
    """

    _class_iri = S223.HumiditySensor

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        super().__init__(ofMedium=Air, **kwargs)
