"""
Lofty - Real Estate Core Schema Classes for Bob
"""

from bob.core import (
    bind_namespace,
    Node as _Node,
    PhysicalSpace as _PhysicalSpace,
)

_namespace = REC = bind_namespace("rec", "https://w3id.org/rec#")


class Asset(_Node):
    """
    Something which is placed inside of a building, but is not an integral
    part of that building's structure; e.g., furniture, equipment,
    systems, etc.
    """

    pass


class ArchitecturalAsset(Asset):
    pass


class BarrierAsset(ArchitecturalAsset):
    pass


class AccessPanel(BarrierAsset):
    pass


class Door(BarrierAsset):
    pass


class Partition(BarrierAsset):
    pass


class Window(BarrierAsset):
    pass


class Furniture(Asset):
    pass


class Bed(Furniture):
    pass


class Bookcase(Furniture):
    pass


class BulletinBoard(Furniture):
    pass


class Cart(Furniture):
    pass


class ComputerCart(Cart):
    pass


class MailroomCart(Cart):
    pass


class PrinterCart(Cart):
    pass


class Chair(Furniture):
    pass


class FoldingChair(Chair):
    pass


class OfficeChair(Chair):
    pass


class CoatRack(Furniture):
    pass


class Desk(Furniture):
    pass


class MobileDesk(Desk):
    pass


class FilingCabinet(Furniture):
    pass


class FloorMat(Furniture):
    pass


class Footrest(Furniture):
    pass


class Lamp(Furniture):
    pass


class DeskLamp(Lamp):
    pass


class FloorLamp(Lamp):
    pass


class Safe(Furniture):
    pass


class Sofa(Furniture):
    pass


class Stand(Furniture):
    pass


class PrinterStand(Stand):
    pass


class TVStand(Stand):
    pass


class StorageCabinet(Furniture):
    pass


class Table(Furniture):
    pass


class CoffeeTable(Table):
    pass


class ConferenceTable(Table):
    pass


class EndTable(Table):
    pass


class FoldingTable(Table):
    pass


class ReceptionTable(Table):
    pass


class WasteBasket(Furniture):
    pass


class Collection(_Node):
    """
    An administrative grouping of entities that are adressed and treated
    as a unit for some purpose. These entities may have some spatial
    arrangement (e.g., an apartment is typically contiguous) but that is
    not a requirement (see, e.g., a distributed campus consisting of
    spatially disjoint plots or buildings). Inclusion in a Collection is
    determined by the 'includes' field on a specific subclass.
    """

    pass


class Apartment(Collection):
    pass


class Campus(Collection):
    """
    A campus represents a collection of location entities. The constituent
    locations may have differing legal ownership and utilization purposes,
    but they are generally perceived as a coherent unit or sub-region
    within a city or other region. E.g., a university campus, a hospital
    campus, a corporate campus, etc.
    """

    pass


class EquipmentCollection(Collection):
    pass


class FurnitureCollection(Collection):
    pass


class Portfolio(Collection):
    """
    A portfolio is a grouping of buildings, sites, apartments, campuses,
    etc. that share some business-relevant commonality, e.g., are managed
    by the same company, are rented out to the same tenant, share
    utilization or legal definition (industrial vs commercial), etc.
    """

    pass


class Premises(Collection):
    """
    A premises is an administrative grouping of spaces that are used for
    some commercial or industrial purpose by a real estate holder or
    tenant. E.g, a suite of offices, a shop, or an industrial workshop.
    """

    pass


class RealEstate(Collection):
    """
    The legal/administrative representation of some lands and/or
    buildings. I.e., "Fastighet" (Swedish), "Ejendom" (Denmark), etc.
    """

    pass


class Space(_PhysicalSpace):
    """
    A contiguous part of the physical world that contains or can contain
    sub-spaces. E.g., a Region can contain many Sites, which in turn can
    contain many Buildings.
    """

    pass


class Architecture(Space):
    """
    A designed/landscaped (or potentially designed/landscaped) part of the
    physical world that has a 3D spatial extent. E.g., a building site, a
    building, levels within the building, rooms, etc.
    """

    pass


class Building(Architecture):
    """
    A confined building structure.
    """

    pass


class Hospital(Building):
    pass


class School(Building):
    pass


class ShoppingMall(Building):
    pass


class Stadium(Building):
    pass


class VirtualBuilding(Building):
    pass


class Level(Architecture):
    """
    The level of a building, a.k.a. storey, floor, etc.
    """

    pass


class BasementLevel(Level):
    pass


class MezzanineLevel(Level):
    pass


class RoofLevel(Level):
    pass


class OutdoorSpace(Architecture):
    pass


