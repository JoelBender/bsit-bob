from rdflib import URIRef

from ..core import P223, S223, Node


class NetworkProfile(Node):
    """
    A s223:Controller can be represented by a Network Controller
    (like a BACnet or a Lonworks Equipment).
    This class will be a higher class that will serve to relate
    the s223:Controller to the said bacnet:Device or other.
    """

    _class_iri: URIRef = P223.NetworkProfile
