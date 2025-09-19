from ..core import BOB, PropertyReference
from ..producer import Function
from ..properties import PercentCommand, Temperature

_namespace = BOB

# WIP : For now, it won't be in hvacspace by default


class IndoorAir(Function):
    # uses_input
    heating: PercentCommand
    cooling: PercentCommand
    # produces_output
    temperture: Temperature
    hasOccupancySensor: PropertyReference
    # What if I need to connect more than 1 ???
    # def __init__(self, **kwargs):
