# Syntax and Shorthand Operators

Operators map to 223P relations or modeling conveniences used in si-builder.

- `A > B`  → containment
  - Equipment/PhysicalSpace: s223:contains
  - System/Zone: s223:hasMember
  - Links: [s223:contains](https://explore.open223.info/s223/contains), [s223:hasMember](https://explore.open223.info/s223/hasMember)

- `A >> B` and `B << A` → connectivity between connection points (CPs)
  - Creates an s223:Connection, binds via s223:connectsAt / s223:connectsThrough and can carry s223:hasMedium
  - Prefer `cp_out >> cp_in`; `cp_in << cp_out` is equivalent
  - Links: [s223:Connection](https://explore.open223.info/s223/Connection), [s223:ConnectionPoint](https://explore.open223.info/s223/ConnectionPoint), [s223:connectsAt](https://explore.open223.info/s223/connectsAt), [s223:connectsThrough](https://explore.open223.info/s223/connectsThrough), [s223:hasMedium](https://explore.open223.info/s223/hasMedium)

- `X | cp` → boundary connection point exposure on systems
  - Declares a s223:BoundaryConnectionPoint on the System and maps it to an internal CP
  - Typical form: `System | ConnectionPoint`
  - Link: [s223:BoundaryConnectionPoint](https://explore.open223.info/s223/BoundaryConnectionPoint)

- `prop @ external_ref` → external reference on a property
  - Adds an s223:ExternalReference to a Property/Setpoint/Observable/Actuatable
  - Link: [s223:ExternalReference](https://explore.open223.info/s223/ExternalReference)

- `node_or_prop += aspect_or_role` → add aspect/role metadata
  - Adds an aspect to a node or property; for Equipment/Sensor also adds roles (EnumerationKinds)
  - Used widely to attach modeling aspects without verbose calls

- `sensor % target` → observation relation
  - Adds s223:observes from the Sensor to the target (connectable or Property)
  - Links: [s223:observes](https://explore.open223.info/s223/observes), [s223:ConnectionPoint](https://explore.open223.info/s223/ConnectionPoint), [s223:BoundaryConnectionPoint](https://explore.open223.info/s223/BoundaryConnectionPoint)

Examples

```python
# Containment / membership
AHU > SF                      # AHU contains SF (s223:contains)
VAV_System > Zone_101         # system membership (s223:hasMember)

# Connectivity
SF.airOutlet >> SA_Duct.airInlet
MA_Duct.airOutlet >> AHU.mixedAirInlet
SA_Terminal.airInlet << SA_Duct.airOutlet  # reverse form

# Boundary exposure on a system
AirSystem | SA_Duct.airOutlet             # expose a boundary CP on the system

# External references (BACnet / Time series / Niagara, etc.)
SupplyTempSensor.temperature @ some_external_reference

# Aspects and roles
SF.fanSpeed += aspect                     # add an aspect to a property
AHU += role                               # add a role (EnumerationKind) to equipment

# Observation
Sensor % AHU.supplyAirTemperature
```

Notes
- The above operators are provided by Python dunder methods:
  - `>` via `__gt__` on Container/Equipment/PhysicalSpace/System/Zone
  - `>>` and `<<` via `__rshift__`/`__lshift__` on ConnectionPoint-like classes
  - `|` via `__or__`/`__ror__` on System and related metaclasses
  - `@` via `__matmul__` on Property/Setpoint types (for external references)
  - `+=` via `__iadd__` on Node/Property/Equipment/Sensor to add aspects or roles
  - `%` via `__mod__` on Sensor to add s223:observes
- If rendering issues persist in HTML, use code formatting (as above) or escape `>` as `&gt;`

