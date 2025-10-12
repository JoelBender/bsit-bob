# YAML Syntax Reference

This section covers the syntax used in templates. si-builder cover the bases of templates
and more options will be available by using si-modeler and si-templates packages. Those
two are not covered here.

Top-level keys
- name: Template identifier
- template_class: System | Equipment | Controller | Space | Junction …
- params: Free-form metadata (label, comment, etc.)
- properties: Property nodes (class, unit)
- sensors: Sensor nodes (if modeled directly)
- cp: Connection points (typed inlets/outlets)
- equipment: Child equipment defined in-line
- physical_spaces: Ducts, rooms, plenums, zones…
- from_catalog: Reusable parts (optional; core docs avoid external catalogs)
- junctions: Multi-port nodes
- boundaries: Boundary CPs (also via operator Node|cp)
- <domain>_connections: air/electrical/water/steam/signal/controllers
- sensors_observation_location: Map sensors to connectables
- internal_references / external_references: Property mappings (also via @)

## One operator: "->" (arrow)

YAML uses a single operator "->" for all directional relations to keep templates simple. The meaning of the arrow is determined by the section name:

- <domain>_connections (air_connections, water_connections, signal_connections, controllers, …)
  - Left -> Right means “flow/signal goes from Left to Right.”
  - Use explicit connection points when possible: Equipment.cpName.
  - Example:
    ```yaml
    air_connections:
      - SF.airOutlet -> Coil.airInlet
      - OADPR.damper.airOutlet -> MixedAirDuct.fromOutdoorAir
    ```

- sensors_observation_location
  - Sensor observes target: Sensor -> Target.
  - Equivalent Python shorthand: sensor % target
  - Target can be a Connectable or a specific Property.
  - Example:
    ```yaml
    sensors_observation_location:
      - SAT_Sensor -> AHU.supplyAirTemperature
    ```

- internal_references / external_references
  - Map a source property to an internal/external reference: Source -> Target.
  - Example:
    ```yaml
    external_references:
      - AHU.supplyAirTemperature -> BACnet:device/300/object/AI:5
    ```

- boundaries
  - Expose an internal CP at the System boundary: InternalCP -> BoundaryCP.
  - Example:
    ```yaml
    boundaries:
      - AHU.SA_Duct.airOutlet -> supplyAir  # supplyAir is a boundary CP name
    ```

Notes
- In YAML, containment/membership is implied by structure (equipment listed under a System), not by an operator.
- Python code may still use overloaded operators (>>, <<, |, @, +=, %) for brevity. YAML intentionally standardizes on "->".
- Always prefer explicit CP names (e.g., airOutlet/airInlet). If omitted, resolution is template-specific and may error.

Abridged template (System)
```yaml
name: ahu_template
template_class: System
params:
  label: "SYSTEM 1"

equipment:
  SF:
    class: Fan
    cp:
      airInlet: AirInletConnectionPoint
      airOutlet: AirOutletConnectionPoint

junctions:
  MixedAirDuct:
    class: Junction
    hasMedium: Fluid.Air
    fromReturnAir: AirInletConnectionPoint
    fromOutdoorAir: AirInletConnectionPoint
    toFilter: AirOutletConnectionPoint

air_connections:
  - OADPR.damper.airOutlet -> MixedAirDuct.fromOutdoorAir
```

Controllers (IO only; BACnet profile kept separate)
```yaml
name: M1
template_class: [Controller]
cp:
  electricalInlet: Electricity_24VLN_1Ph_60HzInletConnectionPoint
  bacnet_mstp: RS485BidirectionalConnectionPoint
  in10: ModulationSignalInletConnectionPoint
  out7: ModulationSignalOutletConnectionPoint

signal_connections:
  - Sensor1.signalOut -> M1.in10
  - M1.out7 -> Valve.signalIn
```

See also
- [Templates and Catalog](templates-and-catalog.md)
- [Connections](connections.md)
