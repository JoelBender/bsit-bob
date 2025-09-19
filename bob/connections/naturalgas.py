from ..core import (
    BOB,
    S223,
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    Medium,
    OutletConnectionPoint,
)
from ..enum import NaturalGas

_namespace = BOB


class NaturalGasConnection(Connection):
    hasMedium: Medium = NaturalGas
    _class_iri = S223.Connection


class NaturalGasConnectionPoint(ConnectionPoint):
    hasMedium: Medium = NaturalGas


class NaturalGasInletConnectionPoint(InletConnectionPoint, NaturalGasConnectionPoint):
    _class_iri = S223.InletConnectionPoint


class NaturalGasOutletConnectionPoint(OutletConnectionPoint, NaturalGasConnectionPoint):
    _class_iri = S223.OutletConnectionPoint
