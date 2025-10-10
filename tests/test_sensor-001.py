from pathlib import Path

import pytest
from .header import ttl_test_header

from bob.core import UNIT, bind_model_namespace, dump
from bob.enum import Air
from bob.sensor.humidity import AirHumiditySensor
from bob.sensor.temperature import AirTemperatureSensor, TemperatureSensor

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_create_sensor(bob_fixture):
    with pytest.raises(ValueError):
        ats = TemperatureSensor( #noqa F841
            label="DA-T",
            comment="Supply Air Temperature Sensor",
            # hasExternalReference=["bacnet://570005/analog-input,10084/present-value"],
        )

    ats1 = TemperatureSensor( #noqa F841
        label="ats1",
        comment="Supply Air Temperature Sensor",
        hasUnit=UNIT.DEG_C,
        ofMedium=Air,
        # hasExternalReference=["bacnet://570005/analog-input,10084/present-value"],
    )

    ats2 = AirTemperatureSensor( #noqa F841
        label="ats2",
        comment="Supply Air Temperature Sensor",
        # hasExternalReference=["bacnet://570005/analog-input,10084/present-value"],
        hasUnit=UNIT.DEG_C,
    )

    ahs1 = AirHumiditySensor( #noqa F841
        label="ahs1", comment="Zone Humidity Sensor with a value of 20", hasValue=20
    )

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
