from bob.core import  S223, Property
from bob.equipment.control.controller import Controller

_namespace = S223


class _VFD(Controller):
    """
    This is required here so actuatesProperty gets its namespace from S223
    """

    _class_iri = S223.VariableFrequencyDrive
    actuatesProperty: Property
