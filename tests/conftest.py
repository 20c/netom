import os

import pytest


@pytest.fixture
def this_dir():
    return os.path.dirname(__file__)
