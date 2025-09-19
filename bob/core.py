"""
Bob the SI-WG Builder
"""

from __future__ import annotations

import inspect
import io
import itertools
import logging
import os
import re
import sys
import warnings
from collections import Counter, defaultdict
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Set,
    TextIO,
    Tuple,
    TypeVar,
    Union,
    cast,
    get_origin,
)

from rdflib import RDF, RDFS, SH, XSD, BNode, Graph, Literal, Namespace, URIRef

from .multimethods import multimethod, new_class

T = TypeVar("T")
NodeMap = Dict[str, Union[type, str]]
_next_node = Counter()

# environment
try:
    _dotenv_import_error = False
    _env_file = os.path.join(os.getcwd(), ".env")
    if os.path.isfile(_env_file):
        from dotenv import load_dotenv as _load_dotenv

        _load_dotenv(_env_file)
except ImportError:
    _dotenv_import_error = True

# create a package logger, turn off propagation
bob_logger = logging.getLogger("bob")
bob_logger.propagate = False

# set the level if it hasn't already been set so that child loggers can
# have handlers attached and have their effective level default to DEBUG
if bob_logger.level == 0:
    bob_logger.setLevel(logging.DEBUG)

# logging
_log_level = os.getenv("BOB_LOG", None)
if _log_level:
    try:
        _numeric_level = int(_log_level)
    except ValueError:
        _numeric_level = getattr(logging, _log_level.upper(), None)
    if not isinstance(_numeric_level, int):
        raise ValueError(f"invalid log level: {_log_level}")

    # create a file or stream handler
    _log_filename = os.getenv("BOB_LOG_FILENAME", None)
    if _log_filename:
        _handler = logging.FileHandler(_log_filename)
    else:
        _handler = logging.StreamHandler()
    _handler.setLevel(_numeric_level)
    _handler.setFormatter(logging.Formatter(logging.BASIC_FORMAT, None))

    # add the handler and set the level
    bob_logger.addHandler(_handler)
    bob_logger.setLevel(_numeric_level)
else:
    # add a null handler:
    # https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library
    bob_logger.addHandler(logging.NullHandler())

# create a module logger
_log = logging.getLogger(__name__)

if _dotenv_import_error:
    _log.warning("install python-dotenv to use your .env file")


prefixes = {
    "s223": "http://data.ashrae.org/standard223#",
    "p223": "http://data.ashrae.org/proposal-to-standard223#",
    "scratch": "http://data.ashrae.org/standard223/si-builder/prototype#",
    "bob": "http://data.ashrae.org/standard223/si-builder#",
    "ex": "http://example/",
    "g36": "http://data.ashrae.org/standard223/1.0/extension/g36#",
    "qudt": "http://qudt.org/schema/qudt/",
    "qudtqk": "http://qudt.org/vocab/quantitykind/",
    "unit": "http://qudt.org/vocab/unit/",
    "brick": "https://brickschema.org/schema/Brick#",
    "bacnet": "http://data.ashrae.org/bacnet/2020#",
    "rec": "https://w3id.org/rec/core/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "ref": "https://brickschema.org/schema/Brick/ref#",
}


# options
MANDITORY_LABEL = os.getenv("MANDITORY_LABEL", "True") == "True"

# include cnx by default
INCLUDE_CNX = os.getenv("INCLUDE_CNX", "True") == "True"

# other inverse relations excluded by default
INCLUDE_INVERSE = os.getenv("INCLUDE_INVERSE", "False") == "True"

# connection requires hasMedium
CONNECTION_HAS_MEDIUM = os.getenv("CONNECTION_HAS_MEDIUM", "True") == "True"

#
#
#

# globals
data_graph = None
schema_graph = None


# include/exclude predicates
include_predicates: Set[str] = set(os.getenv("BOB_INCLUDE", "").split())
exclude_predicates: Set[str] = set(os.getenv("BOB_EXCLUDE", "").split())

# include/exclude defaults
if (not include_predicates) and (not exclude_predicates):
    include_predicates.add("*")

# include/exclude combination error checking
if "*" in exclude_predicates:
    if len(exclude_predicates) != 1:
        raise RuntimeError("no")
    if not include_predicates:
        raise RuntimeError("no")
if "*" in include_predicates:
    if len(include_predicates) != 1:
        raise RuntimeError("no")
if include_predicates.intersection(exclude_predicates):
    raise RuntimeError("include/exclude overlap")
_log.debug(f"include_predicates {include_predicates}")
_log.debug(f"exclude_predicates {exclude_predicates}")


class DataGraph(Graph):
    def add(self, triple: Tuple[Any, Any, Any]) -> None:
        """
        Add a triple to the data graph, checking the predicate to see if it should
        be included or excluded.
        """
        # _log.debug(f"DataGraph.add {triple}")
        subj, pred, obj = triple

        (
            namespace,
            namespace_uriref,
            suffix,
        ) = data_graph.namespace_manager.compute_qname(pred)
        for test_name in (namespace + ":" + suffix, namespace + ":*", "*"):
            if test_name in include_predicates:
                break
            if test_name in exclude_predicates:
                return

        # passes the tests
        super().add(triple)


class SchemaGraph(Graph):
    def add(self, triple: Tuple[Any, Any, Any]) -> None:
        """
        Add a triple to the schema graph for statements about things in the
        model being build (like subtypes of an equipment) but not about things
        in the S223 namespace.
        """
        # _log.debug(f"SchemaGraph.add {triple}")
        subj, pred, obj = triple

        # exclude the schema content in the S223 namespace by default
        if subj.startswith(S223):  # and (not isinstance(obj, BNode)):
            return

        # passes the tests
        super().add(triple)


data_graph = DataGraph()
schema_graph = SchemaGraph()


def bind_namespace(prefix: str, uri: str) -> Namespace:
    """
    Create a Namespace and bind a prefix to it in both the default data graph
    and the default schema graph.
    """
    global data_graph, schema_graph

    namespace = Namespace(uri)
    data_graph.namespace_manager.bind(prefix, URIRef(uri))
    schema_graph.namespace_manager.bind(prefix, URIRef(uri))
    return namespace


# the namespace for a node is defined in the node as the _namespace attribute
# or in the _namespace special global for the module of the class, or the
# parent module, or it is inherited from a superclass that is defined in the
# same module
S223 = bind_namespace("s223", prefixes["s223"])

# This namespace is added so in the development of Bob, when new cases occurs
# we can clearly establish that a new class is not yet part of the standard
P223 = bind_namespace("p223", prefixes["p223"])

# This namespace is added so si-builder/scratch (aka Scratch), can provide its own schema
# of classes which are opiniated examples assemblage of S223 classes
SCRATCH = bind_namespace("scratch", prefixes["scratch"])

# This namespace is added so si-builder (aka Bob), can provide its own schema
# of classes which are assemblage of S223 classes
BOB = bind_namespace("bob", prefixes["bob"])

# This namespace is used when the module does not have a namespace provided
# which makes short examples easier to create
EX = bind_namespace("ex", os.getenv("BOB_EX", prefixes["ex"]))

# This namespace is used for all related logics in Guideline 36
G36 = bind_namespace("g36", prefixes["g36"])

# everything in this module belongs in the standard
_namespace = S223

# common namespaces
QUDT = bind_namespace("qudt", prefixes["qudt"])
QUANTITYKIND = bind_namespace("qudtqk", prefixes["qudtqk"])
UNIT = bind_namespace("unit", prefixes["unit"])
BRICK = bind_namespace("brick", prefixes["brick"])

# the model_namespace is used to create "blank" node identifiers, a serial
# number to make it easier to debug a constructed file
model_namespace = None


def bind_model_namespace(prefix: str, uri: str) -> Namespace:
    """
    Create a Namespace for blank node identifiers and bind a prefix to the
    prefix in the graph.
    """
    global model_namespace
    model_namespace = bind_namespace(prefix, uri)
    return model_namespace


def dump(
    graph: Graph = data_graph,
    file: TextIO = sys.stdout,
    filename: str = None,
    format: str = "turtle",
    header: str = None,
) -> None:
    if not header:
        content = graph.serialize(format=format)
    else:
        content = header + graph.serialize(format=format)
    if not isinstance(content, str):
        content = content.decode("UTF-8")

    content = clean_and_sort_turtle_file(content)

    if filename:
        with open(filename, "w", encoding="UTF-8") as ttl_file:
            ttl_file.write(content)
    else:
        file.write(content)


def clean_and_sort_turtle_file(content: str) -> str:
    """
    This will assure the TTL file header contains no
    duplicates, header is well formatted and
    all triples are sorted.
    """
    _log.debug("clean_and_sort_turtle_file ...")

    header_chunks = []  # lines that start like '# baseURI: ...'
    prefix_chunks = []  # lines that start like '@prefix ...'

    # pattern for triple quoted literals
    tql = re.compile("\"\"\".*\"\"\"|'''.*'''", re.DOTALL)
    tql_archive = []

    def tql_save(match) -> str:
        _log.debug("    - match: %r", match)
        mstart, mend = match.span()
        tql_archive.append(match.string[mstart:mend])
        return "\0"

    def tql_restore(match) -> str:
        return tql_archive.pop(0)

    # save the triple quoted strings
    content = tql.sub(tql_save, content)

    chunk = ""  # lines that belong together
    chunks = []  # groups of lines sorted later
    for line in io.StringIO(content).readlines():
        _log.debug("    - %r", line)

        # filter out comments and prefixes
        if line.startswith("# "):
            _log.debug("    - header")
            header_chunks.append(line)
            if chunk:
                chunks.append(chunk)
                chunk = ""
            continue
        if line.startswith("@prefix"):
            _log.debug("    - prefix")
            prefix_chunks.append(line)
            if chunk:
                chunks.append(chunk)
                chunk = ""
            continue

        chunk += line
        if line == "\n":
            _log.debug("    - end of chunk")
            chunks.append(chunk)
            chunk = ""

    # trailing chunk
    if chunk:
        _log.debug("    - trailing chunk")
        chunks.append(chunk)
        chunk = ""

    new_content = ""

    # dump the header chunks
    if header_chunks:
        new_content += "".join(header_chunks) + "\n"

    # sort prefix chunks and remove the duplicates
    if prefix_chunks:
        prefix_chunks.sort()
        prefix_chunks = list(dict.fromkeys(prefix_chunks))
        new_content += "".join(prefix_chunks) + "\n"

    # restore the triple quoted strings
    chunks = [re.sub("\0", tql_restore, chunk) for chunk in chunks]

    # sort them
    chunks.sort()
    new_content += "".join(chunks)

    return new_content


def get_datagraph(graph: Graph = data_graph) -> Graph:
    content = graph
    return content


def clear(graph: Graph = data_graph) -> None:
    """Remove all the triples from the graph, reset the blank node counter."""
    global _next_node

    # remove all the triples
    graph.remove((None, None, None))

    # reset the "blank" node counter
    _next_node = Counter()


class NodeMetaclass(type):
    def __new__(
        cls: Any,
        clsname: str,
        superclasses: Tuple[type, ...],
        attributedict: Dict[str, Any],
    ) -> NodeMetaclass:
        _log.debug(f"NodeMetaclass.__new__ {clsname}")

        # start with empty maps
        _nodes: NodeMap = {}
        _datatypes: Dict[str, Literal] = {}
        _attr_uriref: Dict[str, URIRef] = {}

        # add these special attributes to the class before building it
        attributedict["_resolved"] = False
        attributedict["_nodes"] = _nodes
        attributedict["_datatypes"] = attributedict.get("_datatypes", _datatypes)
        attributedict["_attr_uriref"] = attributedict.get("_attr_uriref", _attr_uriref)

        # build the class
        metaclass = cast(
            NodeMetaclass,
            super(NodeMetaclass, cls).__new__(
                cls, clsname, superclasses, attributedict
            ),
        )

        # let the multimethods know this is a new class, the typemap might have
        # to be reconstructed
        new_class(metaclass)

        return metaclass


