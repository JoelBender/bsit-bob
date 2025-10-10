# Controllers and BACnet Profiles

223P concepts
- Controller → s223:Controller (may s223:executes a s223:Function)
- External reference → s223:hasExternalReference to s223:BACnetExternalReference
- Property wiring → s223:hasInternalReference to model properties

Controller IO (CPs)
```yaml
name: M1
template_class: [Controller]
cp:
  electricalInlet: Electricity_24VLN_1Ph_60HzInletConnectionPoint
  bacnet_mstp: RS485BidirectionalConnectionPoint
  in10: ModulationSignalInletConnectionPoint
  out7: ModulationSignalOutletConnectionPoint
```

BACnet profile (properties + external references)
```yaml
properties:
  discharge_air_temperature:
    class: Temperature
    hasUnit: UNIT.DEG_C
external_references:
  - discharge_air_temperature @ BACnet:analogInput,10444.presentValue
```

Best practices
- Keep IO (CPs) and network mapping (ExternalReference) separate.
- Use InternalReference to relate controller properties to system/equipment properties.
