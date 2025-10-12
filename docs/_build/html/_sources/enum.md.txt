# Enumerations (enum.py) and 223P vocab alignment

si-builder’s enum.py defines typed vocabularies that align with ASHRAE 223P vocabularies. These map to s223 terms and are serialized as IRIs in the model.

## Implementation details from the 223P vocab
### EnumerationKind
  - s223:EnumerationKind is the base for vocabularies like Medium, Domain, Role, Signal.
  - Concrete vocabularies are subclasses of EnumerationKind (e.g., s223:Medium, s223:Domain, s223:Role, s223:Signal).
  - Individual enumeration values are instances of these vocabularies and carry rdfs:label and rdfs:comment.
### Medium
  - s223:Medium categorizes carriers such as Air, Water, Steam, Refrigerant.
  - Typical usage: s223:hasMedium points from s223:Connection to a s223:Medium instance (e.g., Fluid.Air, Water.ChilledWater).
### Domain
  - s223:Domain tags elements with modeling domains (HVAC, Electrical, Networking, …).
  - Used via properties like s223:hasDomain in templates or roles/aspects.
### Role
  - s223:Role captures functional roles (Supply, Return, Cooling, Heating, …).
  - Attached via s223:hasRole to equipment or sensors where applicable.
### Mix, Substance, Constituent (for media composition)
  - s223:Mix and s223:Substance allow composition of media (e.g., Refrigerants).
  - Composition is expressed with constituent relationships including fractions and units when defined.
### Signal (electrical and IO)
  - s223:Signal is a vocabulary for data/communication carriers (RS485, Ethernet, WiFi, …).
  - s223:ModulatedSignal is a specialization (sub-vocabulary) of s223:Signal for analog modulation families (e.g., DC0_10, MA4_20).
  - Modulated signal variants are instances of s223:ModulatedSignal and have precise labels/comments describing their ranges.

## Open223 term links
- Medium: [s223:Medium](https://explore.open223.info/s223/Medium)
- Domain: [s223:Domain](https://explore.open223.info/s223/Domain)
- Role: [s223:Role](https://explore.open223.info/s223/Role)
- Signal: [s223:Signal](https://explore.open223.info/s223/Signal)
- ModulatedSignal: [s223:ModulatedSignal](https://explore.open223.info/s223/ModulatedSignal)

## How enum.py maps to s223
- Each top-level family (Medium, Domain, Role, Signal) corresponds to the s223 class of the same name (subclass of EnumerationKind).
- Members are created as individuals with:
  - rdf:type = that s223 class (e.g., s223:Medium)
  - rdfs:label set from the Python name (humanized) or explicit label
  - Optional rdfs:comment carried through when provided
- Nested families reflect vocab specialization:
  - Signal.ModulatedSignal corresponds to s223:ModulatedSignal (a specialization of s223:Signal).
  - Members like Signal.ModulatedSignal.DC0_10 and Signal.ModulatedSignal.MA4_20 are instances of s223:ModulatedSignal with precise labels.

## Examples

### Medium on a connection
```python
from bob.enum import Fluid, Water
from bob.core import Connection

cnx = Connection(label="SA-conn")
cnx.hasMedium = Fluid.Air          # rdf:type s223:Medium, used by s223:hasMedium
chw = Connection(label="CHW-conn")
chw.hasMedium = Water.ChilledWater
```

### Domains and roles on equipment
```python
from bob.enum import Domain, Role
from bob.core import Equipment

ahu = Equipment(label="AHU-1")
ahu.hasDomain = Domain.HVAC        # s223:hasDomain HVAC
ahu += Role.Supply                 # s223:hasRole Supply
ahu += Role.Cooling
```

### Signals and modulated signals
```python
from bob.enum import Signal

fieldbus = Signal.RS485            # instance of s223:Signal (EIA-485)
analog = Signal.ModulatedSignal.DC0_10  # instance of s223:ModulatedSignal (0–10 VDC)
current = Signal.ModulatedSignal.MA4_20 # 4–20 mA analog signal
```

## Notes
- All enum members serialize as resources (not literals). Labels/comments originate from the 223P vocab and are preserved in the graph.
- Use Open223 links above for canonical definitions and descriptions sourced from the standard.