class Node(metaclass=NodeMetaclass):
    """
    A node in the graph that optionally has a label and a comment.  Instances
    of this would be something like blank nodes.
    """

    _namespace: Namespace
    _data_graph: Graph = data_graph
    _schema_graph: Graph = schema_graph

    # resolved annotations into nodes and datatypes
    _resolved: bool
    _nodes: NodeMap
    _datatypes: Dict[str, Literal] = {"label": Literal, "comment": Literal}
    _attr_uriref: Dict[str, URIRef] = {"label": RDFS.label, "comment": RDFS.comment}

    # attributes that can be changed
    _volatile: Tuple[str, ...] = ()

    _node_iri: URIRef
    _class_iri: Optional[URIRef] = None

    def __init__(
        self,
        *,
        _node_iri: URIRef = None,
        **kwargs: Any,
    ) -> None:
        _log.debug(f"Node.__init__ {kwargs} class={self.__class__.__name__}")
        global _next_node, model_namespace

        if not self._resolved:
            self._resolve_annotations()
        _log.debug("    - continue Node.__init__")

        if _node_iri is not None:
            if not isinstance(_node_iri, URIRef):
                raise TypeError(f"URIRef expected: {_node_iri}")
        elif model_namespace:
            _next_node[model_namespace] += 1
            _node_iri = model_namespace[f"{_next_node[model_namespace]:05d}"]
        else:
            _node_iri = BNode()
        super().__setattr__("_node_iri", _node_iri)

        # allow kwargs to overide
        self._schema_graph = kwargs.pop("_schema_graph", self._schema_graph)
        self._data_graph = kwargs.pop("_data_graph", self._data_graph)

        if hasattr(self, "_class_iri"):
            if self._class_iri is not None:
                self._data_graph.add((self._node_iri, RDF.type, self._class_iri))
                _log.debug(f"    - has _class_iri: {self._class_iri}")

        # pull out the kwargs that are nodes and datatypes
        inits = {}
        for k, v in kwargs.items():
            if k in self._nodes or k in self._datatypes:
                inits[k] = v
        _log.debug(f"    - inits: {inits!r}")

        # pull out the init values in classes that aren't already found
        for supercls in self.__class__.__mro__:
            if issubclass(supercls, Node):
                _class_iri = vars(supercls).get("_class_iri")
                if _class_iri is not None:
                    self._data_graph.add((self._node_iri, RDF.type, _class_iri))
                    _log.debug(f"    - supercls {supercls} _class_iri: {_class_iri}")

            for k, v in supercls.__dict__.items():
                if k.startswith("_") or (k in inits):
                    continue
                if (k in self._datatypes) or (k in self._nodes):
                    inits[k] = v
                if inspect.isclass(v) and issubclass(v, Node):
                    _log.debug(f"    - ding {k!r} = {v!r}")

        # set the values
        for attr, attr_value in inits.items():
            _log.debug(f"    - init {attr}: {attr_value!r}")
            if attr_value is None:
                super().__setattr__(attr, None)
            else:
                setattr(self, attr, attr_value)

        # clear the nodes with no values
        for attr in self._nodes:
            if attr not in inits:
                super().__setattr__(attr, None)

        # unknown args
        unknown_kwargs = [attr for attr in kwargs if attr not in inits]
        if unknown_kwargs:
            raise RuntimeError(
                f"unexpected keyword arguments: {', '.join(unknown_kwargs)}"
            )

    @classmethod
    def _resolve_annotations(cls) -> None:
        """
        .
        """
        _log.debug(f"Node._resolve_annotations {cls}")
        if cls is Node:
            _log.debug("    - nothing to resolve here")
            cls._resolved = True
            return

        # include the maps this class is inheriting
        for supercls in reversed(cls.__mro__[1:]):
            _log.debug(f"    - supercls: {supercls}")
            if supercls is cls:
                break

            if not hasattr(supercls, "_resolved"):
                continue
            if not supercls._resolved:
                supercls._resolve_annotations()

            if hasattr(supercls, "_nodes"):
                cls._nodes.update(supercls._nodes)  # type: ignore[attr-defined]
            if hasattr(supercls, "_datatypes"):
                cls._datatypes.update(supercls._datatypes)  # type: ignore[attr-defined]
            if hasattr(supercls, "_attr_uriref"):
                cls._attr_uriref.update(supercls._attr_uriref)  # type: ignore[attr-defined]
        _log.debug("    - from super classes:")
        _log.debug(f"    -     _nodes: {cls._nodes!r}")
        _log.debug(f"    -     _datatypes: {cls._datatypes!r}")
        _log.debug(f"    -     _attr_uriref: {cls._attr_uriref!r}")

        # find the namespace in the class definition
        _namespace = vars(cls).get("_namespace")
        if _namespace:
            _log.debug(f"    - class namespace: {_namespace}")
        else:
            # check the module
            cls_module = inspect.getmodule(cls)
            _log.debug(f"    - cls_module: {cls_module} {cls_module.__name__}")

            _namespace = vars(cls_module).get("_namespace")
            if _namespace:
                _log.debug(f"    - module {cls_module} namespace: {_namespace}")
            else:
                # check the parent module
                parent_module = sys.modules[
                    ".".join(cls_module.__name__.split(".")[:-1]) or "__main__"
                ]
                _log.debug(f"    - parent_module: {parent_module}")
                _namespace = vars(parent_module).get("_namespace")
                if _namespace:
                    _log.debug(
                        f"    - parent module {parent_module} namespace: {_namespace}"
                    )
                else:
                    # check the superclasses that are in the same module
                    for supercls in cls.__mro__:
                        supercls_module = inspect.getmodule(supercls)
                        _log.debug(
                            f"    - supercls {supercls} module: {supercls_module}"
                        )
                        if supercls_module is not cls_module:
                            continue

                        _namespace = vars(supercls).get("_namespace")
                        if _namespace:
                            _log.debug(
                                f"    - supercls {supercls} namespace: {_namespace}"
                            )
                            break

        # use the "example" namespace if nothing else available
        if _namespace is None:
            _namespace = EX

        # save a reference to the namespace in the class
        cls._namespace = _namespace  # type: ignore[attr-defined]

        # give the class an IRI if it doesn't have one
        if "_class_iri" not in vars(cls):
            cls._class_iri = _namespace[cls.__name__]  # type: ignore[attr-defined]
            _log.debug(f"    - class given IRI: {cls._class_iri!r}")

        # this is a class, and a subclass of the super classes
        if cls._class_iri is not None:
            cls._schema_graph.add((cls._class_iri, RDF.type, RDFS.Class))

            # some documentation is nice
            if cls.__doc__:
                cls._schema_graph.add(
                    (cls._class_iri, RDFS.comment, Literal(cls.__doc__))
                )
            cls._schema_graph.add(
                (
                    cls._class_iri,
                    RDFS.label,
                    Literal(cls.__module__ + "." + cls.__name__),
                )
            )

            for supercls in cls.__mro__[1:]:
                if issubclass(supercls, Node):
                    _class_iri = vars(supercls).get("_class_iri")
                    if _class_iri is not None:
                        cls._schema_graph.add(
                            (cls._class_iri, RDFS.subClassOf, supercls._class_iri)
                        )

        attr_annotations = vars(cls).get("__annotations__", {})
        for attr, attr_annotation in attr_annotations.items():
            if attr.startswith("_") or attr == "node_type":
                continue
            _log.debug(f"    - attr: {attr!r}")
            _log.debug(f"        - attr_annotation: {attr_annotation!r}")

            if isinstance(attr_annotation, str) and not isinstance(
                attr_annotation, URIRef
            ):
                # eval the string in the context of the globals in its module
                try:
                    cls_module = inspect.getmodule(cls)
                    _log.debug(f"        - {cls_module=}")
                    attr_type = eval(attr_annotation, vars(cls_module))
                except NameError:
                    raise RuntimeError(
                        f"class {cls}, attribute {attr}: unable to resolve {attr_annotation}"
                    )
            else:
                attr_type = attr_annotation
            _log.debug(f"        - attr_type: {attr_type!r}")

            attr_origin = get_origin(attr_type)
            _log.debug(f"        - attr_origin: {attr_origin!r}")

            attr_uriref = cls._attr_uriref.get(attr, _namespace[attr])
            _log.debug(f"        - attr_uriref: {attr_uriref!r}")

            # create a property restriction for the attribute
            sh_property: Optional[BNode] = None
            if cls._class_iri is not None and not cls._class_iri.startswith(S223):
                sh_property = BNode()
                cls._schema_graph.add((sh_property, RDF.type, SH.PropertyShape))
                cls._schema_graph.add((sh_property, SH.path, attr_uriref))

                cls._schema_graph.add((cls._class_iri, RDF.type, SH.NodeShape))
                cls._schema_graph.add((cls._class_iri, SH.property, sh_property))

            if isinstance(attr_type, URIRef):
                if not attr_type.startswith(XSD):
                    raise ValueError(f"datatype URI expected for {attr}: {attr_type}")

                cls._datatypes[attr] = attr_type
                cls._attr_uriref[attr] = attr_uriref
                cls._schema_graph.add((attr_uriref, RDF.type, RDF.Property))
                if sh_property:
                    cls._schema_graph.add((sh_property, SH.datatype, attr_type))

            elif attr_origin in (Any, Dict, Set, List, Union, list, set, dict):
                warnings.warn(
                    f"class {cls}, attribute {attr}: inspection not supported {attr_type}"
                )

                cls._nodes[attr] = attr_type
                cls._attr_uriref[attr] = attr_uriref
                cls._schema_graph.add((attr_uriref, RDF.type, RDF.Property))

            elif inspect.isclass(attr_type):
                cls._nodes[attr] = attr_type
                cls._attr_uriref[attr] = attr_uriref
                cls._schema_graph.add((attr_uriref, RDF.type, RDF.Property))

                if issubclass(attr_type, Property):
                    cls._schema_graph.add(
                        (attr_uriref, RDFS.subPropertyOf, S223.hasProperty)
                    )
                elif issubclass(attr_type, ConnectionPoint):
                    cls._schema_graph.add(
                        (
                            attr_uriref,
                            RDFS.subPropertyOf,
                            S223.hasConnectionPoint,
                        )
                    )
                elif issubclass(attr_type, OptionalConnectionPoint):
                    cls._schema_graph.add(
                        (
                            attr_uriref,
                            RDFS.subPropertyOf,
                            S223.hasOptionalConnectionPoint,
                        )
                    )
                    cls._schema_graph.add(
                        (
                            attr_uriref,
                            RDFS.subPropertyOf,
                            S223.hasBoundaryConnectionPoint,
                        )
                    )
                elif issubclass(attr_type, BoundaryConnectionPoint):
                    cls._schema_graph.add(
                        (
                            attr_uriref,
                            RDFS.subPropertyOf,
                            S223.hasBoundaryConnectionPoint,
                        )
                    )
                elif issubclass(attr_type, ZoneConnectionPoint):
                    cls._schema_graph.add(
                        (
                            attr_uriref,
                            RDFS.subPropertyOf,
                            BOB.hasZoneConnectionPoint,
                        )
                    )

            elif isinstance(attr_type, EnumerationKind):
                cls._nodes[attr] = attr_type
                cls._attr_uriref[attr] = attr_uriref
                cls._schema_graph.add((attr_uriref, RDF.type, RDF.Property))
                if sh_property:
                    cls._schema_graph.add(
                        (sh_property, SH["class"], attr_type._class_iri)
                    )

            else:
                raise ValueError(f"unknown annotation for {attr}: {attr_type}")

        for attr, attr_value in vars(cls).items():
            if attr.startswith("_"):
                continue
            if attr in attr_annotations:
                continue
            if inspect.isclass(attr_value) and issubclass(attr_value, Node):
                _log.debug(f"    - future init {attr!r} to instance of {attr_value!r}")
                attr_uriref = cls._attr_uriref.get(attr, _namespace[attr])

                cls._nodes[attr] = attr_value
                cls._attr_uriref[attr] = attr_uriref

        cls._resolved = True
        _log.debug(f"    - resolved {cls}")

    def __setattr__(self, attr: str, value: Any) -> None:
        """
        .
        """
        # continue with normal process for attributes that aren't special to us
        if attr.startswith("_") or (
            (attr not in self._nodes) and (attr not in self._datatypes)
        ):
            super().__setattr__(attr, value)
            return
        _log.debug("__setattr__ %r %r", attr, value)

        # make sure the value isn't None, no "deleting" content
        if value is None:
            raise ValueError(f"{attr} is None")

        # make sure the current value is None, no "reassigning" content
        current_value = vars(self).get(attr)
        if current_value is not None:
            if attr not in getattr(self, "_volatile", {}):
                raise RuntimeError(
                    f"attribute {attr} already has a value: {current_value}"
                )

        # if this is a node, double check the type
        if attr in self._nodes:
            attr_type = self._nodes[attr]
            _log.debug("    - attr_type: %r", attr_type)

            # if the type reference is still a string, find the real type
            if isinstance(attr_type, str):
                raise RuntimeError(f"{attr_type!r} still a string for {attr!r}")

            # attr_type allows any instance of an enumeration kind
            if attr_type is EnumerationKind:
                if not isinstance(value, EnumerationKind):
                    raise TypeError(
                        f"value {value} for attribute {attr} not a {attr_type}"
                    )

            # attr_type requires a some sub-kind
            elif isinstance(attr_type, EnumerationKind):
                if (not isinstance(value, EnumerationKind)) or (
                    value not in attr_type._children
                ):
                    raise TypeError(
                        f"value {value} for attribute {attr} not a {attr_type}"
                    )

            # special case assigning type means creating an instance
            elif value is attr_type:
                _log.debug(f"    - construct new {attr_type}")
                value = attr_type()

            # pass the value to the class to build one
            elif not isinstance(value, attr_type):
                try:
                    _log.debug(f"    - construct {attr_type} from: {value!r}")
                    value = attr_type(value)
                except TypeError:
                    _log.debug("    - why is this trapped?")
                    value = attr_type(_node_iri=value)
                _log.debug("    - new value: %r", value)

            # add the link(s)
            if isinstance(value, (URIRef, Literal)):
                # volatile attributes use set() so the old triple is removed
                if attr in getattr(self, "_volatile", {}):
                    self._data_graph.set(
                        (self._node_iri, self._attr_uriref[attr], value)
                    )  # type: ignore[attr-defined]
                else:
                    self._data_graph.add(
                        (self._node_iri, self._attr_uriref[attr], value)
                    )  # type: ignore[attr-defined]

            # if the value is a Node, link to it
            if isinstance(value, Node):
                _log.debug(
                    "    - add (self, %r, %r)", self._attr_uriref[attr], value._node_iri
                )
                self._data_graph.add(
                    (self._node_iri, self._attr_uriref[attr], value._node_iri)
                )  # type: ignore[attr-defined]

            # if the value is a property, link it to the node
            if isinstance(value, Property) and issubclass(attr_type, Property):
                self.add_property(value)

            # if the value is an external reference, link it to the node
            if isinstance(value, ExternalReference):
                self.add_external_reference(value)

            # if the value is a ConnectionPoint and the attribute type is a
            # BoundaryConnectionPoint, link it to the node
            if isinstance(value, ConnectionPoint) and issubclass(
                attr_type, BoundaryConnectionPoint
            ):
                self.add_boundary_connection_point(value)

            # if the value is a ConnectionPoint and the attribute type is an
            # OptionalConnectionPoint it is already linked but needs an extra
            # triple, link it to the node
            if isinstance(value, ConnectionPoint) and issubclass(
                attr_type, OptionalConnectionPoint
            ):
                _log.debug("    - optional connection point")
                self._data_graph.add(
                    (self._node_iri, S223.hasOptionalConnectionPoint, value._node_iri)
                )  # type: ignore[attr-defined]

        # if this needs some datatype decoration, turn it into a literal
        if attr in self._datatypes:
            attr_datatype = self._datatypes[attr]
            if attr_datatype is Literal:
                if not isinstance(value, Literal):
                    value = Literal(value)
            elif isinstance(value, Literal):
                if value.datatype != attr_datatype:
                    raise TypeError(f"{attr}: literal {attr_datatype} expected")
            elif isinstance(value, (str, int, float)):
                value = Literal(value, datatype=attr_datatype)
            else:
                value = Literal(value)
                if value.datatype != attr_datatype:
                    raise TypeError(f"{attr}: literal {attr_datatype} expected")

            # add the literal
            self._data_graph.add((self._node_iri, self._attr_uriref[attr], value))  # type: ignore[attr-defined]

        # carry on
        _log.debug("    - carry on")
        super().__setattr__(attr, value)

    def __rshift__(self, other: Any) -> Any:
        """Build a connection from this thing to another thing."""
        connect_mm(self, other)
        return other

    def __lshift__(self, other: Any) -> Any:
        """Build a connection to this thing from another thing."""
        connect_mm(other, self)
        return self

    def __iadd__(self, other: Any) -> Any:
        """Add something (aspect, role...) to the node
        prop += aspect
        """
        add_mm(self, other)
        return self

    def __repr__(self) -> str:
        label = getattr(self, "label", "")
        if label:
            label = " " + label
        return f"<{self.__class__.__name__}{label} at {self._node_iri}>"

    def add_property(self, prop: Property) -> Property:
        """Add a property to a node, returns the added property."""
        assert isinstance(prop, Property)

        # link the two together
        self._data_graph.add((self._node_iri, S223.hasProperty, prop._node_iri))

        return prop


