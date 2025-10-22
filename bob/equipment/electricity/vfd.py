from typing import Dict, Optional

from rdflib import URIRef

from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    ElectricalOutletConnectionPoint,
)
from ...core import (
    S223,
    SCRATCH,
    logging,
)
from ...equipment.electricity import _VFD
from ...template import configure_relations, template_update

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = SCRATCH


vfd_template = {
    "cp": {
        "electricalInlet": ElectricalInletConnectionPoint,
        "electricalOutlet": ElectricalOutletConnectionPoint,
    },
    "properties": {},
    "parts": {},
}


class VFD(_VFD):
    _class_iri: URIRef = S223.VariableFrequencyDrive

    def __init__(self, config: dict | None = None, **kwargs):
        _config = template_update(vfd_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.debug(f"VFD.__init__ {_config} {kwargs}")
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _relations)
