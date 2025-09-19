"""
Testing Utilities
-----------------
"""

import logging

# parsed test options
test_options = None


def setup_package() -> None:
    logging.debug("setup_package")


def teardown_package() -> None:
    logging.debug("teardown_package")
