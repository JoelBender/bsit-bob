from bob.connections.air import (
    AirBidirectionalConnectionPoint,
    AirInletConnectionPoint,
    AirInletZoneConnectionPoint,
    AirOutletConnectionPoint,
    AirOutletZoneConnectionPoint,
)
from bob.properties import (
    AirChangePerHour,
    GasConcentration,
    OccupancyStatus,
    RelativeHumidity,
    Temperature,
)

from ..core import BOB, Domain, DomainSpace, Setpoint, Zone

_namespace = BOB


class HVACSpace(DomainSpace):
    _class_iri = BOB.HVACSpace
    hasDomain = Domain.HVAC
    # hasMedium: Medium = Air
    # Connection points
    ductAirInlet: AirInletConnectionPoint
    ductAirOutlet: AirOutletConnectionPoint
    airTransfer: AirBidirectionalConnectionPoint
    doors: AirBidirectionalConnectionPoint
    windows: AirBidirectionalConnectionPoint
    radiantHeating: AirBidirectionalConnectionPoint
    radiantCooling: AirBidirectionalConnectionPoint

    # Function Block
    # indoorAir: IndoorAir

    # Properties
    occupancy: OccupancyStatus
    temperature: Temperature
    temperature_setpoint: Setpoint
    humidity: RelativeHumidity
    co2: GasConcentration
    co: GasConcentration
    no2: GasConcentration
    airChangePerHour: AirChangePerHour


class HVACZone(Zone):
    _class_iri = BOB.HVACZone
    hasDomain = Domain.HVAC

    # Connection points
    airInlet: AirInletZoneConnectionPoint
    airOutlet: AirOutletZoneConnectionPoint

    # Properties
    occupancy: OccupancyStatus
    temperature: Temperature
    temperature_setpoint: Setpoint
    co2: GasConcentration
