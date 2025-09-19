from typing import Dict


from bob.enum import ElectricalPhaseIdentifier, Aspect
from bob.properties import ElectricPowerkW
from bob.properties.electricity import Amps

from ...connections import electricity as elec_cnx
from ...core import (
    BOB,
    P223,
    S223,
    Equipment,
    System,
    QuantifiableObservableProperty,
)

_namespace = BOB


class Transformer(Equipment):
    _class_iri = S223.ElectricTransformer
    hasPower: ElectricPowerkW

    def __init__(self, config: Dict = {}, **kwargs):
        kwargs = {**config.get("params", {}), **kwargs}
        _electricalInlet = kwargs.pop("electricalInlet")
        _electricalOutlet = kwargs.pop("electricalOutlet")

        super().__init__(config, **kwargs)

        self.electricalInlet = _electricalInlet(
            self, label=f"{self.label}.electricalInlet"
        )
        self.electricalOutlet = _electricalOutlet(
            self, label=f"{self.label}.electricalOutlet"
        )


class SinglePhaseDistributionPanel(System):
    _class_iri = P223.ElectricalDistributionPanel
    manufacturer: str
    modelNumber: str
    number_of_circuits: QuantifiableObservableProperty

    # Bus Bar
    _cross_ref = {
        "120_240": (
            elec_cnx.Electricity_120VLN_1Ph_60HzConnection,
            elec_cnx.Electricity_120VLN_1Ph_60HzConnection,
            elec_cnx.Electricity_240VLL_1Ph_60HzConnection,
        ),
        "240": (
            elec_cnx.Electricity_120VLN_1Ph_60HzConnection,
            elec_cnx.Electricity_120VLN_1Ph_60HzConnection,
            elec_cnx.Electricity_240VLL_1Ph_60HzConnection,
        ),
    }

    def __init__(self, config: Dict = {}, **kwargs) -> None:
        kwargs = {**config.get("params", {}), **kwargs}
        voltage = kwargs.pop("voltage")

        # look up the connection point classes
        _electricalBusA, _electricalBusB, _electricalBusAB = self._cross_ref[
            str(voltage)
        ]

        super().__init__(config, **kwargs)

        self.electricalBusA = _electricalBusA(label=f"{self.label}.electricalBusA")
        self.electricalBusB = _electricalBusB(label=f"{self.label}.electricalBusB")
        self.electricalBusAB = _electricalBusAB(label=f"{self.label}.electricalBusAB")

        self.electricalBusA.electrical_phase(ElectricalPhaseIdentifier.A)
        self.electricalBusB.electrical_phase(ElectricalPhaseIdentifier.B)
        self.electricalBusAB.electrical_phase(ElectricalPhaseIdentifier.AB)

        for _lit, circuit_breaker in self._contents.items():
            if isinstance(circuit_breaker, TwoPolesMainCircuitBreaker):
                circuit_breaker.electricalOutletA >> self.electricalBusA
                circuit_breaker.electricalOutletB >> self.electricalBusB
                circuit_breaker.electricalOutlet >> self.electricalBusAB
            elif isinstance(circuit_breaker, TwoPolesCircuitBreaker):
                self.electricalBusAB >> circuit_breaker
            elif isinstance(circuit_breaker, SinglePoleCircuitBreaker):
                if circuit_breaker._bus_bar in ("A", "odd"):
                    self.electricalBusA >> circuit_breaker
                else:
                    self.electricalBusB >> circuit_breaker
            elif isinstance(circuit_breaker, TandemSinglePoleCircuitBreaker):
                if circuit_breaker._bus_bar in ("A", "odd"):
                    self.electricalBusA >> circuit_breaker
                else:
                    self.electricalBusB >> circuit_breaker


