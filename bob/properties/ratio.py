from ..core import (
    BOB,
    QUANTITYKIND,
    UNIT,
    Medium,
    QuantifiableActuatableProperty,
    QuantifiableObservableProperty,
)
from ..enum import Air

_namespace = BOB


class Percent(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.DimensionlessRatio
    hasUnit = UNIT.PERCENT


class PercentCommand(QuantifiableActuatableProperty):
    hasQuantityKind = QUANTITYKIND.DimensionlessRatio
    hasUnit = UNIT.PERCENT


class RPM(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.AngularVelocity
    hasUnit = UNIT["REV-PER-MIN"]


class RelativeHumidity(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.RelativeHumidity
    hasUnit = UNIT.PERCENT_RH
    ofMedium: Medium = Air


class GasConcentration(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.DimensionlessRatio
    hasUnit = UNIT.PPM
    ofMedium: Medium = Air
