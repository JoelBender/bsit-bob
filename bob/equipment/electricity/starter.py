from typing import Dict

from ...equipment.electricity import _MotorStarter
from ...properties.states import OnOffCommand

from ...connections import electricity as elec_cnx
from ...core import (
    BOB,
    P223,
    logging,
)
from ...template import template_update, configure_relations

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = BOB

electric_starter_template = {
    "cp": {
        "electricalInlet": elec_cnx.InletConnectionPoint,
        "electricalOutlet": elec_cnx.OutletConnectionPoint,
    },
    "properties": {
        # ("actuatesProperty", PercentCommand): {},
        ("onOffCommand", OnOffCommand): {},
    },
}


class MotorStarter(_MotorStarter):
    """
    Motor starter
    This Equipment provides command and status for an electrical
    Equipment like a fan or a pump

    """

    _class_iri = P223.MotorStarter

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(electric_starter_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.debug(f"MotorStarter.__init__ {_config} {kwargs}")
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _config.pop("relations", []))
