# Systems vs Equipment (and mapsTo)

223P concepts
- Equipment is connectable → s223:Equipment ⊂ s223:Connectable (has CPs, connections)
- System is a logical grouping → s223:System (uses s223:hasMember, no CPs itself)
- System boundaries reference child CPs → s223:hasBoundaryConnectionPoint / s223:hasOptionalConnectionPoint

Equipment
- Encapsulates details; expose minimal CPs (s223:hasConnectionPoint).

System
- Group equipment via s223:hasMember; connect at the same layer.
- Reduces mapsTo duplication.

Rule of layers
- Do not link a top-level element directly to a contained element’s CP; either keep connections flat at System level or expose CPs with s223:mapsTo (advanced).

See tests
- test_system-001.py … -007.py