class Room(Architecture):
    pass


class Atrium(Room):
    pass


class Auditorium(Room):
    pass


class BackOffice(Room):
    pass


class MailRoom(BackOffice):
    pass


class Bathroom(Room):
    pass


class Bedroom(Room):
    pass


class Cinema(Room):
    pass


class CleaningRoom(Room):
    pass


class CloakRoom(Room):
    pass


class ConferenceRoom(Room):
    pass


class ConversationRoom(Room):
    pass


class CopyingRoom(Room):
    pass


class DressingRoom(Room):
    pass


class EducationalRoom(Room):
    pass


class Classroom(EducationalRoom):
    pass


class GroupRoom(EducationalRoom):
    pass


class SmallStudyRoom(EducationalRoom):
    pass


class ElevatorRoom(Room):
    pass


class ElevatorShaft(Room):
    pass


class Entrance(Room):
    pass


class MainEntrance(Entrance):
    pass


class ServiceEntrance(Entrance):
    pass


class ExerciseRoom(Room):
    pass


class ExhibitionRoom(Room):
    pass


class FoodHandlingRoom(Room):
    pass


class BarRoom(FoodHandlingRoom):
    pass


class CafeteriaRoom(FoodHandlingRoom):
    pass


class CookingRoom(FoodHandlingRoom):
    pass


class DiningRoom(FoodHandlingRoom):
    pass


class DishingRoom(FoodHandlingRoom):
    pass


class Kitchenette(FoodHandlingRoom):
    pass


class Pantry(FoodHandlingRoom):
    pass


class Garage(Room):
    pass


class BicycleGarage(Garage):
    pass


class Hallway(Room):
    pass


class HealthcareRoom(Room):
    pass


class AdmittingRoom(HealthcareRoom):
    pass


class Morgue(HealthcareRoom):
    pass


class NeonatalNursingRoom(HealthcareRoom):
    pass


class OperatingRoom(HealthcareRoom):
    pass


class OutpatientServicesRoom(HealthcareRoom):
    pass


class PharmacyRoom(HealthcareRoom):
    pass


class RadiologyRoom(HealthcareRoom):
    pass


class TherapyRoom(HealthcareRoom):
    pass


class Laboratory(Room):
    pass


class LaboratoryDry(Laboratory):
    pass


class LaboratoryWet(Laboratory):
    pass


class LaundryRoom(Room):
    pass


class Library(Room):
    pass


class LivingRoom(Room):
    pass


class LoadingReceivingRoom(Room):
    pass


class LockerRoom(Room):
    pass


class MeditationRoom(Room):
    pass


class MothersRoom(Room):
    pass


class MultiPurposeRoom(Room):
    pass


class Office(Room):
    pass


class OfficeLandscape(Office):
    pass


class OfficeRoom(Office):
    pass


class PhoneBooth(Office):
    pass


class PersonalHygiene(Room):
    pass


class DisabledToilet(PersonalHygiene):
    pass


class Sauna(PersonalHygiene):
    pass


class ShowerRoom(PersonalHygiene):
    pass


class Toilet(PersonalHygiene):
    pass


class Reception(Room):
    pass


class RecordingRoom(Room):
    pass


class RecreationalRoom(Room):
    pass


class RestingRoom(Room):
    pass


class RetailRoom(Room):
    pass


class FittingRoom(RetailRoom):
    pass


class SecurityRoom(Room):
    pass


class ServiceShaft(Room):
    pass


class Shelter(Room):
    pass


class ShelterGasLock(Shelter):
    pass


class ShelterRoom(Shelter):
    pass


class StaffRoom(Room):
    pass


class Stairwell(Room):
    pass


class Storage(Room):
    pass


class Theater(Room):
    pass


class TreatmentRoom(Room):
    pass


class TreatmentWaitingRoom(TreatmentRoom):
    pass


class UtilitiesRoom(Room):
    pass


class Cabinet(UtilitiesRoom):
    pass


class CableRoom(UtilitiesRoom):
    pass


class TelecommunicationRoom(CableRoom):
    pass


class ClimateControlRoom(UtilitiesRoom):
    pass


class DataServerRoom(UtilitiesRoom):
    pass


class ElectricityRoom(UtilitiesRoom):
    pass


class SprinklerRoom(UtilitiesRoom):
    pass


class WasteManagementRoom(Room):
    pass


class Workshop(Room):
    pass


class Site(Architecture):
    """
    A piece of land upon which zero or more buildings may be situated.
    """

    pass


class SubBuilding(Architecture):
    pass


class Zone(Architecture):
    """
    A sub-zone within or outside of a building defined to support some
    technology and/or use, e.g., an HVAC zone, a parking space, a security
    zone, etc.
    """

    pass


