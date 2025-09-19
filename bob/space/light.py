from bob.connections.light import LightVisibleInletConnectionPoint
from bob.properties.states import OccupancyStatus

from ..core import BOB, Domain, DomainSpace, PropertyReference, Zone

_namespace = BOB


class LightingSpace(DomainSpace):
    _class_iri = BOB.LightingSpace
    hasDomain = Domain.Lighting
    lightInlet: LightVisibleInletConnectionPoint
    naturalLightInlet: LightVisibleInletConnectionPoint
    occupancy: OccupancyStatus


class LightingZone(Zone):
    _class_iri = BOB.LightingZone
    hasDomain = Domain.Lighting
    # lightInlet: LightVisibleInletZoneConnectionPoint
    occupancy: PropertyReference  # promoted from a space
