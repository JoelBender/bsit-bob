from typing import Dict


from ...connections.liquid import (
    WaterInletConnectionPoint,
    WaterOutletConnectionPoint,
)
from ...core import BOB, S223, Equipment
from ...template import template_update, configure_relations

_namespace = BOB

class Chiller(Equipment):
    _class_iri = S223.Chiller
    chilledWaterEntering: WaterInletConnectionPoint
    chilledWaterLeaving: WaterOutletConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _relations)
