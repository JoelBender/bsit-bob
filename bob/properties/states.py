from rdflib import URIRef

from ..core import (
    BOB,
    S223,
    EnumerableProperty,
    EnumeratedActuatableProperty,
    EnumeratedObservableProperty,
    Medium,
    Substance,
)
from ..enum import (
    Light,
    Motion,
    NormalAlarmEnum,
    Occupancy,
    OnOff,
    Position,
    Smoke,
    YesNoEnum,
)

_namespace = BOB


# On Off Status is telemetry so the value depends on hasExternalReference
# Using EnumerationKind will lead to the reading being written down in the model
# which is not what we want. We want to know where to find this real time status.


class OnOffStatus(EnumeratedObservableProperty):
    _class_iri: URIRef = S223.EnumeratedObservableProperty
    hasEnumerationKind = OnOff
    hasValue: OnOff


class OnOffCommand(EnumeratedActuatableProperty):
    _class_iri: URIRef = S223.EnumeratedActuatableProperty
    hasEnumerationKind = OnOff
    hasValue: OnOff


class NormalAlarmStatus(EnumeratedObservableProperty):
    _class_iri: URIRef = S223.EnumeratedObservableProperty
    hasEnumerationKind = NormalAlarmEnum
    hasValue: NormalAlarmEnum


class OpenCloseCommand(EnumeratedActuatableProperty):
    _class_iri: URIRef = S223.EnumeratedActuatableProperty
    hasEnumerationKind = Position
    hasValue: Position


class OpenCloseStatus(EnumeratedActuatableProperty):
    _class_iri: URIRef = S223.EnumeratedActuatableProperty
    hasEnumerationKind = Position
    hasValue: Position


class Schedule(EnumerableProperty):
    _class_iri: URIRef = S223.EnumerableProperty
    hasEnumerationKind = Occupancy
    hasValue: Occupancy


class OccupancyStatus(EnumeratedObservableProperty):
    _class_iri: URIRef = S223.EnumeratedObservableProperty
    hasEnumerationKind = Occupancy
    hasValue: Occupancy


class Motion(EnumeratedObservableProperty):
    _class_iri: URIRef = S223.EnumeratedObservableProperty
    hasEnumerationKind = Motion
    hasValue: Motion


class SmokePresence(EnumeratedObservableProperty):
    ofMedium: Medium  # set from the sensor
    ofSubstance: Substance = Smoke
    # isObservedBy: Sensor
    hasEnumerationKind = YesNoEnum
    hasValue: YesNoEnum


class DaylightDetected(EnumeratedObservableProperty):
    ofMedium: Light.Visible
    hasEnumerationKind = YesNoEnum
    hasValue: YesNoEnum
