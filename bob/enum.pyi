from typing import Any, TypeAlias

from .core import Constituent as _Constituent

# Define the constituent type with all dynamic attributes
class ConstituentType(_Constituent):
    def __getattr__(self, name: str) -> Any: ...  # Catch-all for dynamic attributes

    # Water and vapor
    H2O: Any
    Vapor_H2O: Any

    # Oils and particles
    Oil: Any
    Smoke: Any

    # Gases
    Ar: Any  # Argon
    CO: Any  # Carbon monoxide
    CO2: Any  # Carbon dioxide
    NOX: Any  # Nitrogen oxides
    CH4: Any  # Methane
    NH3: Any  # Ammonia
    H2S: Any  # Hydrogen sulfide
    O2: Any  # Oxygen
    O3: Any  # Ozone
    SO2: Any  # Sulfur dioxide
    N: Any  # Nitrogen
    VOC: Any  # Volatile Organic Compounds
    Radon: Any

    # Refrigerants
    R22: Any
    R134A: Any
    R410A: Any
    R32: Any

    # Other
    Glycol: Any

# Electromagnetic constituent type
class EMType(_Constituent):
    def __getattr__(self, name: str) -> Any: ...  # Catch-all for dynamic attributes
    Light: Any
    Microwave: Any
    RF: Any

class ElectricityType(_Constituent):
    def __getattr__(self, name: str) -> Any: ...  # Catch-all for dynamic attributes
    # Base types
    AC: Any
    DC: Any

    # AC voltage types - all dynamically created
    AC10000VLL_1Ph_60Hz: Any
    AC10000VLL_3Ph_60Hz: Any
    AC10000VLL_5770VLN_1Ph_60Hz: Any
    AC10000VLL_5770VLN_3Ph_60Hz: Any
    AC110VLN_1Ph_50Hz: Any
    AC120VLN_1Ph_60Hz: Any
    AC127VLN_1Ph_50Hz: Any
    AC139VLN_1Ph_50Hz: Any
    AC1730VLN_1Ph_60Hz: Any
    AC1900VLN_1Ph_60Hz: Any
    AC190VLL_110VLN_1Ph_50Hz: Any
    AC190VLL_110VLN_3Ph_50Hz: Any
    AC190VLL_1Ph_50Hz: Any
    AC190VLL_3Ph_50Hz: Any
    AC208VLL_120VLN_1Ph_60Hz: Any
    AC208VLL_120VLN_3Ph_60Hz: Any
    AC208VLL_1Ph_60Hz: Any
    AC208VLL_3Ph_60Hz: Any
    AC219VLN_1Ph_60Hz: Any
    AC220VLL_127VLN_1Ph_50Hz: Any
    AC220VLL_127VLN_3Ph_50Hz: Any
    AC220VLL_1Ph_50Hz: Any
    AC220VLL_3Ph_50Hz: Any
    AC231VLN_1Ph_50Hz: Any
    AC2400VLN_1Ph_60Hz: Any
    AC240VLL_120VLN_1Ph_60Hz: Any
    AC240VLL_139VLN_1Ph_50Hz: Any
    AC240VLL_139VLN_3Ph_50Hz: Any
    AC240VLL_1Ph_50Hz: Any
    AC240VLL_1Ph_60Hz: Any
    AC240VLL_208VLN_120VLN_1Ph_60Hz: Any
    AC240VLL_208VLN_120VLN_3Ph_60Hz: Any
    AC240VLL_3Ph_50Hz: Any
    AC240VLL_3Ph_60Hz: Any
    AC240VLN_1Ph_50Hz: Any
    AC24VLN_1Ph_50Hz: Any
    AC24VLN_1Ph_60Hz: Any
    AC277VLN_1Ph_60Hz: Any
    AC3000VLL_1730VLN_1Ph_60Hz: Any
    AC3000VLL_1730VLN_3Ph_60Hz: Any
    AC3000VLL_1Ph_60Hz: Any
    AC3000VLL_3Ph_60Hz: Any
    AC3300VLL_1900VLN_1Ph_60Hz: Any
    AC3300VLL_1900VLN_3Ph_60Hz: Any
    AC3300VLL_1Ph_60Hz: Any
    AC3300VLL_3Ph_60Hz: Any
    AC3460VLN_1Ph_60Hz: Any
    AC347VLN_1Ph_60Hz: Any
    AC380VLL_1Ph_60Hz: Any
    AC380VLL_219VLN_1Ph_60Hz: Any
    AC380VLL_219VLN_3Ph_60Hz: Any
    AC380VLL_3Ph_60Hz: Any
    AC3810VLN_1Ph_60Hz: Any
    AC400VLL_1Ph_50Hz: Any
    AC400VLL_231VLN_1Ph_50Hz: Any
    AC400VLL_231VLN_3Ph_50Hz: Any
    AC400VLL_3Ph_50Hz: Any
    AC415VLL_1Ph_50Hz: Any
    AC415VLL_240VLN_1Ph_50Hz: Any
    AC415VLL_240VLN_3Ph_50Hz: Any
    AC415VLL_3Ph_50Hz: Any
    AC4160VLL_1Ph_60Hz: Any
    AC4160VLL_2400VLN_1Ph_60Hz: Any
    AC4160VLL_2400VLN_3Ph_60Hz: Any
    AC4160VLL_3Ph_60Hz: Any
    AC480VLL_1Ph_60Hz: Any
    AC480VLL_277VLN_1Ph_60Hz: Any
    AC480VLL_277VLN_3Ph_60Hz: Any
    AC480VLL_3Ph_60Hz: Any
    AC5770VLN_1Ph_60Hz: Any
    AC6000VLL_1Ph_60Hz: Any
    AC6000VLL_3460VLN_1Ph_60Hz: Any
    AC6000VLL_3460VLN_3Ph_60Hz: Any
    AC6000VLL_3Ph_60Hz: Any
    AC600VLL_1Ph_60Hz: Any
    AC600VLL_347VLN_1Ph_60Hz: Any
    AC600VLL_347VLN_3Ph_60Hz: Any
    AC600VLL_3Ph_60Hz: Any
    AC6600VLL_1Ph_60Hz: Any
    AC6600VLL_3810VLN_1Ph_60Hz: Any
    AC6600VLL_3810VLN_3Ph_60Hz: Any
    AC6600VLL_3Ph_60Hz: Any

    # DC voltage types
    DC12V: Any
    DC24V: Any
    DC380V: Any
    DC48V: Any
    DC5V: Any
    DC6V: Any

    # Other electrical types
    Earth: Any
    Neutral: Any
    Signal: Any
    OnOffSignal: Any

