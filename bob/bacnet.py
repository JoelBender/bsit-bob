"""
This module contains just enough of the BACnet object model to help build
example models.  A complete description of BACnet objects and properties is
beyond the scope of this project.
"""

from __future__ import annotations

import logging
from typing import List

from rdflib import XSD, Literal, URIRef

from .core import (
    INCLUDE_INVERSE,
    ConnectionPoint,
    Node,
    bind_namespace,
    prefixes,
)
from .equipment.control.controller import Controller
from .externalreference.bacnet import BACnetExternalReference
from .multimethods import multimethod

# logging
_log = logging.getLogger(__name__)

# namespace
BACNET = bind_namespace("bacnet", prefixes["bacnet"])
_namespace = BACNET


class Device(Controller):
    _class_iri: URIRef = BACNET.Device
    _namespace = BACNET
    _device_object: DeviceObject  # reference to a device's DeviceObject
    _bacnet_objects = set()  # references to all objects

    deviceInstance: Literal


class Object(Node):
    _attr_uriref = {
        "objectIdentifier": BACNET["object-identifier"],
        "objectName": BACNET["object-name"],
        "objectType": BACNET["object-type"],
        "description": BACNET["description"],
    }
    _device: Device

    objectIdentifier: Literal
    objectName: Literal
    objectType: URIRef
    description: Literal

    _device: Device  # reference from an object to its device
    _present_value: BACnetExternalReference

    @property
    def presentValue(self) -> BACnetExternalReference:
        """
        Creates the present-value reference on demand to be used for a property.
        Cache it in case there are multiple references.
        """
        if getattr(self, "_present_value", None) is None:
            self._present_value = BACnetExternalReference(
                f"bacnet://{self._device.deviceInstance}/{self.objectIdentifier}/present-value"
            )
            self._data_graph.add(
                (self._node_iri, BACNET.hasProperty, self._present_value._node_iri)
            )
        return self._present_value

    @property
    def relinquishDefault(self) -> BACnetExternalReference:
        """
        Creates the relinquish-default reference on demand to be used for a property.
        Cache it in case there are multiple references.
        """
        if getattr(self, "_relinquish_default", None) is None:
            self._relinquish_default = BACnetExternalReference(
                f"bacnet://{self._device.deviceInstance}/{self.objectIdentifier}/relinquish-default"
            )
            self._data_graph.add(
                (self._node_iri, BACNET.hasProperty, self._relinquish_default._node_iri)
            )
        return self._relinquish_default


@multimethod
def contains_mm(device_: Device, object_: Object) -> None:
    """Device > Object"""
    _log.info(f"device {device_} contains object {object_}")

    # link the object to the device and vice versa
    object_._device = device_
    device_._bacnet_objects.add(object_)

    # the device instance number should match the object instance of the
    # device object
    if isinstance(object_, DeviceObject):
        if getattr(device_, "_device_object", None) is not None:
            raise ValueError(f"device already has a Device Object: {device_}")
        device_._device_object = object_

        device_instance = int(object_.objectIdentifier.split(",")[1])
        if device_.deviceInstance is not None:
            if device_.deviceInstance != device_instance:
                raise ValueError(f"device instance mismatch: {device_}")
        else:
            device_.deviceInstance = device_instance

    # add it to the graph
    device_._data_graph.add((device_._node_iri, BACNET.hasObject, object_._node_iri))

    if INCLUDE_INVERSE:
        device_._data_graph.add(
            (object_._node_iri, BACNET.isObjectOf, device_._node_iri)
        )


@multimethod
def contains_mm(device_: Device, object_list: List[Object]) -> None:
    """Device > [ Object, ... ]"""
    _log.info(f"device {device_} contains object list {object_list}")

    for object_ in object_list:
        contains_mm(device_, object_)


@multimethod
def connect_mm(object_: Object, cp_: ConnectionPoint) -> None:
    """Object >> CP"""
    _log.info(f"object {object_} mapsTo {cp_}")

    # add it to the graph
    object_._data_graph.add((object_._node_iri, BACNET.mapsTo, cp_._node_iri))

    # if INCLUDE_INVERSE:
    #    object_._data_graph.add(
    #        (object_._node_iri, BACNET.isObjectOf, device_._node_iri)
    #    )


@multimethod
def connect_mm(object1_: Object, object2_: Object) -> None:
    """Object >> Object"""
    _log.info(f"object {object1_} mapsTo {object2_}")

    # add it to the graph
    object1_._data_graph.add(
        (object1_._node_iri, BACNET.PeerToPeer, object2_._node_iri)
    )

    # if INCLUDE_INVERSE:
    #    object_._data_graph.add(
    #        (object_._node_iri, BACNET.isObjectOf, device_._node_iri)
    #    )


class DeviceObject(Object):
    objectType: URIRef = BACNET["ObjectType.device"]
    _attr_uriref = {
        "systemStatus": BACNET["system-status"],
        "vendorName": BACNET["vendor-name"],
        "vendorIdentifier": BACNET["vendor-identifier"],
        "modelName": BACNET["model-name"],
    }
    systemStatus: URIRef  # one of bacnet:DeviceStatus
    vendorName: Literal
    vendorIdentifier: XSD.nonNegativeInteger
    modelName: Literal


class AnalogInputObject(Object):
    objectType: URIRef = BACNET["ObjectType.analog-input"]


class AnalogOutputObject(Object):
    objectType: URIRef = BACNET["ObjectType.analog-output"]


class AnalogValueObject(Object):
    objectType: URIRef = BACNET["ObjectType.analog-value"]


class BinaryInputObject(Object):
    objectType: URIRef = BACNET["ObjectType.binary-input"]


class BinaryOutputObject(Object):
    objectType: URIRef = BACNET["ObjectType.binary-output"]


class BinaryValueObject(Object):
    objectType: URIRef = BACNET["ObjectType.binary-value"]


class CalendarObject(Object):
    objectType: URIRef = BACNET["ObjectType.calendar"]


class ScheduleObject(Object):
    objectType: URIRef = BACNET["ObjectType.schedule"]
