from __future__ import annotations

from typing import Any, Dict

from rdflib import URIRef

from ..core import (
    BOB,
    QUANTITYKIND,
    S223,
    UNIT,
    PropertyReference,
    Setpoint,
)
from ..enum import Constituent, NOx
from ..properties import GasConcentration
from .sensor import Sensor, split_kwargs

_namespace = BOB

# TODO :
# try to create an exmaple for the sensors found here
# Sal will like :0)
# And those are from Quebec
# http://operadetectors.com/category/gas-monitors-1.aspx


class GasConcentrationSetpoint(Setpoint):
    _class_iri = S223.Setpoint
    hasQuantityKind: URIRef = QUANTITYKIND.DimensionlessRatio
    hasUnit: URIRef = UNIT.PPM


class GasConcentrationSensor(Sensor):
    _class_iri = S223.Sensor
    observes: PropertyReference  # GasConcentration  # type: ignore[assignment]
    hasMinRange: PropertyReference  # type: ignore[assignment]
    hasMaxRange: PropertyReference  # type: ignore[assignment]

    def __init__(self, config: dict[str, Any] = {}, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)
        print(f"{_sensor_kwargs = }, {_property_kwargs = }")

        if "ofSubstance" not in _property_kwargs:
            raise ValueError(
                "You must provide ofSubstance when defining a gas concentration sensor",
            )

        observed_prop = GasConcentration(
            label="observed_property",  # needs more focus
            hasUnit=UNIT.PPM,
            **_property_kwargs,
        )
        _sensor_kwargs["observed_property"] = observed_prop

        super().__init__(config=config,**_sensor_kwargs)


class CO2Sensor(GasConcentrationSensor):
    _class_iri = S223.Sensor
    "Carbon Dioxide concentration sensor"
    hasMinRange: PropertyReference
    hasMaxRange: PropertyReference

    def __init__(self, config: dict[str, Any] = {}, **kwargs):
        # _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)
        super().__init__(config=config, ofSubstance=Constituent.CO2, **kwargs)


class COSensor(GasConcentrationSensor):
    _class_iri = S223.Sensor
    "Carbon monoxide concentration sensor"
    hasMinRange: PropertyReference
    hasMaxRange: PropertyReference

    def __init__(self, config: dict[str, Any] = {}, **kwargs):
        # _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)
        super().__init__(config=config, ofSubstance=Constituent.CO, **kwargs)


class NO2Sensor(GasConcentrationSensor):
    _class_iri = S223.Sensor
    "Diesel (NO2) concentration sensor"
    hasMinRange: PropertyReference
    hasMaxRange: PropertyReference

    def __init__(self, config: dict[str, Any] = {}, **kwargs):
        # _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)
        super().__init__(config=config, ofSubstance=NOx.NO2, **kwargs)


class CH4Sensor(GasConcentrationSensor):
    _class_iri = S223.Sensor
    "Natural gas sensor"
    hasMinRange: PropertyReference
    hasMaxRange: PropertyReference

    def __init__(self, config: dict[str, Any] = {}, **kwargs):
        # _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)
        super().__init__(config=config, ofSubstance=Constituent.CH4, **kwargs)
