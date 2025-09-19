from bob.connections.naturalgas import NaturalGasInletConnectionPoint
from bob.properties import PercentCommand

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...connections.electricity import ElectricalInletConnectionPoint
from ...connections.liquid import (
    SteamInletConnectionPoint,
    SteamOutletConnectionPoint,
    WaterInletConnectionPoint,
)
from ...core import BOB, S223, Equipment

_namespace = BOB


class SteamPipe(Equipment):
    # One way of providing humidity to air
    # a simple pie with steam
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    steamInlet: SteamInletConnectionPoint  # from the humidifier


class Humidifier(Equipment):
    _class_iri = S223.Humidifier
    steamOutlet: SteamOutletConnectionPoint
    waterInlet: WaterInletConnectionPoint


class ElectricalHumidifier(Humidifier):
    _class_iri = S223.Humidifier
    powerInlet: ElectricalInletConnectionPoint
    modulation = PercentCommand


class NaturalGasHumidifier(Humidifier):
    _class_iri = S223.Humidifier
    naturalGasInlet: NaturalGasInletConnectionPoint
    modulation = PercentCommand
