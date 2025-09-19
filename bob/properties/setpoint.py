from rdflib import Literal, URIRef

from ..core import (
    BOB,
    S223,
    EnumerationKind,
    QuantifiableProperty,
)

_namespace = BOB


class Setpoint(QuantifiableProperty):
    _class_iri: URIRef = S223.Setpoint
    hasAspect: EnumerationKind
    hasDeadband: Literal
    hasValue: Literal
    hasQuantityKind: URIRef
    hasUnit: URIRef

    def __init__(self, **kwargs):
        _properties = {}
        for k, v in self.__annotations__.items():
            if k in kwargs:
                _properties[k] = kwargs.pop(k)
        super().__init__(**kwargs)
        for k, v in _properties.items():
            if v is not None:
                setattr(self, k, self.__annotations__[k](v))