class ThreePhaseDistributionPanel(System):
    _class_iri = P223.ElectricalDistributionPanel
    manufacturer: str
    modelNumber: str
    number_of_circuits: QuantifiableObservableProperty

    # Bus Bar
    _cross_ref = {
        "HighLeg": (
            elec_cnx.Electricity_120VLN_1Ph_60HzConnection,
            elec_cnx.Electricity_120VLN_1Ph_60HzConnection,
            elec_cnx.Electricity_208VLL_1Ph_60HzConnection,
            elec_cnx.Electricity_240VLL_1Ph_60HzConnection,
            elec_cnx.Electricity_240VLL_1Ph_60HzConnection,
            elec_cnx.Electricity_240VLL_1Ph_60HzConnection,
            elec_cnx.Electricity_240VLL_3Ph_60HzConnection,
        ),
        "208": (
            elec_cnx.Electricity_120VLN_1Ph_60HzConnection,
            elec_cnx.Electricity_120VLN_1Ph_60HzConnection,
            elec_cnx.Electricity_120VLN_1Ph_60HzConnection,
            elec_cnx.Electricity_208VLL_1Ph_60HzConnection,
            elec_cnx.Electricity_208VLL_1Ph_60HzConnection,
            elec_cnx.Electricity_208VLL_1Ph_60HzConnection,
            elec_cnx.Electricity_208VLL_1Ph_60HzConnection,
        ),
        "575": (
            (elec_cnx.Electricity_347VLN_1Ph_60HzConnection),
            (elec_cnx.Electricity_347VLN_1Ph_60HzConnection),
            (elec_cnx.Electricity_347VLN_1Ph_60HzConnection),
            elec_cnx.Electricity_600VLL_1Ph_60HzConnection,
            (elec_cnx.Electricity_600VLL_1Ph_60HzConnection),
            (elec_cnx.Electricity_600VLL_1Ph_60HzConnection),
            (elec_cnx.Electricity_600VLL_3Ph_60HzConnection),
        ),
        "600": (
            (elec_cnx.Electricity_347VLN_1Ph_60HzConnection),
            (elec_cnx.Electricity_347VLN_1Ph_60HzConnection),
            (elec_cnx.Electricity_347VLN_1Ph_60HzConnection),
            elec_cnx.Electricity_600VLL_1Ph_60HzConnection,
            (elec_cnx.Electricity_600VLL_1Ph_60HzConnection),
            (elec_cnx.Electricity_600VLL_1Ph_60HzConnection),
            (elec_cnx.Electricity_600VLL_3Ph_60HzConnection),
            elec_cnx.Electricity_6000VLL_1Ph_60HzConnection,
        ),
    }

    def __init__(self, config: Dict = {}, **kwargs) -> None:
        kwargs = {**config.get("params", {}), **kwargs}
        voltage = kwargs.pop("voltage")

        # look up the connection point classes
        (
            _electricalBusA,
            _electricalBusB,
            _electricalBusC,
            _electricalBusAB,
            _electricalBusBC,
            _electricalBusCA,
            _electricalBusABC,
        ) = self._cross_ref[str(voltage)]

        super().__init__(config, **kwargs)

        self.electricalBusA = _electricalBusA(label=f"{self.label}.electricalBusA")
        self.electricalBusB = _electricalBusB(label=f"{self.label}.electricalBusB")
        self.electricalBusC = _electricalBusC(label=f"{self.label}.electricalBusC")
        self.electricalBusAB = _electricalBusAB(label=f"{self.label}.electricalBusAB")
        self.electricalBusBC = _electricalBusBC(label=f"{self.label}.electricalBusBC")
        self.electricalBusCA = _electricalBusCA(label=f"{self.label}.electricalBusCA")
        self.electricalBusABC = _electricalBusABC(
            label=f"{self.label}.electricalBusABC"
        )

        self.electricalBusA.electrical_phase(ElectricalPhaseIdentifier.A)
        self.electricalBusB.electrical_phase(ElectricalPhaseIdentifier.B)
        self.electricalBusC.electrical_phase(ElectricalPhaseIdentifier.C)
        self.electricalBusAB.electrical_phase(ElectricalPhaseIdentifier.AB)
        self.electricalBusBC.electrical_phase(ElectricalPhaseIdentifier.BC)
        self.electricalBusCA.electrical_phase(ElectricalPhaseIdentifier.CA)
        self.electricalBusABC.electrical_phase(ElectricalPhaseIdentifier.ABC)

        for lit, circuit_breaker in self._contents.items():
            if isinstance(circuit_breaker, ThreePolesMainCircuitBreaker):
                circuit_breaker.electricalOutletA >> self.electricalBusA
                circuit_breaker.electricalOutletB >> self.electricalBusB
                circuit_breaker.electricalOutletC >> self.electricalBusC
                circuit_breaker.electricalOutletAB >> self.electricalBusAB
                circuit_breaker.electricalOutletBC >> self.electricalBusBC
                circuit_breaker.electricalOutletCA >> self.electricalBusCA
                circuit_breaker.electricalOutlet >> self.electricalBusABC
            elif isinstance(circuit_breaker, ThreePolesCircuitBreaker):
                self.electricalBusABC >> circuit_breaker
            elif isinstance(circuit_breaker, SinglePoleCircuitBreaker):
                if circuit_breaker._bus_bar == "A":
                    self.electricalBusA >> circuit_breaker
                elif circuit_breaker._bus_bar == "B":
                    self.electricalBusB >> circuit_breaker
                else:
                    self.electricalBusC >> circuit_breaker
            elif isinstance(circuit_breaker, TwoPolesCircuitBreaker):
                if circuit_breaker._bus_bar == "AB":
                    self.electricalBusAB >> circuit_breaker
                elif circuit_breaker._bus_bar == "BC":
                    self.electricalBusBC >> circuit_breaker
                else:
                    self.electricalBusCA >> circuit_breaker


