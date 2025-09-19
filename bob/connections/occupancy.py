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

_namespace = BOB


class OccupancyConnection(Connection):
    hasMedium: Medium
    _class_iri = S223.Connection


class OccupancyConnectionPoint(ConnectionPoint):
    hasMedium: Medium


class OccupancyInletConnectionPoint(OccupancyConnectionPoint, InletConnectionPoint):
    _class_iri = S223.InletConnectionPoint


class OccupancyOutletConnectionPoint(OccupancyConnectionPoint, OutletConnectionPoint):
    _class_iri = S223.OutletConnectionPoint


class OccupancyZoneConnectionPoint(ZoneConnectionPoint):
    hasMedium: Medium
    _class_iri = S223.ZoneConnectionPoint


class OccupancyInletZoneConnectionPoint(
    OccupancyZoneConnectionPoint, InletZoneConnectionPoint
):
    _class_iri = BOB.InletZoneConnectionPoint


class OccupancyOutletZoneConnectionPoint(
    OccupancyZoneConnectionPoint, OutletZoneConnectionPoint
):
    _class_iri = BOB.OutletZoneConnectionPoint
