# Templates and Catalog

Catalog source
- Use `catalog_source: si_templates|get_template` to load catalog items.
- `from_catalog` pulls reusable blocks (sensors, controllers, packages).

Example: Using from_catalog for sensors
```yaml
from_catalog:
  STG:
    template: generic.sensor.rtd
    hasUnit: UNIT.DEG_C
  TPD:
    template: differential_pressure
    hasUnit: UNIT.PA
```

Programmatic instantiation
```python
from bob.template import config_from_yaml
from scratch.schemaorg import ProductGroupFromTemplate

config = config_from_yaml("ahu.yaml")
ahu = ProductGroupFromTemplate(config=config, label="SYSTEM_1")
```

When to create custom templates
- Missing CPs (e.g., VFD modulation/status).
- Multi-sensor “equipment” with IO CPs (RTD, 0-10V, 4-20mA).
- Assemblies (e.g., Humidifier with controller and auxiliaries).

Expose CPs via controller_mapsTo only if external layer needs them.

See also
- [Sensors and Observation Locations](sensors-and-observation.md)

# Templates: authoring, building, and helpers (template.py)

This page explains how YAML templates are parsed and built by si-builder, and documents the helper functions in template.py.

Overview
- Parse YAML into a normalized config dict: config_from_yaml(yaml_path)
- Instantiate a System or Equipment from that config:
  - SystemFromTemplate(config, label=...) for template_class: System
  - EquipmentFromTemplate(config, label=...) for template_class: Equipment
- Relations and boundaries are then applied to create connections, references, etc.
- Serialize the result with dump(data_graph, filename=...); see core.md

Create from YAML
```python
from bob.template import config_from_yaml, SystemFromTemplate
from bob.core import data_graph, dump

cfg = config_from_yaml("doc/examples/ahu_system.yaml")
ahu = SystemFromTemplate(config=cfg, label="AHU-1")

dump(data_graph, filename="build/ahu_system.ttl")
```

YAML structure (quick reference)
- name: Template identifier
- template_class: System | Equipment | [List of mixin classes]
- params: label, comment, plus optional params_XYZ blocks
- cp: Connection points (name: ClassName)
- equipment, properties, sensors, connections, junctions: nested entities
- <domain>_connections: directional links using the single arrow operator "->"
- sensors_observation_location: Sensor -> Target mappings
- boundaries: expose internal CPs at the System boundary
- *_references: internal/external references using "->"
- *_executes, functions_inputs, functions_outputs: function wiring using "->"
- from_catalog (+ catalog_source): reuse templates from catalog modules

Important: one YAML operator "->"
- YAML uses only "->" to keep authoring simple (see syntax.md)
- The section name determines the semantic: connectivity, mapsTo, executes, IO, references, etc.

Top-level example

```yaml
name: ahu_system
template_class: System
params:
  label: "AHU-1"

cp:
  supplyAir: AirOutletConnectionPoint
  mixedAir: AirInletConnectionPoint

equipment:
  SF:
    class: Fan
    cp:
      airInlet: AirInletConnectionPoint
      airOutlet: AirOutletConnectionPoint
  Coil:
    class: ChilledWaterCoil
    cp:
      airInlet: AirInletConnectionPoint
      airOutlet: AirOutletConnectionPoint

air_connections:
  - SF.airOutlet -> Coil.airInlet

boundaries:
  - SF.airOutlet -> supplyAir
```

How parsing works (config_from_yaml)
- Resolves class names to Python classes with get_class_from_name("Fan"), etc.
- Collects entities into categories:
  - "equipment", "properties", "sensors", "connections", "junctions", "cp"
- Keeps plain-text values for known text fields (label, comment, hasValue, …)
- Handles params_XYZ sections:
  - Keys like params_Product from an external package let you pass additional kwargs if the class is importable (package must be provided)
- Supports from_catalog:
  - Provide catalog_source: "module.path|function_name"
  - from_catalog: { Alias: { template: "NameOrPath", addon: "addon.yaml" } }
  - Catalog entries are embedded as nested EquipmentFromTemplate or SystemFromTemplate

Building the model
- SystemFromTemplate(config, **kwargs)
  - Determines the dynamic class from template_class (can be a list of mixins)
  - Applies params into constructor kwargs
  - Instantiates nested entities and CPs
  - Applies relations and boundaries (see below)
- EquipmentFromTemplate(config, **kwargs)
  - Same pattern for Equipment templates

