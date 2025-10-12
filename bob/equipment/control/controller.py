from typing import Dict, Optional

from rdflib import URIRef

from ...core import (
    P223,
    S223,
    Equipment,
    data_graph,
    logging,
)
from ...functions import Function
from ...template import template_update

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = P223

# empty, because other equipments can be defined as controller
# and I don't want them to inherit from example properties
controller_template: dict[str, dict[str, dict]] = {
    "cp": {},
    "properties": {},
}

class Controller(Equipment):
    """A controller executes function blocks and connect to other Equipment
    through different connection points (AI, AO, BI, BO)
    """

    _class_iri: URIRef = S223.Controller

    def __init__(self, config: dict | None = None, **kwargs):
        _config = template_update(controller_template, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.debug(f"Controller.__init__ {_config} {kwargs}")

        super().__init__(config=_config, **kwargs)

    def executes(self, function_block: Function):
        _log.debug(f"Controller {self._node_iri} executes  {function_block._node_iri}")
        data_graph.add((self._node_iri, S223.executes, function_block._node_iri))