class ExternalReferenceValue:
    """
    This class is actually a mapping function that returns a URIRef or literal
    and is used like:

        class X:
            someProperty: ExternalReferenceValue

        x = X(someProperty=12)

    The current REF schema (see Brick) doesn't have a subclass of ExternalReference
    that has a shape that can point to a literal.
    """

    def __new__(cls, value):
        _log.debug(f"ExternalReferenceValue.__new__ {cls!r} {value!r}")
        raise RuntimeError("needs technical assistance")

        if isinstance(value, Literal):
            pass
        elif isinstance(value, URIRef):
            pass
        elif isinstance(value, Node):
            value = value._node_iri
        else:
            value = Literal(value)

        return value


class ExternalReference(Node):
    """
    This will be subclassed by different specific datasources.
    """

    def __init__(
        self,
        arg: Any = None,  # Union[str, Literal, URIRef, Node]
        **kwargs: Any,
    ):
        _log.debug(f"ExternalReference.__init__ {arg!r} {kwargs}")
        if self.__class__ is ExternalReference:
            warnings.warn("ExternalReference is an abstract base class")

        super().__init__(**kwargs)

        if arg:
            self._data_graph.add((self._node_iri, RDFS.comment, Literal(str(arg))))


class Property(Node):
    """
    An attribute, quality, or characteristic of a feature of interest.  This is
    an abstract base class.
    """

    ofMedium: Medium
    ofConstituent: Constituent
    ofSubstance: Substance
    hasValue: Literal
    # hasExternalReference: set() see below
    # hasAspect: set() see below

    # override this for a specialize subclass
    _external_reference_class: type = ExternalReference

    # override this for other volatile attributes
    _volatile = ("hasValue",)

    def __init__(self, value: Any = None, **kwargs: Any):
        _log.debug(f"Property.__init__ {value!r} {kwargs}")

        init_value = None
        if value is None:
            if "hasValue" in kwargs:
                init_value = kwargs.pop("hasValue")
        elif "hasValue" in kwargs:
            raise RuntimeError("initialization conflict")
        else:
            init_value = value

        external_reference = None
        internal_reference = None

        if "hasExternalReference" in kwargs:
            if init_value or internal_reference:
                raise RuntimeError(
                    "initialization conflict, can't have a value and an external datasource"
                )
            external_reference = kwargs.pop("hasExternalReference")

        if "hasInternalReference" in kwargs:
            if init_value or external_reference:
                raise RuntimeError(
                    "initialization conflict, can't have a value and an internal datasource"
                )
            internal_reference = kwargs.pop("hasExternalReference")
        # Retrieve aspects so we can add them after the creation
        aspects = []
        if "hasAspect" in kwargs:
            _aspects = kwargs.pop("hasAspect")
            if isinstance(_aspects, list):
                aspects.extend(_aspects)
            else:
                aspects.append(_aspects)

        # Create the property
        super().__init__(**kwargs)
        self.hasAspect = set()
        self.hasExternalReference = set()
        self.hasInternalReference = set()
        self._hasValue = None

        # Add aspects
        for each in aspects:
            self += each

        # if there is an initial value, link to it
        if init_value is not None and init_value != ():
            if not isinstance(init_value, Literal):
                init_value = Literal(init_value)
            self.hasValue = init_value
            self._hasValue = init_value

        # same for ExternalReference, allow initializing with a list of them
        if external_reference is not None:
            if isinstance(external_reference, list):
                for ref in external_reference:
                    self @ ref
            elif isinstance(external_reference, ExternalReference):
                self @ external_reference
            else:
                raise TypeError(f"external reference expected: {external_reference}")
        if internal_reference is not None:
            if isinstance(internal_reference, list):
                for ref in internal_reference:
                    self >> ref
            elif isinstance(internal_reference, Property):
                self >> internal_reference
            else:
                raise TypeError(f"external reference expected: {external_reference}")

    def __matmul__(self, other: Any) -> Any:
        """Add an external reference to the node
        property @ ref
        """
        reference_mm(self, other)
        return self

    def add_external_reference(self, external_reference):
        if (
            self.hasInternalReference
            or self._hasValue is not None
            or self.hasValue is not None
        ):
            raise AttributeError(
                f"Can't add external reference if property already have a value or internal reference {self.hasInternalReference} {self._hasValue}"
            )
        if not isinstance(external_reference, self._external_reference_class):
            external_reference = self._external_reference_class(
                comment=external_reference,
            )
            if hasattr(self, "label"):
                external_reference.label = self.label + ".ExternalReference"

        # link the two together
        self._data_graph.add(
            (self._node_iri, S223.hasExternalReference, external_reference._node_iri)
        )
        self.hasExternalReference.add(external_reference)

    def add_internal_reference(self, internal_reference):
        if (
            self.hasExternalReference
            or self._hasValue is not None
            or self.hasValue is not None
        ):
            raise AttributeError(
                "Can't add internal reference if property already have a value or external reference"
            )
        if not isinstance(internal_reference, Property):
            raise TypeError(f"property expected: {internal_reference}")

        # link the two together
        self._data_graph.add(
            (self._node_iri, S223.hasInternalReference, internal_reference._node_iri)
        )
        self.hasInternalReference.add(internal_reference)


@multimethod
def add_mm(prop: Property, aspect: EnumerationKind) -> None:
    """
    Add a role to an equipment
    """
    _log.info(f"add aspect {aspect} to {prop}")
    prop.hasAspect.add(aspect)
    prop._data_graph.add((prop._node_iri, S223.hasAspect, aspect._node_iri))
    if INCLUDE_INVERSE:
        aspect.isAspectOf = prop


@multimethod
def reference_mm(prop: Property, external_reference: ExternalReference) -> None:
    """Add an additional external reference to a property."""
    _log.info(f"add external reference {external_reference} to {prop}")
    prop.add_external_reference(external_reference)


@multimethod
def reference_mm(property: Property, internal_reference: Property) -> None:
    """Property @ Property"""
    _log.info(f"Property {property} hasInternalReference {internal_reference}")
    property.add_internal_reference(internal_reference)


class ActuatableProperty(Property):
    """
    Such as the setting of a switch.
    """

    _class_iri: URIRef = S223.ActuatableProperty
    # TODO : Would it be possible for an Actuatable property, to actuates another actuatable property ?
    # actuatesProperty: Property


class ObservableProperty(Property):
    """
    Such as the state of an alarm detector.
    """

    _class_iri: URIRef = S223.ObservableProperty
    _attr_uriref = {"isObservedBy": BOB.isObservedBy}

    isObservedBy: Node


class QuantifiableProperty(Property):
    """
    A property to be expressed as a quantity, it has units.
    """

    _attr_uriref = {
        "hasUnit": QUDT["hasUnit"],
        "hasQuantityKind": QUDT["hasQuantityKind"],
    }

    _class_iri: URIRef = S223.QuantifiableProperty
    hasUnit: URIRef
    hasQuantityKind: URIRef

    def __init__(self, value: Any = None, **kwargs: Any) -> None:
        _log.debug(f"QuantifiableProperty.__init__ {value!r} {kwargs}")
        init_value = None
        if value is None:
            if "hasValue" in kwargs:
                init_value = kwargs.pop("hasValue")
        elif "hasValue" in kwargs:
            raise RuntimeError("initialization conflict")
        else:
            init_value = value

        if init_value is not None:
            if isinstance(init_value, (int, float)):
                init_value = Literal(init_value, datatype=XSD.decimal)
            elif isinstance(init_value, Literal):
                init_value = Literal(init_value)
            else:
                raise TypeError(f"decimal expected: {init_value}")

        super().__init__(init_value, **kwargs)

    def set_value(self, value):
        self.hasValue = Literal(value, datatype=XSD.decimal)


class QuantifiableActuatableProperty(QuantifiableProperty, ActuatableProperty):
    """
    Such as a numerical setpoint.
    """

    _class_iri: URIRef = S223.QuantifiableActuatableProperty

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)


# Setpoints are subclasses of properties currently, but should they be quantifiable actuatable subclass?
# Setpoint can be actuatable be they can also be the result of an algortithm in which case, they
# are observable
# There could be 2 subclasses of setpoint ?
#
# Opinion
# Setpoints is the "usage" we do of the property, it's not the property itself
# an aspect would be much more appropriate - Christian
#
class Setpoint(QuantifiableProperty):
    _class_iri: URIRef = S223.Setpoint
    hasDeadband: Literal
    hasValue: Literal

    def __init__(self, **kwargs):
        _properties = {}
        for k, v in self.__annotations__.items():
            if k in kwargs:
                _properties[k] = kwargs.pop(k)
        super().__init__(**kwargs)
        for k, v in _properties.items():
            if v is not None:
                setattr(self, k, self.__annotations__[k](v))


class QuantifiableObservableProperty(QuantifiableProperty, ObservableProperty):
    """
    Such as a temperature reading.
    """

    _class_iri: URIRef = S223.QuantifiableObservableProperty
    hasSetpoint: Setpoint

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)


class EnumerableProperty(Property):
    """
    A property to be expressed as an EnumerationKind.
    """

    # _attr_uriref = {}

    _class_iri: URIRef = S223.EnumerableProperty
    hasEnumerationKind: EnumerationKind

    def __init__(self, value: Any = None, **kwargs: Any) -> None:
        _log.debug(f"EnumerableProperty.__init__ {value!r} {kwargs}")

        init_value = None
        if value is None:
            if "hasValue" in kwargs:
                init_value = kwargs.pop("hasValue")
        elif "hasValue" in kwargs:
            raise RuntimeError("initialization conflict")
        else:
            init_value = value

        # TODO : Find a way to be sure it's a good Enumeration for the EnumerationKind ?
        if init_value is not None:
            if isinstance(init_value, Literal):
                init_value = Literal(init_value)
            else:
                raise TypeError(f"enumeration expected: {init_value}")

        super().__init__(init_value, **kwargs)


class EnumeratedObservableProperty(EnumerableProperty, ObservableProperty):
    """
    Such as a On-Off Status.
    """

    _class_iri: URIRef = S223.EnumeratedObservableProperty

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)


class EnumeratedActuatableProperty(EnumerableProperty, ActuatableProperty):
    """
    Such as a On-Off command.
    """

    _class_iri: URIRef = S223.EnumeratedActuatableProperty

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)


class PropertyReference:
    def __new__(cls, property):
        if not isinstance(property, Property):
            raise TypeError(f"property expected: {property}")
        return property


class LocationReference:
    def __new__(cls, location):
        if not isinstance(
            location, (Connectable, Connection, ConnectionPoint, PhysicalSpace)
        ):
            raise TypeError(f"location expected: {location}")
        return location


class Container(Node):
    """
    This class implements the Container Abstract Base Class.
    """

    _class_iri: URIRef = None
    _contents: Dict[str, Node]

    def __init__(self, *args, **kwargs) -> None:
        _log.debug(f"Container.__init__ {args} {kwargs}")
        if self.__class__ is Container:
            raise RuntimeError("Container is an abstract base class")

        super().__init__(*args, **kwargs)
        self._contents = {}

    def __getitem__(self, label: Union[str, Literal]) -> Node:
        _log.debug(f"Container.__getitem__ {label!r}")
        if isinstance(label, str):
            label = Literal(label)
        elif not isinstance(label, Literal):
            raise TypeError(f"Literal or string expected: {label!r}")
        try:
            return self._contents[label]
        except KeyError:
            # maybe it's the name of a property
            return self.__dict__[str(label)]

    def __setitem__(self, label: Union[str, Literal], value: Node) -> None:
        _log.debug(f"Container.__getitem__ {label!r} {value!r}")
        if isinstance(label, str):
            label = Literal(label)
        elif not isinstance(label, Literal):
            raise TypeError(f"Literal or string expected: {label!r}")
        self._contents[label] = value

    def __contains__(self, label: Union[str, Literal]) -> bool:
        _log.debug(f"Container.__contains__ {label!r}")
        if isinstance(label, str):
            label = Literal(label)
        elif not isinstance(label, Literal):
            raise TypeError(f"Literal or string expected: {label!r}")
        return label in self._contents

    # def __len__(self):
    #     Do not define this function or `a < b < c` will break.

    def __gt__(self, other: Node) -> Node:
        """This node contains some other node."""
        _log.debug(f"Container.__gt__ {self} > {other}")

        if hasattr(other, "label"):
            if other.label in self._contents:
                raise ValueError(f"label already used: {self._contents[other.label]}")
            self._contents[other.label] = other

        contains_mm(self, other)
        return self

    def __lt__(self, other: Container) -> Node:
        """This node is contained in some other node."""
        _log.debug(f"Container.__lt__ {self} < {other}")

        if hasattr(self, "label"):
            if self.label in other._contents:
                raise ValueError(f"label already used: {other._contents[self.label]}")
            other._contents[self.label] = self

        contains_mm(other, self)
        return self

    def content(self):
        for k, v in self._contents.items():
            print(k, v)


#
#   Enumerations
#