class CircuitBreaker(Equipment):
    _class_iri = S223.ElectricBreaker
    # electricalInlet: ElectricalInletConnectionPoint
    # electricalOutlet: ElectricalOutletConnectionPoint
    currentRating: Amps

    def __init__(self, config: Dict = {}, **kwargs):
        kwargs = {**config.get("params", {}), **kwargs}
        amps = kwargs.pop("amps")

        super().__init__(config, **kwargs)

        self.currentRating = Amps(
            amps, label="Current rating of breaker", hasAspect=Aspect.Nominal
        )


class SinglePoleCircuitBreaker(CircuitBreaker):
    """
    One inlet and one outlet
    hasMaxRange = current max of breaker
    A rule could check inlet and outlet are same class

    208V single pole available in the High Leg Configuration
    """

    _cross_ref = {
        "120": (
            elec_cnx.Electricity_120VLN_1Ph_60HzInletConnectionPoint,
            elec_cnx.Electricity_120VLN_1Ph_60HzOutletConnectionPoint,
        ),
        "208": (
            elec_cnx.Electricity_208VLL_1Ph_60HzInletConnectionPoint,
            elec_cnx.Electricity_208VLL_1Ph_60HzOutletConnectionPoint,
        ),
        "277": (
            elec_cnx.Electricity_277VLN_1Ph_60HzInletConnectionPoint,
            elec_cnx.Electricity_277VLN_1Ph_60HzOutletConnectionPoint,
        ),
        "347": (
            elec_cnx.Electricity_347VLN_1Ph_60HzInletConnectionPoint,
            elec_cnx.Electricity_347VLN_1Ph_60HzOutletConnectionPoint,
        ),
    }

    def __init__(self, config: Dict = {}, **kwargs):
        kwargs = {**config.get("params", {}), **kwargs}
        voltage = kwargs.pop("voltage")
        self._bus_bar = kwargs.pop("bus_bar")

        # look up the inlet and outlet classes
        _electricalInlet, _electricalOutlet = self._cross_ref[str(voltage)]

        super().__init__(config, **kwargs)

        self.electricalInlet = _electricalInlet(
            self, label=f"{self.label}.electricalInlet"
        )
        self.electricalOutlet = _electricalOutlet(
            self, label=f"{self.label}.electricalOutlet"
        )


