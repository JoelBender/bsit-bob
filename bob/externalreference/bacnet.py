import logging
import re

from rdflib import XSD, Literal

from ..core import S223, ExternalReference, bind_namespace, prefixes

# logging
_log = logging.getLogger(__name__)

# namespace
BACNET = bind_namespace("bacnet", prefixes["bacnet"])

url_pattern = re.compile(
    "^bacnet:[/][/]([0-9]+)?[/]([A-Za-z0-9-]+),([1-9][0-9]*)(?:[/]([A-Za-z0-9-]+)(?:[/]([1-9][0-9]*))?)?$"
)


# class BACnetDevice(NetworkProfile):
#     _class_iri: URIRef = BACNET.Device
#     _namespace = BACNET
#     deviceId: XSD.integer
#     deviceName: Literal
#     networkNumber: XSD.integer
#     address: XSD.integer
#     vendorId: XSD.integer
#     isNetworkProfileOf: Controller


class BACnetExternalReference(ExternalReference):
    _class_iri = S223.BACnetExternalReference
    _attr_uriref = {
        "objectIdentifier": BACNET["object-identifier"],
        "propertyIdentifier": BACNET["property-identifier"],
        "propertyArrayIndex": BACNET["property-array-index"],
        "deviceIdentifier": BACNET["device-identifier"],
    }
    objectIdentifier: Literal
    propertyIdentifier: Literal
    propertyArrayIndex: XSD.nonNegativeInteger
    deviceIdentifier: Literal

    # objectType: URIRef
    # objectInstance: XSD.integer
    # objectOf: BACnetDevice
    # objectName: Literal
    # description: Literal

    # deviceName: Literal
    # networkNumber: XSD.nonNegativeInteger
    # address: Literal
    # vendorId: XSD.nonNegativeInteger

    def __init__(self, arg: str = "", **kwargs) -> None:
        _log.debug("BACnetExternalReference.__init__ %r %r", arg, kwargs)

        if arg:
            url_match = url_pattern.match(arg)
            if not url_match:
                raise ValueError("not a BACnet URL")
            (
                device_instance,
                object_type,
                object_instance,
                property_identifier,
                property_array_index,
            ) = url_match.groups()

            if "deviceIdentifier" in kwargs:
                if device_instance is not None:
                    raise ValueError("initialization conflict: deviceIdentifier")
            elif device_instance is not None:
                kwargs["deviceIdentifier"] = f"device,{device_instance}"

            if "objectIdentifier" in kwargs:
                raise ValueError("initialization conflict: objectIdentifier")
            kwargs["objectIdentifier"] = f"{object_type},{object_instance}"

            if "propertyIdentifier" in kwargs:
                if property_identifier is not None:
                    raise ValueError("initialization conflict: propertyIdentifier")
                property_identifier = kwargs.get("propertyIdentifier")

            if isinstance(property_identifier, Literal):
                kwargs["propertyIdentifier"] = property_identifier
            elif isinstance(property_identifier, int):
                raise NotImplementedError("integer property identifiers")  # TODO
                kwargs["propertyIdentifier"] = property_identifier
            elif isinstance(property_identifier, str):
                if property_identifier.isdigit():
                    raise NotImplementedError("integer property identifiers")  # TODO
                    kwargs["propertyIdentifier"] = int(property_identifier)
                else:
                    kwargs["propertyIdentifier"] = BACNET[
                        "PropertyIdentifier." + property_identifier
                    ]
            elif property_identifier is None:
                kwargs["propertyIdentifier"] = BACNET[
                    "PropertyIdentifier.present-value"
                ]
            else:
                raise TypeError("propertyIdentifier")

            # Issue with Validation, rules ask for sh:datatype xsd:string
            kwargs["propertyIdentifier"] = Literal(kwargs["propertyIdentifier"])

            if "propertyArrayIndex" in kwargs:
                raise ValueError("initialization conflict: propertyArrayIndex")
            if property_array_index:
                kwargs["propertyArrayIndex"] = Literal(property_array_index)

        super().__init__(**kwargs)