Relations and boundaries application
- configure_relations(container, relations)
  - After parsing, relations are normalized into tuples: (source, operator, target)
  - Supported operators (internally):
    - ">>", "<<": connectivity (Python uses __rshift__/__lshift__)
    - "mapsTo": CP boundary mapping
    - "@": references (external/internal)
    - "%": observation location (Sensor % Target)
    - "executes", "hasInput", "hasOutput": function wiring
    - "=": assignment of an attribute
  - In YAML you only write "->"; parser maps by section name:
    - *_connections: "->" -> ">>"
    - *mapsTo: "->" -> "mapsTo"
    - *_executes: "->" -> "executes"
    - functions_inputs: "->" -> "hasInput"
    - functions_outputs: "->" -> "hasOutput"
    - *_references: "->" -> "@"
    - sensors_observation_location uses "%" (Sensor -> Target in YAML)
- configure_boundaries(container, boundaries)
  - boundaries entries are normalized and applied as: system | internal_cp

Helper functions (template.py)
- print_console(msg, style=None, panel=False)
  - Optional rich console output if rich is installed; falls back to print
- template_update(base: dict = {}, config: dict = None, bases: list = None)
  - Deep-merge helper to compose a user config on top of a base template
  - Supports merging two bases via bases=[base1, base2] then overlay config
- get_instance(container, blob: str)
  - Resolves expressions created by the parser, e.g.:
    - "self['SF'].airOutlet" or "self['AHU']['Coil'].airInlet"
  - Returns (object, attribute_name) or (object, None) if the expression points directly to an object
- configure_relations(container, relations)
  - Iterates normalized relations and invokes the corresponding Python operators/methods
- configure_boundaries(container, boundaries)
  - Applies System | ConnectionPoint for boundary exposure

Dynamic classes (template_class)
- template_class may be a single class name or a list of classes
- At instantiation, template code creates a Dynamic<ClassA>_<ClassB>… that inherits from the requested class list plus the base (System or Equipment)
- This lets you add explicit types (e.g., align with schema.org or REC) without writing dedicated Python classes

Catalogs (external libraries)
- Catalogs are published Python packages that expose validated templates for reuse.
- Purpose
  - Provide ready-to-use, validated Systems and Equipment (complex assemblies and simple parts).
  - Include both generic variants (e.g., generic Sensor, Pump, VFD) and manufacturer-specific models (with brand/model metadata).
  - Enable consistency across projects and reduce authoring time.
- Quality and validation
  - Catalog authors can ship tests and SHACL validations; consumers get versioned, reusable building blocks.
  - Pin catalog package versions to ensure reproducibility.
- Referencing catalogs in YAML
  ```yaml
  catalog_source: "vendor_catalog.templates|get_template"
  from_catalog:
    MyPump:
      template: "PUMP_Inline_3in"   # or a YAML path inside the package
      addon: "overrides.yaml"       # optional overlay for local changes
  ```
  - catalog_source points to a callable returning catalog entries.
  - from_catalog entries become nested Systems/Equipment in your template.
- Generic vs manufacturer-specific
  - Generic: pump, VFD, temperatureSensor with standard CPs/properties.
  - Manufacturer-specific: include brand/model/sku and datasheet links; CPs and properties match the product.
- schema.org enrichment (optional)
  - Basic schema.org support can be layered via external packages (e.g., si-modeler).
  - Catalog templates may add schema.org annotations (Product, Brand, model, sku) through mixins or params blocks.
  - si-builder’s dynamic class composition lets catalogs mix in such types without changes to si-builder.

Catalog reuse
```yaml
catalog_source: "my_project.catalog|get_template"
from_catalog:
  FanModule:
    template: "SF_basic"
    addon: "overrides.yaml"
```
- add-on YAML is merged via template_update before instantiation

Boundaries and observation examples
```yaml
# Expose internal CP at system boundary
boundaries:
  - AHU.SA_Duct.airOutlet -> supplyAir

# Sensor observation location (Sensor -> Target)
sensors_observation_location:
  - SAT_Sensor -> AHU.supplyAirTemperature
```

End-to-end example (Python)
```python
from bob.template import config_from_yaml, SystemFromTemplate
from bob.core import data_graph, dump

cfg = config_from_yaml("doc/examples/ahu_system.yaml")
ahu = SystemFromTemplate(config=cfg, label="AHU-1")

dump(data_graph, filename="build/ahu_system.ttl")
```

Notes
- YAML only uses "->"; the parser (config_from_yaml) maps it based on section names.
- Labels/comments are passed through from params. Additional params_* blocks require importable packages and classes.
- Rich console output is optional; install rich for styled build
