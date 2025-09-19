from __future__ import annotations

from typing import Any

from rdflib import URIRef

from ..core import (
    INCLUDE_INVERSE,
    S223,
    LocationReference,
    Node,
    PropertyReference,
    QuantifiableProperty,
    _Sensor,
    logging,
)

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = S223


def split_kwargs(given_kwargs):
    # specific properties given to a sensor for creation
    # but that must be applied to the observed property, see
    # sorted(QuantifiableObservableProperty._attr_uriref.keys())
    property_attrs = [
        "hasAspect",
        "hasExternalReference",
        "hasQuantityKind",
        "hasSetpoint",
        "hasUnit",
        "hasValue",
        "ofConstituent",
        "ofMedium",
        "ofSubstance",
    ]
    property_kwargs = {}
    sensor_kwargs = {}

    for k, v in given_kwargs.items():
        if v is None:
            continue
        if k in property_attrs:
            property_kwargs[k] = v
        else:
            sensor_kwargs[k] = v

    return (sensor_kwargs, property_kwargs)


def define_sensors(config):
    if not config:
        return []
    sensors = []
    for sensor_label_and_class, sensor_data in config["sensors"].items():
        _label, _cls = sensor_label_and_class
        try:
            if issubclass(_cls, Sensor):
                _cls = _cls
        except:
            raise TypeError("Please provide class for sensor")

        sensors.append(_cls(label=_label, **sensor_data))

    return sensors


class Sensor(_Sensor):
    """
    An equipment meant to observe a property
    """

    _class_iri: URIRef = S223.Sensor
    hasMeasurementPrecision: QuantifiableProperty
    hasMeasurementUncertainty: QuantifiableProperty
    hasMaxRange: QuantifiableProperty
    hasMinRange: QuantifiableProperty
    hasObservationLocation: LocationReference
    observes: PropertyReference

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)
        super().__init__(**_sensor_kwargs)

    @property
    def observedProperty(self):
        """
        When accessing the property, it feels ackward to use sensor.observes
        The terms fit for assignation...but for retrieval, feel unnatural
        So let's try this shortcut
        """
        return self.observes

    def add_hasObservationLocation(self, node: Node) -> None:
        # For now, make that a secret, or we end up with s223.hasObservationLocation
        # self._hasObservationLocation = node

        # link the two together
        self._data_graph.add(
            (self._node_iri, S223.hasObservationLocation, node._node_iri)
        )
        if INCLUDE_INVERSE:
            node.isObservationLocationOf = self

    def __mod__(self, other: Node) -> Node:
        """This sensor measurementLocation taken from some other node."""
        _log.debug(f"Container.__mod__ {self} % {other}")

        self.add_hasObservationLocation(other)
        return self


# class VirtualSensor(Sensor):
#    "Virtal Sensor"
#    _class_iri: URIRef = S223.VirtualSensor
#    # hasObservationLocation: # maxCount = 0
#    hasFunctionInput: Property
