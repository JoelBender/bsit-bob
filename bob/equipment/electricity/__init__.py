from bob.core import  P223, S223, Property
from bob.equipment.control.controller import Controller
from bob.equipment.actuator import Actuator

_namespace = S223

class _MotorStarter(Actuator):
    _class_iri = P223._MotorStarter
    actuatesProperty: Property

class _VFD(Controller):
    """
    This is required here so actuatesProperty gets its namespace from S223
    """

    _class_iri = S223.VariableFrequencyDrive
    actuatesProperty: Property
