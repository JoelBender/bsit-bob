from typing import Any, Tuple, Union, Dict


from ..functions import Function
from ..properties.force import DifferentialStaticPressure, Pressure

from ..core import (
    BOB,
    S223,
    Node,
    PropertyReference,
    LocationReference,
)
from ..enum import Air, Water
from .sensor import Sensor, split_kwargs

_namespace = BOB


class PressureSensor(Sensor):
    _class_iri = S223.PressureSensor
    observes: PropertyReference  # Temperature
    # hasObservationLocation: LocationReference

    def __init__(self, config: Dict[str, Any] = {}, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        if "hasUnit" not in _property_kwargs:
            raise ValueError("You must provide hasUnit when defining a pressure sensor")
        if "ofMedium" not in _property_kwargs:
            raise ValueError(
                "You must provide ofMedium when defining a pressure sensor"
            )

        observed_prop = Pressure(
            # isObservedBy=self,
            label="observed_property",
            **_property_kwargs,
        )

        _sensor_kwargs["observed_property"] = observed_prop

        super().__init__(config=config, **_sensor_kwargs)


class DifferentialStaticPressureSensor(Sensor):
    _class_iri = S223.PressureSensor
    observes: PropertyReference
    observation_pressure: Pressure
    reference_pressure: Pressure
    differential_static_pressure: DifferentialStaticPressure
    hasObservationLocation: LocationReference
    hasReferenceLocation: LocationReference

    def __init__(self, config: Dict[str, Any] = {}, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)

    def add_hasReferenceLocation(self, node: Node) -> None:
        # link the two together
        reference_location = node
        self._data_graph.add(
            (self._node_iri, S223.hasReferenceLocation, reference_location._node_iri)
        )
        self.hasReferenceLocation = reference_location  # type: ignore[assignment]

    def add_hasObservationLocation(self, node: Union[Tuple[Node, Node], Node]) -> None:
        """
        When defining the observation localtion and the reference location with a template
        we can use the same function twice. First run will set the observation location,
        second run will set the reference location.
        """
        if isinstance(node, tuple):
            observation_location, reference_location = node
            self._data_graph.add(
                (
                    self._node_iri,
                    S223.hasObservationLocation,
                    observation_location._node_iri,
                )
            )
            self.hasObservationLocation = observation_location  # type: ignore[assignment]
            self.add_hasReferenceLocation(reference_location)
        elif self.hasObservationLocation is not None:
            self.add_hasReferenceLocation(node)

        else:
            self._data_graph.add(
                (self._node_iri, S223.hasObservationLocation, node._node_iri)
            )
            self.hasObservationLocation = node


class AirDifferentialStaticPressureSensor(DifferentialStaticPressureSensor):
    _class_iri = S223.PressureSensor
    # observes: PropertyReference

    def __init__(self, config: Dict[str, Any] = {}, **kwargs):
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)
        super().__init__(config=config, **_sensor_kwargs)
        self.differential_static_pressure = DifferentialStaticPressure(
            ofMedium=Air,
            label=f"{self.label}.DifferentialStaticPressure",  # type: ignore[attr-defined]
            **_property_kwargs,
        )
        self.observation_pressure = Pressure(
            ofMedium=Air,
            label=f"{self.label}.ObservationPressure",  # type: ignore[attr-defined]
            **_property_kwargs,
        )
        self.reference_pressure = Pressure(
            ofMedium=Air,
            label=f"{self.label}.ReferencePressure",  # type: ignore[attr-defined]
            **_property_kwargs,
        )

        diff_function = Function(
            label="differential calculation", comment="Will output High minus Low"
        )
        self > diff_function  # type: ignore[operator]
        diff_function.hasInput(self.observation_pressure)
        diff_function.hasInput(self.reference_pressure)
        diff_function.hasOutput(self.differential_static_pressure)

        self.observes = self.differential_static_pressure  # type: ignore[assignment]


class WaterDifferentialStaticPressureSensor(DifferentialStaticPressureSensor):
    _class_iri = S223.PressureSensor

    def __init__(self, config: Dict[str, Any] = {}, **kwargs):
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)
        super().__init__(config=config, **_sensor_kwargs)
        self.differential_static_pressure = DifferentialStaticPressure(
            ofMedium=Water,
            label=f"{self.label}.DifferentialStaticPressure",  # type: ignore[attr-defined]
            **_property_kwargs,
        )
        self.observation_pressure = Pressure(
            ofMedium=Water,
            label=f"{self.label}.ObservationPressure",  # type: ignore[attr-defined]
            **_property_kwargs,
        )
        self.reference_pressure = Pressure(
            ofMedium=Water,
            label=f"{self.label}.ReferencePressure",  # type: ignore[attr-defined]
            **_property_kwargs,
        )

        diff_function = Function(
            label="differential calculation", comment="Will output High minus Low"
        )
        self > diff_function  # type: ignore[operator]
        diff_function.hasInput(self.observation_pressure)
        diff_function.hasInput(self.reference_pressure)
        diff_function.hasOutput(self.differential_static_pressure)

        self.observes = self.differential_static_pressure  # type: ignore[assignment]
