from __future__ import annotations

from typing import Any

from ..core import (
    BOB,
    S223,
    PropertyReference,
)
from ..enum import Air, Particulate
from ..properties import ParticulateCount
from .sensor import Sensor, split_kwargs

_namespace = BOB


class ParticulateSensor(Sensor):
    _class_iri = S223.ParticulateSensor
    observes: PropertyReference  # ParticulateCount

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)

        self.observes = ParticulateCount(
            label=f"{self.label}.ParticulateCount",  # needs more focus
            ofMedium=Air,
            **_property_kwargs,
        )


class UltraFineParticulateSensor(ParticulateSensor):
    _class_iri = S223.ParticulateSensor
    "PM 1.0 Count"
    comment = "Ultra Fine Particulate Sensor"

    # measuresSubstance: Substance = PM1_0
    def __init__(self, **kwargs):
        super().__init__(ofSubstance=Particulate.PM1_0, **kwargs)


class FineParticulateSensor(ParticulateSensor):
    _class_iri = S223.ParticulateSensor
    "PM 2.5 Count"
    comment = "Fine Particulate Sensor"

    # measuresSubstance: Substance = PM2_5
    def __init__(self, **kwargs):
        super().__init__(ofSubstance=Particulate.PM2_5, **kwargs)


class CoarseParticulateSensor(ParticulateSensor):
    _class_iri = S223.ParticulateSensor
    "PM 10 Count"
    comment = "Coarse Particulate Sensor"

    # measuresSubstance: Substance = PM10_0
    def __init__(self, **kwargs):
        super().__init__(ofSubstance=Particulate.PM10_0, **kwargs)
