from typing import Any, Dict

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

    def __init__(self, config: Dict[str, Any] = {}, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        observed_prop = Flow(
            label="observed_property",
            **_property_kwargs,
        )
        _sensor_kwargs["observed_property"] = observed_prop

        super().__init__(config=config, **_sensor_kwargs)


class AirFlowSensor(FlowSensor):
    _class_iri = S223.Sensor

    # typical unit : hasUnit=UNIT["FT3-PER-MIN"]
    def __init__(self, config: Dict[str, Any] = {}, **kwargs: Any) -> None:
        super().__init__(config=config, ofMedium=Air, **kwargs)


class WaterFlowSensor(FlowSensor):
    _class_iri = S223.Sensor

    # typical unit : hasUnit=UNIT["GAL_UK-PER-MIN"]
    def __init__(self, config: Dict[str, Any] = {}, **kwargs: Any) -> None:
        super().__init__(config=config, ofMedium=Water, **kwargs)
