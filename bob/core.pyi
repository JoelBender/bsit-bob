import logging
from typing import Any, Dict, Optional, Set, TypeAlias

from rdflib import Graph, URIRef

# Export logging explicitly
__all__ = ["ConnectionPoint", "EnumerationKind", "Equipment", "Graph", "Node", "Property", "URIRef", "logging"]

# Base Node class
class Node:
    _node_iri: URIRef
    _data_graph: Graph
    _schema_graph: Graph
    def __init__(self, **kwargs: Any) -> None: ...

# Property classes
class Property(Node):
    ofConstituent: Any
    label: Any
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

class QuantifiableProperty(Property):
    hasValue: Any
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

class QuantifiableObservableProperty(QuantifiableProperty):
    def __init__(self, **kwargs: Any) -> None: ...

class QuantifiableActuatableProperty(QuantifiableProperty):
    def __init__(self, **kwargs: Any) -> None: ...

class EnumerableProperty(Property):
    def __init__(self, **kwargs: Any) -> None: ...

class EnumeratedObservableProperty(EnumerableProperty):
    def __init__(self, **kwargs: Any) -> None: ...

class EnumeratedActuatableProperty(EnumerableProperty):
    def __init__(self, **kwargs: Any) -> None: ...

# Connection Point classes
class ConnectionPoint(Node):
    hasMedium: Any
    def __init__(self, **kwargs: Any) -> None: ...

class BidirectionalConnectionPoint(ConnectionPoint):
    def __init__(self, **kwargs: Any) -> None: ...

class InletConnectionPoint(ConnectionPoint):
    _class_iri: URIRef
    def __init__(self, **kwargs: Any) -> None: ...

class OutletConnectionPoint(ConnectionPoint):
    _class_iri: URIRef
    def __init__(self, **kwargs: Any) -> None: ...

class BoundaryConnectionPoint(ConnectionPoint):
    def __init__(self, **kwargs: Any) -> None: ...

# Additional missing classes from sensor and equipment modules
class PropertyReference(Node):
    def __init__(self, **kwargs: Any) -> None: ...

class FunctionInput(PropertyReference):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

class FunctionOutput(PropertyReference):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

class LocationReference(Node):
    def __init__(self, **kwargs: Any) -> None: ...

class _Sensor(Node):
    def __init__(self, **kwargs: Any) -> None: ...

class _Function(Node):
    _resolved: bool
    def __init__(self, **kwargs: Any) -> None: ...
    def _resolve_annotations(self) -> None: ...

class Function(_Function):
    inputs: dict[str, Any]
    outputs: dict[str, Any]
    def __init__(self, **kwargs: Any) -> None: ...
    def hasInput(self, *args: Any, **kwargs: Any) -> Any: ...
    def hasOutput(self, *args: Any, **kwargs: Any) -> Any: ...

class Setpoint(Property):
    def __init__(self, **kwargs: Any) -> None: ...

# Constants and flags
INCLUDE_INVERSE: Any
SCRATCH: Any

# Missing system connection points
class InletSystemConnectionPoint(ConnectionPoint):
    def __init__(self, **kwargs: Any) -> None: ...

class OutletSystemConnectionPoint(ConnectionPoint):
    def __init__(self, **kwargs: Any) -> None: ...

class ZoneConnectionPoint(ConnectionPoint):
    def __init__(self, **kwargs: Any) -> None: ...

class InletZoneConnectionPoint(ZoneConnectionPoint):
    def __init__(self, **kwargs: Any) -> None: ...

class OutletZoneConnectionPoint(ZoneConnectionPoint):
    def __init__(self, **kwargs: Any) -> None: ...

# Container and Equipment classes
class Container(Node):
    def __init__(self, **kwargs: Any) -> None: ...

class Connectable(Node):
    _class_iri: URIRef
    _connection_points: dict[str, ConnectionPoint]
    def __init__(self, **kwargs: Any) -> None: ...

class Equipment(Container, Connectable):
    _class_iri: URIRef
    hasPhysicalLocation: Any  # PhysicalSpace
    def __init__(self, **kwargs: Any) -> None: ...

class PhysicalSpace(Container):
    _class_iri: URIRef
    def __init__(self, **kwargs: Any) -> None: ...

class Zone(PhysicalSpace):
    def __init__(self, **kwargs: Any) -> None: ...

class DomainSpace(PhysicalSpace):
    def __init__(self, **kwargs: Any) -> None: ...

class Junction(Connectable):
    def __init__(self, **kwargs: Any) -> None: ...

class System(Container):
    hasRole: set[Any]
    _boundary_connection_points: set[Any]
    _serves_zones: dict[str, Any]
    def __init__(self, **kwargs: Any) -> None: ...

class Connection(Node):
    hasMedium: Any
    _class_iri: URIRef
    def __init__(self, **kwargs: Any) -> None: ...

# EnumerationKind and related classes
class EnumerationKind(Node):
    _name: str
    _parent: EnumerationKind | None
    _children: set[EnumerationKind]
    _constituents: set[Any]
    composedOf: set[Any]

    def __init__(self, name: str, *args: Any, **kwargs: Any) -> None: ...
    def __call__(self, name: str, *, _alt_namespace: Any = None, **kwargs: Any) -> EnumerationKind: ...
    def __getattr__(self, name: str) -> Any: ...  # Allow dynamic attribute access
    def add_constituent(self, constituent: Any, *args: Any, **kwargs: Any) -> None: ...

# Define types for the dynamically created enumeration hierarchies
class SubstanceType(EnumerationKind):
    Medium: Any  # MediumType
    Particle: Any  # Particulate

class MediumType(EnumerationKind):
    Constituent: Any  # This is the Constituent class
    Mix: Any
    ThermalContact: Any

class RoleType(EnumerationKind):
    ...

class DomainType(EnumerationKind):
    ...

# The actual Constituent class that inherits from EnumerationKind
class Constituent(EnumerationKind):
    def __init__(self, name: str, *args: Any, **kwargs: Any) -> None: ...
    def __getattr__(self, name: str) -> Any: ...  # Allow dynamic attribute access

# Namespace objects
class NamespaceType:
    def __getitem__(self, key: str) -> URIRef: ...
    def __call__(self, key: str) -> URIRef: ...
    def __getattr__(self, name: str) -> URIRef: ...  # Support attribute access like S223.Conductor

BOB: NamespaceType
S223: NamespaceType
P223: NamespaceType
G36: NamespaceType
QUANTITYKIND: NamespaceType
UNIT: NamespaceType

# Graph objects
data_graph: Graph
schema_graph: Graph

# Variables that are dynamically created as EnumerationKind instances
Substance: SubstanceType  # EnumerationKind instance
Medium: MediumType  # EnumerationKind instance
Domain: DomainType  # EnumerationKind instance

# Medium instances
Mix: EnumerationKind  # Medium instance defined as Medium("Mix")

# EnumerationKind instances
Role: RoleType  # Role enumeration kind

# Additional variables and objects
QUDT: Any  # QUDT namespace

# Functions
def bind_model_namespace(**kwargs: Any) -> None: ...
def dump(**kwargs: Any) -> str: ...

# Standard library modules re-exported by core
logging = logging
