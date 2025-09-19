from ..core import BOB, QUANTITYKIND, QuantifiableObservableProperty

_namespace = BOB

# all = [HP, Pressure, DifferentialStaticPressure]


class Length(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.Length


class Area(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.Area
