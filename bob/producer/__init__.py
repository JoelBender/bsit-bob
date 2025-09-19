"""
Producers

This is an adaptation of the S223 Function Blocks
"""

from __future__ import annotations

import inspect
import logging
from typing import Any, AnyStr, Dict

from rdflib import Literal, URIRef  # type: ignore

from ..core import (
    BOB,
    G36,
    INCLUDE_INVERSE,
    P223,
    S223,
    Container,
    Equipment,
    LocationReference,
    Node,
    Property,
    _Producer,
    data_graph,
)
from ..equipment.control import AnalogInput, AnalogOutput, BinaryInput, BinaryOutput
from ..functions import Function, FunctionInput, FunctionOutput
from ..multimethods import multimethod
from ..template import template_update

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = BOB


class old_Producer(Container, Node):
    "Placeholder to prevent circular reference"
    _class_iri: URIRef = P223.Producer

    def __init__(self, config: Dict[str, Any] = {}, *args, **kwargs: Any) -> None:
        _log.debug(f"Producer.__init__ {config} {args} {kwargs}")

        # if there are "params" in the configuation, use those as defaults for
        # kwargs and allow them to be overriden by additional kwargs
        # if config and "params" in config:
        #     kwargs = {**config["params"], **kwargs}

        # When passing kwargs to create an instance of a class, some datatype
        # are not yet visible in the chain of creation. This lead to
        # ex. TypeError: unexpected keyword argument: waterInlet
        # By removing properties and connection points from kwargs and explicitly
        # putting them in config, it should be better
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
                    # Beware here... _Producer are function Block so...FB in and out only....
                    _config["cp"] = (
                        {**_config["cp"], **{attr_name: kwargs.pop(attr_name)}}
                        if "cp" in _config.keys()
                        else {attr_name: kwargs.pop(attr_name)}
                    )

        super().__init__(*args, **kwargs)

        if _config:
            for group_name, group_items in _config.items():
                if group_name == "params":
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

                    if isinstance(thing, (_Producer)):
                        self > thing
                    if isinstance(thing, Property):
                        self[thing_name] = thing
                        self.add_property(thing)

                    things.append(thing)

                setattr(self, "_" + group_name, things)


@multimethod
def contains_mm(producer: Producer, sub_producer: _Producer) -> None:
    """Producer > Producer"""
    _log.info(f"producer {producer} contains producer {sub_producer}")

    producer._data_graph.add((producer._node_iri, BOB.contains, sub_producer._node_iri))


#
#   Function Inputs and Outputs
#


class ProducerInput(Node):
    _class_iri: URIRef = P223.ProducerInput
    hasCauseLocation: LocationReference

    def __init__(self, function_block: Producer, **kwargs: Any) -> None:
        _log.debug(
            f"ProducerInput({self.__class__.__name__}).__init__ {function_block} {kwargs}"
        )

        super().__init__(**kwargs)

        data_graph.add((function_block._node_iri, S223.hasInput, self._node_iri))

    def __rshift__(self, other: Any) -> Any:
        """Build a connection from this thing to another thing."""
        connect_mm(self, other)
        return other

    def __lshift__(self, other: Any) -> Any:
        """Build a connection to this thing from another thing."""
        connect_mm(other, self)
        return self


class ProducerOutput(Node):
    _class_iri: URIRef = P223.ProducerOutput
    hasEffectLocation: LocationReference

    def __init__(self, function_block: Producer, **kwargs: Any) -> None:
        _log.debug(
            f"ProducerOutput({self.__class__.__name__}).__init__ {function_block} {kwargs}"
        )

        super().__init__(**kwargs)

        data_graph.add((function_block._node_iri, S223.hasOutput, self._node_iri))

    def add_hasEffectLocation(self, node: Node) -> None:
        # Must be from a sensor
        self.hasEffectLocation = node

        # link the two together
        self._data_graph.add((self._node_iri, P223.hasEffectLocation, node._node_iri))
        if INCLUDE_INVERSE:
            node.isEffectLocationOf = self

    def __rshift__(self, other: Any) -> Any:
        """Build a connection from this thing to another thing."""
        connect_mm(self, other)
        return other

    def __lshift__(self, other: Any) -> Any:
        """Build a connection to this thing from another thing."""
        connect_mm(other, self)
        return self

    def __mod__(self, other: Node) -> Node:
        """This producer output has effect location on other node."""
        _log.debug(f"Container.__mod__ {self} % {other}")

        self.add_hasEffectLocation(other)
        return self


@multimethod
def connect_mm(
    output_connector: ProducerOutput, input_connector: ProducerInput
) -> None:
    """ProducerOutput >> ProducerInput"""
    _log.info(f"connect from {output_connector} to {input_connector}")

    data_graph.add(
        (output_connector._node_iri, S223.connect, input_connector._node_iri)
    )


@multimethod
def connect_mm(prop: Property, input_connector: ProducerInput) -> None:
    """Property >> ProducerInput"""
    _log.info(f"connect from {prop} to {input_connector}")

    data_graph.add((input_connector._node_iri, S223.uses, prop._node_iri))


