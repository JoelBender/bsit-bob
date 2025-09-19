from typing import Dict

from rdflib import URIRef

from ...connections.liquid import (
    WaterInletConnectionPoint,
    WaterOutletConnectionPoint,
)
from ...core import BOB, P223, Equipment
from ...template import configure_relations, template_update

_namespace = BOB

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


class GeothermalWell(Equipment):
    _class_iri: URIRef = P223.GeothermalWell
    waterInlet: WaterInletConnectionPoint
    waterOutlet: WaterOutletConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _relations)
        self.waterOutlet.paired_to(self.waterInlet)
