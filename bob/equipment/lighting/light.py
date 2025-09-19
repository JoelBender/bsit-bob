from typing import Dict


from bob.properties.electricity import ElectricPower

from ...connections.light import LightVisibleOutletConnectionPoint
from ...core import BOB, S223, Equipment
from ...properties.light import RelativeLuminousFlux
from ...properties.ratio import PercentCommand
from ...properties.states import OnOffCommand, OnOffStatus

_namespace = BOB


class Luminaire(Equipment):
    _class_iri = S223.Luminaire
    lightOutlet: LightVisibleOutletConnectionPoint
    brightness: RelativeLuminousFlux
    brightnessRatio: PercentCommand
    onOffStatus: OnOffStatus
    onOffCommand: OnOffCommand
    electricalPower: ElectricPower

    def __init__(self, config: Dict = {}, **kwargs):
        kwargs = {**config.get("params", {}), **kwargs}
        _electricalInlet = kwargs.pop("electricalInlet", None)

        super().__init__(config, **kwargs)

        if _electricalInlet:
            self.electricalInlet = _electricalInlet(
                self, label=f"{self.label}.electricalInlet"
            )
