from rdflib import URIRef

from .core import P223, Node

_namespace = P223


class AirHandlingUnit(Node):
    _class_iri: URIRef = P223["Application-AirHandlingUnit"]


class Boiler(Node):
    _class_iri: URIRef = P223["Application-Boiler"]


class Chiller(Node):
    _class_iri: URIRef = P223["Application-Chiller"]


class CoolingTower(Node):
    _class_iri: URIRef = P223["Application-CoolingTower"]


class FumeHood(Node):
    _class_iri: URIRef = P223["Application-FumeHood"]


class Furnace(Node):
    _class_iri: URIRef = P223["Application-Furnace"]


class HeatExchanger(Node):
    _class_iri: URIRef = P223["Application-HeatExchanger"]


class HeatPump(Node):
    _class_iri: URIRef = P223["Application-HeatPump"]


class HotWaterHeater(Node):
    _class_iri: URIRef = P223["Application-HotWaterHeater"]


class AirToAirHeatPump(HeatPump):
    _class_iri: URIRef = P223["HeatPump-AirToAirHeatPump"]


class GroundToAirHeatPump(HeatPump):
    _class_iri: URIRef = P223["HeatPump-GroundToAirHeatPump"]


class WaterToAirHeatPump(HeatPump):
    _class_iri: URIRef = P223["HeatPump-WaterToAirHeatPump"]


class WaterToWaterHeatPump(HeatPump):
    _class_iri: URIRef = P223["HeatPump-WaterToWaterHeatPump"]


class TerminalUnit(Node):
    _class_iri: URIRef = P223["Application-TerminalUnit"]


class FanCoilUnit(TerminalUnit):
    _class_iri: URIRef = P223["TerminalUnitApplication-FanCoilUnit"]


class FanPoweredTerminal(TerminalUnit):
    _class_iri: URIRef = P223["TerminalUnitApplication-FanPoweredTerminal"]


class SingleDuctTerminal(TerminalUnit):
    _class_iri: URIRef = P223["TerminalUnitApplication-SingleDuctTerminal"]


class DualDuctTerminal(TerminalUnit):
    _class_iri: URIRef = P223["TerminalUnitApplication-DualDuctTerminal"]


class ElectricalDistribution(Node):
    _class_iri: URIRef = P223["Application-ElectricalDistribution"]


class ElectricalPanel(ElectricalDistribution):
    _class_iri: URIRef = P223["ElectricalDistribution-ElectricalPanel"]
