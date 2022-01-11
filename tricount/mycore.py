"""Personal OOP version of Tricount
"""

from functools import reduce
import random
from dataclasses import dataclass, field
from typing import List
from uuid import UUID, uuid4

import faker
import pandas as pd


@dataclass   #(init=False) # enables to 
class Contributor:
    uid: UUID = field(init=False)  # deactivate init generation. Need to implement it with __post_init__
    name: str = field(compare=False)
    email : str = field(compare=False,default=None)

    # def __init__(self,name,email:str = None) -> None:
    #     self.

    # def __eq__(self, __o: object) -> bool:
    #     if isinstance(__o,Contributor):
    #         return self.uid==__o.uid

    def __hash__(self) -> int:
        return hash(self.uid)
    
    def __post_init__(self):
        self.uid = uuid4()

class Transaction:
    
    def __init__(self, amount, who : Contributor, contributors : List[Contributor] = None) -> None:
        self._type = "expense"  # by default : expense
        self._id = uuid4()
        self._amount = amount
        self._owner = who
        if contributors is None:
            self._contributors = []
        else:
            self._contributors = contributors  #  all of people involved in the transaction

    def add_contributor(self, new_contributor: Contributor):
        # updates list of contributors for transaction and recalculates balance
        if new_contributor not in self._contributors:
            self._contributors.append(new_contributor)
            self._balance()
        return True

    def remove_contributor(self, contributor_to_delete : Contributor):
        # updates list of contributors for transaction and recalculates balance
        self._contributors.remove(contributor_to_delete)
        self._balance()
        return True

    @property
    def amount(self):
        return self._amount
    
    @property
    def owner(self):
        return self._owner

    @property
    def balance(self):
        return self._balance()

    def __repr__(self):
        temp = ",".join([toto.name for toto in self._contributors])
        return f"Transaction by {self.owner},{self._amount}, for : {temp})"

    def _balance(self,uniform : bool =True):
        if uniform:
            # hypothesis : uniform distribution among contributors
            res = []  # list of transactions owings
            for contrib in self._contributors:
                contrib_value = self._amount/len(self._contributors)

                hihi = {"transaction_id":self._id,"total_amount":self._amount,
                        "creditor":self._owner,"contributor":contrib,"value":contrib_value}
                res.append(hihi)

        else:
            print("Non uniform distribution not valid")

        return pd.DataFrame(res)


class Expenses:
    def __init__(self,transactions : List[Transaction]) -> None:
        if len(transactions):
            self._transactions = transactions
            self._contributors = set([item.owner for item in transactions])
        self._balance = None

    @property
    def transactions(self):
        """Provides all transactions objects

        Returns
        -------
        List[Transactions]
            All transactons objects as list
        """
        return self._transactions

    def total(self):
        total = 0.
        for item in self._transactions:
            total += item.amount
        return total

    def generate_detailed_owings(self):
        # the goal is to create a dataframe of all transactions owings, even from a contributor to himself
        data = []
        for transaction in self._transactions:
            data.append(transaction.balance)
        
        # merging all dataframes
        output_df = reduce(lambda  left,right: pd.merge(left,right,how='outer'), data)
        return output_df


    def generate_simplified_owings(self):
        # returns dataframe of transactions to perform for equilibrium
        
        df_start = self.generate_detailed_owings()

        # temporary function for row-wise apply
        def settify(row):
            # identifies a pair of contributors by a unique string, whoever owes to the other
            # The tip is to join their uid in a single string
            return "-".join(sorted([item.uid.hex for item in row if isinstance(item,Contributor)]))

        gb_creditor_and_contributor = df_start.groupby(["creditor","contributor"],as_index=False,sort=False)
        df_one_dir = gb_creditor_and_contributor[["value"]].sum()  # all one-directional owings summed.
        df_one_dir = df_one_dir[df_one_dir["creditor"]!=df_one_dir["contributor"]]
        df_one_dir["set"] = df_one_dir[["creditor","contributor"]].apply(settify,axis=1)

        for item in df_one_dir.set.unique():
            tempdf = df_one_dir.loc[df_one_dir["set"]==item,:]
            # This part reduces the number of readjustments between contributors
            # For example, if John owes 34 to Marie and Marie owes 28 to John,
            # it will simplify by proposing that John owes 34-28 to Marie.
            if len(tempdf)==2:
                min_value = tempdf["value"].min()
                max_value = tempdf["value"].max()
                index_of_min = tempdf["value"].idxmin()
                index_of_max = tempdf["value"].idxmax()
                df_one_dir.loc[index_of_min,"value"] = 0.
                df_one_dir.loc[index_of_max,"value"] = max_value-min_value
            else:
                print(f'no reverse transaction for {item}')

            df_one_dir.drop(df_one_dir[df_one_dir["value"]==0.0].index,inplace=True)
            df_one_dir.sort_values("value",ascending=False,inplace=True)

        return df_one_dir

    def calculate_individual_expenses(self) -> pd.DataFrame:
        # expenses by each contributor, after theoretical adjustments and equilibrium
        gb_contributor = self.generate_detailed_owings().groupby("contributor",as_index=False,sort=False)
        return gb_contributor["value"].sum().sort_values("value",ascending=False,inplace=False)


    def bilan(self):
        """Prints some balance information to standard output
        """
        print(f"Number of transactions : {len(self._transactions)}")
        print(f"Total expenses : {self.total()}")
        print("Contributors : \n\t"+"\n\t".join([repr(item) for item in self._contributors]))
        print("\n")

        df_for_reporting = self.generate_simplified_owings()
        # prepare sentences
        out = ""
        for _,row in df_for_reporting.iterrows():
            out += f"{row.contributor.name} owes {row.value} to {row.creditor.name}\n"

        print(out)


def generate_random_scenario(number_of_contributors=5, 
                    number_of_transactions=10,
                    min_expense=0.1,
                    max_expense=1200.):
    # using faker to generate profiles

    contribs = set()
    i=0
    while i<number_of_contributors:
        f = faker.Faker(["fr-FR","en-US"])
        p = Contributor(name=f.name(),email=f.email())
        # all_names = [item.name for item in contribs if item]
        if p not in contribs:
            contribs.add(p)
            i = len(contribs)
    contribs = list(contribs)
   
    transactions = []
    # generate false transactions
    for i in range(number_of_transactions):
        value = random.uniform(min_expense, max_expense)
        random_number_of_contributors = random.randint(1,number_of_contributors)
        trans = Transaction(amount=value,
                            who=random.choice(contribs),
                            contributors=random.sample(contribs,random_number_of_contributors))

        transactions.append(trans)
    
    data = Expenses(transactions=transactions)

    return data

def generate_simple_scenario():
    
    Jacques = Contributor(name="Jacques")
    Toto = Contributor(name="Toto")
    Tata = Contributor(name="Tata")
    
    transactions = []
    t1 = Transaction(10,Jacques,[Jacques,Toto])  # Toto 5 > Jacques 
    transactions.append(t1)
    t2 = Transaction(27,Toto,[Jacques,Toto,Tata])  # # Jacques 9 > Toto
    transactions.append(t2)
    t3 = Transaction(20,Tata,[Jacques,Toto])
    transactions.append(t3)
    t4 = Transaction(40,Jacques,[Jacques,Toto])  # Toto 20 > Jacques 
    transactions.append(t4)
    
    data = Expenses(transactions=transactions)

    return data

if __name__=="__main__":

    # e = generate_simple_scenario()
    e = generate_random_scenario(20,100)
    e.bilan()
    df = e.generate_detailed_owings()

