import logging
from typing import Dict

from rdflib import URIRef


from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...connections.electricity import (
    ElectricalInletConnectionPoint,
)
from ...core import (
    BOB,
    S223,
    Equipment,
)
from ...template import configure_relations, template_update

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = BOB


fan_template = {"cp": {"electricalInlet": ElectricalInletConnectionPoint}}


class Fan(Equipment):
    """
    A fan is composed of a blower and an electrical motor
    """

    _class_iri: URIRef = S223.Fan
    # electricalInlet: ElectricalInletConnectionPoint # needs to be in a template so other templates can override it.
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(fan_template, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.info(f"Fan.__init__ {_config} {kwargs}")
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _relations)
        self.airOutlet.paired_to(self.airInlet)
