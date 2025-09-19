from ..core import BOB, P223, QUANTITYKIND, UNIT, Medium, QuantifiableObservableProperty

_namespace = BOB


class AirChangePerHour(QuantifiableObservableProperty):
    """
    airflow / volume * 1hour


    ft^3           1
    ____   *   __________  *  60min = ACH
    min        vol (ft^3)

    """

    _class_iri = P223.AirChangePerHour
    hasQuantityKind = QUANTITYKIND.Dimensionless
    hasUnit = UNIT.UNITLESS


class Count(QuantifiableObservableProperty):
    _class_iri = BOB.Count
    hasQuantityKind = QUANTITYKIND.Dimensionless
    hasUnit = UNIT["NUM"]
    ofMedium: Medium
