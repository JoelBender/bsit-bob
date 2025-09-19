from bob.enum import AnalogSignalTypeEnum, BinarySignalTypeEnum

from ..core import (
    BOB,
    P223,
    S223,
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    OutletConnectionPoint,
)
from ..enum import Electricity, ModulatedSignal

_namespace = BOB
# It is modeling dry contact, Triac and other On-Off relationships


# === GENERAL
class OnOffSignalConnection(Connection):
    hasMedium = Electricity.OnOffSignal
    _class_iri = S223.Connection


class OnOffSignalConnectionPoint(ConnectionPoint):
    _attr_uriref = {"hasSignalType": P223.hasSignalType}

    hasMedium = Electricity.OnOffSignal
    hasSignalType: BinarySignalTypeEnum


class OnOffSignalInletConnectionPoint(InletConnectionPoint, OnOffSignalConnectionPoint):
    _class_iri = P223.BinaryInput


class OnOffSignalOutletConnectionPoint(
    OutletConnectionPoint, OnOffSignalConnectionPoint
):
    _class_iri = P223.BinaryOutput


# This is high level and we don't know if it's using 0-10VDC, 4-20mA, etc...
# === Modulation signals


class ModulationSignalConnection(Connection):
    hasMedium = ModulatedSignal
    _class_iri = S223.Connection


class ModulationSignalConnectionPoint(ConnectionPoint):
    _attr_uriref = {"hasSignalType": P223.hasSignalType}

    hasMedium = ModulatedSignal
    hasSignalType: AnalogSignalTypeEnum


class ModulationSignalInletConnectionPoint(
    InletConnectionPoint, ModulationSignalConnectionPoint
):
    _class_iri = P223.AnalogInput


class ModulationSignalOutletConnectionPoint(
    OutletConnectionPoint, ModulationSignalConnectionPoint
):
    _class_iri = P223.AnalogOutput
