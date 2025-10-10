from pathlib import Path

import pytest
from header import ttl_test_header

from bob.core import UNIT, Property, bind_model_namespace, dump
from bob.externalreference.bacnet import BACnetExternalReference
from bob.properties.temperature import Temperature

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_create_internal_reference(bob_fixture):
    ref1 = BACnetExternalReference( #noqa F841
        "bacnet://12345/analog-value,1/present-value", label="ref1"
    )

    # dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))


def test_add_external_reference_to_property_then_create_internal_ref(bob_fixture):
    ref_prop = Property(label="fake prop with ext ref")
    ref1 = BACnetExternalReference(
        "bacnet://12345/analog-value,1/present-value", label="ref1"
    )
    ref_prop @ ref1

    prop = Property(label="fake prop with ext ref")
    prop @ ref_prop
    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))


def test_add_internal_reference_to_temperature_property_with_ext_ref(bob_fixture):
    with pytest.raises(AttributeError):
        prop = Temperature(label="fake temp", hasUnit=UNIT.DEG_C)
        intref_prop = Temperature(label="another fake temp", hasUnit=UNIT.DEG_C)
        ref1 = BACnetExternalReference(
            "bacnet://12345/analog-value,1/present-value", label="ref1"
        )
        prop @ ref1
        prop @ intref_prop
