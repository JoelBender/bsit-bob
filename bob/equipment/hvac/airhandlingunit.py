import logging
from typing import Dict


from ... import application
from ...core import BOB, BoundaryConnectionPoint, System
from ...template import SystemFromTemplate, template_update

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = BOB

ahu_template = {
    "params": {},
    "sensors": {},
    "equipment": {},
}

fan_coil_template = {
    "params": {},
    "sensors": {},
    "equipment": {},
}


class AirHandlingUnit(SystemFromTemplate, application.AirHandlingUnit):
    """
        This is treated as a system.
        We will add multiple devices inside using a template

        example from pritoni (2024-01-06)
        ahu_template = {
        "params": {"label": "AHU", "comment": "AHU delivering air to 2 VAV boxes"},
        "sensors": {
            ("OA-T", AirTemperatureSensor): {
                "hasUnit": UNIT.DEG_C,
                "comment": "Oudoor air temperature (S3)",
            },
            ("TPD1", AirDifferentialStaticPressureSensor): {
                "hasUnit": UNIT.PA,
                "comment": "Filter Differential Pressure Sensor (S5)",
            },
            ("HC-T", AirTemperatureSensor): {
                "hasUnit": UNIT.DEG_C,
                "comment": "Air temperature after heating coil (S6)",
            },
            ("MA-T", AirTemperatureSensor): {
                "hasUnit": UNIT.DEG_F,
                "comment": "Return Air temperature (S4)",
            },
            ("DA-T", AirTemperatureSensor): {
                "hasUnit": UNIT.DEG_F,
                "comment": "Discharge Air temperature after cooling coil (S7)",
            },
            ("RA-T", AirTemperatureSensor): {
                "hasUnit": UNIT.DEG_F,
                "comment": "Return Air temperature (S2)",
            },
            ("TPD2", AirDifferentialStaticPressureSensor): {
                "hasUnit": UNIT.PA,
                "comment": "Supply Duct Static Pressure (S8)",
            },
            ("TPD3", AirDifferentialStaticPressureSensor): {
                "hasUnit": UNIT.PA,
                "comment": "Return Duct Static Pressure (S1)",
            },
        },
        "equipment": {
            ("RF", Fan): {
                "comment": "Return Air Fan",
                "electricalInlet": Electricity_600VLL_3Ph_60HzInletConnectionPoint,
                "hasRole": Role.Return,
            },
            ("RF_VFD", VFD): {
                "comment": "Return Air Fan VFD",
            },
            ("SF", Fan): {
                "comment": "Supply Air Fan",
                "electricalInlet": Electricity_600VLL_3Ph_60HzInletConnectionPoint,
                "hasRole": Role.Supply,
            },
            ("SF_Starter", MotorStarter): {
                "comment": "Supply Air Fan Starter",
            },
            ("CLGCOIL", ChilledWaterCoil): {"comment": "Cooling Coil"},
            ("HTGCOIL", HotWaterCoil): {"comment": "Heating coil"},
            ("FILTER", Filter): {"comment": "Filter"},
            ("OADPR", ElectricalActuatedProportionalDamper): {
                "comment": "Outdoor air damper (A3)"
            },
            ("MADPR", ElectricalActuatedProportionalDamper): {
                "comment": "Mixed Air Damper (A2)"
            },
            ("EADPR", ElectricalActuatedProportionalDamper): {
                "comment": "Exhaust Air Damper (A1)"
            },
        },
    }

    """

    _class_iri = BOB.AirHandlingUnit
    outsideAirInlet: BoundaryConnectionPoint
    returnAirInlet: BoundaryConnectionPoint
    supplyAirOutlet: BoundaryConnectionPoint
    exhaustAirOutlet: BoundaryConnectionPoint
    electricalInlet: BoundaryConnectionPoint
    # The system connection points are now a Bob thing only, there is no such thing in 223P anymore

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(ahu_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.debug(f"AirHandlingUnit.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)


class FanCoil(System, application.FanCoilUnit):
    _class_iri = BOB.FanCoilUnit
    returnAirInlet: BoundaryConnectionPoint
    supplyAirOutlet: BoundaryConnectionPoint
    exhaustAirOutlet: BoundaryConnectionPoint
    electricalInlet: BoundaryConnectionPoint

    def __init__(self, config: Dict = {}, **kwargs) -> None:
        _config = template_update(fan_coil_template, config)
        kwargs = {**_config.get("params", {}), **kwargs}
        _log.debug(f"FanCoil.__init__ {_config} {kwargs}")
        super().__init__(config, **kwargs)
        # self += SystemType.FanCoilUnit
