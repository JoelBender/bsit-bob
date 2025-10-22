from pathlib import Path

from rdflib import URIRef

from bob.connections.electricity import ElectricalInletConnectionPoint
from bob.connections.light import (
    LightVisibleConnection,
    LightVisibleOutletConnectionPoint,
)
from bob.core import P223, Equipment, bind_model_namespace, dump

from .header import ttl_test_header

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_Light_Subclass_of_Medium_Connection(bob_fixture):
    class WeirdLuminaire(Equipment):
        _class_iri: URIRef = P223.Light
        lightOutlet: LightVisibleOutletConnectionPoint
        electricalInlet: ElectricalInletConnectionPoint

    lightcnx = LightVisibleConnection(label="Sun")

    WeirdLuminaire(label="WL") >> lightcnx

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
