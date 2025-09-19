from ..core import (
    P223,
    QUANTITYKIND,
    UNIT,
    Medium,
    Substance,
    QuantifiableObservableProperty,
)

_namespace = P223


class ParticulateCount(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.NumberDensity
    hasUnit = UNIT["NUM-PER-M3"]
    ofMedium: Medium
    ofSubstance: Substance
