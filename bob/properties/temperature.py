from rdflib import URIRef

from ..core import (
    BOB,
    QUANTITYKIND,
    Medium,
    QuantifiableObservableProperty,
)

_namespace = BOB


class Temperature(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.Temperature
    hasUnit: URIRef
    ofMedium: Medium  # set from the sensor
    # isObservedBy: Sensor
