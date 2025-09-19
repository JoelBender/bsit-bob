from ..core import (
    BOB,
    S223,
    BidirectionalConnectionPoint,
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    InletZoneConnectionPoint,
    Medium,
    OutletConnectionPoint,
    OutletZoneConnectionPoint,
    ZoneConnectionPoint,
)
from ..enum import Air

_namespace = BOB


class AirConnection(Connection):
    hasMedium: Medium = Air
    _class_iri = S223.Connection


class AirConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Air


class AirInletConnectionPoint(AirConnectionPoint, InletConnectionPoint):
    _class_iri = S223.InletConnectionPoint


class AirOutletConnectionPoint(AirConnectionPoint, OutletConnectionPoint):
    _class_iri = S223.OutletConnectionPoint


class AirBidirectionalConnectionPoint(AirConnectionPoint, BidirectionalConnectionPoint):
    _class_iri = S223.BidirectionalConnectionPoint


class AirZoneConnectionPoint(ZoneConnectionPoint):
    hasMedium: Medium = Air
    _class_iri = BOB.ZoneConnectionPoint


class AirInletZoneConnectionPoint(AirZoneConnectionPoint, InletZoneConnectionPoint):
    _class_iri = BOB.InletZoneConnectionPoint


class AirOutletZoneConnectionPoint(AirZoneConnectionPoint, OutletZoneConnectionPoint):
    _class_iri = BOB.OutletZoneConnectionPoint


class CompressedAirConnection(Connection):
    hasMedium = Air.CompressedAir
    _class_iri = S223.Connection


class CompressedAirConnectionPoint(ConnectionPoint):
    hasMedium = Air.CompressedAir


class CompressedAirInletConnectionPoint(
    CompressedAirConnectionPoint, InletConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class CompressedAirOutletConnectionPoint(
    CompressedAirConnectionPoint, OutletConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint
