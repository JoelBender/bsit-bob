# Basics: Equipment, Systems, Spaces
> Definitions for Equipment, System, PhysicalSpace, DomainSpace, Zone, and Junction are drawn from the ASHRAE 223P RDF and aligned with Real Estate Core (see lofty.py). See the Glossary page for canonical descriptions.

This section mirrors the simplest patterns covered by tests and builds up progressively.

223P mapping (nodes and edges)
- Nodes are instances of s223:Concept subclasses:
  - Equipment → s223:Equipment
  - Junction → s223:Junction
- Edges are s223 relations:
  - Containment → s223:contains (Equipment, PhysicalSpace), s223:hasMember (System)
  - Location/Grouping → s223:hasPhysicalLocation, s223:encloses, s223:hasDomain, s223:hasZone

---

## Equipment (single device)

### Using python directly

Python Code to define a Fan
```{literalinclude} examples/fan_device_from_class.py
:language: python
:caption: Example: fan_device_from_class.py
```

```{literalinclude} _artifacts/basics_fan_from_class.ttl
:language: turtle
:caption: Listing: basics_fan_from_class.ttl
```

```{figure} _static/artifacts/basics_fan_from_class.svg
:alt: Fan example graph when created from class
:align: center

Figure: basics_fan_from_class graph
```

### Using Templates

#### Fan Template
YAML template
```{literalinclude} examples/fan_device.yaml
:language: yaml
:caption: Example: fan_device.yaml
```

#### Python code for Fan
Python Code to use YAML template
```{literalinclude} examples/fan_device_from_yaml.py
:language: python
:caption: Example: fan_device_from_yaml.py
```

#### Fan Resulting TTL File
```{literalinclude} _artifacts/basics_fan_from_yaml.ttl
:language: turtle
:caption: Listing: basics_fan_from_yaml.ttl
```

#### Fan Graph picture
```{figure} _static/artifacts/basics_fan_from_yaml.svg
:alt: Fan example graph using YAML template
:align: center

Figure: basics_fan_from_yaml graph
```

#### Legends
```{admonition} Legend (SVG)
- Boxes: Equipment, Systems, Spaces, and other nodes
- Circles: s223:Property
- Diamonds: s223:ConnectionPoint
- Edge labels: s223 predicates (contains, hasMember, hasProperty, connectsAt, mapsTo, …)
```

```{admonition} Legend (TTL)
- Prefixes declare namespaces (S223, BOB, EX, …)
- Triples are subject predicate object . in Turtle syntax
- Predicates align with s223 relations (contains, hasMember, hasProperty, connectsAt, …)
- The SVG filters common predicates; the TTL shows the full model content
```

---

## System (simple AHU fragment)

### Building a AHU using Python directly

#### Python code to build a AHU
Python Code to define a AHU
```{literalinclude} examples/ahu_system_from_class.py
:language: python
:caption: Example: ahu_system_from_class.py
```

#### AHU Resulting TTL File
```{literalinclude} _artifacts/basics_ahu_from_class.ttl
:language: turtle
:caption: Listing: basics_ahu_from_class.ttl
```

#### AHU from clases Graph picture
```{figure} _static/artifacts/basics_ahu_from_class.svg
:alt: AHU example graph from classes
:align: center

Figure: basics_ahu_from_clases graph
```

### Building a AHU using Templates

#### AHU Template
YAML template
```{literalinclude} examples/ahu_system.yaml
:language: yaml
:caption: Example: ahu_system.yaml
```

#### Python code to build a AHU from template
```{literalinclude} examples/ahu_system_from_yaml.py
:language: python
:caption: Example: ahu_system_from_yaml.py
```

#### Resulting AHU TTL from Template
```{literalinclude} _artifacts/basics_ahu_from_yaml.ttl
:language: turtle
:caption: Listing: basics_ahu_from_yaml.ttl
```

#### AHU Graph Picture (from template)
```{figure} _static/artifacts/basics_ahu_from_yaml.svg
:alt: AHU example graph from YAML
:align: center

Figure: basics_ahu_from_yaml graph
```

#### Legends
```{admonition} Legend (SVG)
- Boxes: Equipment, Systems, Spaces, and other nodes
- Circles: s223:Property
- Diamonds: s223:ConnectionPoint
- Edge labels: s223 predicates (contains, hasMember, hasProperty, connectsAt, mapsTo, …)
```

```{admonition} Legend (TTL)
- Prefixes declare namespaces (S223, BOB, EX, …)
- Triples are subject predicate object . in Turtle syntax
- Predicates align with s223 relations (contains, hasMember, hasProperty, connectsAt, …)
- The SVG filters common predicates; the TTL shows the full