class EnumerationKind(Node):
    _class_iri: URIRef = S223["EnumerationKind"]
    _data_graph = schema_graph

    def __init__(self, name, *args, **kwargs) -> None:
        _log.debug("EnumerationKind.__init__ %r", name)

        # give it a default label that matches the name
        if "label" not in kwargs:
            kwargs["label"] = name

        if "_alt_namespace" in kwargs:
            _ns = kwargs.pop("_alt_namespace")
            kwargs["_node_iri"] = _ns["EnumerationKind" + "-" + name]
        elif "_node_iri" not in kwargs:
            kwargs["_node_iri"] = _namespace["EnumerationKind" + "-" + name]

        super().__init__(**kwargs)

        self._schema_graph.add((self._node_iri, RDF.type, RDFS.Class))
        self._schema_graph.add((self._node_iri, RDF.type, self._node_iri))
        self._schema_graph.add((self._node_iri, RDF.type, SH.NodeShape))

        self._schema_graph.add(
            (self._node_iri, RDFS.subClassOf, _namespace["EnumerationKind"])
        )

        self._name = name
        self._parent = None
        self._children = set([self])
        self._constituents = set()
        self.composedOf = set()

    def __call__(self, name, *, _alt_namespace=None, **kwargs) -> EnumerationKind:
        _log.debug("EnumerationKind.__call__ %r", name)

        # give it a default label that matches the name
        if "label" not in kwargs:
            kwargs["label"] = name

        if _alt_namespace:
            new_child = self.__class__(
                name, _node_iri=_alt_namespace[self._name + "-" + name], **kwargs
            )
        else:
            new_child = self.__class__(
                name, _node_iri=_namespace[self._name + "-" + name], **kwargs
            )
        _log.debug("    - new_child: %r", new_child)

        # constituent references cascade to children and are added as
        # non-quantifiable properties
        for each in self._constituents:
            new_child.add_constituent(each)

        new_child._parent = self
        new_child._schema_graph.add(
            (new_child._node_iri, RDFS.label, Literal(kwargs["label"]))
        )
        pnode = self
        while pnode:
            pnode._children.add(new_child)
            schema_graph.add((new_child._node_iri, RDFS.subClassOf, pnode._node_iri))
            pnode = pnode._parent

        return new_child

    def add_constituent(self, constituent: Constituent, *args, **kwargs) -> None:
        _log.debug("Mix.add_constituent %r %r %r", constituent, args, kwargs)
        _log.debug("    - self: %r", self)

        if not isinstance(constituent, Constituent):
            raise TypeError("constituent")

        # if not isinstance(self, Mix):
        #    raise TypeError("Only Mix can have constituents")

        if not self.composedOf:
            self.composedOf = set()

        # look for an existing reference to this constituent
        for prop in self.composedOf:
            if prop.ofConstituent == constituent:
                _log.debug("    - existing property reference: %r", prop)

                update_to_quantifiable = False
                if "hasQuantityKind" in kwargs:
                    _log.debug("    - update hasQuantityKind")
                    prop._data_graph.add(
                        (
                            prop._node_iri,
                            QUDT.hasQuantityKind,
                            kwargs["hasQuantityKind"],
                        )
                    )
                    update_to_quantifiable = True
                if "hasUnit" in kwargs:
                    _log.debug("    - update hasUnit")
                    prop._data_graph.add(
                        (prop._node_iri, QUDT.hasUnit, kwargs["hasUnit"])
                    )
                    update_to_quantifiable = True
                if "hasValue" in kwargs:
                    _log.debug("    - update hasValue")
                    if not update_to_quantifiable:
                        _log.debug(
                            "    - should probably specify hasQuantityKind and/or hasUnit"
                        )
                    prop.hasValue = kwargs["hasValue"]

                if update_to_quantifiable:
                    _log.debug("    - upgrade to quantifiable")
                    prop._data_graph.add(
                        (prop._node_iri, RDF.type, S223.QuantifiableProperty)
                    )
                return

        # see if this should be quantifiable or not
        property_class: type
        if ("hasQuantityKind" in kwargs) or ("hasUnit" in kwargs):
            property_class = QuantifiableProperty
        else:
            property_class = Property
        _log.debug("    - property_class: %r", property_class)

        prop = property_class(
            *args,
            label=f"{self._name}.Constituent-{constituent._name}",
            ofConstituent=constituent,
            _data_graph=self._data_graph,
            **kwargs,
        )
        _log.debug("    - new property: %r", prop)

        self._constituents.add(constituent)
        prop._schema_graph.add((self._node_iri, S223.composedOf, prop._node_iri))
        self.composedOf.add(prop)


#
#   Top Level EnumerationKind Instances
#

# General EnumerationKind
Substance = EnumerationKind("Substance")
Substance.Medium = Medium = Substance("Medium")
Medium.Constituent = Medium("Constituent")
Medium.Mix = Mix = Medium("Mix")
Medium.ThermalContact = Medium("ThermalContact")

Role = EnumerationKind("Role")
Domain = EnumerationKind("Domain")


class Constituent(EnumerationKind):
    def __init__(self, name, *args, **kwargs) -> None:
        _log.debug("Constituent.__init__ %r", name)

        # give it a default label that matches the name
        if "label" not in kwargs:
            kwargs["label"] = name

        if "_alt_namespace" in kwargs:
            _ns = kwargs.pop("_alt_namespace")
            kwargs["_node_iri"] = _ns["Constituent" + "-" + name]
        elif "_node_iri" not in kwargs:
            kwargs["_node_iri"] = _namespace["Constituent" + "-" + name]

        super().__init__(name, **kwargs)

        self._schema_graph.add((self._node_iri, RDF.type, RDFS.Class))
        self._schema_graph.add((self._node_iri, RDF.type, self._node_iri))
        self._schema_graph.add((self._node_iri, RDF.type, SH.NodeShape))

        self._schema_graph.add(
            (self._node_iri, RDFS.subClassOf, _namespace["Constituent"])
        )

        # funky parents
        self._parent = Medium.Constituent
        Medium.Constituent._children.add(self)
        Medium._children.add(self)
        Substance._children.add(self)

    # def __call__(self, *args, **kwargs):
    #     raise NotImplementedError("no sub-constituents")


class System(Container):
    """
    System
    """

    _class_iri: URIRef = S223.System
    _boundary_connection_points: Set[BoundaryConnectionPoint]
    _serves_zones: Dict[str, Zone]

    def __init__(self, config: Dict[str, Any] = {}, *args, **kwargs: Any) -> None:
        _log.debug(f"System.__init__ {config} {args} {kwargs}")

        # if there are "params" in the configuation, use those as defaults for
        # kwargs and allow them to be overriden by additional kwargs
        # if config and "params" in config:
        #     kwargs = {**config["params"], **kwargs}

        super().__init__(*args, **kwargs)
        self.hasRole = set()

        if config:
            for group_name, group_items in config.items():
                if group_name in ("params", "relations"):
                    continue

                things = []
                for (thing_name, thing_class), thing_kwargs in group_items.items():
                    _log.debug(
                        f"    - thing_name, thing_class: {thing_name}, {thing_class}"
                    )
                    if thing_name in self:
                        raise ValueError(f"label already used: {self[thing_name]}")
                    thing = thing_class(label=thing_name, **thing_kwargs)

                    if isinstance(thing, (Equipment, System)):
                        self > thing
                    if isinstance(thing, Property):
                        # thing @ self
                        self[thing_name] = thing
                        self.add_property(thing)

                    things.append(thing)

                setattr(self, "_" + group_name, things)

        if MANDITORY_LABEL:
            if "label" not in kwargs:
                raise RuntimeError("no label")
            if not kwargs["label"]:
                raise RuntimeError("empty label")

        # no relationships to connection points or zones yet
        self._boundary_connection_points = set()
        self._serves_zones = {}

    def add_boundary_connection_point(
        self, connection_point: ConnectionPoint
    ) -> ConnectionPoint:
        """Add a boundary connection point to a system, returns the added connection point."""
        assert isinstance(connection_point, ConnectionPoint)

        # add this to the others for this node
        self._boundary_connection_points.add(connection_point)

        # link the two together
        self._data_graph.add(
            (
                self._node_iri,
                S223.hasBoundaryConnectionPoint,
                connection_point._node_iri,
            )
        )

        return connection_point


@multimethod
def contains_mm(system: System, equipment: Equipment) -> None:
    """System > Equipment"""
    _log.info(f"system {system} hasMember Equipment {equipment}")

    system._data_graph.add((system._node_iri, S223.hasMember, equipment._node_iri))


@multimethod
def contains_mm(system: System, subsystem: System) -> None:
    """System > System"""
    _log.info(f"system {system} hasMember subsystem {subsystem}")

    system._data_graph.add((system._node_iri, S223.hasMember, subsystem._node_iri))


@multimethod
def contains_mm(system: System, thing_list: List[Node]) -> None:
    """System > List[Union[Equipment,System]]"""
    _log.info(f"system {system} hasMember list of things {thing_list}")

    ###TODO: the signature should be thing_list: List[Union[Equipment,System]]

    for thing in thing_list:
        if not isinstance(thing, (Equipment, System)):
            raise TypeError(f"Equipment or system expected: {thing}")
        contains_mm(system, thing)


@multimethod
def add_mm(system: System, info: EnumerationKind) -> None:
    if info in Role._children:
        """
        Add a role to a system
        """
        role = info
        _log.info(f"add role {role} to {system}")
        system.hasRole.add(role)
        system._data_graph.add((system._node_iri, S223.hasRole, role._node_iri))
        if INCLUDE_INVERSE:
            role.isRoleOf = system


class ConnectionMetaclass(NodeMetaclass):
    def __new__(
        cls: Any,
        clsname: str,
        superclasses: Tuple[type, ...],
        attributedict: Dict[str, Any],
    ) -> ConnectionMetaclass:
        _log.debug(f"ConnectionMetaclass.__new__ {clsname}")

        # build the class
        new_class = cast(
            ConnectionMetaclass,
            super().__new__(cls, clsname, superclasses, attributedict),
        )

        return new_class


class Connection(Node, metaclass=ConnectionMetaclass):
    """
    Generic connection object type, unrestricted.
    """

    _class_iri: URIRef = S223.Connection
    hasMedium: Medium

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.hasAspect = set()


@multimethod
def add_mm(from_connection: Connection, aspect: EnumerationKind) -> None:
    """
    Add a role to a connection point
    """
    _log.info(f"add aspect {aspect} to {from_connection}")
    from_connection.hasAspect.add(aspect)
    from_connection._data_graph.add(
        (from_connection._node_iri, S223.hasAspect, aspect._node_iri)
    )
    if INCLUDE_INVERSE:
        aspect.isRoleOf = from_connection


class Connectable(Node):
    """
    A type of thing that can have connection points.
    """

    _class_iri: URIRef = S223.Connectable
    _connection_points: Dict[str, ConnectionPoint]

    def __init__(self, **kwargs: Any) -> None:
        _log.debug(f"Connectable.__init__ {kwargs}")
        if self.__class__ is Connectable:
            raise RuntimeError("Connectable is an abstract base class")
        super().__init__(**kwargs)

        # instantiate and associate all of the connection points
        self._connection_points = {}
        for attr_name, attr_type in self._nodes.items():
            if inspect.isclass(attr_type) and issubclass(attr_type, ConnectionPoint):
                # build an instance of this connection point
                attr_element = attr_type(self, label=self.label + "." + attr_name)
                self._connection_points[attr_name] = attr_element
                _log.debug(f"    - connection point {attr_name}: {attr_element}")

                setattr(self, attr_name, attr_element)


@multimethod
def connect_mm(from_thing: Connectable, to_thing: Connectable) -> None:
    """Connectable >> Connectable"""
    _log.info(f"connect from {from_thing} to {to_thing}")

    # build a dict of outlet connection points that are not already connected
    # organize them by medium
    from_out = defaultdict(set)
    for attr, connection_point in from_thing._connection_points.items():
        if connection_point.connectsThrough:
            continue
        if not isinstance(connection_point, OutletConnectionPoint):
            continue

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
        from_out[medium].add(connection_point)

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    from_types: Set[Medium]
    from_types = set(medium for medium in from_out if len(from_out[medium]) == 1)
    if not from_types:
        raise RuntimeError(f"no candidate sources from {from_thing} to {to_thing}")
    _log.debug(f"    - from_types: {from_types}")

    # build a dict of inlet connection points that are not already connected
    # organize them by medium
    to_in = defaultdict(set)
    for attr, connection_point in to_thing._connection_points.items():
        if connection_point.connectsThrough:
            continue
        if not isinstance(connection_point, InletConnectionPoint):
            continue

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
        to_in[medium].add(connection_point)

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    to_types: Set[Medium]
    to_types = set(medium for medium in to_in if len(to_in[medium]) == 1)
    if not to_types:
        raise RuntimeError(f"no candidate destinations from {from_thing} to {to_thing}")
    _log.debug(f"    - to_types: {to_types}")

    # find compatible pairs
    pairs = set()
    for from_medium, to_medium in itertools.product(from_types, to_types):
        if validate_medium(from_medium, to_medium):
            pairs.add((from_medium, to_medium))
    if len(pairs) == 0:
        raise RuntimeError("no compatible connection points")
    if len(pairs) > 1:
        print(pairs)
        raise RuntimeError("too many compatible connection points")

    from_medium, to_medium = pairs.pop()
    from_connection_point = from_out[from_medium].pop()
    _log.debug(f"    - from_connection_point: {from_connection_point}")
    to_connection_point = to_in[to_medium].pop()
    _log.debug(f"    - to_connection_point: {to_connection_point}")

    # continue creating the connection
    connect_mm(from_connection_point, to_connection_point)


@multimethod
def connect_mm(from_thing: Connectable, to_things: List[Connectable]) -> None:
    """Connectable >> [Connectable]"""
    _log.info(f"connect from {from_thing} to {to_things}")

    # build a dict of outlet connection points that are not already connected
    # organize them by medium
    from_out = defaultdict(set)
    for attr, connection_point in from_thing._connection_points.items():
        if connection_point.connectsThrough:
            continue
        if not isinstance(connection_point, OutletConnectionPoint):
            continue

        medium = getattr(connection_point, "hasMedium", None)
        from_out[medium].add(connection_point)

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    from_types: Set[Medium]
    from_types = set(medium for medium in from_out if len(from_out[medium]) == 1)
    if not from_types:
        raise RuntimeError(f"no candidate sources from {from_thing}")
    _log.debug(f"    - from_types: {from_types}")

    to_types_list: List[Set[Medium]] = []

    for to_thing in to_things:
        # build a dict of inlet connection points that are not already connected
        # organize them by medium
        to_in = defaultdict(set)
        for attr, connection_point in to_thing._connection_points.items():
            if connection_point.connectsThrough:
                continue
            if not isinstance(connection_point, InletConnectionPoint):
                continue

            medium = getattr(connection_point, "hasMedium", None)
            to_in[medium].add(connection_point)

        # filter them to a set where there is only one for that medium so it
        # would be unambiguous to use it
        to_types: Set[Medium]
        to_types = set(medium for medium in to_in if len(to_in[medium]) == 1)
        if not to_types:
            raise RuntimeError(f"no candidate destinations to {to_thing}")
        _log.debug(f"    - to_types: {to_types}")
        to_types_list.append(to_types)

    # find the common medium
    common_types = from_types.intersection(*to_types_list)
    if not common_types:
        raise RuntimeError("no common connection types")
    if len(common_types) > 1:
        raise RuntimeError("too many common connection types")
    medium = common_types.pop()
    _log.debug(f"    - medium: {medium}")

    # get from connection point
    from_connection_point = from_out[medium].pop()

    # create a connection
    if CONNECTION_HAS_MEDIUM:
        connection = Connection(hasMedium=medium)
    else:
        connection = Connection()

    # connect the from thing
    connect_mm(from_connection_point, connection)

    # connect the to things
    for to_thing in to_things:
        connect_mm(connection, to_thing)


