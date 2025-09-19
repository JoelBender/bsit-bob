"""
Test Module Template
--------------------
"""

import unittest
import logging

from typing import Callable, Any

_log = logging.getLogger(__name__)


def setup_module() -> None:
    """
    This function is called once at the beginning of all of the tests in this
    module.
    """
    _log.debug("setup_module")


def teardown_module() -> None:
    """
    This function is called once at the end of the tests in this module.
    """
    _log.debug("teardown_module")


def setup_function(function: Callable[..., Any]) -> None:
    """
    This function is called before each module level test function.
    """
    _log.debug("setup_function %r", function)


def teardown_function(function: Callable[..., Any]) -> None:
    """
    This function is called after each module level test function.
    """
    _log.debug("teardown_function %r", function)


def test_some_function(*args: Any, **kwargs: Any) -> None:
    """
    This is a module level test function.
    """
    _log.debug("test_some_function %r %r", args, kwargs)


class TestCaseTemplate(unittest.TestCase):
    @classmethod
    def setup_class(cls) -> None:
        """
        This function is called once before the test case is instantiated
        for each of the tests.
        """
        _log.debug("setup_class")

    @classmethod
    def teardown_class(cls) -> None:
        """
        This function is called once at the end after the last instance
        of the test case has been abandon.
        """
        _log.debug("teardown_class")

    def setup_method(self, method: Callable[..., Any]) -> None:
        """
        This function is called before each test method is called as is
        given a reference to the test method.
        """
        _log.debug("setup_method %r", method)

    def teardown_method(self, method: Callable[..., Any]) -> None:
        """
        This function is called after each test method has been called and
        is given a reference to the test method.
        """
        _log.debug("teardown_method %r", method)

    def test_something(self) -> None:
        """
        This is a method level test function.
        """
        _log.debug("test_something")

    def test_something_else(self) -> None:
        """
        This is another method level test function.
        """
        _log.debug("test_something_else")
