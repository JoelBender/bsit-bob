from ..core import P223, S223, ExternalReference, Node  # type: ignore[attr-defined]

_namespace = P223


class TimeSeriesReference(ExternalReference):
    _class_iri = S223.ExternalReference

class Database(Node):
    _class_iri = None