# Instance declarations for mypy - use Any to bypass type checking for dynamic attributes
Constituent: Any
EM: Any
Electricity: Any
Numerical: Any
Particulate: Any

# Individual constituent instances that are also available at module level
H2O: Any
Vapor_H2O: Any
Oil: Any
Smoke: Any
Argon: Any
CO: Any
CO2: Any
NOx: Any
CH4: Any
NH3: Any
H2S: Any
O2: Any
O3: Any
SO2: Any
Nitrogen: Any
VOC: Any
Radon: Any
const_R22: Any
const_R134A: Any
const_R410A: Any
const_R32: Any
Glycol: Any
Microwave: Any
RF: Any
Signal: Any

# Additional enum classes that are imported by various modules
type Motion = Any
type NormalAlarmEnum = Any
type Occupancy = Any
type OnOff = Any
type Position = Any
type YesNoEnum = Any
type Air = Any
type Medium = Any  # Medium type imported from core
type Fluid = Any
type GlycolSolution_15Percent = Any
type GlycolSolution_30Percent = Any
type Water = Any
type NaturalGas = Any
type Refrigerant = Any
type ProtocolEnum = Any
type PowerAndSignal = Any
type AnalogSignalTypeEnum = Any
type BinarySignalTypeEnum = Any
type ModulatedSignal = Any
type ElectricalPhaseIdentifier = Any

# Additional enumeration classes
class Role:
    """Role enumeration for equipment and systems"""

    def __getattr__(self, name: str) -> Any: ...

class Light:
    """Light enumeration"""

    Visible: Any
    def __getattr__(self, name: str) -> Any: ...
