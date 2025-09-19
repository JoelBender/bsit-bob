from typing import Dict

from rdflib import URIRef

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...core import (
    BOB,
    P223,
    Equipment,
    PropertyReference,
)
from ...sensor.gas import (
    COSensor,
    NO2Sensor,
)

# namespace
_namespace = BOB

gasmonitor_template = {
    "params": {
        "label": "Name Of Equipment",
        "comment": "Description",
    },
    "sensors": {
        ("COSensor", COSensor): {
            "hasExternalReference": "bacnet://",
            # "properties": {
            #   "ofSubstance": Constituent.CO,
            #                 ("hasMinRange", QuantifiableObservableProperty): {
            #                     "hasQuantityKind": QUANTITYKIND.DimensionlessRatio,
            #                     "hasUnit": UNIT.PPM,
            #                 },
            #                 ("hasMaxRange", QuantifiableObservableProperty): {
            #                     "hasQuantityKind": QUANTITYKIND.DimensionlessRatio,
            #                     "hasUnit": UNIT.PPM,
            #                 },
            # },
        },
        ("NO2Sensor", NO2Sensor): {
            "hasExternalReference": "bacnet://",
            # "properties": {
            # "ofSubstance": Constituent.NO2,
            #             "hasMinRange": QuantifiableObservableProperty(
            #                 0, hasQuantityKind=QUANTITYKIND.DimensionlessRatio, hasUnit=UNIT.PPM
            #             ),
            #             "hasMaxRange": QuantifiableObservableProperty(
            #                 100, hasQuantityKind=QUANTITYKIND.DimensionlessRatio, hasUnit=UNIT.PPM
            #             ),
            #    },
        },
    },
    "properties": {},
}


class GasMonitor(Equipment):
    """
    Gas monitor that contains 1 or more gas sensors
    """

    _class_iri: URIRef = P223.GasMonitor
    airInletSupply: AirInletConnectionPoint
    airOutletExhaust: AirOutletConnectionPoint

    alarmStatus: PropertyReference

    def __init__(self, config: Dict = gasmonitor_template, **kwargs):
        config["properties"] = config.get(
            "properties", gasmonitor_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
