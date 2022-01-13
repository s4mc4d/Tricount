import pytest
import sys
import pathlib
import pandas as pd

SRC_LOCATION = pathlib.Path(__file__).parent.parent
print(SRC_LOCATION)
sys.path.insert(0,str(SRC_LOCATION))

from tricount import core

## ---- Testing contributors

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
    """Defining 5 contributors

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

##-----Testing transactions

@pytest.fixture
def normal_amount():
    return 100.0

@pytest.fixture
def abnormal_amount():
    return "a"

def test_normal_transaction(normal_amount,multiple_contributors):
    t = core.Transaction(normal_amount,multiple_contributors[0],multiple_contributors)
    assert len(t.contributors)

def test_transaction_amount_type_error(abnormal_amount,multiple_contributors):
    with pytest.raises(TypeError): # should raise TypeError
        t = core.Transaction(abnormal_amount,multiple_contributors[0],multiple_contributors)


@pytest.fixture
def pair_of_contributors():
    Jacques = core.Contributor(name="Jacques")
    Toto = core.Contributor(name="Toto")
    return [Toto,Jacques]

@pytest.fixture
def transaction_from_2_contributors(pair_of_contributors):
    return core.Transaction(100,pair_of_contributors[0],[pair_of_contributors[0],pair_of_contributors[1]])

def test_transaction_balance_type(transaction_from_2_contributors):    
    assert isinstance(transaction_from_2_contributors.balance,pd.DataFrame)

def test_transaction_balance_value_unique(transaction_from_2_contributors):
    # CHeck that there is only 1 value in total_amount column
    assert len(transaction_from_2_contributors.balance.total_amount.unique())==1

def test_transaction_balance_value_is_valid_for_2_contrib(transaction_from_2_contributors):
    df_balance = transaction_from_2_contributors.balance
    second_contributor = transaction_from_2_contributors.contributors[1]
    assert df_balance.loc[df_balance.contributor==second_contributor,"value"].values[0]*2==100.0

def test_transaction_balance_has_only_2_contributors(transaction_from_2_contributors):
    df_balance = transaction_from_2_contributors.balance
    assert len(df_balance.contributor.unique())==2



## ------Testing Expenses

@pytest.fixture
def ten_transactions(multiple_contributors):
    pass






