from ..core import (
    BOB,
    S223,
    BidirectionalConnectionPoint,
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    Medium,
    OutletConnectionPoint,
)
from ..enum import Refrigerant

_namespace = BOB


class RefrigerantConnection(Connection):
    _volatile = ("hasMedium",)
    hasMedium: Medium = Refrigerant
    _class_iri = S223.Connection


class RefrigerantConnectionPoint(ConnectionPoint):
    _volatile = ("hasMedium",)
    hasMedium: Medium = Refrigerant


class RefrigerantInletConnectionPoint(InletConnectionPoint, RefrigerantConnectionPoint):
    _class_iri = S223.InletConnectionPoint


class RefrigerantOutletConnectionPoint(
    OutletConnectionPoint, RefrigerantConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class RefrigerantBidirectionalConnectionPoint(
    BidirectionalConnectionPoint, RefrigerantConnectionPoint
):
    _class_iri = S223.BidirectionalConnectionPoint
