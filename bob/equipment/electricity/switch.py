from typing import Dict

from ...producer.causality import Causality
from ...properties.electricity import Amps
from ...properties.ratio import PercentCommand
from ...properties.states import OnOffCommand, OnOffStatus

from ...enum import Electricity
from ...connections import electricity as elec_cnx
from ...connections.controlsignal import OnOffSignalOutletConnectionPoint
from ...core import (
    BOB,
    P223,
    Equipment,
)
from ...properties.time import Hour
from ...sensor.electricity import CurrentSensor
from ...template import template_update

_namespace = BOB

# TODO : Use templates

switch_template = {
    "cp": {
        "electricalInlet": elec_cnx.Electricity_120VLN_1Ph_60HzInletConnectionPoint,
        "electricalOutlet": elec_cnx.Electricity_120VLN_1Ph_60HzOutletConnectionPoint,
    },
    "properties": {
        ("amps", Amps): {},
    },
}


class Switch(Equipment):
    _class_iri = P223.ElectricalSwitch
    # electricalInlet: ElectricalInletConnectionPoint
    # electricalOutlet: ElectricalOutletConnectionPoint
    hasMaxRange: Amps
    onOffStatus: OnOffStatus
    onOffCommand: OnOffCommand

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(switch_template, config)
        kwargs = {**_config.get("params", {}), **kwargs}

        super().__init__(_config, **kwargs)


class SinglePoleSwitch(Switch):
    """
    One inlet and one outlet
    hasMaxRange = current max of switch
    A rule could check inlet and outlet are same class
    """

    _cross_ref = {
        "120": (
            elec_cnx.Electricity_120VLN_1Ph_60HzInletConnectionPoint,
            elec_cnx.Electricity_120VLN_1Ph_60HzOutletConnectionPoint,
        ),
        "277": (
            elec_cnx.Electricity_277VLN_1Ph_60HzInletConnectionPoint,
            elec_cnx.Electricity_277VLN_1Ph_60HzOutletConnectionPoint,
        ),
        "347": (
            elec_cnx.Electricity_347VLN_1Ph_60HzInletConnectionPoint,
            elec_cnx.Electricity_347VLN_1Ph_60HzOutletConnectionPoint,
        ),
    }

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(switch_template, config)
        if config:
            _config.update(config)
        _voltage = kwargs.pop("voltage") if "voltage" in kwargs else None
        if _voltage:
            _electricalInlet, _electricalOutlet = self._cross_ref[str(_voltage)]
            _config["cp"]["electricalInlet"] = _electricalInlet
            _config["cp"]["electricalOutlet"] = _electricalOutlet
        kwargs = {**_config.get("params", {}), **kwargs}

        super().__init__(_config, **kwargs)


current_relay_template = {
    "cp": {"dryContact": OnOffSignalOutletConnectionPoint},
    "properties": {("amps_rating", Amps): {}, ("onOffStatus", OnOffStatus): {}},
}


class CurrentRelay(Equipment):
    """
    Current detection Equipment that gives a OnOff status by the action
    of a dry contact when electricity is detected.

    This serves as motor status sensor

    """

    _class_iri = P223.CurrentRelay

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(current_relay_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}

        # _hasObservationLocation = kwargs.pop("hasObservationLocation", None)

        _label = kwargs["label"]

        super().__init__(_config, **kwargs)

        sensor = CurrentSensor(
            label="currentSensor",
            ofMedium=Electricity,
        )
        # sensor % _hasObservationLocation
        self > sensor
        status_producer = Causality(label="statusProducer")
        status_producer.cause_input << sensor.observedProperty
        status_producer.effect_output >> self["onOffStatus"]
        self > status_producer
        # self["onOffStatus"] += RunStatus
        # self.dryContact += RunStatus


class TimerSwitch(SinglePoleSwitch):
    """
    Manuel switch with integrated timer
    Typically used for exhaust fan in bathrooms for example
    """

    delay: Hour
    onOffStatus: OnOffStatus
    onOffCommand: OnOffCommand

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(current_relay_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _delay = kwargs.pop("delay") if "delay" in kwargs else None

        if _delay:
            _config["properties"][("delay", Hour)] = {"hasValue": _delay}
        super().__init__(_config, **kwargs)


class DimmableSwitch(SinglePoleSwitch):
    """
    Manuel dimmable switch

    """

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(current_relay_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _dimmer_command = (
            kwargs.pop("dimmer_command") if "dimmer_command" in kwargs else 0
        )
        _config["properties"][("dimmer_command", PercentCommand)] = {
            "hasValue": _dimmer_command
        }
        super().__init__(_config, **kwargs)
