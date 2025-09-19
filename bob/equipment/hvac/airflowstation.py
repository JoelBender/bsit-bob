from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...core import BOB, S223, Equipment
from ...sensor import Sensor

_namespace = BOB


class AirFlowMonitor(Equipment):
    _class_iri = S223.FlowSensor
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    flowSensor: Sensor


# TODO : Create the template and make that the same than the others.
