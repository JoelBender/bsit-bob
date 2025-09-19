from typing import Any

from rdflib import URIRef

from ..core import (
    BOB,
    P223,
    QUANTITYKIND,
    UNIT,
    QuantifiableObservableProperty,
)

_namespace = BOB


class Volts(QuantifiableObservableProperty):
    _node_iri = P223.Volts
    hasQuantityKind = QUANTITYKIND.Voltage
    hasUnit = UNIT.V


class Amps(QuantifiableObservableProperty):
    _node_iri = P223.Amps
    hasQuantityKind = QUANTITYKIND.ElectricCurrent
    hasUnit = UNIT.A


class PowerFactor(QuantifiableObservableProperty):
    _node_iri = P223.PowerFactor
    hasQuantityKind = QUANTITYKIND.PowerFactor
    hasUnit = UNIT.UNITLESS


class Frequency(QuantifiableObservableProperty):
    _node_iri = P223.Frequency
    hasQuantityKind = QUANTITYKIND.Frequency
    hasUnit = UNIT.HZ


class ElectricPower(QuantifiableObservableProperty):
    _node_iri = P223.ElectricPower
    hasQuantityKind = QUANTITYKIND.ElectricPower
    hasUnit: URIRef
    _supported_units = [
        UNIT.KiloW,
        UNIT.W,
        UNIT.TeraW,
        UNIT.PicoW,
        UNIT.NanoW,
        UNIT.MilliW,
        UNIT.MicroW,
        UNIT.MegaW,
        UNIT.HP_Electric,
        UNIT.GigaW,
    ]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if not ("hasUnit" in kwargs and kwargs["hasUnit"] in self._supported_units):
            _unit = kwargs["hasUnit"] if "hasUnit" in kwargs else "None"
            raise ValueError(
                f"You must provide hasUnit when defining {self}. This unit must be one of those types : {self._supported_units}. You provided {_unit}"
            )
        super().__init__(*args, **kwargs)


class ElectricApparentPower(QuantifiableObservableProperty):
    _node_iri = P223.ElectricApparentPower
    hasQuantityKind = QUANTITYKIND.ApparentPower
    hasUnit: URIRef
    _supported_units = [UNIT["V-A"], UNIT["KiloV-A"]]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if not ("hasUnit" in kwargs and kwargs["hasUnit"] in self._supported_units):
            _unit = kwargs["hasUnit"] if "hasUnit" in kwargs else "None"
            raise ValueError(
                f"You must provide hasUnit when defining {self}. This unit must be one of those types : {self._supported_units}. You provided {_unit}"
            )
        super().__init__(*args, **kwargs)


class ElectricReactivePower(QuantifiableObservableProperty):
    _node_iri = P223.ElectricReactivePower
    hasQuantityKind = QUANTITYKIND.ReactivePower
    hasUnit: URIRef
    _supported_units = [UNIT["V-A_Reactive"], UNIT["KiloV-A_Reactive"]]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if not ("hasUnit" in kwargs and kwargs["hasUnit"] in self._supported_units):
            _unit = kwargs["hasUnit"] if "hasUnit" in kwargs else "None"
            raise ValueError(
                f"You must provide hasUnit when defining {self}. This unit must be one of those types : {self._supported_units}. You provided {_unit}"
            )
        super().__init__(*args, **kwargs)


# Super common....so making a shortcut


class ElectricPowerkW(ElectricPower):
    def __init__(self, **kwargs):
        kwargs["hasUnit"] = UNIT.KiloW
        super().__init__(**kwargs)


class ElectricPowerW(ElectricPower):
    def __init__(self, **kwargs):
        kwargs["hasUnit"] = UNIT.W
        super().__init__(**kwargs)


# Energy
class ElectricEnergy(QuantifiableObservableProperty):
    _node_iri = P223.ElectricEnergy
    hasQuantityKind = QUANTITYKIND.Energy
    hasUnit: URIRef
    _supported_units = [
        UNIT["KiloW-HR"],
        UNIT["W-HR"],
        UNIT["TeraW-HR"],
        UNIT["MegaW-HR"],
        UNIT["GigaW-HR"],
    ]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if not ("hasUnit" in kwargs and kwargs["hasUnit"] in self._supported_units):
            _unit = kwargs["hasUnit"] if "hasUnit" in kwargs else "None"
            raise ValueError(
                f"You must provide hasUnit when defining {self}. This unit must be one of those types : {self._supported_units}. You provided {_unit}"
            )
        super().__init__(*args, **kwargs)


class ElectricApparentEnergy(QuantifiableObservableProperty):
    _node_iri = P223.ElectricApparentEnergy
    hasQuantityKind = QUANTITYKIND.Energy
    hasUnit: URIRef
    _supported_units = [UNIT["V-A-HR"], UNIT["KiloV-A-HR"]]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if not ("hasUnit" in kwargs and kwargs["hasUnit"] in self._supported_units):
            _unit = kwargs["hasUnit"] if "hasUnit" in kwargs else "None"
            raise ValueError(
                f"You must provide hasUnit when defining {self}. This unit must be one of those types : {self._supported_units}. You provided {_unit}"
            )
        super().__init__(*args, **kwargs)


class ElectricReactiveEnergy(QuantifiableObservableProperty):
    _node_iri = P223.ElectricReactiveEnergy
    hasQuantityKind = QUANTITYKIND.Energy
    hasUnit: URIRef
    _supported_units = [UNIT["V-A_Reactive-HR"], UNIT["KiloV-A_Reactive-HR"]]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if not ("hasUnit" in kwargs and kwargs["hasUnit"] in self._supported_units):
            _unit = kwargs["hasUnit"] if "hasUnit" in kwargs else "None"
            raise ValueError(
                f"You must provide hasUnit when defining {self}. This unit must be one of those types : {self._supported_units}. You provided {_unit}"
            )
        super().__init__(*args, **kwargs)