class TandemSinglePoleCircuitBreaker(CircuitBreaker):
    """
    One inlet and two outlets, also known as Twin breakers
    hasMaxRange = current max of breaker
    A rule could check inlet and outlets are same class
    """

    _cross_ref = {
        "120": (
            elec_cnx.Electricity_120VLN_1Ph_60HzInletConnectionPoint,
            elec_cnx.Electricity_120VLN_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_120VLN_1Ph_60HzOutletConnectionPoint,
        ),
    }

    def __init__(self, config: Dict = {}, **kwargs):
        kwargs = {**config.get("params", {}), **kwargs}
        voltage = kwargs.pop("voltage")
        self._bus_bar = kwargs.pop("bus_bar")

        # look up the inlet and outlet classes
        _electricalInlet, _electricalOutletA, _electricalOutletB = self._cross_ref[
            str(voltage)
        ]

        super().__init__(config, **kwargs)

        self.electricalInlet = _electricalInlet(
            self, label=f"{self.label}.electricalInlet"
        )
        self.electricalOutletA = _electricalOutletA(
            self, label=f"{self.label}.electricalOutlet"
        )
        self.electricalOutletB = _electricalOutletB(
            self, label=f"{self.label}.electricalOutlet"
        )


class TwoPolesCircuitBreaker(CircuitBreaker):
    """
    One electrical Inlet because when plugin the breaker
    in the panel, you get no choice. Both poles are connected
    at the same time. Electricity is fed from 2 bus bar (2 x 120V)
    Could also use 208V instead of 240V...
    """

    _cross_ref = {
        "208": (
            elec_cnx.Electricity_208VLL_1Ph_60HzInletConnectionPoint,
            elec_cnx.Electricity_208VLL_1Ph_60HzOutletConnectionPoint,
        ),
        "240": (
            elec_cnx.Electricity_240VLL_1Ph_60HzInletConnectionPoint,
            elec_cnx.Electricity_240VLL_1Ph_60HzOutletConnectionPoint,
        ),
        "480": (
            elec_cnx.Electricity_480VLL_1Ph_60HzInletConnectionPoint,
            elec_cnx.Electricity_480VLL_1Ph_60HzOutletConnectionPoint,
        ),
        "600": (
            elec_cnx.Electricity_600VLL_1Ph_60HzInletConnectionPoint,
            elec_cnx.Electricity_600VLL_1Ph_60HzOutletConnectionPoint,
        ),
    }

    def __init__(self, config: Dict = {}, **kwargs):
        kwargs = {**config.get("params", {}), **kwargs}
        voltage = kwargs.pop("voltage")
        self._bus_bar = kwargs.pop("bus_bar", "AB")

        # look up the connection point classes
        _electricalInlet, _electricalOutlet = self._cross_ref[str(voltage)]

        super().__init__(config, **kwargs)

        self.electricalInlet = _electricalInlet(
            self, label=f"{self.label}.electricalInlet"
        )
        self.electricalOutlet = _electricalOutlet(
            self, label=f"{self.label}.electricalOutlet"
        )


class TwoPolesMainCircuitBreaker(CircuitBreaker):
    """
    A 2 poles Main circuit breaker is modeled differently as I
    wanted to illustrate the fact that it will be connected to
    the 2 bus bars in the panel (A & B) and will also be connected
    to AB. It is really a modeling trick.
    """

    # _cross_ref will map the right voltages to input and bus bars
    _cross_ref = {
        "120_240": (
            elec_cnx.Electricity_240VLL_120VLN_1Ph_60HzInletConnectionPoint,
            elec_cnx.Electricity_120VLN_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_120VLN_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_240VLL_1Ph_60HzOutletConnectionPoint,
        ),
        "240": (
            elec_cnx.Electricity_240VLL_1Ph_60HzInletConnectionPoint,
            elec_cnx.Electricity_120VLN_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_120VLN_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_240VLL_1Ph_60HzOutletConnectionPoint,
        ),
    }

    def __init__(self, config: Dict = {}, **kwargs):
        kwargs = {**config.get("params", {}), **kwargs}
        voltage = kwargs.pop("voltage")

        # look up the connection point classes
        (
            _electricalInlet,
            _electricalOutletA,
            _electricalOutletB,
            _electricalOutlet,
        ) = self._cross_ref[str(voltage)]

        super().__init__(**kwargs)

        self.electricalInlet = _electricalInlet(
            self, label=f"{self.label}.electricalInlet"
        )
        self.electricalOutletA = _electricalOutletA(
            self, label=f"{self.label}.electricalOutlet_LineA_Neutral"
        )
        self.electricalOutletB = _electricalOutletB(
            self, label=f"{self.label}.electricalOutlet_LineB_Neutral"
        )

        self.electricalOutlet = _electricalOutlet(
            self, label=f"{self.label}.electricalOutlet_LineA_LineB"
        )

        self.electricalInlet.electrical_phase(ElectricalPhaseIdentifier.AB)
        self.electricalOutletA.electrical_phase(ElectricalPhaseIdentifier.A)
        self.electricalOutletB.electrical_phase(ElectricalPhaseIdentifier.B)
        self.electricalOutlet.electrical_phase(ElectricalPhaseIdentifier.AB)


