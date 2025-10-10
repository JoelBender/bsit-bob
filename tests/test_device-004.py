from pathlib import Path
from typing import Dict
from header import ttl_test_header
from rdflib import URIRef
from bob.core import (
    QUANTITYKIND,
    UNIT,
    bind_model_namespace,
    dump,
    QuantifiableObservableProperty,
    Equipment
)
from bob.sensor.gas import CO2Sensor, COSensor, NO2Sensor
from bob.sensor.temperature import AirTemperatureSensor
from bob.space.hvac import HVACSpace
from bob.space.physical import Floor
from bob.connections.air import (
    AirInletConnectionPoint,   
    AirOutletConnectionPoint
)
from bob.core import PropertyReference, SCRATCH
from bob.template import template_update, configure_relations

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")

class GasMonitor(Equipment):
    """
    Gas monitor that contains 1 or more gas sensors
    It comes from si-modeler and is presetned here for testing purposes.
    """

    _class_iri: URIRef = SCRATCH.GasMonitor
    airInletSupply: AirInletConnectionPoint
    airOutletExhaust: AirOutletConnectionPoint

    alarmStatus: PropertyReference

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _relations)

def test_create_gas_monitor(bob_fixture):
    _co2_and_temp = {
        "params": {
            "label": "CO2-2",
            "comment": "CO2 Monitor with temperature reading",
        },
        "sensors": {
            ("CO2_sensor", CO2Sensor): {
                # "hasExternalReference": "bacnet://",
                "hasMinRange": QuantifiableObservableProperty(
                    0,
                    hasQuantityKind=QUANTITYKIND.DimensionlessRatio,
                    hasUnit=UNIT.PPM,
                    label="CO2_sensor.MinRange",
                ),
                "hasMaxRange": QuantifiableObservableProperty(
                    2000,
                    hasQuantityKind=QUANTITYKIND.DimensionlessRatio,
                    hasUnit=UNIT.PPM,
                    label="CO2_sensor.MaxRange",
                ),
            },
            ("Temperature_sensor", AirTemperatureSensor): {
                "hasUnit": UNIT.DEG_C,
                # "hasExternalReference": "bacnet://",
                "hasMinRange": QuantifiableObservableProperty(
                    0,
                    hasQuantityKind=QUANTITYKIND.Temperature,
                    hasUnit=UNIT.DEG_C,
                    label="Temperature_sensor.MinRange",
                ),
                "hasMaxRange": QuantifiableObservableProperty(
                    50,
                    hasQuantityKind=QUANTITYKIND.Temperature,
                    hasUnit=UNIT.DEG_C,
                    label="Temperature_sensor.MaxRange",
                ),
                "comment": "Internal temperature sensor of Equipment",
            },
        },
        "properties": {},
    }

    co2_and_temp_monitor = GasMonitor(_co2_and_temp)

    _dual_no2_co = {
        "params": {
            "label": "GM-1",
            "comment": "Dual Gas Monitoring Equipment that measure NO2 and CO. Usually used in underground parking lot",
        },
        "sensors": {
            ("CO_sensor", COSensor): {
                # "hasExternalReference": "bacnet://",
                "hasMinRange": QuantifiableObservableProperty(
                    0,
                    hasQuantityKind=QUANTITYKIND.DimensionlessRatio,
                    hasUnit=UNIT.PPM,
                    label="CO_sensor.MinRange",
                ),
                "hasMaxRange": QuantifiableObservableProperty(
                    100,
                    hasQuantityKind=QUANTITYKIND.DimensionlessRatio,
                    hasUnit=UNIT.PPM,
                    label="CO_sensor.MaxRange",
                ),
            },
            ("NO2_sensor", NO2Sensor): {
                # "hasExternalReference": "bacnet://",
                "hasMinRange": QuantifiableObservableProperty(
                    0,
                    hasQuantityKind=QUANTITYKIND.DimensionlessRatio,
                    hasUnit=UNIT.PPM,
                    label="NO2_sensor.MinRange",
                ),
                "hasMaxRange": QuantifiableObservableProperty(
                    250,
                    hasQuantityKind=QUANTITYKIND.DimensionlessRatio,
                    hasUnit=UNIT.PPM,
                    label="NO2_sensor.MaxRange",
                ),
            },
        },
        "properties": {},
    }

    dual_no2_co_monitor = GasMonitor(_dual_no2_co) #noqa F841

    _co2 = {
        "params": {
            "label": "CO2-1",
            "comment": "CO2 Monitor",
        },
        "sensors": {
            ("CO2_sensor", CO2Sensor): {
                # "hasExternalReference": "bacnet://",
                "hasMinRange": QuantifiableObservableProperty(
                    0,
                    hasQuantityKind=QUANTITYKIND.DimensionlessRatio,
                    hasUnit=UNIT.PPM,
                    label="CO2_sensor.MinRange",
                ),
                "hasMaxRange": QuantifiableObservableProperty(
                    2000,
                    hasQuantityKind=QUANTITYKIND.DimensionlessRatio,
                    hasUnit=UNIT.PPM,
                    label="CO2_sensor.MaxRange",
                ),
            },
        },
        "properties": {},
    }

    co2_monitor_1 = GasMonitor(_co2) #noqa F841

    co2_monitor_2 = GasMonitor(_co2, label="CO2-4") #noqa F841

    # someplace in the basement
    basement = Floor(label="Basement")
    basement_hvac = HVACSpace(label="Basement HVAC Space") 

    co2_and_temp_monitor.hasPhysicalLocation = basement
    co2_and_temp_monitor["CO2_sensor"] % basement_hvac
    co2_and_temp_monitor["Temperature_sensor"] % basement_hvac

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
