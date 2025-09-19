from typing import Any


from bob.producer.causality import Causality
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

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)

        self.observes = Motion(
            # isObservedBy=self,
            label=f"{self.label}.OccupantMotion",
            ofMedium=Light.Infrared,
            **_property_kwargs,
        )


# That should provide a producer of count value
class OccupantCounterSensor(OccupantMotionSensor):
    _class_iri = S223.Sensor
    # measuresMedium: Medium = Light
    occupantCount = Count

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)
        self.OccupantCount = Count(
            label=f"{self.label}.OccupantCount",
            **_property_kwargs,
        )
        counter = Causality(label="countProducer")
        counter.cause_input << self.observedProperty
        counter.effect_output >> self.occupantCount
        self > counter


# TODO : NOPE.... should observe something and produce a presence property
class OccupantPresenceSensor(OccupancySensor):
    _class_iri = S223.OccupantPresenceSensor
    # measuresMedium: Medium = Light
    observes: PropertyReference  # Intrusion...good for Windows and doors

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _measure_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)
        self.observes = OnOffStatus(
            # isObservedBy=self,
            label=f"{self.label}.OccupantPresence",
            **_measure_kwargs,
        )


class PositionSensor(Sensor):
    _class_iri = S223.Sensor
    observes: PropertyReference  # Movement

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)

        self.observes = Percent(
            # isObservedBy=self,
            label=f"{self.label}.Position",
            **_property_kwargs,
        )
