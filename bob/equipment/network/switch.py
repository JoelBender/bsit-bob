import logging
from typing import Dict

from rdflib import URIRef

from bob.properties.network import Mbit_per_seconds

from ...connections.electricity import ElectricalInletConnectionPoint
from ...connections.network import (
    EthernetBidirectionalConnectionPoint,
    PoEBidirectionalConnectionPoint,
)
from ...core import (
    BOB,
    S223,
    Equipment,
)
from ...template import template_update

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = BOB

ethernet_switch_template = {
    "cp": {
        "electricalInlet": ElectricalInletConnectionPoint,
    },
    "properties": {},
}


class EthernetSwitch(Equipment):
    """
    An Ethernet Switch
    """

    _class_iri: URIRef = S223.EthernetSwitch

    def __init__(self, config: Dict = None, **kwargs):
        if "ports" in kwargs:
            _number_of_ports = int(kwargs.pop("ports"))
        else:
            raise ValueError("Please provide number of IP ports using ports=x")
        if "data_rate" in kwargs:
            _data_rate = float(kwargs.pop("data_rate"))
        else:
            raise ValueError("Please provide data rate using data_rate=x in Mbit/s")
        _config = template_update(ethernet_switch_template, config)
        for i, each in enumerate(range(_number_of_ports)):
            _config["cp"][f"port{i}"] = EthernetBidirectionalConnectionPoint
        kwargs = {**_config.get("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        for k, v in self._connection_points.items():
            if isinstance(v, EthernetBidirectionalConnectionPoint):
                v.data_rate = Mbit_per_seconds(_data_rate)


class PoESwitch(Equipment):
    """
    An Ethernet Switch
    """

    _class_iri: URIRef = S223.PoESwitch

    def __init__(self, config: Dict = None, **kwargs):
        if "ports" in kwargs:
            _number_of_ports = int(kwargs.pop("ports"))
        else:
            raise ValueError("Please provide number of IP ports using ports=x")
        if "data_rate" in kwargs:
            _data_rate = float(kwargs.pop("data_rate"))
        else:
            raise ValueError("Please provide data rate using data_rate=x in Mbit/s")
        _config = template_update(ethernet_switch_template, config)
        for i, each in enumerate(range(_number_of_ports)):
            _config["cp"][f"port{i}"] = PoEBidirectionalConnectionPoint
        kwargs = {**_config.get("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        for k, v in self._connection_points.items():
            if isinstance(v, EthernetBidirectionalConnectionPoint):
                v.data_rate = Mbit_per_seconds(_data_rate)
