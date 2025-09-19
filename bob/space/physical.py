"""
Physical Space subclasses, see also Real Estate Core.
"""

from ..core import BOB, PhysicalSpace
from ..properties.physical import Area

_namespace = BOB


class Site(PhysicalSpace):
    area: Area


class Building(PhysicalSpace):
    area: Area


class Roof(PhysicalSpace):
    area: Area


class Floor(PhysicalSpace):
    area: Area


class Basement(Floor):
    area: Area


class Room(PhysicalSpace):
    area: Area


class Hall(Room):
    area: Area


class Corridor(Room):
    area: Area


class Bathroom(Room):
    area: Area


class Office(Room):
    area: Area


class MechanicalRoom(Room):
    area: Area
