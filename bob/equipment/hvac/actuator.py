import logging
from typing import Dict, Optional

from ...core import S223, Equipment, Property
from ...template import configure_relations, template_update

# logging
_log = logging.getLogger(__name__)

_namespace = S223

"""
 
__|___|__|___|___|__                                                                                  
|     Actuator     |------------s223:actuates-------------------> A (s223:Equipment)                                   
|  s223:Equipment  |------------s223:actuatedByProperty---------> B (s223:Property)
|                  |
|                  |
|__________________|

"""


class Actuator(Equipment):
    _class_iri = S223.Actuator
    actuates: Equipment

    def __init__(self, config: dict | None = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.info(f"Actuator.__init__ {_config} {kwargs}")
        _relations = _config.pop("relations", [])
        super().__init__(config=_config, **kwargs)
        configure_relations(self, _relations)

    def actuatedby(self, actuatedby: Property):
        self._data_graph.add(
            (self._node_iri, S223.actuatedByProperty, actuatedby._node_iri),
        )
