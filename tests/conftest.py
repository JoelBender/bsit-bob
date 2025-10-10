import logging
import os
import sys
from bob.core import clear
import pytest

print("======================", sys.path)


_log = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def run_before_and_after_tests(tmpdir):
    """Be sure to clear graph after each test"""
    # Setup: fill with any logic you want

    yield  # this is where the testing happens

    clear()


@pytest.fixture(scope="session")
def bob_fixture(request):
    _log.debug("bob_fixture")

    params = {}
    params["nonconforming_samples_directory"] = os.path.join(
        os.getcwd(), "samples", "nonconforming"
    )
    params["conforming_samples_directory"] = os.path.join(
        os.getcwd(), "samples", "conforming"
    )
    params["samples_ttl_directory"] = os.path.join(
        os.getcwd(), "samples", "nonconforming", "ttl"
    )
    params["g36_directory"] = os.path.join(os.getcwd(), "G36")
    params["g36_ttl_directory"] = os.path.join(os.getcwd(), "G36", "ttl")
    params["root_directory"] = os.path.join(os.getcwd())
    yield params
    # teardown
