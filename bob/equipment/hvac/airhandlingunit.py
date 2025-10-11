import logging

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...core import BOB, S223, Equipment

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = BOB

class AirHandlingUnit(Equipment):
    _class_iri = S223.AirHandlingUnit
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
