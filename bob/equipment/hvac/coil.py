from typing import Dict, Optional

from bob.properties import PercentCommand
from bob.properties.electricity import Amps, ElectricPowerkW
from bob.properties.states import OnOffCommand

from ...connections.air import (
    AirBidirectionalConnectionPoint,
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
)
from ...connections.electricity import (
    Electricity_240VLL_1Ph_60HzInletConnectionPoint,
    Electricity_600VLL_3Ph_60HzInletConnectionPoint,
)
from ...connections.liquid import (
    ChilledWaterInletConnectionPoint,
    ChilledWaterOutletConnectionPoint,
    HotWaterInletConnectionPoint,
    HotWaterOutletConnectionPoint,
    WaterBidirectionalConnectionPoint,
    WaterInletConnectionPoint,
    WaterOutletConnectionPoint,
)
from ...connections.refrigerant import (
    RefrigerantBidirectionalConnectionPoint,
    RefrigerantInletConnectionPoint,
    RefrigerantOutletConnectionPoint,
)
from ...core import BOB, S223, Equipment, PropertyReference
from ...enum import (  # , R134a, R404a, R407c, R448a, R449a, R452a, R454b, R507a
    Refrigerant,
    Role,
)
from ...properties.force import Pressure
from ...properties.temperature import Temperature
from ...template import template_update

_namespace = BOB

coil_template: dict[str, dict] = {
    "cp": {},
    "properties": {
        ("averageSurfaceTemperature", Temperature): {},
        ("internalPressure", Pressure): {},
        ("internalTemperature", Temperature): {},
    },
}


class Coil(Equipment):
    _class_iri = S223.Coil
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    # Those could come from a valve, SCR, Triac, etc...
    modulation: PropertyReference
    onOffCommand: PropertyReference

    def __init__(self, config: dict | None = None, **kwargs):
        if config is None:
            config = coil_template.copy()
        config["properties"] = config.get("properties", coil_template["properties"])
        kwargs = {**config.pop("params", {}), **kwargs}
        super().__init__(**{**config, **kwargs})
        self.airOutlet.paired_to(self.airInlet)  # type: ignore


class WaterCoil(Coil):
    _class_iri = S223.Coil
    waterInlet: WaterInletConnectionPoint
    waterOutlet: WaterOutletConnectionPoint

    def __init__(self, config: dict | None = None, **kwargs):
        if config is None:
            config = coil_template.copy()
        config["properties"] = config.get("properties", coil_template["properties"])
        kwargs = {**config.pop("params", {}), **kwargs}
        super().__init__(**{**config, **kwargs})
        self.waterOutlet.paired_to(self.waterInlet)  # type: ignore


class DXCoolingCoil(Coil):
    _class_iri = S223.CoolingCoil
    refrigerantInlet: RefrigerantInletConnectionPoint
    refrigerantOutlet: RefrigerantOutletConnectionPoint

    def __init__(self, config: dict | None = None, **kwargs):
        _config = template_update({}, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(**{**_config, **kwargs})
        self += Role.Cooling  # type: ignore
        self.refrigerantOutlet.paired_to(self.refrigerantInlet)  # type: ignore


class ChilledWaterCoil(Coil):
    _class_iri = S223.CoolingCoil
    chilledWaterInlet: ChilledWaterInletConnectionPoint
    chilledWaterOutlet: ChilledWaterOutletConnectionPoint

    def __init__(self, config: dict | None = None, **kwargs):
        _config = template_update({}, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(**{**_config, **kwargs})
        self += Role.Cooling  # type: ignore
        self.chilledWaterOutlet.paired_to(self.chilledWaterInlet)  # type: ignore


class HotWaterCoil(Coil):
    _class_iri = S223.HeatingCoil
    hotWaterInlet: HotWaterInletConnectionPoint
    hotWaterOutlet: HotWaterOutletConnectionPoint

    def __init__(self, config: dict | None = None, **kwargs):
        _config = template_update({}, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(**{**_config, **kwargs})
        self += Role.Heating  # type: ignore
        self.hotWaterOutlet.paired_to(self.hotWaterInlet)  # type: ignore


class HeatpumpCoil(Coil):
    _class_iri = S223.Coil
    gasPortA: RefrigerantBidirectionalConnectionPoint
    gasPortB: RefrigerantBidirectionalConnectionPoint
    # airInlet: AirInletConnectionPoint
    # airOutlet: AirOutletConnectionPoint

    def __init__(self, config: dict | None = None, **kwargs):
        _config = template_update(coil_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(**{**_config, **kwargs})
        self += Role.Heating  # type: ignore
        self += Role.Cooling  # type: ignore
        self.gasPortB.paired_to(self.gasPortA)  # type: ignore

    def set_gas_type(self, gas: Refrigerant):
        self.set_medium(["gasPortA", "gasPortB"], gas)  # type: ignore


# Electrical Coil
electricalheating_template: dict[str, dict] = {
    "cp": {"electricalInlet": Electricity_600VLL_3Ph_60HzInletConnectionPoint},
    "properties": {
        ("amps", Amps): {},
        ("kW", ElectricPowerkW): {},
        ("modulation", PercentCommand): {},
        ("onOffCommand", OnOffCommand): {},
    },
}


class ElectricalHeatingCoil(Equipment):
    _class_iri = S223.ElectricResistanceElement
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    # Those could come from a valve, SCR, Triac, etc...
    modulation: PropertyReference
    onOffCommand: PropertyReference

    def __init__(self, config: dict | None = None, **kwargs):
        _config = template_update(electricalheating_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(**{**_config, **kwargs})
        self += Role.Heating  # type: ignore
        self.airOutlet.paired_to(self.airInlet)  # type: ignore


# Electrical Coil
electricalradiant_template: dict[str, dict] = {
    "cp": {"electricalInlet": Electricity_240VLL_1Ph_60HzInletConnectionPoint},
    "properties": {
        ("amps", Amps): {},
        ("kW", ElectricPowerkW): {},
    },
}


# Baseboard, radiant panel, heating floor
class ElectricalRadiantHeatingCoil(Equipment):
    _class_iri = S223.RadiantHeater
    airContact: AirBidirectionalConnectionPoint

    def __init__(self, config: dict | None = None, **kwargs):
        _config = template_update(electricalradiant_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(**{**_config, **kwargs})
        self += Role.Heating  # type: ignore


# Water heaters
element_template: dict[str, dict] = {
    "cp": {"electricalInlet": Electricity_240VLL_1Ph_60HzInletConnectionPoint},
    "properties": {
        ("amps", Amps): {},
        ("kW", ElectricPowerkW): {},
        ("modulation", PercentCommand): {},
        ("onOffCommand", OnOffCommand): {},
    },
}


class ImmersedResistanceHeaterElement(Equipment):
    _class_iri = S223.ElectricResistanceElement
    fluidContact: WaterBidirectionalConnectionPoint

    def __init__(self, config: dict | None = None, **kwargs):
        _config = template_update(element_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(**{**_config, **kwargs})
        self += Role.Heating  # type: ignore