class ConnectionPoint(Node):
    """
    Connection Point
    """

    _class_iri: URIRef = S223.ConnectionPoint
    hasMedium: Medium

    mapsTo: ConnectionPoint
    connectsThrough: Connection
    isConnectionPointOf: Connectable

    def __init__(self, thing: Connectable, **kwargs: Any) -> None:
        # abstract base class
        if self.__class__ is ConnectionPoint:
            raise RuntimeError("ConnectionPoint is an abstract base class")

        super().__init__(**kwargs)
        self.hasRole = set()
        self.paired_cp = None

        self._data_graph.add((thing._node_iri, S223.hasConnectionPoint, self._node_iri))
        if INCLUDE_CNX:
            if isinstance(self, InletConnectionPoint) or isinstance(
                self, BidirectionalConnectionPoint
            ):
                self._data_graph.add((self._node_iri, S223.cnx, thing._node_iri))

            if isinstance(self, OutletConnectionPoint) or isinstance(
                self, BidirectionalConnectionPoint
            ):
                self._data_graph.add((thing._node_iri, S223.cnx, self._node_iri))

        self.isConnectionPointOf = thing

        # this is one of the connection points of the Equipment
        thing._connection_points[str(self._node_iri)] = self

    def maps_to(self, other: ConnectionPoint) -> None:
        """
        Maps this connection point to a connection point of enclosing equipment.
        """
        _log.info(f"map from {self} to {other}")

        if not isinstance(other, ConnectionPoint):
            raise TypeError("ConnectionPoint expected")

        if self.connectsThrough:
            raise RuntimeError("connection point connected")
        if self.mapsTo:
            raise RuntimeError("connection point mapped")
        if other.connectsThrough:
            raise RuntimeError("other connection point connected")

        self.mapsTo = other

    def paired_to(self, other: ConnectionPoint) -> None:
        """
        Pair this connection point with another connection point.
        """
        _log.info(f"pair from {self} to {other}")

        if not isinstance(other, ConnectionPoint):
            raise TypeError("ConnectionPoint expected")

        if self.paired_cp is None and other.paired_cp is None:
            self.paired_cp = other
            other.paired_cp = self
            self._data_graph.add(
                (self._node_iri, S223.pairedConnectionPoint, other._node_iri)
            )
            self._data_graph.add(
                (other._node_iri, S223.pairedConnectionPoint, self._node_iri)
            )

    def __ipow__(self, other: Any) -> None:
        """Use **= to pair the connection point with another connection point."""
        self.paired_to(other)
        # return self


@multimethod
def add_mm(from_connection_point: ConnectionPoint, role: EnumerationKind) -> None:
    """
    Add a role to a connection point
    """
    _log.info(f"add role {role} to {from_connection_point}")
    from_connection_point.hasRole.add(role)
    from_connection_point._data_graph.add(
        (from_connection_point._node_iri, S223.hasRole, role._node_iri)
    )
    if INCLUDE_INVERSE:
        role.isRoleOf = from_connection_point


@multimethod
def connect_mm(
    from_connection_point: ConnectionPoint, to_connection_point: ConnectionPoint
) -> None:
    """ConnectionPoint >> ConnectionPoint"""
    _log.info(f"connect from {from_connection_point} to {to_connection_point}")

    if isinstance(from_connection_point, InletConnectionPoint):
        raise TypeError(f"connection point direction: {from_connection_point}")
    if from_connection_point.connectsThrough:
        raise RuntimeError("outlet connection point already connected")
    # if from_connection_point.mapsTo:
    #     raise RuntimeError("outlet connection point already mapped")

    if isinstance(to_connection_point, OutletConnectionPoint):
        raise TypeError("connection point direction: {to_connection_point}")
    if to_connection_point.connectsThrough:
        raise RuntimeError("inlet connection point already connected")
    # if to_connection_point.mapsTo:
    #     raise RuntimeError("inlet connection point already mapped")

    # check medium
    if not (from_medium := getattr(from_connection_point, "hasMedium", None)):
        raise AttributeError(f"{from_connection_point} hasMedium")
    _log.debug(f"    - from_medium: {from_medium}")

    if not (to_medium := getattr(to_connection_point, "hasMedium", None)):
        raise AttributeError(f"{to_connection_point} hasMedium")
    _log.debug(f"    - to_medium: {to_medium}")

    if not validate_medium(from_medium, to_medium):
        raise RuntimeError(
            f"mismatched medium: {from_connection_point} >> {to_connection_point}"
        )

    # create a connection between the two
    if CONNECTION_HAS_MEDIUM:
        connection = Connection(hasMedium=from_medium)
    else:
        connection = Connection()

    # link the two things together
    from_connection_point._data_graph.add(
        (
            from_connection_point.isConnectionPointOf._node_iri,
            S223.connectedTo,
            to_connection_point.isConnectionPointOf._node_iri,
        )
    )
    from_connection_point._data_graph.add(
        (
            from_connection_point.isConnectionPointOf._node_iri,
            S223.connected,
            to_connection_point.isConnectionPointOf._node_iri,
        )
    )
    from_connection_point._data_graph.add(
        (
            to_connection_point.isConnectionPointOf._node_iri,
            S223.connectedFrom,
            from_connection_point.isConnectionPointOf._node_iri,
        )
    )
    from_connection_point._data_graph.add(
        (
            to_connection_point.isConnectionPointOf._node_iri,
            S223.connected,
            from_connection_point.isConnectionPointOf._node_iri,
        )
    )

    # set the relationships
    connect_mm(from_connection_point, connection)
    connect_mm(connection, to_connection_point)


@multimethod
def connect_mm(connection_point: ConnectionPoint, connection: Connection) -> None:
    """ConnectionPoint >> Connection"""
    _log.info(f"connect from {connection_point} to {connection}")

    if isinstance(connection_point, InletConnectionPoint):
        raise TypeError("connection point direction")
    if connection_point.connectsThrough:
        raise RuntimeError("connection point already connected")
    if connection_point.mapsTo:
        if not connection_point.mapsTo.connectsThrough:
            raise RuntimeError(
                f"connect the mapped connection point: {connection_point.mapsTo}"
            )
        if connection_point.mapsTo.connectsThrough is not connection:
            raise RuntimeError(
                f"connection point connection mismatch: {connection_point.mapsTo.connectsThrough}"
            )

    # check medium
    if CONNECTION_HAS_MEDIUM:
        if not (connection_medium := getattr(connection, "hasMedium", None)):
            raise AttributeError(f"{connection} hasMedium")
        _log.debug(f"    - connection_medium: {connection_medium}")

        if not (
            connection_point_medium := getattr(connection_point, "hasMedium", None)
        ):
            raise AttributeError(f"{connection_point} hasMedium")
        _log.debug(f"    - connection_point_medium: {connection_point_medium}")

        if not validate_medium(connection_medium, connection_point_medium):
            raise RuntimeError(f"mismatched medium: {connection_point} >> {connection}")

    # property based link
    connection_point.connectsThrough = connection

    # link connection to the connection point and its Equipment
    connection_point._data_graph.add(
        (connection._node_iri, S223.connectsAt, connection_point._node_iri)
    )
    if INCLUDE_CNX:
        if isinstance(connection_point, InletConnectionPoint) or isinstance(
            connection_point, BidirectionalConnectionPoint
        ):
            connection_point._data_graph.add(
                (connection._node_iri, S223.cnx, connection_point._node_iri)
            )
        if isinstance(connection_point, OutletConnectionPoint) or isinstance(
            connection_point, BidirectionalConnectionPoint
        ):
            connection_point._data_graph.add(
                (connection_point._node_iri, S223.cnx, connection._node_iri)
            )

    connection_point._data_graph.add(
        (
            connection_point.isConnectionPointOf._node_iri,
            S223.connectedThrough,
            connection._node_iri,
        )
    )
    connection_point._data_graph.add(
        (
            connection._node_iri,
            S223.connectsFrom,
            connection_point.isConnectionPointOf._node_iri,
        )
    )


@multimethod
def connect_mm(connection: Connection, connection_point: ConnectionPoint) -> None:
    """Connection >> ConnectionPoint"""
    _log.info(f"connect from {connection} to {connection_point}")

    if isinstance(connection_point, OutletConnectionPoint):
        raise TypeError("connection point direction")
    if connection_point.connectsThrough:
        raise RuntimeError("connection point already connected")
    if connection_point.mapsTo:
        if not connection_point.mapsTo.connectsThrough:
            raise RuntimeError(
                f"connect the mapped connection point: {connection_point.mapsTo}"
            )
        if connection_point.mapsTo.connectsThrough is not connection:
            raise RuntimeError(
                f"connection point connection mismatch: {connection_point.mapsTo.connectsThrough}"
            )

    # check medium
    if CONNECTION_HAS_MEDIUM:
        if not (connection_medium := getattr(connection, "hasMedium", None)):
            raise AttributeError(f"{connection} hasMedium")
        _log.debug(f"    - connection_medium: {connection_medium}")

        if not (
            connection_point_medium := getattr(connection_point, "hasMedium", None)
        ):
            raise AttributeError(f"{connection_point} hasMedium")
        _log.debug(f"    - connection_point_medium: {connection_point_medium}")

        if not validate_medium(connection_medium, connection_point_medium):
            raise RuntimeError(f"mismatched medium: {connection} >> {connection_point}")

    # property based link
    connection_point.connectsThrough = connection

    # link connection to the connection point and its Equipment
    connection_point._data_graph.add(
        (
            connection_point.isConnectionPointOf._node_iri,
            S223.connectedThrough,
            connection._node_iri,
        )
    )
    connection._data_graph.add(
        (connection._node_iri, S223.connectsAt, connection_point._node_iri)
    )
    if INCLUDE_CNX:
        if isinstance(connection_point, InletConnectionPoint) or isinstance(
            connection_point, BidirectionalConnectionPoint
        ):
            connection._data_graph.add(
                (connection._node_iri, S223.cnx, connection_point._node_iri)
            )
        if isinstance(connection_point, OutletConnectionPoint) or isinstance(
            connection_point, BidirectionalConnectionPoint
        ):
            connection._data_graph.add(
                (connection_point._node_iri, S223.cnx, connection._node_iri)
            )

    connection._data_graph.add(
        (
            connection._node_iri,
            S223.connectsTo,
            connection_point.isConnectionPointOf._node_iri,
        )
    )


@multimethod
def connect_mm(equipment: Equipment, connection_point: ConnectionPoint) -> None:
    """Equipment >> ConnectionPoint"""
    _log.info(f"connect from {equipment} to {connection_point}")

    if connection_point.connectsThrough:
        raise RuntimeError("connection point already connected")
    if not (to_medium := getattr(connection_point, "hasMedium", None)):
        raise AttributeError(f"{connection_point} hasMedium")
    _log.debug(f"    - to_medium: {to_medium}")

    # build a dict of outlet connection points of the Equipment that are not
    # already connected that have a compatiable medium
    from_out = set()
    for attr, cp in equipment._connection_points.items():
        if connection_point.connectsThrough:
            continue
        if not isinstance(cp, OutletConnectionPoint):
            continue

        if not (medium := getattr(cp, "hasMedium", None)):
            continue
        if (medium in to_medium._children) or (to_medium in medium._children):
            from_out.add(cp)
    _log.debug(f"    - from_out: {from_out}")

    if not from_out:
        raise RuntimeError(
            f"no candidate sources from {equipment} to {connection_point}"
        )
    if len(from_out) > 1:
        raise RuntimeError("too many candidate connection points")
    from_thing = from_out.pop()
    _log.debug(f"    - from_thing: {from_thing}")

    # link the two things together
    from_thing._data_graph.add(
        (
            from_thing.isConnectionPointOf._node_iri,
            S223.connectedTo,
            connection_point.isConnectionPointOf._node_iri,
        )
    )
    from_thing._data_graph.add(
        (
            from_thing.isConnectionPointOf._node_iri,
            S223.connected,
            connection_point.isConnectionPointOf._node_iri,
        )
    )
    from_thing._data_graph.add(
        (
            connection_point.isConnectionPointOf._node_iri,
            S223.connectedFrom,
            from_thing.isConnectionPointOf._node_iri,
        )
    )
    from_thing._data_graph.add(
        (
            connection_point.isConnectionPointOf._node_iri,
            S223.connected,
            from_thing.isConnectionPointOf._node_iri,
        )
    )

    # set the relationships
    connect_mm(from_thing, connection_point)


@multimethod
def connect_mm(equipment: Equipment, connection: Connection) -> None:
    """Equipment >> Connection"""
    _log.info(f"connect from {equipment} to {connection}")

    if CONNECTION_HAS_MEDIUM:
        if not (connection_medium := getattr(connection, "hasMedium", None)):
            raise AttributeError(f"{connection} hasMedium")
        _log.debug(f"    - connection_medium: {connection_medium}")

    # build a dict of outlet connection points of the Equipment that are not
    # already connected that have a compatable medium
    from_out = set()
    for attr, connection_point in equipment._connection_points.items():
        if connection_point.connectsThrough:
            continue
        if not isinstance(connection_point, OutletConnectionPoint):
            continue

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
        if CONNECTION_HAS_MEDIUM:
            if validate_medium(medium, connection_medium):
                from_out.add(connection_point)
        else:
            from_out.add(connection_point)
    _log.debug(f"    - from_out: {from_out}")

    if not from_out:
        raise RuntimeError(f"no candidate sources from {equipment} to {connection}")
    if len(from_out) > 1:
        raise RuntimeError("too many connection points")
    from_thing = from_out.pop()

    # set the relationships
    connect_mm(from_thing, connection)


@multimethod
def connect_mm(connection: Connection, equipment: Equipment) -> None:
    """Connection >> Equipment"""
    _log.info(f"connect from {connection} to {equipment}")

    if CONNECTION_HAS_MEDIUM:
        if not (connection_medium := getattr(connection, "hasMedium", None)):
            raise AttributeError(f"{connection} hasMedium")
        _log.debug(f"    - connection_medium: {connection_medium}")

    # build a dict of inlet connection points that are not already connected
    # that have a compatable medium
    to_in = set()
    for attr, connection_point in equipment._connection_points.items():
        if connection_point.connectsThrough:
            continue
        if isinstance(connection_point, OutletConnectionPoint):
            continue

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue

        if CONNECTION_HAS_MEDIUM:
            if validate_medium(medium, connection_medium):
                to_in.add(connection_point)
        else:
            to_in.add(connection_point)
    _log.debug("    - to_in: %r", to_in)

    if not to_in:
        raise RuntimeError(
            f"no candidate destinations from {connection} to {equipment}"
        )
    if len(to_in) > 1:
        raise RuntimeError("too many connection points")
    to_thing = to_in.pop()
    _log.debug("    - to_thing: %r", to_thing)

    # set the relationships
    connect_mm(connection, to_thing)


@multimethod
def connect_mm(connection: Connection, equipment_list: List[Equipment]) -> None:
    """Connection >> [Equipment]"""
    _log.info(f"connect from {connection} to {equipment_list}")

    if CONNECTION_HAS_MEDIUM:
        if not (connection_medium := getattr(connection, "hasMedium", None)):
            raise AttributeError(f"{connection} hasMedium")
        _log.debug(f"    - connection_medium: {connection_medium}")

    for equipment in equipment_list:
        # build a dict of inlet connection points that are not already connected
        # that have a compatible medium
        to_in = set()
        for attr, connection_point in equipment._connection_points.items():
            if connection_point.connectsThrough:
                continue
            if isinstance(connection_point, OutletConnectionPoint):
                continue

            if not (medium := getattr(connection_point, "hasMedium", None)):
                continue

            if CONNECTION_HAS_MEDIUM:
                if validate_medium(medium, connection_medium):
                    to_in.add(connection_point)
            else:
                to_in.add(connection_point)
        _log.debug("    - to_in: %r", to_in)

        if not to_in:
            raise RuntimeError(
                f"no candidate destinations from {connection} to {equipment}"
            )
        if len(to_in) > 1:
            raise RuntimeError("too many destinations from {connection} to {equipment}")
        to_thing = to_in.pop()
        _log.debug("    - to_thing: %r", to_thing)

        # set the relationships
        connect_mm(connection, to_thing)


