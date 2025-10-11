from typing import Dict
from rdflib import Literal

from bob.properties import ElectricPowerkW

from ...core import (
    BOB,
    S223,
    Equipment,
)

_namespace = BOB


class Transformer(Equipment):
    _class_iri = S223.ElectricEnergyTransformer
    hasPower: ElectricPowerkW
    label: Literal  # Explicit type annotation for mypy

    def __init__(self, config: Dict = {}, **kwargs):
        kwargs = {**config.get("params", {}), **kwargs}
        _electricalInlet = kwargs.pop("electricalInlet")
        _electricalOutlet = kwargs.pop("electricalOutlet")

        super().__init__(**kwargs)

        self.electricalInlet = _electricalInlet(
            self, label=f"{self.label}.electricalInlet"
        )
        self.electricalOutlet = _electricalOutlet(
            self, label=f"{self.label}.electricalOutlet"
        )

class CircuitBreaker(Equipment):
    _class_iri = S223.ElectricBreaker
    # electricalInlet: ElectricalInletConnectionPoint
    # electricalOutlet: ElectricalOutletConnectionPoint


    def __init__(self, config: Dict = {}, **kwargs):
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(**kwargs)