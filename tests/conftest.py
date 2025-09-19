"""
Glue routines to simulate package setup and teardown.
"""

import pytest
import _pytest  # type: ignore[import]
import logging

_log = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown_package():
    _log.debug("setup package")
    yield
    _log.debug("teardown package")


def pytest_configure(config: _pytest.config.Config) -> None:
    _log.debug("pytest_configure")


def pytest_unconfigure() -> None:
    _log.debug("pytest_unconfigure")
