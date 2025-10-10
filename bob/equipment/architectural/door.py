from bob.connections.air import AirBidirectionalConnectionPoint
from bob.core import S223, Equipment

_namespace = S223


class Door(Equipment):
    _class_iri = S223.Door
    door: AirBidirectionalConnectionPoint
