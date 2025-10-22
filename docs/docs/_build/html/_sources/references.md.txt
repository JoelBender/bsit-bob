# Internal vs External References

223P concepts
- Internal reference → s223:hasInternalReference (max 1 target by shape)
- External reference → s223:hasExternalReference (e.g., s223:BACnetExternalReference)

Operator
- X @ Y means “X references Y”.

Internal reference (model-to-model) [s223:hasInternalReference]
```yaml
internal_references:
  - STG.temperature @ AHU.discharge_air_temperature
```

External reference (model-to-network) [s223:hasExternalReference]
```yaml
external_references:
  - AHU.discharge_air_temperature @ BACnet:analogInput,10444.presentValue
```

Why both
- Clarifies multiple readers/writers of the same physical quantity.
- Keeps commissioning mappings auditable.
