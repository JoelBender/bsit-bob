from bob.connections.air import AirBidirectionalConnectionPoint
from bob.connections.light import LightVisibleOutletConnectionPoint
from bob.core import BOB, S223, Equipment, PropertyReference

_namespace = BOB


class Door(Equipment):
    _class_iri = S223.Door
    door: AirBidirectionalConnectionPoint
    naturalLight: LightVisibleOutletConnectionPoint

    # Those will come from something else, but be accessible from here.
    openCloseStatus: PropertyReference
    openCloseCommand: PropertyReference
