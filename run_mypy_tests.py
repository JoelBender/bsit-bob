#!/usr/bin/env python3
"""MyPy testing script for bsit-bob type annotations.

This script demonstrates how to test the mypy integration and provides
several methods for running mypy checks.
"""

import subprocess
import sys
from pathlib import Path


def check_mypy_installed():
    """Check if mypy is installed."""
    try:
        result = subprocess.run([sys.executable, "-m", "mypy", "--version"],
                              check=False, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ MyPy is installed: {result.stdout.strip()}")
            return True
        print("✗ MyPy is not installed")
        return False
    except FileNotFoundError:
        print("✗ MyPy is not installed")
        return False

def install_mypy():
    """Install mypy if not present."""
    print("Installing mypy...")
    result = subprocess.run([sys.executable, "-m", "pip", "install", "mypy"], check=False)
    return result.returncode == 0

def run_mypy_on_file(file_path):
    """Run mypy on a specific file."""
    print(f"\n=== Running mypy on {file_path} ===")
    result = subprocess.run([
        sys.executable, "-m", "mypy",
        str(file_path),
        "--show-error-codes",
        "--no-error-summary",
    ], check=False, capture_output=True, text=True)

    print("STDOUT:")
    print(result.stdout)
    print("STDERR:")
    print(result.stderr)
    print(f"Return code: {result.returncode}")
    return result.returncode == 0

def run_mypy_on_module(module_path):
    """Run mypy on an entire module."""
    print(f"\n=== Running mypy on module {module_path} ===")
    result = subprocess.run([
        sys.executable, "-m", "mypy",
        str(module_path),
        "--show-error-codes",
        "--ignore-missing-imports",
    ], check=False, capture_output=True, text=True)

    print("STDOUT:")
    print(result.stdout)
    print("STDERR:")
    print(result.stderr)
    print(f"Return code: {result.returncode}")
    return result.returncode == 0

def test_specific_patterns():
    """Test specific code patterns that were causing issues."""
    test_code = """
from bob.enum import Constituent, Electricity, EM
from bob.core import Substance, Medium

# Test the original error case
voltage = Electricity.AC110VLN_1Ph_50Hz

# Test constituent attributes
water = Constituent.H2O
co2 = Constituent.CO2

# Test core hierarchy
medium = Substance.Medium
constituent_class = Medium.Constituent

print("All type checks should pass!")
"""

    # Write test code to a temporary file
    test_file = Path("temp_mypy_test.py")
    test_file.write_text(test_code)

    try:
        success = run_mypy_on_file(test_file)
        return success
    finally:
        # Clean up
        if test_file.exists():
            test_file.unlink()

def main():
    """Main testing function."""
    print("=== MyPy Integration Test for bsit-bob ===\n")

    # Check if mypy is installed
    if not check_mypy_installed():
        print("Installing mypy...")
        if not install_mypy():
            print("Failed to install mypy")
            return False

    # Test the integration file
    integration_file = Path("test_mypy_integration.py")
    if integration_file.exists():
        print("\n1. Testing integration file...")
        run_mypy_on_file(integration_file)

    # Test specific patterns
    print("\n2. Testing specific problematic patterns...")
    test_specific_patterns()

    # Test the main bob modules
    bob_path = Path("bob")
    if bob_path.exists():
        print("\n3. Testing bob/enum.py...")
        run_mypy_on_file(bob_path / "enum.py")

        print("\n4. Testing bob/core.py...")
        run_mypy_on_file(bob_path / "core.py")

        # Test connections if they exist
        connections_path = bob_path / "connections"
        if connections_path.exists():
            print("\n5. Testing bob/connections/...")
            run_mypy_on_module(connections_path)

    print("\n=== MyPy testing complete ===")

if __name__ == "__main__":
    main()