@multimethod
def connect_mm(connection_point: ConnectionPoint, equipment: Equipment) -> None:
    """ConnectionPoint >> Equipment"""
    _log.info(f"connect from {connection_point} to {equipment}")
    if not (connection_point_medium := getattr(connection_point, "hasMedium", None)):
        raise AttributeError(f"{connection_point} hasMedium")
    _log.debug("    - connection_point_medium: %r", connection_point_medium)

    # build a dict of inlet connection points that are not already connected
    # that have a compatable medium
    to_in = set()
    for attr, connection_point in equipment._connection_points.items():
        if connection_point.connectsThrough:
            continue
        if isinstance(connection_point, OutletConnectionPoint):
            continue

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
        if validate_medium(medium, connection_point_medium):
            to_in.add(connection_point)
    _log.debug("    - to_in: %r", to_in)

    if not to_in:
        raise RuntimeError(
            f"no candidate destinations from {connection_point} to {equipment}"
        )
    if len(to_in) > 1:
        raise RuntimeError("too many connection points")
    to_thing = to_in.pop()
    _log.debug("    - to_thing: %r", to_thing)

    # set the relationships
    connect_mm(connection_point, to_thing)


@multimethod
def connect_mm(connection: Connection, system: System) -> None:
    """Connection >> System"""
    _log.info(f"connect from {connection} to {system}")

    if CONNECTION_HAS_MEDIUM:
        if not (connection_medium := getattr(connection, "hasMedium", None)):
            raise AttributeError(f"{connection} hasMedium")
        _log.debug(f"    - connection_medium: {connection_medium}")

    # build a set of inlet connection points that are not
    # already connected, filtered by medium
    to_in = set()
    for connection_point in system._boundary_connection_points:
        if isinstance(connection_point, OutletConnectionPoint):
            continue
        if connection_point.connectsThrough:
            continue

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
        if CONNECTION_HAS_MEDIUM:
            if validate_medium(medium, connection_medium):
                to_in.add(connection_point)
        else:
            to_in.add(connection_point)

    if not to_in:
        raise RuntimeError(f"no candidate destinations from {connection} to {system}")
    if len(to_in) > 1:
        raise RuntimeError("too many connection points")
    to_thing = to_in.pop()
    _log.debug("    - to_thing: %r", to_thing)

    # set the relationships
    connect_mm(connection, to_thing)


@multimethod
def connect_mm(system: System, connection: Connection) -> None:
    """System >> Connection"""
    _log.info(f"connect from {system} to {connection}")

    if CONNECTION_HAS_MEDIUM:
        if not (connection_medium := getattr(connection, "hasMedium", None)):
            raise AttributeError(f"{connection} hasMedium")
        _log.debug(f"    - connection_medium: {connection_medium}")

    # build a dict of mapped outlet connection points that are not
    # already connected, organized by medium
    from_out = set()
    for connection_point in system._boundary_connection_points:
        if isinstance(connection_point, InletConnectionPoint):
            continue
        if connection_point.connectsThrough:
            continue

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
        if CONNECTION_HAS_MEDIUM:
            if validate_medium(medium, connection_medium):
                from_out.add(connection_point)
        else:
            from_out.add(connection_point)

    if not from_out:
        raise RuntimeError(f"no candidate destinations from {system} to {connection}")
    if len(from_out) > 1:
        raise RuntimeError("too many connection points")
    from_thing = from_out.pop()
    _log.debug("    - from_thing: %r", from_thing)

    # set the relationships
    connect_mm(from_thing, connection)


@multimethod
def connect_mm(equipment: Equipment, system: System) -> None:
    """Equipment >> System"""
    _log.info(f"connect from {equipment} to {system}")

    # build a dict of outlet connection points that are not already connected
    # that have the same medium
    from_out = defaultdict(set)
    for attr, connection_point in equipment._connection_points.items():
        if connection_point.connectsThrough:
            continue
        if not isinstance(connection_point, OutletConnectionPoint):
            continue

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
        from_out[medium].add(connection_point)

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    from_types: Set[Medium]
    from_types = set(medium for medium in from_out if len(from_out[medium]) == 1)
    if not from_types:
        raise RuntimeError(f"no candidate sources from {equipment} to {system}")
    _log.debug(f"    - from_types: {from_types}")

    # build a dict of mapped inlet connection points that are not
    # already connected, organized by medium
    to_in = defaultdict(set)
    for connection_point in system._boundary_connection_points:
        if connection_point.connectsThrough:
            continue
        if not isinstance(connection_point, InletConnectionPoint):
            continue

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
        to_in[medium].add(connection_point)

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    to_types: Set[Medium]
    to_types = set(medium for medium in to_in if len(to_in[medium]) == 1)
    if not to_types:
        raise RuntimeError(f"no candidate destinations from {equipment} to {system}")
    _log.debug(f"    - to_types: {to_types}")

    # find compatible pairs
    pairs = set()
    for from_medium, to_medium in itertools.product(from_types, to_types):
        if validate_medium(from_medium, to_medium):
            pairs.add((from_medium, to_medium))
    if len(pairs) == 0:
        raise RuntimeError("no compatiable connection points")
    if len(pairs) > 1:
        raise RuntimeError("too many compatiable connection points")

    from_medium, to_medium = pairs.pop()
    from_connection_point = from_out[from_medium].pop()
    _log.debug(f"    - from_connection_point: {from_connection_point}")
    to_connection_point = to_in[to_medium].pop()
    _log.debug(f"    - to_connection_point: {to_connection_point}")

    # continue creating the connection
    connect_mm(from_connection_point, to_connection_point)


@multimethod
def connect_mm(system: System, equipment: Equipment) -> None:
    """System >> Equipment"""
    _log.info(f"connect from {system} to {equipment}")

    # build a dict of mapped outlet connection points that are not
    # already connected, organized by medium
    from_out = defaultdict(set)
    for connection_point in system._boundary_connection_points:
        _log.debug(f"    - attr, connection_point: {attr} {connection_point}")
        if connection_point.connectsThrough:
            _log.debug("        - already connected")
            continue
        if not isinstance(connection_point, OutletConnectionPoint):
            _log.debug("        - not an outlet")
            continue

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
        from_out[medium].add(connection_point)
    _log.debug("    - from_out: %r", from_out)

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    from_types: Set[Medium]
    from_types = set(medium for medium in from_out if len(from_out[medium]) == 1)
    if not from_types:
        raise RuntimeError(f"no candidate sources from {system} to {equipment}")
    _log.debug("    - from_types: %r", from_types)

    # build a dict of outlet connection points that are not already connected
    # that have the same medium
    to_in = defaultdict(set)
    for attr, connection_point in equipment._connection_points.items():
        if connection_point.connectsThrough:
            continue
        if not isinstance(connection_point, InletConnectionPoint):
            continue

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
        to_in[medium].add(connection_point)

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    to_types: Set[Medium]
    to_types = set(medium for medium in to_in if len(to_in[medium]) == 1)
    if not to_types:
        raise RuntimeError(f"no candidate destinations from {system} to {equipment}")
    _log.debug(f"    - from_types: {from_types}")

    # find compatible pairs
    pairs = set()
    for from_medium, to_medium in itertools.product(from_types, to_types):
        if validate_medium(from_medium, to_medium):
            pairs.add((from_medium, to_medium))
    if len(pairs) == 0:
        raise RuntimeError("no compatiable connection points")
    if len(pairs) > 1:
        raise RuntimeError("too many compatiable connection points")

    # get the two connection points
    from_medium, to_medium = pairs.pop()
    from_connection_point = from_out[from_medium].pop()
    _log.debug(f"    - from_connection_point: {from_connection_point}")
    to_connection_point = to_in[to_medium].pop()
    _log.debug(f"    - to_connection_point: {to_connection_point}")

    # continue creating the connection
    connect_mm(from_connection_point, to_connection_point)


class BoundaryConnectionPoint:
    def __new__(cls, connection_point):
        if not isinstance(connection_point, ConnectionPoint):
            raise TypeError(f"connection point expected: {connection_point}")
        return connection_point

    def __init__(self) -> None:
        _log.debug("BoundaryConnectionPoint.__init__")
        raise RuntimeError("BoundaryConnectionPoint heirarchy are abstract classes")


class OptionalConnectionPoint(BoundaryConnectionPoint):
    pass


@multimethod
def connect_mm(from_system: System, to_system: System) -> None:
    """System >> System"""
    _log.info(f"connect from {from_system} to {to_system}")

    # build a dict of mapped outlet connection points that are not
    # already connected, organized by medium
    from_out = defaultdict(set)
    for connection_point in from_system._boundary_connection_points:
        if connection_point.connectsThrough:
            continue
        if isinstance(connection_point, InletConnectionPoint):
            continue

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
        from_out[medium].add(connection_point)
    _log.debug(f"    - from_out: {from_out}")

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    from_types: Set[Medium]
    from_types = set(medium for medium in from_out if len(from_out[medium]) == 1)
    if not from_types:
        raise RuntimeError(f"no candidate sources from {from_system} to {to_system}")
    _log.debug(f"    - from_types: {from_types}")

    # build a dict of mapped outlet connection points that are not
    # already connected, organized by medium
    to_in = defaultdict(set)
    for connection_point in to_system._boundary_connection_points:
        if connection_point.connectsThrough:
            continue
        if isinstance(connection_point, OutletConnectionPoint):
            continue

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
        to_in[medium].add(connection_point)
    _log.debug(f"    - to_in: {to_in}")

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    to_types: Set[Medium]
    to_types = set(medium for medium in to_in if len(to_in[medium]) == 1)
    if not to_types:
        raise RuntimeError(
            f"no candidate destinations from {from_system} to {to_system}"
        )
    _log.debug(f"    - to_types: {to_types}")

    # find compatible pairs
    pairs = set()
    for from_medium, to_medium in itertools.product(from_types, to_types):
        if validate_medium(from_medium, to_medium):
            pairs.add((from_medium, to_medium))
    if len(pairs) == 0:
        raise RuntimeError("no compatiable connection points")
    if len(pairs) > 1:
        raise RuntimeError("too many compatiable connection points")

    from_medium, to_medium = pairs.pop()
    from_connection_point = from_out[from_medium].pop()
    _log.debug(f"    - from_connection_point: {from_connection_point}")
    to_connection_point = to_in[to_medium].pop()
    _log.debug(f"    - to_connection_point: {to_connection_point}")

    # continue creating the connection
    connect_mm(from_connection_point, to_connection_point)


class Zone(Container, Node):
    """
    A collection of spaces.
    """

    _class_iri: URIRef = S223.Zone

    hasDomain: Domain

    _zone_connection_points: Dict[str, ZoneConnectionPoint]

    def __init__(self, **kwargs: Any) -> None:
        _log.debug(f"Zone.__init__ {kwargs}")
        super().__init__(**kwargs)

        if MANDITORY_LABEL:
            if "label" not in kwargs:
                raise RuntimeError("no label")
            if not kwargs["label"]:
                raise RuntimeError("empty label")

        # instantiate and associate all of the zone connection points
        self._zone_connection_points = {}
        for attr_name, attr_type in self._nodes.items():
            if inspect.isclass(attr_type) and issubclass(
                attr_type, ZoneConnectionPoint
            ):
                # build an instance of this connection point
                attr_element = attr_type(self, label=self.label + "." + attr_name)
                self._zone_connection_points[attr_name] = attr_element
                _log.debug(f"    - connection point {attr_name}: {attr_element}")

                setattr(self, attr_name, attr_element)


@multimethod
def connect_mm(from_system: System, to_zone: Zone) -> None:
    """System >> Zone"""
    _log.info(f"connect from {from_system} to {to_zone}")

    # stash this in the system
    from_system._serves_zones[to_zone.label] = to_zone

    # from_system._data_graph.add((from_system._node_iri, BRICK.feeds, to_zone._node_iri))
    # if INCLUDE_INVERSE:
    #     from_system._data_graph.add(
    #         (to_zone._node_iri, BRICK.isFedBy, from_system._node_iri)
    #     )

    # build a dict of mapped outlet connection points that are not
    # already connected, organized by medium
    from_out = defaultdict(set)
    for connection_point in from_system._boundary_connection_points:
        if connection_point.connectsThrough:
            continue
        if isinstance(connection_point, InletConnectionPoint):
            continue

        medium = getattr(connection_point, "hasMedium", None)
        from_out[medium].add(connection_point)

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    from_types: Set[Medium]
    from_types = set(medium for medium in from_out if len(from_out[medium]) == 1)
    if not from_types:
        raise RuntimeError(f"no candidate sources from {from_system} to {to_zone}")
    _log.debug(f"    - from_types: {from_types}")

    # build a dict of mapped inlet connection points that are not
    # already connected, organized by medium
    to_in = defaultdict(set)
    for attr, boundary_connection_point in to_zone._zone_connection_points.items():
        if isinstance(boundary_connection_point, OutletSystemConnectionPoint):
            continue
        connection_point = boundary_connection_point.mapsTo
        if not connection_point:
            continue
        if connection_point.connectsThrough:
            continue
        if isinstance(connection_point, OutletConnectionPoint):
            continue

        medium = getattr(connection_point, "hasMedium", None)
        to_in[medium].add(connection_point)

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    to_types: Set[Medium]
    to_types = set(medium for medium in to_in if len(to_in[medium]) == 1)
    if not to_types:
        raise RuntimeError(f"no candidate destinations from {from_system} to {to_zone}")
    _log.debug(f"    - to_types: {to_types}")

    # find compatible pairs
    pairs = set()
    for from_medium, to_medium in itertools.product(from_types, to_types):
        if validate_medium(from_medium, to_medium):
            pairs.add((from_medium, to_medium))
    if len(pairs) == 0:
        raise RuntimeError("no compatiable connection points")
    if len(pairs) > 1:
        raise RuntimeError("too many compatiable connection points")

    from_medium, to_medium = pairs.pop()
    from_connection_point = from_out[from_medium].pop()
    _log.debug(f"    - from_connection_point: {from_connection_point}")
    to_connection_point = to_in[to_medium].pop()
    _log.debug(f"    - to_connection_point: {to_connection_point}")

    # continue creating the connection
    connect_mm(from_connection_point, to_connection_point)

    from_system._data_graph.add(
        (from_system._node_iri, S223.servesZone, to_zone._node_iri)
    )
    if INCLUDE_INVERSE:
        from_system._data_graph.add(
            (to_zone._node_iri, S223.isServedBy, from_system._node_iri)
        )


