import logging
from typing import Dict

from ...connections.air import AirInletConnectionPoint
from ...core import BOB, S223, BoundaryConnectionPoint, Equipment, System
from ... import application
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


class SingleDuctTerminal(System, application.SingleDuctTerminal):
    # _class_iri = S223.SingleDuctTerminal
    airInlet: BoundaryConnectionPoint
    airOutlet: BoundaryConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(TerminalUnit_template, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.info(f"SingleDuctTerminal.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)


# Generic
class GenericSingleDuctTerminal(Equipment, application.SingleDuctTerminal):
    _class_iri = S223.SingleDuctTerminal
    airInlet: AirInletConnectionPoint
    airOutlet: AirInletConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.info(f"GenericSingleDuctTerminal.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)
        self.airOutlet.paired_to(self.airInlet)
