import logging
from typing import Dict, Optional

from ...connections.air import AirInletConnectionPoint
from ...core import BOB, S223, Equipment
from ...equipment.hvac.damper import Damper
from ...template import template_update

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = BOB

TerminalUnit_template = {
    "equipment": {
        ("damper", Damper): {"comment": "VAV Box Damper including"},
        # ("flow_sensor", AirFlowSensor): {"comment": "Air flow sensor"}
    },
}


# Generic
class SingleDuctTerminal(Equipment):
    _class_iri = S223.SingleDuctTerminal
    airInlet: AirInletConnectionPoint
    airOutlet: AirInletConnectionPoint

    def __init__(self, config: dict | None = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.info(f"GenericSingleDuctTerminal.__init__ {_config} {kwargs}")
        super().__init__(config=_config, **kwargs)
        self.airOutlet.paired_to(self.airInlet)  # type: ignore
