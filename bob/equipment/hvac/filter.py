from typing import Dict, Optional

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...core import BOB, S223, Equipment, PropertyReference
from ...template import configure_relations, template_update

_namespace = BOB

filter_template: dict[str, dict] = {}


class Filter(Equipment):
    _class_iri = S223.Filter
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint

    # Those come from sensors, but accessible from here
    differentialPressure: PropertyReference
    alarmStatus: PropertyReference

    def __init__(self, config: dict | None = None, **kwargs):
        _config = template_update(filter_template, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _relations = _config.pop("relations", [])
        super().__init__(config=_config, **kwargs)
        configure_relations(self, _relations)
        self.airOutlet.paired_to(self.airInlet)  # type: ignore
