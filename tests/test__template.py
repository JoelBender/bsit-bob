#!/usr/bin/env python

"""Test Module Template
--------------------
"""

import logging
import unittest
from collections.abc import Callable
from typing import Any

LOGGER = logging.getLogger(__name__)


def setup_module() -> None:
    """This function is called once at the beginning of all of the tests
    in this module.
    """
    LOGGER.debug("setup_module")  # type: ignore[attr-defined]


def teardown_module() -> None:
    """This function is called once at the end of the tests in this module."""
    LOGGER.debug("teardown_module")  # type: ignore[attr-defined]


def setup_function(function: Callable[..., Any]) -> None:
    """This function is called before each module level test function."""
    LOGGER.debug("setup_function %r", function)  # type: ignore[attr-defined]


def teardown_function(function: Callable[..., Any]) -> None:
    """This function is called after each module level test function."""
    LOGGER.debug("teardown_function %r", function)  # type: ignore[attr-defined]


def test_some_function(*args: Any, **kwargs: Any) -> None:
    """This is a module level test function."""
    LOGGER.debug("test_some_function %r %r", args, kwargs)  # type: ignore[attr-defined]


class TestCaseTemplate(unittest.TestCase):
    @classmethod
    def setup_class(cls) -> None:
        """This function is called once before the test case is instantiated
        for each of the tests.
        """
        LOGGER.debug("setup_class")

    @classmethod
    def teardown_class(cls) -> None:
        """This function is called once at the end after the last instance
        of the test case has been abandon.
        """
        LOGGER.debug("teardown_class")

    def setup_method(self, method: Callable[..., Any]) -> None:
        """This function is called before each test method is called as is
        given a reference to the test method.
        """
        LOGGER.debug("setup_method %r", method)

    def teardown_method(self, method: Callable[..., Any]) -> None:
        """This function is called after each test method has been called and
        is given a reference to the test method.
        """
        LOGGER.debug("teardown_method %r", method)

    def test_something(self) -> None:
        """This is a method level test function."""
        LOGGER.debug("test_something")

    def test_something_else(self) -> None:
        """This is another method level test function."""
        LOGGER.debug("test_something_else")
