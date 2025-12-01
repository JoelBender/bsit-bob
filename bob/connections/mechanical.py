from ..core import (
    P223,
    S223,
    BidirectionalConnectionPoint,
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    Medium,
    OutletConnectionPoint,
    MechanicalLinkage,
)

_namespace = S223


# === GENERAL


class MechanicalConnection(Connection):
    hasMedium: Medium = MechanicalLinkage
    _class_iri = S223.Connection


class MechanicalConnectionPoint(ConnectionPoint):
    hasMedium: Medium = MechanicalLinkage


class MechanicalInletConnectionPoint(InletConnectionPoint, MechanicalConnectionPoint):
    _class_iri = S223.InletConnectionPoint


class MechanicalOutletConnectionPoint(OutletConnectionPoint, MechanicalConnectionPoint):
    _class_iri = S223.OutletConnectionPoint


class MechanicalBidirectionalConnectionPoint(
    BidirectionalConnectionPoint, MechanicalConnectionPoint,
):
    _class_iri = S223.BidirectionalConnectionPoint
