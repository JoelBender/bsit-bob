# Sensors and Observation Locations

223P concepts
- Sensor → s223:Sensor
- Observed property → s223:ObservableProperty (often s223:QuantifiableObservableProperty)
- Locations → s223:hasObservationLocation, s223:hasReferenceLocation
- Medium and substance context → s223:ofMedium, s223:ofSubstance; delta flag via qudt:isDeltaQuantity

Observation and reference locations
```yaml
sensors_observation_location:
  - TPD.pressure_sensor -> SupplyAirDuct.supplyAir    # observation (H)
  - TPD.pressure_sensor -> ReturnAirDuct.returnAir    # reference (L)
```

References (properties) with @
```yaml
internal_references:
  - STG.temperature @ AHU.discharge_air_temperature
external_references:
  - AHU.discharge_air_temperature @ BACnet:analogInput,10444.presentValue
```

Notes
- For differential readings, first mapping is observation; second is reference; set qudt:isDeltaQuantity true where applicable (per 223P core.ttl).
- Units and quantity kind follow QUDT (qudt:hasUnit, qudt:hasQuantityKind).

# Observation location operator (%)

- Python shorthand: `sensor % target` adds `s223:observes` from the sensor to the target.
- YAML uses a single arrow in the `sensors_observation_location` section; the template parser maps it to `%` in Python.

Example (YAML)
```yaml
sensors_observation_location:
  - SAT_Sensor -> AHU.supplyAirTemperature
```

Equivalent (Python)
```python
SAT_Sensor % AHU.supplyAirTemperature
```

Notes
- Target can be a connectable node or a specific Property.
- The SVG renderer includes observes edges; TTL shows the full triple.