@multimethod
def connect_mm(zone: Zone, connection: Connection) -> None:
    """Zone >> Connection"""
    _log.info(f"connect from {zone} to {connection}")

    if CONNECTION_HAS_MEDIUM:
        if not (connection_medium := getattr(connection, "hasMedium", None)):
            raise AttributeError(f"{connection} hasMedium")
        _log.debug(f"    - connection_medium: {connection_medium}")

    # build a dict of mapped outlet connection points that are not
    # already connected, organized by medium
    from_out = set()
    for attr, zone_connection_point in zone._zone_connection_points.items():
        if isinstance(zone_connection_point, InletSystemConnectionPoint):
            continue
        connection_point = zone_connection_point.mapsTo
        if not connection_point:
            continue
        if connection_point.connectsThrough:
            continue
        if isinstance(connection_point, InletConnectionPoint):
            continue

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
        if CONNECTION_HAS_MEDIUM:
            if validate_medium(medium, connection_medium):
                from_out.add(connection_point)
        else:
            from_out.add(connection_point)

    if len(from_out) > 1:
        raise RuntimeError("too many source connection points")

    # get the two connection points
    connection_point = from_out.pop()

    # continue the connection
    connect_mm(connection_point, connection)


class ZoneConnectionPoint(Node):
    """
    Zone Connection Point
    """

    _class_iri: URIRef = BOB.ZoneConnectionPoint
    _attr_uriref: Dict[str, URIRef] = {
        "mapsTo": BOB.mapsTo,
        "isZoneConnectionPointOf": BOB.isZoneConnectionPointOf,
    }
    hasMedium: Medium

    isZoneConnectionPointOf: Zone
    mapsTo: Node

    def __init__(self, zone: Zone, **kwargs: Any) -> None:
        _log.debug(f"ZoneConnectionPoint.__init__ {zone} {kwargs}")
        # abstract base class
        if self.__class__ is ZoneConnectionPoint:
            raise RuntimeError("ZoneConnectionPoint is an abstract base class")

        super().__init__(**kwargs)

        self._data_graph.add(
            (zone._node_iri, BOB.hasZoneConnectionPoint, self._node_iri)
        )
        if INCLUDE_INVERSE:
            self.isZoneConnectionPointOf = zone

        # this is one of the connection points of the zone
        zone._zone_connection_points[str(self._node_iri)] = self

    def maps_to(self, other: Union[Junction, ConnectionPoint]) -> None:
        """
        Maps this connection point to a domain space connection point.
        """
        _log.debug(f"ZoneConnectionPoint.maps_to {other}")
        if self.mapsTo:
            raise RuntimeError("zone connection point already mapped")

        if not isinstance(other, (Junction, ConnectionPoint)):
            raise TypeError("ConnectionPoint expected")

        self.mapsTo = other


@multimethod
def connect_mm(
    zone_connection_point: ZoneConnectionPoint, connection: Connection
) -> None:
    """ZoneConnectionPoint >> Connection"""
    raise NotImplementedError("ZoneConnectionPoint >> Connection")


@multimethod
def connect_mm(
    connection: Connection, zone_connection_point: ZoneConnectionPoint
) -> None:
    """Connection >> ZoneConnectionPoint"""
    raise NotImplementedError("Connection >> ZoneConnectionPoint")


@multimethod
def connect_mm(
    from_zone_connection_point: ZoneConnectionPoint,
    to_zone_connection_point: ZoneConnectionPoint,
) -> None:
    """ZoneConnectionPoint >> ZoneConnectionPoint"""
    _log.info(
        f"connect from {from_zone_connection_point} to {to_zone_connection_point}"
    )

    from_connection_point = from_zone_connection_point.mapsTo
    if not from_connection_point:
        raise RuntimeError(
            f"unmapped system connection point {from_zone_connection_point}"
        )

    to_connection_point = to_zone_connection_point.mapsTo
    if not to_connection_point:
        raise RuntimeError(
            f"unmapped system connection point {to_zone_connection_point}"
        )

    connect_mm(from_connection_point, to_connection_point)


class ZoneGroup(Container, Node):
    """
    A collection of zones.
    """

    _class_iri: URIRef = S223.ZoneGroup
    # hasDomain: Domain

    def __init__(self, **kwargs: Any) -> None:
        _log.debug(f"Zone.__init__ {kwargs}")
        super().__init__(**kwargs)

        if MANDITORY_LABEL:
            if "label" not in kwargs:
                raise RuntimeError("no label")
            if not kwargs["label"]:
                raise RuntimeError("empty label")


@multimethod
def contains_mm(zone_group: ZoneGroup, zone: Zone) -> None:
    """ZoneGroup > Zone"""
    _log.info(f"zone group {zone_group} contains zone {zone}")

    zone_group._data_graph.add((zone_group._node_iri, S223.hasZone, zone._node_iri))


class PhysicalSpace(Container, Node):
    """
    A part of the physical world whose 3D spatial extent is bounded.
    """

    _class_iri: URIRef = S223.PhysicalSpace


@multimethod
def contains_mm(parent_space: PhysicalSpace, child_space: PhysicalSpace) -> None:
    """PhysicalSpace > PhysicalSpace"""
    _log.info(f"physical space {parent_space} contains physical space {child_space}")

    parent_space._data_graph.add(
        (parent_space._node_iri, S223.contains, child_space._node_iri)
    )


@multimethod
def contains_mm(physical_space: PhysicalSpace, domain_space: DomainSpace) -> None:
    """PhysicalSpace > DomainSpace"""
    _log.info(f"physical space {physical_space} encloses {domain_space}")

    physical_space._data_graph.add(
        (physical_space._node_iri, S223.encloses, domain_space._node_iri)
    )


@multimethod
def contains_mm(physical_space: PhysicalSpace, thing_list: List[Node]) -> None:
    """PhysicalSpace >> List[Union[PhysicalSpace,DomainSpace]]"""
    _log.info(f"physical space {physical_space} contains/encloses list {thing_list}")

    ###TODO: the signature should be thing_list: List[Union[PhysicalSpace,DomainSpace]]

    for thing in thing_list:
        if not isinstance(thing, (PhysicalSpace, DomainSpace)):
            raise TypeError(f"Equipment or system expected: {thing}")
        contains_mm(physical_space, thing)


class Junction(Connectable):
    """
    Junction.
    """

    _class_iri: URIRef = S223.Junction
    hasMedium: Medium

    def __init__(self, **kwargs: Any) -> None:
        _log.debug(f"Junction.__init__ {kwargs}")
        super().__init__(**kwargs)

    def maps_to(self, other: ConnectionPoint) -> None:
        """
        Maps a junction to a connection point of enclosing equipment by
        creating an outlet connection point.
        """
        _log.info(f"map from {self} to {other}")

        if not isinstance(other, ConnectionPoint):
            raise TypeError("ConnectionPoint expected")
        if other.connectsThrough:
            raise RuntimeError("other connection point connected")

        # get the medium of the junction if it has one
        junction_medium = getattr(self, "hasMedium", None)
        other_medium = getattr(other, "hasMedium", None)

        if (not junction_medium) and (not other_medium):
            raise RuntimeError(f"medium required: {self} or {other}")

        if junction_medium:
            if not validate_medium(junction_medium, other_medium):
                raise RuntimeError(
                    f"incompatiable medium: {junction_medium} or {other_medium}"
                )
        else:
            self.hasMedium = other_medium

        # make a connection point matching the other
        connection_point = other.__class__(self)
        _log.debug(f"    - new connection point: {connection_point}")

        connection_point.mapsTo = other


@multimethod
def connect_mm(connectable: Connectable, junction: Junction) -> None:
    """Connectable >> Junction"""
    _log.info(f"connect from {connectable} to {junction}")

    # get the medium of the junction if it has one
    junction_medium = getattr(junction, "hasMedium", None)

    # build a dict of outlet connection points that are not already connected
    # organize them by medium
    from_out = defaultdict(set)
    for attr, connection_point in connectable._connection_points.items():
        if connection_point.connectsThrough:
            continue
        if not isinstance(connection_point, OutletConnectionPoint):
            continue

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
        if junction_medium:
            if not validate_medium(medium, junction_medium):
                continue
        from_out[medium].add(connection_point)

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    from_types: Set[Medium]
    from_types = set(medium for medium in from_out if len(from_out[medium]) == 1)
    if not from_types:
        raise RuntimeError(f"no candidate sources from {connectable} to {junction}")
    _log.debug(f"    - from_types: {from_types}")

    # build a dict of inlet connection points that are not already connected
    # organize them by medium
    to_in = defaultdict(set)
    for attr, connection_point in junction._connection_points.items():
        if connection_point.connectsThrough:
            continue
        if not isinstance(connection_point, InletConnectionPoint):
            continue

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
        to_in[medium].add(connection_point)

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    to_types: Set[Medium]
    to_types = set(medium for medium in to_in if len(to_in[medium]) == 1)
    if not to_types:
        if len(from_types) > 1:
            raise RuntimeError("too many possible connection points")

        # get the type without removing it
        for medium in from_types:
            break

        connection_point = InletConnectionPoint(junction, hasMedium=medium)
        _log.debug(f"    - new inlet connection point: {connection_point}")

        # lock down the junction to the medium
        if not junction_medium:
            junction.hasMedium = medium

        # this is now available
        to_types.add(medium)
        to_in[medium].add(connection_point)

    # find compatible pairs
    pairs = set()
    for from_medium, to_medium in itertools.product(from_types, to_types):
        if validate_medium(from_medium, to_medium):
            pairs.add((from_medium, to_medium))
    if len(pairs) == 0:
        raise RuntimeError("no compatiable connection points")
    if len(pairs) > 1:
        raise RuntimeError("too many compatiable connection points")

    from_medium, to_medium = pairs.pop()
    from_connection_point = from_out[from_medium].pop()
    _log.debug(f"    - from_connection_point: {from_connection_point}")
    to_connection_point = to_in[to_medium].pop()
    _log.debug(f"    - to_connection_point: {to_connection_point}")

    # continue creating the connection
    connect_mm(from_connection_point, to_connection_point)


@multimethod
def connect_mm(junction: Junction, connectable: Connectable) -> None:
    """Junction >> Connectable"""
    _log.info(f"connect from {junction} to {connectable}")

    # get the medium of the junction if it has one
    junction_medium = getattr(junction, "hasMedium", None)
    _log.debug(f"    - junction_medium: {junction_medium}")

    # build a dict of outlet connection points that are not already connected
    # organize them by medium
    from_out = defaultdict(set)
    for attr, connection_point in junction._connection_points.items():
        if connection_point.connectsThrough:
            continue
        if not isinstance(connection_point, OutletConnectionPoint):
            continue

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
        from_out[medium].add(connection_point)

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    from_types: Set[Medium]
    from_types = set(medium for medium in from_out if len(from_out[medium]) == 1)
    _log.debug(f"    - from_types: {from_types}")

    # build a dict of inlet connection points that are not already connected
    # organize them by medium
    to_in = defaultdict(set)
    for attr, connection_point in connectable._connection_points.items():
        if connection_point.connectsThrough:
            continue
        if not isinstance(connection_point, InletConnectionPoint):
            continue

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
        if junction_medium:
            if not validate_medium(medium, junction_medium):
                continue
        to_in[medium].add(connection_point)

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    to_types: Set[Medium]
    to_types = set(medium for medium in to_in if len(to_in[medium]) == 1)
    if not to_types:
        raise RuntimeError(
            f"no candidate destinations from {junction} to {connectable}"
        )

    if not from_types:
        if len(to_types) > 1:
            raise RuntimeError("too many possible connection points")

        # get the type without removing it
        for medium in to_types:
            break

        connection_point = OutletConnectionPoint(junction, hasMedium=medium)
        _log.debug(f"    - new outlet connection point: {connection_point}")

        # lock down the junction to the medium
        if not junction_medium:
            junction.hasMedium = medium

        # this is now available
        from_types.add(medium)
        from_out[medium].add(connection_point)

    # find compatible pairs
    pairs = set()
    for from_medium, to_medium in itertools.product(from_types, to_types):
        if validate_medium(from_medium, to_medium):
            pairs.add((from_medium, to_medium))
    if len(pairs) == 0:
        raise RuntimeError("no compatiable connection points")
    if len(pairs) > 1:
        raise RuntimeError("too many compatiable connection points")

    from_medium, to_medium = pairs.pop()
    from_connection_point = from_out[from_medium].pop()
    _log.debug(f"    - from_connection_point: {from_connection_point}")
    to_connection_point = to_in[to_medium].pop()
    _log.debug(f"    - to_connection_point: {to_connection_point}")

    # continue creating the connection
    connect_mm(from_connection_point, to_connection_point)


@multimethod
def connect_mm(junction: Junction, to_things: List[Connectable]) -> None:
    """Junction >> [Connectable]"""
    _log.info(f"connect from {junction} to {to_things}")

    # get the medium of the junction if it has one
    junction_medium = getattr(junction, "hasMedium", None)
    _log.debug(f"    - junction_medium: {junction_medium}")

    # build a dict of outlet connection points that are not already connected
    # organize them by medium
    from_out = defaultdict(set)
    for attr, connection_point in junction._connection_points.items():
        if connection_point.connectsThrough:
            continue
        if not isinstance(connection_point, OutletConnectionPoint):
            continue

        medium = getattr(connection_point, "hasMedium", None)
        from_out[medium].add(connection_point)

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    from_types: Set[Medium]
    from_types = set(medium for medium in from_out if len(from_out[medium]) == 1)
    _log.debug(f"    - from_types: {from_types}")

    to_types_list: List[Set[Medium]] = []

    for to_thing in to_things:
        # build a dict of inlet connection points that are not already connected
        # organize them by medium
        to_in = defaultdict(set)
        for attr, connection_point in to_thing._connection_points.items():
            if connection_point.connectsThrough:
                continue
            if not isinstance(connection_point, InletConnectionPoint):
                continue

            medium = getattr(connection_point, "hasMedium", None)
            to_in[medium].add(connection_point)

        # filter them to a set where there is only one for that medium so it
        # would be unambiguous to use it
        to_types: Set[Medium]
        to_types = set(medium for medium in to_in if len(to_in[medium]) == 1)
        if not to_types:
            raise RuntimeError(f"no candidate destinations to {to_thing}")
        _log.debug(f"    - to_types: {to_types}")
        to_types_list.append(to_types)

    if not from_types:
        if len(to_types) > 1:
            raise RuntimeError("too many possible connection point types")

        # get the type without removing it
        for medium in to_types:
            break

        connection_point = OutletConnectionPoint(junction, hasMedium=medium)
        _log.debug(f"    - new outlet connection point: {connection_point}")

        # lock down the junction to the medium
        if not junction_medium:
            junction.hasMedium = medium

        # this is now available
        from_types.add(medium)
        from_out[medium].add(connection_point)

    # find the common medium
    common_types = from_types.intersection(*to_types_list)
    if not common_types:
        raise RuntimeError("no common connection types")
    if len(common_types) > 1:
        raise RuntimeError("too many common connection types")
    medium = common_types.pop()
    _log.debug(f"    - medium: {medium}")

    # get from connection point
    from_connection_point = from_out[medium].pop()

    # create a connection
    if CONNECTION_HAS_MEDIUM:
        connection = Connection(hasMedium=medium)
    else:
        connection = Connection()

    # connect the from thing
    connect_mm(from_connection_point, connection)

    # connect the to things
    for to_thing in to_things:
        connect_mm(connection, to_thing)


