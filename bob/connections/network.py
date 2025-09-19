from rdflib import Literal

from ..core import (
    BOB,
    P223,
    S223,
    BidirectionalConnectionPoint,
    Connection,
    ConnectionPoint,
)
from bob.enum import ProtocolEnum
from bob.properties.network import Mbit_per_seconds
from ..enum import PowerAndSignal, Signal

_namespace = BOB


# === Networks - RS485


class RS485Connection(Connection):
    hasMedium = Signal.RS485
    _class_iri = S223.Connection


class RS485ConnectionPoint(ConnectionPoint):
    _attr_uriref = {"hasProtocol": P223.hasProtocol}

    hasMedium = Signal.RS485
    hasProtocol: ProtocolEnum


class RS485BidirectionalConnectionPoint(
    BidirectionalConnectionPoint, RS485ConnectionPoint
):
    _class_iri = S223.BidirectionalConnectionPoint


# === Networks - Ethernet


class EthernetConnection(Connection):
    hasMedium = Signal.Ethernet
    _class_iri = S223.Connection


class EthernetConnectionPoint(ConnectionPoint):
    _attr_uriref = {
        "hasProtocol": P223.hasProtocol,
        "data_rate": P223.data_rate,
        "vlan": P223.VLAN,
    }
    hasMedium = Signal.Ethernet
    hasProtocol: ProtocolEnum
    data_rate: Mbit_per_seconds
    vlan: Literal


class EthernetBidirectionalConnectionPoint(
    BidirectionalConnectionPoint, EthernetConnectionPoint
):
    _class_iri = S223.BidirectionalConnectionPoint


# === Networks - PoE


class PoEConnection(Connection):
    hasMedium = PowerAndSignal.PoE
    _class_iri = S223.Connection


class PoEConnectionPoint(ConnectionPoint):
    _attr_uriref = {
        "hasProtocol": P223.hasProtocol,
        "data_rate": P223.data_rate,
        "vlan": BOB.VLAN,
    }
    hasMedium = PowerAndSignal.PoE
    hasProtocol: ProtocolEnum
    data_rate: Mbit_per_seconds
    vlan: Literal


class PoEBidirectionalConnectionPoint(BidirectionalConnectionPoint, PoEConnectionPoint):
    _class_iri = S223.BidirectionalConnectionPoint