@multimethod
def connect_mm(output_connector: ProducerOutput, prop: Property) -> None:
    """ProducerOutput >> Property"""
    _log.info(f"connect from {output_connector} to {prop}")

    data_graph.add((output_connector._node_iri, S223.produces, prop._node_iri))


@multimethod
def connect_mm(output_connector: ProducerOutput, cp: AnalogOutput) -> None:
    """ProducerOutput >> Property"""
    _log.info(f"connect from {output_connector} to {cp}")

    data_graph.add((cp._node_iri, P223.hasProducerOutput, output_connector._node_iri))


@multimethod
def connect_mm(output_connector: ProducerOutput, cp: BinaryOutput) -> None:
    """ProducerOutput >> Controller connection point"""
    _log.info(f"connect from {output_connector} to {cp}")

    data_graph.add((cp._node_iri, P223.hasProducerOutput, output_connector._node_iri))


@multimethod
def connect_mm(output_connector: ProducerOutput, cp: AnalogOutput) -> None:
    """ProducerOutput >> Controller connection point"""
    _log.info(f"connect from {output_connector} to {cp}")

    data_graph.add((cp._node_iri, P223.hasProducerOutput, output_connector._node_iri))


#
#   Connector types, parameters, and constants
#


class G36AnalogInput(FunctionInput):
    _class_iri: URIRef = G36.AnalogInput


class G36AnalogOutput(FunctionOutput):
    _class_iri: URIRef = G36.AnalogOutput


class G36DigitalInput(FunctionInput):
    _class_iri: URIRef = G36.DigitalInput


class G36DigitalOutput(FunctionOutput):
    _class_iri: URIRef = G36.DigitalOutput


#
#   Producer
#


class Producer(_Producer):
    """
    Producers are black boxes representing causality.
    Their inputs are causes and they produce an effect on a property
    It is very similar to a function, but it is meant to show the relation
    between an input and an output of something not-driven by an algorithm.
    A common example would be a relay. You feed it voltage and the relay contact
    is actuated.
    """

    _class_iri: URIRef = P223.Producer

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}

        _log.debug(f"Producer.__init__ {kwargs}")

        # resolve annotations if necessary
        if not self._resolved:
            self._resolve_annotations()
        _log.debug("    - continue Producer.__init__")

        # pull out the inputs and outputs
        connector_inits: Dict[str, Any] = {}
        for attr_name, attr_type in self._nodes.items():
            if inspect.isclass(attr_type) and (attr_name in kwargs):
                if issubclass(attr_type, (ProducerInput, ProducerOutput)):
                    connector_inits[attr_name] = kwargs.pop(attr_name)
        _log.debug(f"    - connector_inits: {connector_inits}")
        _log.debug(f"    - remaining kwargs: {kwargs}")

        # continue with initialization
        # super().__init__(_config, **kwargs)
        super().__init__(**kwargs)

        # instantiate and associate all of the connectors
        self._connectors = {}
        for attr_name, attr_type in self._nodes.items():
            if not inspect.isclass(attr_type):
                continue

            if issubclass(attr_type, (ProducerInput, ProducerOutput)):
                # build an instance of this connector
                attr_element = attr_type(self, label=self.label + "." + attr_name)
                self._connectors[attr_name] = attr_element
                _log.debug(f"    - connector {attr_name}: {attr_element}")

                if attr_name in connector_inits:
                    _log.debug(f"        - init: {connector_inits[attr_name]}")
                    if issubclass(attr_type, ProducerInput):
                        connector_inits[attr_name] >> attr_element
                    if issubclass(attr_type, ProducerOutput):
                        attr_element >> connector_inits[attr_name]

                setattr(self, attr_name, attr_element)

        if _config:
            for group_name, group_items in _config.items():
                if group_name == "params":
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

                    if isinstance(thing, Producer):
                        self > thing
                    if isinstance(thing, Property):
                        self[thing_name] = thing
                        self.add_property(thing)

                    things.append(thing)

                setattr(self, "_" + group_name, things)

    def uses(
        self,
        prop: Property,
        klass: ProducerInput = ProducerInput,
        label: AnyStr = "input",
    ) -> None:
        connector = klass(self, label=f"{self.label}.{label}")
        setattr(self, label, connector)
        prop >> connector

    def produces(
        self,
        prop: Property,
        klass: ProducerOutput = ProducerOutput,
        label: AnyStr = "output",
    ) -> None:
        connector = klass(self, label=f"{self.label}.{label}")
        setattr(self, label, connector)
        connector >> prop


@multimethod
def contains_mm(producer: Producer, sub_producer: Producer) -> None:
    """Producer > Producer"""
    _log.info(f"producer {producer} contains producer {sub_producer}")

    producer._data_graph.add((producer._node_iri, BOB.contains, sub_producer._node_iri))


@multimethod
def contains_mm(equipment: Equipment, producer: Producer) -> None:
    """Equipment > Producer"""
    _log.info(f"equipment {equipment} contains producer {producer}")

    producer._data_graph.add((equipment._node_iri, BOB.contains, producer._node_iri))