class AccessControlZone(Zone):
    pass


class HVACZone(Zone):
    pass


class OccupancyZone(Zone):
    """
    Occupancy Zone is a spatial area where devices are monitoring or
    reporting on the concept of Occupancy (motion sensors, people
    counters, cameras, etc.)
    """

    pass


class ParkingSpace(Zone):
    pass


class Workspace(Zone):
    pass


class Region(Space):
    """
    An administrative geospatial unit larger than the individual real
    estate. For instance, "Lombary", "North America", "The Back Bay",
    "Elnätsområde Syd", etc.
    """

    pass


class Information(_Node):
    pass


class ArchitectureArea(Information):
    """
    Describes business-relevant area measurements typically associated
    with architected spaces. As the exact requirements on these
    measurements will vary from case to case or jurisdiction to
    jurisdiction, subclassing and specializing this definition is
    encouraged.
    """

    pass


class ArchitectureCapacity(Information):
    """
    Describes business-relevant capacity measurements typically associated
    with architected spaces. As the exact requirements on these
    measurements will vary from case to case or jurisdiction to
    jurisdiction, subclassing and specializing this definition is
    encouraged.
    """

    pass


class Document(Information):
    pass


class LeaseContract(Document):
    """
    Formal document that identifies the Tenant and the leased asset or
    property; states lease term and fee (rent), and detailed terms and
    conditions of the lease agreement.
    """

    pass


class Geometry(Information):
    pass


class MultiPoint(Geometry):
    pass


class MultiPolygon(Geometry):
    pass


class Point(Geometry):
    pass


class Polygon(Geometry):
    pass


class Georeference(Information):
    """
    A georeference creates a relationship between a local coordinate
    system into a geographic coordinate system.
    """

    pass


class Geotransform(Georeference):
    """
    A transform following GDAL's Affine Transform that transforms a local
    coordinate into a WGS84 coordinate. Created from Ground Control Points
    (GCP) using GDAL's GCPsToGeotransform method.
    """

    pass


class PointOfInterest(Information):
    pass


class PostalAddress(Information):
    pass


class ServiceObject(Information):
    pass


class AlarmObject(ServiceObject):
    pass


class ErrorReport(ServiceObject):
    pass


class NotificationObject(ServiceObject):
    pass


class WorkOrder(ServiceObject):
    pass


class ICTEquipment:
    """
    Equipment and devices that are part of a building's ICT
    infrastructure.
    """

    pass


class AudioVisualEquipment(ICTEquipment):
    """
    Audio visual equipment.
    """

    pass


class Controller(ICTEquipment):
    """
    Controller.
    """

    pass


class BACnetController(Controller):
    """
    BACnet controller.
    """

    pass


class ModbusController(Controller):
    """
    Modbus controller.
    """

    pass


class DataNetworkEquipment(ICTEquipment):
    """
    Data network equipment.
    """

    pass


class EthernetPort(DataNetworkEquipment):
    """
    Ethernet port.
    """

    pass


class EthernetSwitch(DataNetworkEquipment):
    """
    Ethernet switch.
    """

    pass


class NetworkRouter(DataNetworkEquipment):
    """
    Network router.
    """

    pass


class NetworkSecurityEquipment(DataNetworkEquipment):
    """
    Network security equipment.
    """

    pass


class WirelessAccessPoint(DataNetworkEquipment):
    """
    Wireless access point.
    """

    pass


class Gateway(ICTEquipment):
    """
    Gateway.
    """

    pass


class ICTHardware(ICTEquipment):
    """
    ICT hardware.
    """

    pass


class Server(ICTHardware):
    """
    Server.
    """

    pass


class ITRack(ICTEquipment):
    """
    IT rack.
    """

    pass


class SensorEquipment(ICTEquipment):
    """
    Sensor equipment.
    """

    pass


class DaylightSensorEquipment(SensorEquipment):
    """
    Daylight sensor.
    """

    pass


class IAQSensorEquipment(SensorEquipment):
    """
    Indoor air quality sensor.
    """

    pass


class LeakDetectorEquipment(SensorEquipment):
    """
    Leak detector.
    """

    pass


class OccupancySensorEquipment(SensorEquipment):
    """
    Occupancy sensor.
    """

    pass


class PeopleCountSensorEquipment(SensorEquipment):
    """
    People count sensor.
    """

    pass


class ThermostatEquipment(SensorEquipment):
    """
    Thermostat.
    """

    pass


class VibrationSensorEquipment(SensorEquipment):
    """
    Vibration sensor.
    """

    pass


