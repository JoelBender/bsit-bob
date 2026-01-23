"""Test file to verify mypy integration with our stub files.

This file contains examples of the code patterns that were causing mypy errors
and should now work correctly with our .pyi stub files.
"""

# Test imports
from bob.core import Medium, Substance
from bob.enum import EM, Constituent, Electricity


def test_constituent_attributes() -> None:
    """Test that Constituent class attributes are recognized by mypy."""
    # These should not cause mypy errors anymore
    h2o = Constituent.H2O
    co2 = Constituent.CO2
    oxygen = Constituent.O2

    # Test some refrigerants
    r22 = Constituent.R22
    r410a = Constituent.R410A

    print(f"Water: {h2o}")
    print(f"CO2: {co2}")
    print(f"oxygen: {oxygen}")
    print(f"r22: {r22}")
    print(f"r410a: {r410a}")

def test_electricity_attributes() -> None:
    """Test that Electricity class attributes are recognized by mypy."""
    # This was the original error case
    voltage_110 = Electricity.AC110VLN_1Ph_50Hz
    voltage_120 = Electricity.AC120VLN_1Ph_60Hz

    # Test AC/DC base types
    ac_base = Electricity.AC
    dc_base = Electricity.DC

    # Test DC voltages
    dc12v = Electricity.DC12V
    dc24v = Electricity.DC24V

    print(f"110V AC: {voltage_110}")
    print(f"120V AC: {voltage_120}")
    print(f"12V DC: {dc12v}")
    print(f"24V DC: {dc24v}")

def test_electromagnetic_attributes() -> None:
    """Test that EM class attributes are recognized by mypy."""
    light = EM.Light
    microwave = EM.Microwave
    rf = EM.RF

    print(f"Light: {light}")
    print(f"Microwave: {microwave}")
    print(f"RF: {rf}")

def test_core_hierarchy() -> None:
    """Test that core enumeration hierarchy is recognized by mypy."""
    # Test Substance.Medium
    medium = Substance.Medium

    # Test Medium.Constituent
    constituent_class = Medium.Constituent

    # Test Medium.Mix
    mix_class = Medium.Mix

    print(f"Medium: {medium}")
    print(f"Constituent class: {constituent_class}")
    print(f"Mix: {mix_class}")

def test_electrical_connections() -> None:
    """Test electrical connection pattern that was causing the original error."""
    from bob.connections.electricity import Electricity_110VLN_1Ph_50HzConnection

    # This should work without mypy errors
    connection = Electricity_110VLN_1Ph_50HzConnection()
    print(f"Connection medium: {connection.hasMedium}")

if __name__ == "__main__":
    print("Testing mypy integration...")

    test_constituent_attributes()
    test_electricity_attributes()
    test_electromagnetic_attributes()
    test_core_hierarchy()

    # Uncomment this if you have the connections module
    # test_electrical_connections()

    print("All tests completed!")
