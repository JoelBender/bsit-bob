import logging
from typing import Dict

from rdflib import URIRef

from ...connections.air import (
    AirBidirectionalConnectionPoint,
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

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.info(f"AirHeatExchanger.__init__ {_config} {kwargs}")
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _relations)
        self.supplyAirOutlet.paired_to(self.supplyAirInlet)
        self.exhaustAirOutlet.paired_to(self.exhaustAirInlet)


class Accumulator(Equipment):
    """
    Type of heat exchanger that accumulate heat from exhaust air
    passing through it. Then air flow will switch side. Air will flow
    so outdoor air will use energy accumulated in the substrat. This cycle
    will repeat.
    """

    _class_iri: URIRef = S223.Equipment
    outdoorSide: AirBidirectionalConnectionPoint
    indoorSide: AirBidirectionalConnectionPoint


class Accumulator4SidesDuct(Equipment):
    """
    This is part of the exchanger and allow air to comes in or out of accumulator
    depending on the position of the pneumatic damper
    Return and supply are directional, but accumulator 1 and 2 are bidirectional
    """

    _class_iri: URIRef = S223.Equipment
    accumulator1Connection: AirBidirectionalConnectionPoint
    accumulator2Connection: AirBidirectionalConnectionPoint
    supplyDuctOutlet: AirOutletConnectionPoint
    returnDuctInlet: AirInletConnectionPoint
