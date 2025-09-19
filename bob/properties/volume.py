from ..core import BOB, QUANTITYKIND, UNIT, Medium, QuantifiableObservableProperty

_namespace = BOB


class Gallons(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.LiquidVolume
    hasUnit = UNIT.GAL_US
    measuresMedium: Medium  # set from the sensor