@multimethod
def connect_mm(from_connection_point: ConnectionPoint, junction: Junction) -> None:
    """ConnectionPoint >> Junction"""
    _log.info(f"connect from {from_connection_point} to {junction}")

    # get the medium of the connection point
    if not (medium := getattr(from_connection_point, "hasMedium", None)):
        raise RuntimeError(f"medium required: {from_connection_point}")
    from_types = set([medium])

    # get the medium of the junction if it has one
    junction_medium = getattr(junction, "hasMedium", None)
    if junction_medium:
        if not validate_medium(medium, junction_medium):
            raise RuntimeError(f"incompatible medium: {medium}, {junction_medium}")

    # build a dict of inlet connection points that are not already connected
    # organize them by medium
    to_in = defaultdict(set)
    for attr, connection_point in junction._connection_points.items():
        if connection_point.connectsThrough:
            continue
        if not isinstance(connection_point, InletConnectionPoint):
            continue

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
        to_in[medium].add(connection_point)

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    to_types: Set[Medium]
    to_types = set(medium for medium in to_in if len(to_in[medium]) == 1)
    if not to_types:
        connection_point = InletConnectionPoint(junction, hasMedium=medium)
        _log.debug(f"    - new inlet connection point: {connection_point}")

        # lock down the junction to the medium
        if not junction_medium:
            junction.hasMedium = medium

        # this is now available
        to_types.add(medium)
        to_in[medium].add(connection_point)

    # find compatible pairs
    pairs = set()
    for from_medium, to_medium in itertools.product(from_types, to_types):
        if validate_medium(from_medium, to_medium):
            pairs.add((from_medium, to_medium))
    if len(pairs) == 0:
        raise RuntimeError("no compatiable connection points")
    if len(pairs) > 1:
        raise RuntimeError("too many compatiable connection points")

    from_medium, to_medium = pairs.pop()
    to_connection_point = to_in[to_medium].pop()
    _log.debug(f"    - to_connection_point: {to_connection_point}")

    # continue creating the connection
    connect_mm(from_connection_point, to_connection_point)


@multimethod
def connect_mm(junction: Junction, to_connection_point: ConnectionPoint) -> None:
    """Junction >> ConnectionPoint"""
    _log.info(f"connect from {junction} to {to_connection_point}")

    # get the medium of the connection point
    if not (medium := getattr(to_connection_point, "hasMedium", None)):
        raise RuntimeError(f"medium required: {to_connection_point}")
    to_types = set([medium])

    # get the medium of the junction if it has one
    junction_medium = getattr(junction, "hasMedium", None)
    if junction_medium:
        if not validate_medium(medium, junction_medium):
            raise RuntimeError(f"incompatible medium: {medium}, {junction_medium}")

    # build a dict of outlet connection points that are not already connected
    # organize them by medium
    from_out = defaultdict(set)
    for attr, connection_point in junction._connection_points.items():
        if connection_point.connectsThrough:
            continue
        if not isinstance(connection_point, OutletConnectionPoint):
            continue

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
        from_out[medium].add(connection_point)

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    from_types: Set[Medium]
    from_types = set(medium for medium in from_out if len(from_out[medium]) == 1)
    if not from_types:
        connection_point = OutletConnectionPoint(junction, hasMedium=medium)
        _log.debug(f"    - new outlet connection point: {connection_point}")

        # lock down the junction to the medium
        if not junction_medium:
            junction.hasMedium = medium

        # this is now available
        from_types.add(medium)
        from_out[medium].add(connection_point)

    # find compatible pairs
    pairs = set()
    for from_medium, to_medium in itertools.product(from_types, to_types):
        if validate_medium(from_medium, to_medium):
            pairs.add((from_medium, to_medium))
    if len(pairs) == 0:
        raise RuntimeError("no compatiable connection points")
    if len(pairs) > 1:
        raise RuntimeError("too many compatiable connection points")

    from_medium, to_medium = pairs.pop()
    from_connection_point = from_out[from_medium].pop()
    _log.debug(f"    - from_connection_point: {from_connection_point}")

    # continue creating the connection
    connect_mm(from_connection_point, to_connection_point)


class Equipment(Container, Connectable):
    """
    A Equipment is normally a physical entity that one might buy from a vendor - a tangible object designed to accomplish a specific task.
    """

    _class_iri: URIRef = S223.Equipment
    # hasContextualRoleShape: Any
    # hasPropertyShape: Any
    # hasRole: Set # set of enumerationKind
    hasPhysicalLocation: PhysicalSpace

    def __init__(self, config: Dict[str, Any] = {}, *args, **kwargs: Any) -> None:
        _log.debug(f"Equipment.__init__ {config} {args} {kwargs}")

        # if there are "params" in the configuation, use those as defaults for
        # kwargs and allow them to be overriden by additional kwargs
        # if config and "params" in config:
        #     kwargs = {**config["params"], **kwargs}

        # When passing kwargs to create an instance of a class, some datatype
        # are not yet visible in the chain of creation. This lead to
        # ex. TypeError: unexpected keyword argument: waterInlet
        # By removing properties and connection points from kwargs and explicitly
        # putting them in config, it should be better
        _role = kwargs.pop("hasRole", None)
        _config = dict(config.items())
        for attr_name, attr_value in kwargs.copy().items():
            if inspect.isclass(attr_value):
                # if issubclass(attr_value, Property):
                #    config["properties"] = (
                #        {**config["properties"], **{attr_name: kwargs.pop(attr_name)}}
                #        if "properties" in config.keys()
                #        else {attr_name: kwargs.pop(attr_name)}
                #    )
                if issubclass(attr_value, ConnectionPoint):
                    _config["cp"] = (
                        {**_config["cp"], **{attr_name: kwargs.pop(attr_name)}}
                        if "cp" in _config.keys()
                        else {attr_name: kwargs.pop(attr_name)}
                    )

        if MANDITORY_LABEL:
            if "label" not in kwargs:
                raise RuntimeError("no label")
            if not kwargs["label"]:
                raise RuntimeError("empty label")

        super().__init__(*args, **kwargs)

        self.hasRole = set()
        self.hasSystemType = set()
        if _role:
            self += _role

        if _config:
            for group_name, group_items in _config.items():
                if group_name in ("params", "relations"):
                    continue
                if group_name == "cp":
                    for thing_name, thing_class in group_items.items():
                        setattr(
                            self,
                            thing_name,
                            thing_class(self, label=f"{self.label}.{thing_name}"),
                        )
                    continue
                things = []
                for (thing_name, thing_class), thing_kwargs in group_items.items():
                    if thing_name in self:
                        raise ValueError(f"label already used: {self[thing_name]}")
                    thing = thing_class(label=thing_name, **thing_kwargs)

                    if isinstance(thing, (Equipment, System, _Sensor, _Producer)):
                        self > thing
                    if isinstance(thing, Property):
                        self[thing_name] = thing
                        self.add_property(thing)

                    things.append(thing)

                setattr(self, "_" + group_name, things)

    def __iadd__(self, role: EnumerationKind) -> Node:
        """
        Add a role to an equipment
        """
        add_mm(self, role)
        return self

    def set_medium(self, cps: List[str] = None, medium: Medium = None):
        """
        Set the medium of the connection points of the equipment. This allows creating
        basics equipment with connection points and then set the medium of the connection
        """
        if cps is None:
            raise ValueError("List of connection Points is required")
        if medium is None:
            raise ValueError("Medium is required")
        for each in cps:
            if medium in self[each].hasMedium._children:
                self[each].hasMedium = medium
                self[each]._data_graph.set(
                    (self[each]._node_iri, S223.hasMedium, medium._node_iri)
                )
            else:
                raise ValueError(f"Incompatible medium {medium} for {each}")


@multimethod
def add_mm(equipment: Equipment, info: EnumerationKind) -> None:
    """
    Add a role to an equipment
    """
    if info in Role._children:
        role = info
        _log.info(f"add role {role} to {equipment}")
        equipment.hasRole.add(role)
        equipment._data_graph.add((equipment._node_iri, S223.hasRole, role._node_iri))
        if INCLUDE_INVERSE:
            role.isRoleOf = equipment


@multimethod
def contains_mm(parent_equipment: Equipment, child_equipment: Equipment) -> None:
    """Equipment > Equipment"""
    _log.info(f"equipment {parent_equipment} contains equipment {child_equipment}")

    parent_equipment._data_graph.add(
        (parent_equipment._node_iri, S223.contains, child_equipment._node_iri)
    )


@multimethod
def contains_mm(parent_equipment: Equipment, equipment_list: List[Equipment]) -> None:
    """Equipment > List[Equipment]"""
    _log.info(f"equipment {parent_equipment} contains other equipment {equipment_list}")

    for child_equipment in equipment_list:
        if not isinstance(child_equipment, Equipment):
            raise RuntimeError(f"equipment expected: {child_equipment}")
        contains_mm(parent_equipment, child_equipment)


@multimethod
def contains_mm(parent_equipment: Equipment, child_junction: Junction) -> None:
    """Equipment > Junction"""
    _log.info(f"equipment {parent_equipment} contains junction {child_junction}")

    parent_equipment._data_graph.add(
        (parent_equipment._node_iri, S223.contains, child_junction._node_iri)
    )


class _Sensor(Equipment):
    """
    Placeholder to prevent circular reference, actual class definition in
    the bob.sensor.sensor module.

    I also need that so __matmul__ work when relating sensor to their property.
    """

    _class_iri: URIRef = None


@multimethod
def contains_mm(equipment: Equipment, sensor: _Sensor) -> None:
    """Equipment > Sensor"""
    _log.info(f"equipment {equipment} contains sensor {sensor}")

    equipment._data_graph.add((equipment._node_iri, S223.contains, sensor._node_iri))


class _Producer(Container, Node):
    """
    Placeholder to prevent circular reference, actual class definition in
    the bob.producer module.
    """

    _class_iri: URIRef = None


@multimethod
def contains_mm(parent_equipment: Equipment, child_producer: _Producer) -> None:
    """Equipment > Producer"""
    _log.info(f"Equipment {parent_equipment} contains Producer {child_producer}")

    parent_equipment._data_graph.add(
        (parent_equipment._node_iri, BOB.contains, child_producer._node_iri)
    )


class DomainSpace(Connectable):
    """
    A part of the physical world or a virtual world whose 3D spatial extent is
    bounded actually or theoretically, and provides for certain functions
    within the zone it is contained in.
    """

    _class_iri: URIRef = S223.DomainSpace
    hasDomain: Domain

    def __init__(self, **kwargs: Any) -> None:
        _log.debug(f"DomainSpace.__init__ {kwargs}")
        super().__init__(**kwargs)


@multimethod
def contains_mm(zone: Zone, domain_space: DomainSpace) -> None:
    """Zone > DomainSpace"""
    _log.info(f"zone {zone} contains domain space {domain_space}")

    zone._data_graph.add((zone._node_iri, S223.hasDomainSpace, domain_space._node_iri))


@multimethod
def contains_mm(zone: Zone, domain_spaces: List[DomainSpace]) -> None:
    """Zone > List[DomainSpace]"""
    _log.info(f"zone {zone} contains domain spaces {domain_spaces}")

    for domain_space in domain_spaces:
        contains_mm(zone, domain_space)


@multimethod
def connect_mm(domain_space: DomainSpace, connection_point: ConnectionPoint) -> None:
    """DomainSpace >> ConnectionPoint"""
    _log.info(f"connect from {domain_space} to {connection_point}")
    raise NotImplementedError("DomainSpace >> ConnectionPoint")

    if connection_point.connectsThrough:
        raise RuntimeError("connection point already connected")
    to_medium = getattr(connection_point, "hasMedium", None)
    _log.debug(f"    - to_medium: {to_medium}")

    # build a dict of outlet connection points that are not already connected
    # that have the same medium
    from_out = set()
    for attr, cp in domain_space._connection_points.items():
        if connection_point.connectsThrough:
            continue
        if isinstance(cp, InletConnectionPoint):
            continue

        medium = getattr(cp, "hasMedium", None)
        if medium == to_medium:
            from_out.add(cp)
    _log.debug(f"    - from_out: {from_out}")

    if not from_out:
        raise RuntimeError(
            f"no candidate sources from {domain_space} to {connection_point}"
        )
    if len(from_out) > 1:
        raise RuntimeError("too many connection points")
    from_thing = from_out.pop()
    _log.debug(f"    - from_thing: {from_thing}")

    connect_mm(from_thing, connection_point)


#
#   Direction EnumerationKind Instances
#

Direction = EnumerationKind("Direction")
_log.debug("Direction: %r", Direction)

Inlet = Direction("Inlet")
Outlet = Direction("Outlet")
Bidirectional = Direction("Bidirectional")

#
#   Direction Specific Connection Points
#


class InletConnectionPoint(ConnectionPoint):
    _class_iri: URIRef = S223.InletConnectionPoint


class OutletConnectionPoint(ConnectionPoint):
    _class_iri: URIRef = S223.OutletConnectionPoint


class BidirectionalConnectionPoint(ConnectionPoint):
    _class_iri: URIRef = S223.BidirectionalConnectionPoint


#
#   Direction Specific Zone Connection Points
#


class InletZoneConnectionPoint(ZoneConnectionPoint):
    _class_iri: URIRef = BOB.InletZoneConnectionPoint


class OutletZoneConnectionPoint(ZoneConnectionPoint):
    _class_iri: URIRef = BOB.OutletZoneConnectionPoint


class BidirectionalZoneConnectionPoint(ZoneConnectionPoint):
    _class_iri: URIRef = BOB.BidirectionalZoneConnectionPoint


def validate_medium(from_medium, to_medium):
    # print(from_medium, to_medium)
    if (
        (
            from_medium not in to_medium._children
            and to_medium not in from_medium._children
        )
        and not (
            from_medium in to_medium._constituents
            or to_medium in from_medium._constituents
        )
        and not (
            any(
                element in to_medium._constituents
                for element in from_medium._constituents
            )
        )
    ):
        return False
    else:
        return True
