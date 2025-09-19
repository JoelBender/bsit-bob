from ..core import BOB, QUANTITYKIND, UNIT, QuantifiableObservableProperty

_namespace = BOB


class Brightness(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.Illuminance
    hasUnit = UNIT.LUX


class RelativeLuminousFlux(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.RelativeLuminousFlux
    hasUnit = UNIT.PERCENT
