import logging
from typing import Dict


from bob.properties.network import Mbit_per_seconds

from ...connections.electricity import Electricity_120VLN_1Ph_60HzInletConnectionPoint
from ...connections.network import (
    EthernetBidirectionalConnectionPoint,
    EthernetConnection,
)
from ...core import (
    BOB,
    P223,
    Equipment,
)
from ...template import template_update

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = BOB

ethernet_firewall_template = {
    "cp": {
        "electricalInlet": Electricity_120VLN_1Ph_60HzInletConnectionPoint,
    },
    "properties": {},
}

internet = EthernetConnection(label="internet")


class EthernetFirewall(Equipment):
    """
    An Ethernet Firewall with wan and lan ports
    """

    _class_iri = P223.EthernetFirewall

    def __init__(self, config: Dict = None, **kwargs):
        if "wan_ports" in kwargs:
            _number_of_wanports = int(kwargs.pop("wan_ports"))
        else:
            raise ValueError("Please provide number of IP ports using wan_ports=x")
        if "lan_ports" in kwargs:
            _number_of_lanports = int(kwargs.pop("lan_ports"))
        else:
            raise ValueError("Please provide number of IP ports using wan_ports=x")
        if "data_rate" in kwargs:
            _data_rate = float(kwargs.pop("data_rate"))
        else:
            raise ValueError("Please provide data rate using data_rate=x in Mbit/s")
        _config = template_update(ethernet_firewall_template, config)
        for i, each in enumerate(range(_number_of_wanports)):
            _config["cp"][f"wan_port{i}"] = EthernetBidirectionalConnectionPoint
        for i, each in enumerate(range(_number_of_lanports)):
            _config["cp"][f"lan_port{i}"] = EthernetBidirectionalConnectionPoint
        kwargs = {**_config.get("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        for k, v in self._connection_points.items():
            if isinstance(v, EthernetBidirectionalConnectionPoint):
                v.data_rate = Mbit_per_seconds(_data_rate)
