import logging
from typing import Dict, Optional

from rdflib import URIRef

from ...connections.air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
)
from ...core import BOB, S223, Equipment
from ...template import configure_relations, template_update  # logging

_namespace = BOB
_log = logging.getLogger(__name__)

"""
chilledWaterCoil_template = {
    "params": {"label": "Name", "comment": "Description"},
    "sensors": {},
    "equipment": {("valve", Equipment): {"comment": "SubDev comment"}},
}
"""

# SEMANTIC QUESTION
# here, that could be a good way to define the coil and its valve...
# but the valve connect to the coil
# can this be considered "contained" in the Coil Equipment ?
# Should this b ea system


class AirHeatExchanger(Equipment):
    _class_iri: URIRef = S223.AirHeatExchanger
    supplyAirInlet: AirInletConnectionPoint
    supplyAirOutlet: AirOutletConnectionPoint
    exhaustAirInlet: AirInletConnectionPoint
    exhaustAirOutlet: AirOutletConnectionPoint

    def __init__(self, config: dict | None = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.info(f"AirHeatExchanger.__init__ {_config} {kwargs}")
        _relations = _config.pop("relations", [])
        super().__init__(config=_config, **kwargs)
        configure_relations(self, _relations)
        self.supplyAirOutlet.paired_to(self.supplyAirInlet)  # type: ignore
        self.exhaustAirOutlet.paired_to(self.exhaustAirInlet)  # type: ignore
