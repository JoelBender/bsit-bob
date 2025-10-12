# Junctions and Boundaries

223P concepts
- Junction → s223:Junction (a Connectable with CPs, cannot change medium)
- Boundary CPs on a System → s223:hasBoundaryConnectionPoint, s223:hasOptionalConnectionPoint

Junctions [s223:Junction, s223:hasMedium]
```yaml
junctions:
  MixedAirDuct:
    class: Junction
    hasMedium: Fluid.Air
    fromReturnAir: AirInletConnectionPoint
    fromOutdoorAir: AirInletConnectionPoint
    toFilter: AirOutletConnectionPoint

air_connections:
  - OADPR.damper.airOutlet >> MixedAirDuct.fromOutdoorAir
  - RADPR.damper.airOutlet >> MixedAirDuct.fromReturnAir
  - MixedAirDuct.toFilter >> Filters.airInlet
```

Boundaries [s223:hasBoundaryConnectionPoint]
```yaml
boundaries:
  - MixedAirDuct|fromOutdoorAir
  - ChilledWaterSupply|fromChillerPlant
```

Notes
- Junction and its CPs share one s223:Substance-Medium.
- Use boundaries to validate partial models without dangling-CP errors.