class ThreePolesCircuitBreaker(CircuitBreaker):
    """
    One electrical Inlet because when plugin the breaker
    in the panel, you get no choice. Three poles are connected
    at the same time. Electricity is fed from 3 bus bars
    """

    _cross_ref = {
        "208": (
            elec_cnx.Electricity_208VLL_3Ph_60HzInletConnectionPoint,
            elec_cnx.Electricity_208VLL_3Ph_60HzOutletConnectionPoint,
        ),
        "240": (
            elec_cnx.Electricity_240VLL_3Ph_60HzInletConnectionPoint,
            elec_cnx.Electricity_240VLL_3Ph_60HzOutletConnectionPoint,
        ),
        "480": (
            elec_cnx.Electricity_480VLL_3Ph_60HzInletConnectionPoint,
            elec_cnx.Electricity_480VLL_3Ph_60HzOutletConnectionPoint,
        ),
        "575": (
            elec_cnx.Electricity_600VLL_3Ph_60HzInletConnectionPoint,
            elec_cnx.Electricity_600VLL_3Ph_60HzOutletConnectionPoint,
        ),
        "600": (
            elec_cnx.Electricity_600VLL_3Ph_60HzInletConnectionPoint,
            elec_cnx.Electricity_600VLL_3Ph_60HzOutletConnectionPoint,
        ),
    }

    def __init__(self, config: Dict = {}, **kwargs):
        kwargs = {**config.get("params", {}), **kwargs}
        voltage = kwargs.pop("voltage")

        # look up the connection point classes
        _electricalInlet, _electricalOutlet = self._cross_ref[str(voltage)]

        super().__init__(config, **kwargs)

        self.electricalInlet = _electricalInlet(
            self, label=f"{self.label}.electricalInlet"
        )

        self.electricalOutlet = _electricalOutlet(
            self, label=f"{self.label}.electricalOutlet"
        )


