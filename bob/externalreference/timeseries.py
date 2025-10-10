from ..core import S223, P223, Node, ExternalReference

_namespace = P223


class TimeSeriesReference(ExternalReference):
    _class_iri = S223.ExternalReference

class Database(Node):
    _class_iri = None
