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
from ..properties import Flow
from .sensor import Sensor, split_kwargs

_namespace = BOB


class FlowSetpoint(Setpoint):
    _class_iri = S223.Setpoint
    hasQuantityKind: URIRef = QUANTITYKIND.VolumeFlowRate
    hasUnit: URIRef


class FlowSensor(Sensor):
    _class_iri = S223.Sensor
    observes: PropertyReference  # Flow

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)

        self.observes = Flow(
            # isObservedBy=self,
            label=f"{self.label}.Flow",
            **_property_kwargs,
        )


class AirFlowSensor(FlowSensor):
    _class_iri = S223.Sensor

    # typical unit : hasUnit=UNIT["FT3-PER-MIN"]
    def __init__(self, **kwargs):
        super().__init__(ofMedium=Air, **kwargs)


class WaterFlowSensor(FlowSensor):
    _class_iri = S223.Sensor

    # typical unit : hasUnit=UNIT["GAL_UK-PER-MIN"]
    def __init__(self, **kwargs):
        super().__init__(ofMedium=Water, **kwargs)
