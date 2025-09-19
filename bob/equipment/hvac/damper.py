from typing import Dict


from ...connections.air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
)
from ...core import BOB, S223, Equipment, logging
from ...template import template_update, configure_relations

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = BOB


class Damper(Equipment):
    _class_iri = S223.Damper
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.info(f"Damper.__init__ {_config} {kwargs}")
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _relations)
        self.airOutlet.paired_to(self.airInlet)
