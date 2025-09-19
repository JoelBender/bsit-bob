from rdflib import XSD, Literal

from ..core import (
    BOB,
    QUANTITYKIND,
    QUDT,
    UNIT,
    Medium,
    QuantifiableObservableProperty,
)

_namespace = BOB

# all = [HP, Pressure, DifferentialStaticPressure]


class HP(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.Power
    hasUnit = UNIT.HP


class Nm(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.Torque
    hasUnit = UNIT["N-M"]


class Pressure(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.Pressure


class DifferentialStaticPressure(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.ForcePerArea
    ofMedium: Medium  # set from the sensor

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data_graph.add(
            (self._node_iri, QUDT.isDeltaQuantity, Literal(True, datatype=XSD.boolean))
        )
