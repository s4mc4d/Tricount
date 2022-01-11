# Tricount OOP

This is my version to practice OOP by replicating Tricount app algorithm.

## Structure 

Classes defined are :
- Contributor : used to identify a person involved in any expense
- Transaction : object defined by a positive amount (seen as an expense), a owner (of type Contributor) and a list of Contributor objects.
- Expenses : gathers all transactions and provides methods to calculate final equilibrium.

## Testing the core

```shell
cd Tricount
source .env/bin/activate
python3 -m pytest tests -v --cov
```

Parameters `-v` and `--cov` are optional
