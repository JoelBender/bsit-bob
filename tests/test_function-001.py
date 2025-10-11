from pathlib import Path

from bob.core import UNIT, Property, bind_model_namespace, dump
from bob.functions import Function, FunctionInput, FunctionOutput
from bob.properties.temperature import Temperature

from .header import ttl_test_header

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_function_creation(bob_fixture):
    """Create a thing `x` with an outlet connection point and two things `y` and
    `z` with inlets.  Connect the outlet of `x` to the junction with one
    connection and the junction to both inlets each with their own connection.
    """
    f = Function(label="f")

    t1 = Temperature(label="t1", value=20, hasUnit=UNIT.DEG_C)
    t2 = Temperature(label="t2", value=10, hasUnit=UNIT.DEG_C)
    t3 = Temperature(label="t3", hasUnit=UNIT.DEG_C)

    f.hasInput(t1)
    f.hasInput(t2)
    f.hasInput(Property(hasValue=22.1, label="constante"))
    f.hasOutput(t3)

    assert f.outputs["t3"] == t3
    assert len(f.outputs) == 1
    assert len(f.inputs) == 3

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))

def test_function_declaration(bob_fixture):
    """Create a function with inputs and outputs.
    """
    class MyFunction(Function):
        _class_iri = _namespace.Function
        input1: FunctionInput
        input2: FunctionInput
        output1: FunctionOutput

    t1 = Temperature(label="label_t1", value=20, hasUnit=UNIT.DEG_C)
    t2 = Temperature(label="label_t2", value=10, hasUnit=UNIT.DEG_C)
    t3 = Temperature(label="label_t3", hasUnit=UNIT.DEG_C)

    f = MyFunction(label="f")

    f.hasInput(t1, attr="input1")
    f.input2 = t2
    f.hasOutput(t3)

    assert f.inputs["input1"] == t1
    assert f.inputs["input2"] == t2
    # inserted without attr, which creates a default label
    assert f.outputs["label_t3"] == t3

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
