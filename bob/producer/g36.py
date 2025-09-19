import logging
from typing import Dict

from ..core import (
    G36,
    DomainSpace,
    Zone,
)
from ..sensor.flow import FlowSetpoint
from ..sensor.temperature import TemperatureSetpoint
from ..template import template_update
from . import (
    Function,
    FunctionInput,
    G36AnalogInput,
    G36AnalogOutput,
    G36DigitalInput,
)

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = G36


class G36Sequence(Function):
    """
    This function is a subclass of a Function Block kept
    in the namespace of G36.

    In Guideline 36, models present the notion of AI, AO, BI, BO
    and those concept can be modeled using a Function block.
    Function block is then an abstraction of the sequence of
    operation suggested by G36.

    Comment of this block is the description of the sequence.
    """

    _class_iri = G36.Function


class G36ZoneTemperatureControl(G36Sequence):
    _class_iri = G36.Function


class G36AirFlowControl(G36Sequence):
    _class_iri = G36.Function


class G36OccupancyControl(G36Sequence):
    _class_iri = G36.Function


class G36VentilationAndCO2Control(G36Sequence):
    _class_iri = G36.Function


# g36_4-1_VAV_TerminalUnit_CoolingOnly
class G36VAVCoolingOnly(G36Sequence):
    _class_iri = G36.VAVCoolingOnly
    # From table in section 4.1
    # Defined as Function Input and Output as we will connect
    # to existing properties in the model
    boxDamperPosition: G36AnalogOutput
    supplyAirFlow: G36AnalogInput
    zoneTemperature: G36AnalogInput
    localOverride: G36DigitalInput
    zoneOccupancySensor: G36DigitalInput
    zonewindowSwitch: G36DigitalInput
    zoneSetpointAdj: G36AnalogInput
    zoneCO2: G36AnalogInput
    effectiveOccupancy: FunctionInput
    ahuSupplyAirTemp: FunctionInput

    ### PROPERTIES
    # Airflow setpoints
    zoneMaximumCoolingAirflowSetpoint: FlowSetpoint
    zoneMaximumHeatingAirflowSetpoint: FlowSetpoint

    # Temperature setpoint
    occupiedHtgSetpoint: TemperatureSetpoint
    occupiedClgSetpoint: TemperatureSetpoint
    unoccupiedHtgSetpoint: TemperatureSetpoint
    unoccupiedClgSetpoint: TemperatureSetpoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.debug(f"G36VAVCoolingOnly.__init__ {_config} {kwargs}")

        super().__init__(**kwargs)


class G36Figure_A_3(G36VAVCoolingOnly):
    def __init__(self, comment=None, **kwargs):
        super().__init__(comment=comment, **kwargs)


class G36Figure_A_2(G36VAVCoolingOnly):
    def __init__(self, comment=None, **kwargs):
        super().__init__(comment=comment, **kwargs)


class G36VAVCoolingOnly0(G36Sequence):
    def __init__(self, comment=None, **kwargs):
        super().__init__(comment=comment, **kwargs)

    _class_iri = G36.Function


class G36ZoneGroup(Zone):
    _class_iri = G36.ZoneGroup


class G36ZoneFromZone(Zone):
    _class_iri = G36.Zone


class G36ZoneFromDomainSpace(DomainSpace):
    _class_iri = G36.Zone


VAV_CoolingOnly_template = {
    "cp": {
        "boxDamperPosition": G36AnalogOutput,
        "supplyAirFlow": G36AnalogInput,
        "zoneTemperature": G36AnalogInput,
        "localOverride": G36DigitalInput,
        "zoneOccupancySensor": G36DigitalInput,
        "zonewindowSwitch": G36DigitalInput,
        "zoneSetpointAdj": G36AnalogInput,
        "zoneCO2": G36AnalogInput,
        "effectiveOccupancy": FunctionInput,
        "ahuSupplyAirTemp": FunctionInput,
    },
    "functions": {
        ("zoneTemperatureControl", G36ZoneTemperatureControl): {},
        ("airFlowControl", G36AirFlowControl): {},
        ("occupancyControl", G36OccupancyControl): {},
        ("ventilationAndCO2Control", G36VentilationAndCO2Control): {},
    },
}
