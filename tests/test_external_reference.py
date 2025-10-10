from pathlib import Path

from .header import ttl_test_header

from bob.core import bind_model_namespace, dump, Property, UNIT
from bob.externalreference.bacnet import BACnetExternalReference
from bob.properties.temperature import Temperature

from bob.bacnet import (
    Device,
    DeviceObject,
    AnalogInputObject,
)

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_create_external_reference(bob_fixture):
    ref1 = BACnetExternalReference( #noqa F841
        "bacnet://12345/analog-value,1/present-value", label="ref1"
    )

    # dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))


def test_add_external_reference_to_property(bob_fixture):
    prop = Property(label="fake prop")
    ref1 = BACnetExternalReference(
        "bacnet://12345/analog-value,1/present-value", label="ref1"
    )
    prop @ ref1


def test_add_external_reference_to_temperature_property(bob_fixture):
    prop = Temperature(label="fake temp", hasUnit=UNIT.DEG_C)
    ref1 = BACnetExternalReference(
        "bacnet://12345/analog-value,1/present-value", label="ref1"
    )
    prop @ ref1


def test_a_bacnet_object_as_external_reference(bob_fixture):
    # An HVAC BACnet Device
    CGM_2_004 = Device(
        label="CGM-2-004",
        comment="AHU Controller",
    )

    CGM_2_004_device_object = DeviceObject(
        objectIdentifier="device,5204",
        objectName="CGM-2-004",
        vendorName="Unknown",
        vendorIdentifier=5,
    )
    CGM_2_004 > CGM_2_004_device_object
    rat = AnalogInputObject(
        objectIdentifier="analog-input,1209",
        objectName="RA-T",
        description="Return Air Temeprature",
    )
    CGM_2_004 > rat
    prop = Temperature(label="fake temp", hasUnit=UNIT.DEG_C)
    prop @ rat.presentValue

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
