from typing import Any, Dict


from bob.functions import Function
from bob.properties.ratio import Percent
from bob.properties.states import OnOffStatus

from ..core import (
    S223,
    PropertyReference,
)
from ..enum import Light
from ..properties import Count, Motion
from .sensor import Sensor, split_kwargs

_namespace = S223


class OccupancySensor(Sensor):
    _class_iri = S223.Sensor


class OccupantMotionSensor(OccupancySensor):
    _class_iri = S223.OccupantMotionSensor
    # measuresMedium: Medium = Light
    observes: PropertyReference  # Movement

    def __init__(self, config: Dict[str, Any] = {}, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        observes_prop = Motion(
            label="observed_property",  # needs more focus
            ofMedium=Light.Infrared,
            **_property_kwargs,
        )
        _sensor_kwargs["observed_property"] = observes_prop

        super().__init__(config=config, **_sensor_kwargs)


class OccupantCounterSensor(OccupancySensor):
    _class_iri = S223.Sensor
    # measuresMedium: Medium = Light
    occupantCount = Count

    def __init__(self, config: Dict[str, Any] = {}, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        observed_property = Count(
            label="observed_property",
            **_property_kwargs,
        )
        _sensor_kwargs["observed_property"] = observed_property

        super().__init__(config=config, **_sensor_kwargs)

        counter = Function(label="Counting Function From Sensor")
        counter.hasInput(self.observedProperty)
        counter.hasOutput(self.occupantCount)


# TODO : NOPE.... should observe something and produce a presence property
class OccupantPresenceSensor(OccupancySensor):
    _class_iri = S223.OccupantPresenceSensor
    # measuresMedium: Medium = Light
    observes: PropertyReference  # Intrusion...good for Windows and doors

    def __init__(self, config: Dict[str, Any] = {}, **kwargs: Any) -> None:
        _sensor_kwargs, _measure_kwargs = split_kwargs(kwargs)

        observed_prop = OnOffStatus(
            label="observed_property",  # needs more focus
            **_measure_kwargs,
        )
        _sensor_kwargs["observed_property"] = observed_prop

        super().__init__(config=config, **_sensor_kwargs)


class PositionSensor(Sensor):
    _class_iri = S223.Sensor
    observes: PropertyReference  # Movement

    def __init__(self, config: Dict[str, Any] = {}, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        observed_property = Percent(
            label="observed_property",  # needs more focus
            **_property_kwargs,
        )

        _sensor_kwargs["observed_property"] = observed_property

        super().__init__(config=config, **_sensor_kwargs)
