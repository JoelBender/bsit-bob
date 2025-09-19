from typing import Dict

from rdflib import URIRef

from bob.properties.electricity import Amps, ElectricPowerkW
from bob.properties.states import OnOffCommand

from ...connections.electricity import (
    Electricity_600VLL_3Ph_60HzInletConnectionPoint,
    Electricity_600VLL_3Ph_60HzOutletConnectionPoint,
)
from ...connections.controlsignal import (
    ModulationSignalInletConnectionPoint,
)
from ...core import BOB, P223, Equipment

_namespace = BOB

# TRIAC
Triac_template = {
    "cp": {
        "electricalInlet": Electricity_600VLL_3Ph_60HzInletConnectionPoint,
        "electricalOutlet": Electricity_600VLL_3Ph_60HzOutletConnectionPoint,
        "onOffSignalInlet": ModulationSignalInletConnectionPoint,
    },
    "properties": {
        ("onOffCommand", OnOffCommand): {},
        ("amps", Amps): {},
        ("kW", ElectricPowerkW): {},
    },
}


class Triac(Equipment):
    # takes 600V (or 347V) in and use PWM to modulate
    # power given to electrical coil
    # a triac accept On-Off pulsed signal to modulate
    _class_iri: URIRef = P223.Triac

    def __init__(self, config: Dict = Triac_template, **kwargs):
        config["properties"] = config.get("properties", Triac_template["properties"])
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
