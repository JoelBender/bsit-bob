# Core Concepts (ASHRAE 223P)

- Equipment: Tangible device or component (fan, valve, VFD, sensor package).
- System: Grouping of equipment, with connections at the same level.
- Space/Zone: Physical or functional spaces; supported but often modeled separately.
- ConnectionPoint (CP): Typed ports on equipment/systems (e.g., AirInletConnectionPoint).
- Connection: Link between two compatible CPs, sharing a Medium.
- Medium: Substance/domain carried (Air, Water, Steam, Electricity.Signal, etc.).
- Constituent: Allows a medium to include another medium (e.g., Steam as constituent of Air for humidification).
- Junction: Multi-port node for merging/splitting flows; supports boundaries.
- BoundaryConnectionPoint: Declares model boundaries for partial models.
- Properties: Modeled values (e.g., Temperature) possibly linked to sensors and references.
- Sensor: Measurement device class; often embedded inside Equipment that provides IO CPs.
- ObservationLocation: Where a sensor observes (Connectable).
- ReferenceLocation: The comparison location for differential sensors.
- InternalReference: Maps a device’s property to the model’s property (within graph).
- ExternalReference: Maps a property to an external system point (e.g., BACnet object).

MapsTo and Layers
- Use mapsTo to expose internal CPs at a higher level only when necessary.
- Prefer “flat” systems where most external connections happen at one layer.

Related
- [Systems vs Equipment](systems-vs-equipment.md)
- [Junctions and Boundaries](junctions-and-boundaries.md)
