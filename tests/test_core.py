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


@pytest.fixture
def multiple_contributors():
    """Defining 5 contributors of

    Returns
    -------
    List[core.Contributor]
        Contributor objects to be used in transactions
    """
    multiple_c = []
    for i in range(5):
        multiple_c.append(core.Contributor("Contributor"+str(i),email=str(i)+"@example.com"))
    return multiple_c


def test_all_different(multiple_contributors):
    assert len(set(multiple_contributors))==len(multiple_contributors)

@pytest.fixture
def normal_amount():
    return 150.0

@pytest.fixture
def abnormal_amount():
    return "23"

def test_normal_transaction(normal_amount,multiple_contributors):
    t = core.Transaction(normal_amount,multiple_contributors[0],multiple_contributors)
    assert len(t.contributors)


def test_string_amount_transaction(abnormal_amount,multiple_contributors):
    with pytest.raises(TypeError): # should raise TypeError
        t = core.Transaction(abnormal_amount,multiple_contributors[0],multiple_contributors)







