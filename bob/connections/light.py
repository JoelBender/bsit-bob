from ..core import (
    BOB,
    S223,
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    InletZoneConnectionPoint,
    Medium,
    OutletConnectionPoint,
    OutletZoneConnectionPoint,
    ZoneConnectionPoint,
)
from ..enum import Light

_namespace = BOB


# === Light
class LightConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Light


class LightInletConnectionPoint(LightConnectionPoint, InletConnectionPoint):
    pass


class LightOutletConnectionPoint(LightConnectionPoint, OutletConnectionPoint):
    _class_iri = S223.OutletConnectionPoint


class LightZoneConnectionPoint(ZoneConnectionPoint):
    hasMedium: Medium = Light
    _class_iri = BOB.ZoneConnectionPoint


class LightInletZoneConnectionPoint(LightZoneConnectionPoint, InletZoneConnectionPoint):
    _class_iri = BOB.InletZoneConnectionPoint


class LightOutletZoneConnectionPoint(
    LightZoneConnectionPoint, OutletZoneConnectionPoint
):
    _class_iri = BOB.OutletZoneConnectionPoint


class LightVisibleConnection(Connection):
    hasMedium = Light.Visible
    _class_iri = S223.Connection


class LightVisibleConnectionPoint(ConnectionPoint):
    hasMedium = Light.Visible


class LightVisibleInletConnectionPoint(
    LightVisibleConnectionPoint, InletConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class LightVisibleOutletConnectionPoint(
    LightVisibleConnectionPoint, OutletConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class LightVisibleZoneConnectionPoint(ZoneConnectionPoint):
    hasMedium = Light.Visible
    _class_iri = BOB.ZoneConnectionPoint


class LightVisibleInletZoneConnectionPoint(
    LightVisibleZoneConnectionPoint, InletZoneConnectionPoint
):
    _class_iri = BOB.InletZoneConnectionPoint


class LightVisibleOutletZoneConnectionPoint(
    LightVisibleZoneConnectionPoint, OutletZoneConnectionPoint
):
    _class_iri = BOB.OutletZoneConnectionPoint
