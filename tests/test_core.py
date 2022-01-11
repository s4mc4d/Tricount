import pytest
import sys
import pathlib

SRC_LOCATION = pathlib.Path(__file__).parent.parent
print(SRC_LOCATION)
sys.path.insert(0,str(SRC_LOCATION))

from tricount import core

@pytest.fixture
def normal_contributor():
    return core.Contributor("example_name","example_email")

@pytest.fixture
def only_name_contributor():
    return core.Contributor("example_name")

def test_contributor_name(normal_contributor):
    assert normal_contributor.name=="example_name"

def test_contributor_email(normal_contributor):
    assert normal_contributor.email=="example_email"

def test_contributor_none_email(only_name_contributor):
    assert only_name_contributor.email is None




