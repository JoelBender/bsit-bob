from typing import Dict, Optional

from rdflib import URIRef

from bob.properties.electricity import ElectricPowerkW
from bob.properties.states import NormalAlarmStatus, OnOffCommand, OnOffStatus

from ...connections.air import CompressedAirOutletConnectionPoint
from ...connections.electricity import (
    Electricity_600VLL_3Ph_60HzInletConnectionPoint,
)
from ...connections.refrigerant import (
    RefrigerantInletConnectionPoint,
    RefrigerantOutletConnectionPoint,
)
from ...core import BOB, S223, Equipment, PropertyReference
from ...enum import (  # , R134a, R404a, R407c, R448a, R449a, R452a, R454b, R507a
    Refrigerant,
)

_namespace = BOB


compressor_template = {
    "cp": {"electricalInlet": Electricity_600VLL_3Ph_60HzInletConnectionPoint},
    "properties": {
        ("kW", ElectricPowerkW): {},
    },
}


class Compressor(Equipment):
    _class_iri: URIRef = S223.Compressor


class AirCompressor(Compressor):
    compressedAirOutlet: CompressedAirOutletConnectionPoint

    onOffStatus: OnOffStatus
    alarmStatus: NormalAlarmStatus
    onOffCommand: OnOffCommand

    # This will come from a sensor, but accessible from here
    outputPressure: PropertyReference

    def __init__(self, config: dict | None = None, **kwargs):
        if config is None:
            config = compressor_template.copy()
        config["properties"] = config.get(
            "properties", compressor_template["properties"],
        )
        kwargs = {**config.get("params", {}), **kwargs}  # type: ignore[dict-item]
        super().__init__(**config, **kwargs)  # type: ignore[misc]


class RefrigerationGasCompressor(Compressor):
    returnPort: RefrigerantInletConnectionPoint
    dischargePort: RefrigerantOutletConnectionPoint

    onOffStatus: OnOffStatus
    alarmStatus: NormalAlarmStatus
    onOffCommand: OnOffCommand

    # This will come from a sensor, but accessible from here
    dischargePressure: PropertyReference
    succionPressure: PropertyReference

    def __init__(self, config: dict | None = None, **kwargs):
        if config is None:
            config = compressor_template.copy()
        config["properties"] = config.get(
            "properties", compressor_template["properties"],
        )
        kwargs = {**config.get("params", {}), **kwargs}  # type: ignore[dict-item]
        super().__init__(**config, **kwargs)  # type: ignore[misc]
        self.dischargePort.paired_to(self.returnPort)  # type: ignore

    def set_gas_type(self, gas: Refrigerant):
        self.set_medium(["returnPort", "dischargePort"], gas)  # type: ignore