class BuildingElement(_Node):
    """
    A part that constitutes a piece of a building's structural makeup.
    E.g., Facade, Wall, Slab, Roof, etc.
    """

    pass


class Balcony(BuildingElement):
    pass


class Facade(BuildingElement):
    pass


class Roof(BuildingElement):
    pass


class Slab(BuildingElement):
    pass


class Wall(BuildingElement):
    pass


class WallInner(Wall):
    pass


class Event(_Node):
    """
    A temporally indexed entity, e.g., an observation, a lease, a
    construction project, etc. Can be instantaneous (timestamp property
    assigned) or have temporal extent (start and end properties assigned).
    Subclasses may define specific behaviour and requirements, e.g., on
    spatial indexing, agent participation, etc.
    """

    pass


class ElevatorTrip(Event):
    pass


class Lease(Event):
    pass


class PointEvent(Event):
    """
    An event emanating from or targeting a Point; e.g., an individual
    Observation from a Sensor point, or an Actuation sent to a Command
    point. In other terms, the Points indicate the capability of some
    Space or Equipment to emit or accept data, while this class represents
    those actual data messages. Note that in most non-trivially sized
    systems, these events are not stored in the knowledge graph itself,
    but are rather forwarded to some C&C system or time series database.
    """

    pass


class ActuationEvent(PointEvent):
    pass


class ExceptionEvent(PointEvent):
    pass


class ObservationEvent(PointEvent):
    pass


class AbsoluteHumidityObservation(ObservationEvent):
    pass


class AccelerationObservation(ObservationEvent):
    pass


class AngleObservation(ObservationEvent):
    pass


class AngularAccelerationObservation(ObservationEvent):
    pass


class AngularVelocityObservation(ObservationEvent):
    pass


class AreaObservation(ObservationEvent):
    pass


class BooleanValueObservation(ObservationEvent):
    """
    Generic xsd:boolean value observation that is not specific to any
    particular QUDT quantitykind or unit.
    """

    pass


class CapacitanceObservation(ObservationEvent):
    pass


class DataRateObservation(ObservationEvent):
    pass


class DataSizeObservation(ObservationEvent):
    pass


class DensityObservation(ObservationEvent):
    pass


class DistanceObservation(ObservationEvent):
    pass


class DoubleValueObservation(ObservationEvent):
    """
    Generic xsd:double value observation that is not specific to any
    particular QUDT quantitykind or unit.
    """

    pass


class ElectricChargeObservation(ObservationEvent):
    pass


class ElectricCurrentObservation(ObservationEvent):
    pass


class EnergyObservation(ObservationEvent):
    pass


class ForceObservation(ObservationEvent):
    pass


class FrequencyObservation(ObservationEvent):
    pass


class IlluminanceObservation(ObservationEvent):
    pass


class InductanceObservation(ObservationEvent):
    pass


class IntegerValueObservation(ObservationEvent):
    """
    Generic xsd:int value observation that is not specific to any
    particular QUDT quantitykind or unit.
    """

    pass


class LengthObservation(ObservationEvent):
    pass


class LuminanceObservation(ObservationEvent):
    pass


class LuminousFluxObservation(ObservationEvent):
    pass


class LuminousIntensityObservation(ObservationEvent):
    pass


class MagneticFluxObservation(ObservationEvent):
    pass


class MassFlowRateObservation(ObservationEvent):
    pass


class MassObservation(ObservationEvent):
    pass


class PowerObservation(ObservationEvent):
    pass


class PressureObservation(ObservationEvent):
    pass


class RelativeHumidityObservation(ObservationEvent):
    pass


class ResistanceObservation(ObservationEvent):
    pass


class SoundPressureObservation(ObservationEvent):
    pass


class TemperatureObservation(ObservationEvent):
    pass


class ThrustObservation(ObservationEvent):
    pass


class TimeSpanObservation(ObservationEvent):
    pass


class TorqueObservation(ObservationEvent):
    pass


class VelocityObservation(ObservationEvent):
    pass


class VoltageObservation(ObservationEvent):
    pass


class VolumeFlowRateObservation(ObservationEvent):
    pass


class VolumeObservation(ObservationEvent):
    pass


class Agent(_Node):
    """
    The human, group, or machine that consumes or acts upon an object or
    data. This higher-level grouping allows properties that are shared
    among its subclasses (Person, Organization, ....) to be anchored in
    one joint place, on the Agent class.
    """

    pass


class Organization(Agent):
    """
    An organization of any sort (e.g., a business, association, project,
    consortium, tribe, etc.)
    """

    pass


class Company(Organization):
    pass


class Department(Organization):
    pass


class Person(Agent):
    """
    A natural person (i.e., an individual human being).
    """

    pass
