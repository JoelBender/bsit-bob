from typing import Dict, Optional

from ...connections.electricity import (
    Electricity_600VLL_3Ph_60HzInletConnectionPoint,
)
from ...connections.liquid import WaterInletConnectionPoint, WaterOutletConnectionPoint
from ...core import BOB, S223, Equipment, PropertyReference, logging
from ...template import template_update

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = BOB

pump_template = {
    "cp": {"electricalInlet": Electricity_600VLL_3Ph_60HzInletConnectionPoint},
    "properties": {
    },
}


class Pump(Equipment):
    _class_iri = S223.Pump
    fluidInlet: WaterInletConnectionPoint
    fluidOutlet: WaterOutletConnectionPoint
    onOffStatus: PropertyReference
    onOffCommand: PropertyReference

    def __init__(self, config: dict | None = None, **kwargs):
        _config = template_update(pump_template, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.debug(f"Fan.__init__ {_config} {kwargs}")

        super().__init__(**_config, **kwargs)
        self.fluidOutlet.paired_to(self.fluidInlet)  # type: ignore
