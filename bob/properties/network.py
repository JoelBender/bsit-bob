from ..core import BOB, QUANTITYKIND, UNIT, QuantifiableObservableProperty

_namespace = BOB


class Mbit_per_seconds(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.DataRate
    hasUnit = UNIT["MegaBIT-PER-SEC"]


class Kbit_per_seconds(QuantifiableObservableProperty):
    hasQuantityKind = QUANTITYKIND.DataRate
    hasUnit = UNIT["KiloBIT-PER-SEC"]
