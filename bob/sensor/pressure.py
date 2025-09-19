from typing import Any, Tuple


from bob.producer.causality import Differential
from bob.properties.force import DifferentialStaticPressure, Pressure

from ..core import (
    BOB,
    INCLUDE_INVERSE,
    S223,
    Node,
    PropertyReference,
)
from ..enum import Air, Water
from ..properties import DifferentialStaticPressure
from .sensor import Sensor, split_kwargs

_namespace = BOB  #


class PressureSensor(Sensor):
    _class_iri = S223.PressureSensor
    observes: PropertyReference  # Temperature
    # hasObservationLocation: LocationReference

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        if "hasUnit" not in _property_kwargs:
            raise ValueError("You must provide hasUnit when defining a pressure sensor")
        if "ofMedium" not in _property_kwargs:
            raise ValueError(
                "You must provide ofMedium when defining a pressure sensor"
            )

        super().__init__(**_sensor_kwargs)

        self.observes = Pressure(
            # isObservedBy=self,
            label=f"{self.label}.GaugePressure",
            **_property_kwargs,
        )


# class DifferentialStaticPressureSetpoint(Setpoint):
#    _class_iri = S223.Sensor
#    hasQuantityKind: URIRef = QUANTITYKIND.ForcePerArea
#    hasUnit: URIRef


class DifferentialStaticPressureSensor(Sensor):
    _class_iri = S223.PressureSensor
    observes: PropertyReference
    observation_pressure: Pressure
    reference_pressure: Pressure
    differential_static_pressure: DifferentialStaticPressure
    highPort: PressureSensor
    lowPort: PressureSensor

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)

    def add_hasObservationLocation(self, node: Tuple[Node, Node]) -> None:
        # For now, make that a secret, or we end up with s223.hasObservationLocation
        # self._hasObservationLocation = node

        # link the two together
        observation_location, reference_location = node
        self._data_graph.add(
            (self._node_iri, S223.hasReferenceLocation, reference_location._node_iri)
        )
        if INCLUDE_INVERSE:
            reference_location.isReferenceLocation = self

        self._data_graph.add(
            (
                self._node_iri,
                S223.hasObservationLocation,
                observation_location._node_iri,
            )
        )
        if INCLUDE_INVERSE:
            observation_location.isReferenceLocation = self

        self["highPort"] % observation_location
        self["lowPort"] % reference_location


class AirDifferentialStaticPressureSensor(DifferentialStaticPressureSensor):
    _class_iri = S223.PressureSensor
    # observes: PropertyReference

    def __init__(self, **kwargs):
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)
        super().__init__(**_sensor_kwargs)
        self.differential_static_pressure = DifferentialStaticPressure(
            ofMedium=Air,
            label=f"{self.label}.DifferentialStaticPressure",
            **_property_kwargs,
        )
        self.observation_pressure = Pressure(
            ofMedium=Air,
            label=f"{self.label}.ObservationPressure",
            **_property_kwargs,
        )
        self.reference_pressure = Pressure(
            ofMedium=Air,
            label=f"{self.label}.ReferencePressure",
            **_property_kwargs,
        )
        self > Differential(
            label="diff_causality", comment="Will output High minus Low"
        )
        self > PressureSensor(label="highPort", ofMedium=Water, **_property_kwargs)
        self > PressureSensor(label="lowPort", ofMedium=Water, **_property_kwargs)
        self > Differential(label="output", comment="Will output High minus Low")
        # self["highPort"].observes >> self.observation_pressure
        # self["lowPort"].observes >> self.reference_pressure
        self.observation_pressure >> self["diff_causality"].high_input
        self.reference_pressure >> self["diff_causality"].low_input
        self["diff_causality"].differential_output >> self.differential_static_pressure
        self.observes = self.differential_static_pressure


class WaterDifferentialStaticPressureSensor(DifferentialStaticPressureSensor):
    _class_iri = S223.DifferentialSensor

    def __init__(self, **kwargs):
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)
        super().__init__(**_sensor_kwargs)
        self.differential_static_pressure = DifferentialStaticPressure(
            ofMedium=Water,
            label=f"{self.label}.DifferentialStaticPressure",
            **_property_kwargs,
        )
        self.observation_pressure = Pressure(
            ofMedium=Water,
            label=f"{self.label}.ObservationPressure",
            **_property_kwargs,
        )
        self.reference_pressure = Pressure(
            ofMedium=Water,
            label=f"{self.label}.ReferencePressure",
            **_property_kwargs,
        )
        self > Differential(
            label="diff_causality", comment="Will output High minus Low"
        )
        self > PressureSensor(label="highPort", ofMedium=Water, **_property_kwargs)
        self > PressureSensor(label="lowPort", ofMedium=Water, **_property_kwargs)
        self > Differential(label="output", comment="Will output High minus Low")
        # self["highPort"].observes >> self.observation_pressure
        # self["lowPort"].observes >> self.reference_pressure
        self.observation_pressure >> self["diff_causality"].high_input
        self.reference_pressure >> self["diff_causality"].low_input
        self["diff_causality"].differential_output >> self.differential_static_pressure
        self.observes = self.differential_static_pressure
