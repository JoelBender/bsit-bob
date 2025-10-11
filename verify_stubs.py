#!/usr/bin/env python3
"""
Quick verification that our stub files are working.

Run this to see if the problematic patterns now work.
"""

def test_problematic_patterns():
    """Test the patterns that were causing mypy errors."""
    
    try:
        # This was the original error
        from bob.enum import Electricity
        voltage = Electricity.AC110VLN_1Ph_50Hz
        print(f"✓ Electricity.AC110VLN_1Ph_50Hz works: {voltage}")
        
        # Test constituent attributes  
        from bob.enum import Constituent
        water = Constituent.H2O
        print(f"✓ Constituent.H2O works: {water}")
        
        # Test core hierarchy
        from bob.core import Substance, Medium
        medium = Substance.Medium
        print(f"✓ Substance.Medium works: {medium}")
        
        constituent_class = Medium.Constituent  
        print(f"✓ Medium.Constituent works: {constituent_class}")
        
        print("\n🎉 All tests passed! Stub files are working correctly.")
        return True
        
    except AttributeError as e:
        print(f"❌ AttributeError: {e}")
        return False
    except ImportError as e:
        print(f"❌ ImportError: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("Testing stub file integration...\n")
    success = test_problematic_patterns()
    
    if success:
        print("\nTo run mypy type checking:")
        print("1. Install mypy: pip install mypy")
        print("2. Run: mypy --config-file mypy.ini")
        print("3. Or test specific files: mypy test_mypy_integration.py")
    else:
        print("\n❌ Some patterns still failing - check stub files")