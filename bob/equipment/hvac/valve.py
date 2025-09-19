from typing import Dict

from rdflib import URIRef

from ...connections.air import (
    CompressedAirInletConnectionPoint,
    CompressedAirOutletConnectionPoint,
)
from ...connections.liquid import WaterInletConnectionPoint, WaterOutletConnectionPoint
from ...connections.mechanical import MechanicalInletConnectionPoint
from ...connections.naturalgas import (
    NaturalGasInletConnectionPoint,
    NaturalGasOutletConnectionPoint,
)
from ...connections.refrigerant import (
    RefrigerantBidirectionalConnectionPoint,
    RefrigerantInletConnectionPoint,
    RefrigerantOutletConnectionPoint,
)
from ...core import BOB, S223, Equipment, PropertyReference, logging
from ...enum import (  # , R134a, R404a, R407c, R448a, R449a, R452a, R454b, R507a
    Fluid,
    Refrigerant,
)
from ...properties import Gallons
from ...template import configure_relations, template_update

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = BOB


class Valve(Equipment):
    """
    Base class for a valve. Must be subclassed to provide inlet and outlet
    depending on configuration
    """

    _class_iri: URIRef = S223.Valve
    linkageInlet: MechanicalInletConnectionPoint
    position: PropertyReference
    command: PropertyReference
    position_feedback: PropertyReference
    flowCoefficient: Gallons


class TwoWayValve(Valve):
    """
    Two-way valve have 1 inlet and 1 outlet
    """

    _class_iri: URIRef = S223.TwoWayValve
    fluidInlet: WaterInletConnectionPoint
    fluidOutlet: WaterOutletConnectionPoint
    is_open: PropertyReference
    is_closed: PropertyReference

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _relations)
        self.fluidOutlet.paired_to(self.fluidInlet)

    def set_fluid_type(self, fluid: Fluid):
        self.set_medium(["fluidInlet", "fluidOutlet"], fluid)


class ThreeWayValveDiverting(Valve):
    """
    A diverting valve has 1 inlet and 2 outlets
    """

    _class_iri = S223.ThreeWayValve
    fluidInletAB: WaterInletConnectionPoint
    fluidOutletA: WaterOutletConnectionPoint
    fluidOutletB: WaterOutletConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _relations)
        self.fluidOutletA.paired_to(self.fluidInletAB)
        self.fluidOutletB.paired_to(self.fluidInletAB)

    def set_fluid_type(self, fluid: Fluid):
        self.set_medium(["fluidInletAB", "fluidOutletA", "fluidOutletB"], fluid)


class ThreeWayValveMixing(Valve):
    """
    A mixing valve has 2 inlet and 1 outlet
    """

    _class_iri: URIRef = S223.ThreeWayValve
    fluidInletA: WaterInletConnectionPoint
    fluidInletB: WaterOutletConnectionPoint
    fluidOutlet: WaterOutletConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _relations)
        self.fluidOutlet.paired_to(self.fluidInletA)
        self.fluidOutlet.paired_to(self.fluidInletB)

    def set_fluid_type(self, fluid: Fluid):
        self.set_medium(["fluidInletA", "fluidInletB", "fluidOutlet"], fluid)


class NaturalGasValve(Valve):
    _class_iri = S223.Valve
    naturalGasInlet: NaturalGasInletConnectionPoint
    naturalGasOutlet: NaturalGasOutletConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _relations)
        self.naturalGasOutlet.paired_to(self.naturalGasInlet)


class PneumaticValve(Valve):
    _class_iri = S223.Valve
    compressedAirInlet: CompressedAirInletConnectionPoint
    compressedAirOutlet: CompressedAirOutletConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _relations)
        self.compressedAirOutlet.paired_to(self.compressedAirInlet)


class ExpansionValve(Valve):
    _class_iri = S223.Valve
    portA: RefrigerantBidirectionalConnectionPoint
    portB: RefrigerantBidirectionalConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _relations)
        self.portB.paired_to(self.portA)

    def set_gas_type(self, gas: Refrigerant):
        self.set_medium(["portA", "portB"], gas)


class ReversingValve(Valve):
    _class_iri = S223.Valve
    refrigerantHighPressureInlet: RefrigerantInletConnectionPoint
    refrigerantLowPressureOutlet: RefrigerantOutletConnectionPoint
    refrigerantIndoorCoilPort: RefrigerantBidirectionalConnectionPoint
    refrigerantOutdoorCoilPort: RefrigerantBidirectionalConnectionPoint
    position: PropertyReference

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _relations)
        # self.refrigerantLowPressureOutlet.paired_to(self.refrigerantHighPressureInlet)

    def set_gas_type(self, gas: Refrigerant):
        self.set_medium(
            [
                "refrigerantHighPressureInlet",
                "refrigerantLowPressureOutlet",
                "refrigerantIndoorCoilPort",
                "refrigerantOutdoorCoilPort",
            ],
            gas,
        )
