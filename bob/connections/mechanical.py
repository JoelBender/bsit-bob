from ..core import (
    P223,
    S223,
    BidirectionalConnectionPoint,
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    Medium,
    OutletConnectionPoint,
)

_namespace = P223


# === GENERAL

MechanicalCoupling = Medium("MechanicalCoupling", _alt_namespace=P223)


class MechanicalConnection(Connection):
    hasMedium: Medium = MechanicalCoupling
    _class_iri = S223.Connection


class MechanicalConnectionPoint(ConnectionPoint):
    hasMedium: Medium = MechanicalCoupling


class MechanicalInletConnectionPoint(InletConnectionPoint, MechanicalConnectionPoint):
    _class_iri = S223.InletConnectionPoint


class MechanicalOutletConnectionPoint(OutletConnectionPoint, MechanicalConnectionPoint):
    _class_iri = S223.OutletConnectionPoint


class MechanicalBidirectionalConnectionPoint(
    BidirectionalConnectionPoint, MechanicalConnectionPoint
):
    _class_iri = S223.BidirectionalConnectionPoint
