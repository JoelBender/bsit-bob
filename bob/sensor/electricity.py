from typing import Any


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
    observes: PropertyReference
    hasMinRange: PropertyReference
    hasMaxRange: PropertyReference

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        if "ofMedium" not in _property_kwargs:
            # raise ValueError(
            #    "You must provide ofMedium when defining a Voltage Sensor"
            # )
            _property_kwargs["ofMedium"] = Electricity

        super().__init__(**_sensor_kwargs)

        self.observes = Volts(
            # isObservedBy=self,
            label=f"{self.label}.Voltage",
            **_property_kwargs,
        )


class CurrentSensor(Sensor):
    _class_iri = S223.Sensor
    observes: PropertyReference
    hasMinRange: PropertyReference
    hasMaxRange: PropertyReference

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        if "ofMedium" not in _property_kwargs:
            _property_kwargs["ofMedium"] = Electricity

        super().__init__(**_sensor_kwargs)

        self.observes = Amps(
            # isObservedBy=self,
            label=f"{self.label}.Amps",
            **_property_kwargs,
        )


class DryContactSensor(Sensor):
    _class_iri = S223.Sensor
    observes: PropertyReference

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        if "ofMedium" not in _property_kwargs:
            _property_kwargs["ofMedium"] = Electricity

        super().__init__(**_sensor_kwargs)

        self.observes = OnOffStatus(
            # isObservedBy=self,
            label=f"{self.label}.Amps",
            **_property_kwargs,
        )
