from typing import Dict

from rdflib import URIRef

from bob.equipment.electricity.starter import MotorStarter
from bob.equipment.electricity.vfd import VFD
from bob.properties.ratio import PercentCommand

from ...connections.electricity import (
    Electricity_600VLL_3Ph_60HzInletConnectionPoint,
    Electricity_600VLL_3Ph_60HzOutletConnectionPoint,
)
from ...connections.liquid import WaterInletConnectionPoint, WaterOutletConnectionPoint
from ...core import BOB, S223, UNIT, Equipment, PropertyReference, logging
from ...properties import (
    HP,
    RPM,
    Amps,
    ElectricPowerkW,
    PowerFactor,
    Pressure,
)
from ...template import template_update

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = BOB

pump_template = {
    "cp": {"electricalInlet": Electricity_600VLL_3Ph_60HzInletConnectionPoint},
    "properties": {
        ("head_pressure", Pressure): {"hasUnit": UNIT.PSI},
        ("amps", Amps): {},
        ("rpm", RPM): {},
        ("hp", HP): {},
        ("kW", ElectricPowerkW): {},
        ("powerFactor", PowerFactor): {},
    },
}


class Pump(Equipment):
    _class_iri = S223.Pump
    fluidInlet: WaterInletConnectionPoint
    fluidOutlet: WaterOutletConnectionPoint
    onOffStatus: PropertyReference
    onOffCommand: PropertyReference

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(pump_template, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.debug(f"Fan.__init__ {_config} {kwargs}")

        super().__init__(_config, **kwargs)
        self.fluidOutlet.paired_to(self.fluidInlet)


starter_addon_template = {
    "equipment": {
        ("starter", MotorStarter): {
            "config": {
                "cp": {
                    "electricalInlet": Electricity_600VLL_3Ph_60HzInletConnectionPoint,
                    "electricalOutlet": Electricity_600VLL_3Ph_60HzOutletConnectionPoint,
                }
            },
        }
    },
    "properties": {("speedRatio", PercentCommand): {}},
}


class PumpWithStarter(Pump):
    """
    This pump is composed of a pump, an electrical motor and a starter
    """

    _class_iri: URIRef = S223.Pump

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            bases=[pump_template, starter_addon_template],
            config=config,
        )
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.debug(f"PumpWithStarter.__init__ {_config} {kwargs}")

        super().__init__(_config, **kwargs)
        self.onOffCommand = self["starter"]["onOffCommand"]
        self.onOffStatus = self["starter"]["starter.current_sensor"].observes
        self["starter"].actuatesProperty = self["speedRatio"]
        self["starter"].electricalOutlet >> self.electricalInlet


VFD_addon_template = {
    "equipment": {("vfd", VFD): {}},
    "properties": {},
}


class PumpWithVFD(Pump):
    """
    This fan is composed of a blower, an electrical motor and a VFD
    """

    _class_iri: URIRef = S223.Pump

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            bases=[pump_template, VFD_addon_template],
            config=config,
        )
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.debug(f"PumpWithVFD.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)
        self.onOffCommand = self["vfd"]["run_command"]
        self.onOffStatus = self["vfd"]["drive_running"]
        self["vfd"].actuatesProperty = self["speedRatio"]
        self["vfd"].electricalOutlet >> self.electricalInlet
