from rdflib import URIRef

from ..core import (
    BOB,
    QUANTITYKIND,
    QuantifiableObservableProperty,
)
from ..enum import Fluid

_namespace = BOB


class Flow(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.VolumeFlowRate
    hasUnit: URIRef
    ofMedium: Fluid  # set from the sensor
    # isObservedBy: Sensor
    measuresMedium: Fluid  # set from the sensor
