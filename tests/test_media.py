from pathlib import Path

from header import ttl_test_header
from rdflib import Literal
from bob import core
from bob.core import bind_model_namespace, dump, data_graph, schema_graph


from bob.core import Substance, Medium
from bob.enum import Constituent, Air, Fluid, Argon, CO2, Nitrogen, O2
from bob.sensor.gas import CO2Sensor

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")
core.INCLUDE_INVERSE = True


def test_substances_are_filled_with_constituents(bob_fixture):
    assert len(Substance._children) > 10


def test_create_constituent(bob_fixture):
    co4 = Constituent("CO4", label="Carbon QuatriOxide, yeah, it's fake")
    assert co4.label == Literal("Carbon QuatriOxide, yeah, it's fake")
    assert co4 in Substance._children
    assert co4 in Medium._children


def test_create_mix_medium_air_with_constituents(bob_fixture):
    myair = Air("Air", label="Air, the stuff we breathe")
    assert myair.label == Literal("Air, the stuff we breathe")
    assert myair in Medium._children
    assert myair in Fluid._children

    myair.add_constituent(Nitrogen)
    myair.add_constituent(O2)
    myair.add_constituent(Argon)
    myair.add_constituent(CO2)
    assert Nitrogen in myair._constituents
    assert O2 in myair._constituents
    assert Argon in myair._constituents
    assert CO2 in myair._constituents

    assert len(myair.composedOf) == 5 # including vapor-h2o


def test_create_a_co2_sensor(bob_fixture):
    s = CO2Sensor(label="CO2 Sensor")
    assert s.label == Literal("CO2 Sensor")
    assert s.observes.ofMedium == Air
    assert s.observes.ofSubstance == CO2


def test_dump_test_media_model(bob_fixture):
    co4 = Constituent("CO4", label="Carbon QuatriOxide, yeah, it's fake") #noqa F841
    myair = Air("Air", label="Air, the stuff we breathe")
    myair.add_constituent(Nitrogen)
    myair.add_constituent(O2)
    myair.add_constituent(Argon)
    myair.add_constituent(CO2)
    s = CO2Sensor(label="CO2 Sensor") #noqa F841
    # dump the result
    dump(
        data_graph,
        filename=f"tests/ttl/{model_name}.data.ttl",
        header=ttl_test_header(model_name),
    )
    dump(schema_graph, filename=f"tests/ttl/{model_name}.schema.ttl")
