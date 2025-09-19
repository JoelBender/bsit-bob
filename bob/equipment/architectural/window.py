from bob.connections.air import AirBidirectionalConnectionPoint
from bob.connections.light import (
    LightVisibleInletConnectionPoint,
    LightVisibleOutletConnectionPoint,
)
from bob.core import BOB, S223, Equipment, PropertyReference

_namespace = BOB


class Window(Equipment):
    _class_iri = S223.Window
    indoor: AirBidirectionalConnectionPoint
    outdoor: AirBidirectionalConnectionPoint
    naturalLightInlet: LightVisibleInletConnectionPoint
    naturalLightOutlet: LightVisibleOutletConnectionPoint

    # Those will come from something else, but be accessible from here.
    openCloseStatus: PropertyReference
    openCloseCommand: PropertyReference
    shadeStatus: PropertyReference
    shadeCommand: PropertyReference
    breakDetection: PropertyReference
