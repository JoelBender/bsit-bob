from typing import Dict

from ...connections.liquid import (
    HotWaterInletConnectionPoint,
    HotWaterOutletConnectionPoint,
)
from ...core import (
    BOB,
    S223,
    Equipment,
)
from ...enum import Role
from ...template import template_update, configure_relations

_namespace = BOB



# 223 Standard Equipment
class Boiler(Equipment):
    _class_iri = S223.Boiler
    hotWaterLeaving: HotWaterOutletConnectionPoint
    hotWaterEntering: HotWaterInletConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _relations)
        self += Role.Heating
        self.hotWaterLeaving.paired_to(self.hotWaterEntering)