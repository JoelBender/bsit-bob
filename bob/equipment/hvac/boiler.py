from typing import Dict

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...connections.electricity import (
    ElectricalInletConnectionPoint,
)
from ...connections.liquid import (
    HotWaterInletConnectionPoint,
    HotWaterOutletConnectionPoint,
    WaterOutletConnectionPoint,
)
from ...connections.naturalgas import NaturalGasInletConnectionPoint
from ...core import (
    BOB,
    S223,
    BoundaryConnectionPoint,
    Equipment,
)
from ...enum import Role
from ... import application
from ...template import SystemFromTemplate, template_update

_namespace = BOB

# if no configuration is passed, use this basic template of a generic hot water heater equipment
basic_hotwaterheater_template = {
    "params": {"label": "HotWaterHeater", "comment": "Hot Water Heater"},
    "equipment": {
        ("hw_heater", Equipment): {
            "config": {
                "cp": {
                    "hotWaterLeaving": HotWaterOutletConnectionPoint,
                    "hotWaterEntering": HotWaterInletConnectionPoint,
                    "electricalInlet": ElectricalInletConnectionPoint,
                }
            },
        },
    },
    "relations": [
        ("self.leavingFluid", "=", "self['hw_heater'].hotWaterLeaving"),
        ("self.enteringFluid", "=", "self['hw_heater'].hotWaterEntering"),
        ("self.electricalInlet", "=", "self['hw_heater'].electricalInlet"),
        (
            "self['hw_heater'].hotWaterLeaving",
            "**=",
            "self['hw_heater'].hotWaterEntering",
        ),
    ],
}


# 223 Standard Systems
class DomesticHotWaterHeater(SystemFromTemplate, application.HotWaterHeater):
    # _class_iri = S223.DomesticHotWaterHeater
    leavingFluid: BoundaryConnectionPoint
    enteringFluid: BoundaryConnectionPoint
    electricalInlet: BoundaryConnectionPoint

    def __init__(self, config: Dict = basic_hotwaterheater_template, **kwargs) -> None:
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self += Role.Heating
        self.leavingFluid.paired_to(self.enteringFluid)


# 223 Standard Equipment
class HotWaterBoiler(Equipment, application.Boiler):
    _class_iri = S223.Boiler
    hotWaterLeaving: HotWaterOutletConnectionPoint
    hotWaterEntering: HotWaterInletConnectionPoint

    def __init__(self, config: Dict = basic_hotwaterheater_template, **kwargs) -> None:
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self += Role.Heating
        self.hotWaterLeaving.paired_to(self.hotWaterEntering)


class ElectricalHotWaterBoiler(HotWaterBoiler, application.Boiler):
    _class_iri = S223.Boiler
    electricalInlet: ElectricalInletConnectionPoint


class NaturalGasHotWaterBoiler(HotWaterBoiler, application.Boiler):
    _class_iri = S223.Boiler
    electricalInlet: ElectricalInletConnectionPoint
    naturalGasInlet: NaturalGasInletConnectionPoint
    combustionAirInlet: AirInletConnectionPoint
    combustionAirOutlet: AirOutletConnectionPoint
    condensedWaterOutlet: WaterOutletConnectionPoint
