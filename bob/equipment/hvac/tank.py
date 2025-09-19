from typing import Dict

from ...connections.liquid import (
    FluidBidirectionalConnectionPoint,
    FluidInletConnectionPoint,
    FluidOutletConnectionPoint,
)
from ...core import BOB, P223, Equipment
from ...enum import Fluid, Water
from ...properties.force import Pressure
from ...properties.temperature import Temperature
from ...template import template_update

_namespace = BOB


class Tank(Equipment):
    _class_iri = P223.Tank
    fluidInlet: FluidInletConnectionPoint
    fluidOutlet: FluidOutletConnectionPoint
    containedFluid: FluidBidirectionalConnectionPoint

    fluidTemperature: Temperature
    internalPressure: Pressure

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self.fluidOutlet.paired_to(self.fluidInlet)

    def set_fluid_type(self, fluid: Fluid = Water):
        self.set_medium(["leavingFluid", "enteringFluid", "containedFluid"], fluid)
