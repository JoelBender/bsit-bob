from bob.connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from bob.connections.light import (
    LightVisibleInletConnectionPoint,
    LightVisibleOutletConnectionPoint,
)
from bob.core import S223, Equipment

_namespace = S223


class Window(Equipment):
    _class_iri = S223.Window
    indoor: AirInletConnectionPoint
    outdoor: AirOutletConnectionPoint
    naturalLightInlet: LightVisibleInletConnectionPoint
    naturalLightOutlet: LightVisibleOutletConnectionPoint