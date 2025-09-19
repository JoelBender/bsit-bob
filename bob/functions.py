"""
Function Blocks
"""

from __future__ import annotations

import inspect
import logging
from datetime import datetime
from typing import Any, AnyStr, Dict

from rdflib import URIRef  # type: ignore

from .core import (
    G36,
    S223,
    Node,
    Property,
    PropertyReference,
    data_graph,
)
from .template import template_update

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = S223


class FunctionInput(PropertyReference):
    def __new__(cls, arg: Any = None, **kwargs) -> Any:
        _log.debug(f"FunctionInput.__new__ {cls} {arg} {kwargs}")
        if (arg is None) or (arg == ()):
            return Property(**kwargs)
        if isinstance(arg, Property):
            return arg
        if isinstance(arg, (int, float, str, datetime)):
            return Property(arg, **kwargs)

        raise TypeError(f"property expected: {arg}")


class FunctionOutput(PropertyReference):
    def __new__(cls, arg: Any = None, **kwargs) -> Any:
        _log.debug(f"FunctionOutput.__new__ {cls} {arg} {kwargs}")
        if (arg is None) or (arg == ()):
            return Property(**kwargs)
        if isinstance(arg, Property):
            return arg
        if isinstance(arg, (int, float, str, datetime)):
            return Property(arg, **kwargs)

        raise TypeError(f"property expected: {arg}")


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


class Function(Node):
    """
    Function blocks are black boxes representing a sequence or an
    algorithm. Function blocks use inputs and produce outputs that are
    related to observable and actuatable properties.
    Functions are executed by a s223:Contoller.
    """

    _class_iri: URIRef = S223.Function

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.debug(f"Function.__init__ {kwargs}")

        if not self._resolved:
            self._resolve_annotations()
        _log.debug("    - continue Function.__init__")

        # super().__init__(_config, **kwargs)
        super().__init__(**kwargs)

        # instantiate and associate all of the inputs and outputs
        for attr_name, attr_type in self._nodes.items():
            if not inspect.isclass(attr_type):
                continue
            if not issubclass(attr_type, (FunctionInput, FunctionOutput)):
                continue

            # check if an instance was passed as a kwarg, if it was then
            # the attribute element will be a node and has its _node_iri
            attr_element = getattr(self, attr_name, None)
            if attr_element is None:
                continue

            # if this is used as a function input/output, make it so
            if issubclass(attr_type, FunctionInput):
                data_graph.add((self._node_iri, S223.hasInput, attr_element._node_iri))
                # data_graph.add(
                #     (attr_element._node_iri, RDF.type, S223.FunctionInput)
                # )
            elif issubclass(attr_type, FunctionOutput):
                data_graph.add((self._node_iri, S223.hasOutput, attr_element._node_iri))
                # data_graph.add(
                #     (attr_element._node_iri, RDF.type, S223.FunctionOutput)
                # )

    def __setattr__(self, attr: str, value: Any) -> None:
        """
        .
        """
        # do the normal things
        super().__setattr__(attr, value)

        # if this is a node, double check the type
        attr_type = self._nodes.get(attr, None)
        _log.debug("    - attr_type: %r", attr_type)
        if not attr_type:
            return

        _log.debug(f"Function.__setattr__ {attr} {value}")

        # get the element after it has been set, it will be an instance of
        # attr_type which might not be the value
        attr_element = vars(self).get(attr)
        _log.debug("    - attr_element: %r", attr_element)

        # if this is used as a function input/output, make it so
        if issubclass(attr_type, FunctionInput):
            data_graph.add((self._node_iri, S223.hasInput, attr_element._node_iri))
            # data_graph.add(
            #     (attr_element._node_iri, RDF.type, S223.FunctionInput)
            # )
        elif issubclass(attr_type, FunctionOutput):
            data_graph.add((self._node_iri, S223.hasOutput, attr_element._node_iri))
            # data_graph.add(
            #     (attr_element._node_iri, RDF.type, S223.FunctionOutput)
            # )

    def uses(
        self,
        prop: Property,
        klass: FunctionInput = FunctionInput,
        label: AnyStr = "input",
    ) -> None:
        connector = klass(self, label=f"{self.label}.{label}")
        setattr(self, label, connector)
        prop >> connector

    def produces(
        self,
        prop: Property,
        klass: FunctionOutput = FunctionOutput,
        label: AnyStr = "output",
    ) -> None:
        connector = klass(self, label=f"{self.label}.{label}")
        setattr(self, label, connector)
        connector >> prop
