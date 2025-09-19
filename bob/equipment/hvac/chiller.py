from typing import Dict

from bob.properties.electricity import ElectricPowerkW
from bob.properties.states import NormalAlarmStatus

from ...connections.electricity import (
    Electricity_600VLL_3Ph_60HzInletConnectionPoint,
)
from ...connections.controlsignal import (
    ModulationSignalInletConnectionPoint,
    OnOffSignalOutletConnectionPoint,
)
from ...connections.liquid import (
    ChilledWaterInletConnectionPoint,
    ChilledWaterOutletConnectionPoint,
    CondenserInletConnectionPoint,
    CondenserOutletConnectionPoint,
    WaterInletConnectionPoint,
    WaterOutletConnectionPoint,
)
from ...core import BOB, S223, Equipment
from ... import application
from ...properties import OnOffCommand, OnOffStatus, Percent

_namespace = BOB

chiller_template = {
    "cp": {"electricalInlet": Electricity_600VLL_3Ph_60HzInletConnectionPoint},
    "properties": {
        ("kW", ElectricPowerkW): {},
    },
}


class Chiller(Equipment, application.Chiller):
    _class_iri = S223.Chiller
    chilledWaterEntering: ChilledWaterInletConnectionPoint
    chilledWaterLeaving: ChilledWaterOutletConnectionPoint
    condenserEntering: CondenserInletConnectionPoint
    condenserLeaving: CondenserOutletConnectionPoint

    # refrigerant
    # manufacturer
    setpointResetInlet: ModulationSignalInletConnectionPoint
    alarmOutlet: OnOffSignalOutletConnectionPoint
    capacityLimitInlet: ModulationSignalInletConnectionPoint

    setpointReset: Percent
    capacityLimit: Percent
    onOffStatus: OnOffStatus
    alarmStatus: NormalAlarmStatus
    onOffCommand: OnOffCommand

    def __init__(self, config: Dict = chiller_template, **kwargs):
        config["properties"] = config.get("properties", chiller_template["properties"])
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
        self.chilledWaterLeaving.paired_to(self.chilledWaterEntering)
        self.condenserLeaving.paired_to(self.condenserEntering)


class AgnosticChiller(Equipment, application.Chiller):
    _class_iri = S223.Chiller
    chilledWaterLeaving: WaterOutletConnectionPoint
    chilledWaterEntering: WaterInletConnectionPoint
    condensedWaterLeaving: WaterOutletConnectionPoint
    condensedWaterEntering: WaterInletConnectionPoint

    # refrigerant
    # manufacturer
    setpointResetInlet: ModulationSignalInletConnectionPoint
    alarmOutlet: OnOffSignalOutletConnectionPoint
    capacityLimitInlet: ModulationSignalInletConnectionPoint

    setpointReset: Percent
    capacityLimit: Percent
    onOffStatus: OnOffStatus
    alarmStatus: NormalAlarmStatus
    onOffCommand: OnOffCommand

    def __init__(self, config: Dict = chiller_template, **kwargs):
        config["properties"] = config.get("properties", chiller_template["properties"])
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
