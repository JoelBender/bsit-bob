from bob.core import P223, S223, Equipment, Property
from bob.equipment.control.controller import Controller

_namespace = S223


class _MotorStarter(Equipment):
    """
    This is required here so actuatesProperty gets its namespace from S223
    """

    _class_iri = S223.Equipment
    actuatesProperty: Property


class _VFD(Controller):
    """
    This is required here so actuatesProperty gets its namespace from S223
    """

    _class_iri = S223.VariableFrequencyDrive
    actuatesProperty: Property