class ThreePolesMainCircuitBreaker(CircuitBreaker):
    """
    One electrical Inlet because when plugin the breaker
    in the panel, you get no choice. Three poles are connected
    at the same time. Electricity is fed from 3 bus bar (3 x 347V to neutral for example)

    Code do not allow to use only one pole of a 3phase breaker. So
    this model is just a trick so we can feed 3 bus bar (connect) inside the panel.
    If not, we would have 3 connections coming from vaccuum of space.

    """

    # _cross_ref will map the right voltages to input and bus bars
    _cross_ref = {
        "HighLeg": (
            elec_cnx.Electricity_240VLL_208VLN_120VLN_3Ph_60HzInletConnectionPoint,
            elec_cnx.Electricity_120VLN_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_120VLN_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_208VLL_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_240VLL_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_240VLL_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_240VLL_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_240VLL_3Ph_60HzOutletConnectionPoint,
        ),
        "208": (
            elec_cnx.Electricity_208VLL_3Ph_60HzInletConnectionPoint,
            elec_cnx.Electricity_120VLN_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_120VLN_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_120VLN_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_208VLL_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_208VLL_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_208VLL_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_208VLL_3Ph_60HzOutletConnectionPoint,
        ),
        "480": (
            elec_cnx.Electricity_480VLL_3Ph_60HzInletConnectionPoint,
            elec_cnx.Electricity_277VLN_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_277VLN_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_277VLN_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_480VLL_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_480VLL_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_480VLL_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_480VLL_3Ph_60HzOutletConnectionPoint,
        ),
        "575": (
            elec_cnx.Electricity_600VLL_3Ph_60HzInletConnectionPoint,
            elec_cnx.Electricity_347VLN_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_347VLN_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_347VLN_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_600VLL_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_600VLL_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_600VLL_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_600VLL_3Ph_60HzOutletConnectionPoint,
        ),
        "600": (
            elec_cnx.Electricity_600VLL_3Ph_60HzInletConnectionPoint,
            elec_cnx.Electricity_347VLN_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_347VLN_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_347VLN_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_600VLL_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_600VLL_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_600VLL_1Ph_60HzOutletConnectionPoint,
            elec_cnx.Electricity_600VLL_3Ph_60HzOutletConnectionPoint,
        ),
    }

    def __init__(self, config: Dict = {}, **kwargs):
        kwargs = {**config.get("params", {}), **kwargs}
        voltage = kwargs.pop("voltage")

        # look up the connection point classes
        (
            _electricalInlet,
            _electricalOutletA,
            _electricalOutletB,
            _electricalOutletC,
            _electricalOutletAB,
            _electricalOutletBC,
            _electricalOutletCA,
            _electricalOutlet,
        ) = self._cross_ref[str(voltage)]

        super().__init__(config, **kwargs)

        self.electricalInlet = _electricalInlet(
            self, label=f"{self.label}.electricalInlet"
        )
        self.electricalOutletA = _electricalOutletA(
            self, label=f"{self.label}.electricalOutletA"
        )
        self.electricalOutletB = _electricalOutletB(
            self, label=f"{self.label}.electricalOutletB"
        )
        self.electricalOutletC = _electricalOutletC(
            self, label=f"{self.label}.electricalOutletC"
        )
        self.electricalOutletAB = _electricalOutletAB(
            self, label=f"{self.label}.electricalOutletAB"
        )
        self.electricalOutletBC = _electricalOutletBC(
            self, label=f"{self.label}.electricalOutletBC"
        )
        self.electricalOutletCA = _electricalOutletCA(
            self, label=f"{self.label}.electricalOutletCA"
        )
        self.electricalOutlet = _electricalOutlet(
            self, label=f"{self.label}.electricalOutletABC"
        )

        self.electricalOutletA.electrical_phase(ElectricalPhaseIdentifier.A)
        self.electricalOutletB.electrical_phase(ElectricalPhaseIdentifier.B)
        self.electricalOutletC.electrical_phase(ElectricalPhaseIdentifier.C)
        self.electricalOutletAB.electrical_phase(ElectricalPhaseIdentifier.AB)
        self.electricalOutletBC.electrical_phase(ElectricalPhaseIdentifier.BC)
        self.electricalOutletCA.electrical_phase(ElectricalPhaseIdentifier.CA)
        self.electricalOutlet.electrical_phase(ElectricalPhaseIdentifier.ABC)


# Define breaker in template
SinglePhasePanel_config = {
    "params": {
        "label": "My Panel",
        "comment": "Description of my panel",
        "voltage": 120_240,
    },
    "sensors": {},
    "equipment": {
        ("MainBreaker", TwoPolesMainCircuitBreaker): {
            "comment": "Main breaker of panel",
            "amps": 200,
            "voltage": 240,
        },
        ("CB#1", SinglePoleCircuitBreaker): {
            "comment": "Lights",
            "amps": 15,
            "voltage": 120,
            "bus_bar": "A",
        },
        ("CB#2", TwoPolesCircuitBreaker): {
            "comment": "Heater",
            "amps": 20,
            "voltage": 240,
        },
    },
    # other properties could go there... ?
}

# Define breaker in template
ThreePhasePanel_config = {
    "params": {
        "label": "My Panel",
        "comment": "Description of my panel",
        "voltage": 575,
    },
    "sensors": {},
    "equipment": {
        ("MainBreaker", ThreePolesMainCircuitBreaker): {
            "comment": "Main breaker of panel",
            "amps": 200,
            "voltage": 575,
        },
        ("CB#1", SinglePoleCircuitBreaker): {
            "comment": "Lights",
            "amps": 15,
            "voltage": 347,
            "bus_bar": "A",
        },
        ("CB#2", ThreePolesCircuitBreaker): {
            "comment": "Heater",
            "amps": 40,
            "voltage": 575,
        },
    },
    # other properties could go there... ?
}
