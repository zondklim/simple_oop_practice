# simple_oop_practice

A small OOP practice project modeling a bank account system.

## Structure

```
src/
  clients/
    customer.py       Customer dataclass
    base_classes.py    AbstractAccount (ABC), AccountStatus, Currency enums
    account.py          BankAccount, concrete implementation
    errors.py           Custom exception hierarchy
tests/
  test_account.py       unittest suite for BankAccount
```

## Core classes

- `Customer` (`customer.py`) — dataclass holding `name`, `surname`, `date_of_birth`.
- `AbstractAccount` (`base_classes.py`) — abstract base class. Generates a card number, sets the `ACTIVE` status and zero balance. Requires subclasses to implement `deposit`, `withdraw`, and `get_account_info`.
- `AccountStatus` — enum: `ACTIVE`, `FROZEN`, `CLOSED`.
- `Currency` — enum: `RUB`, `USD`, `EUR`, `KZT`, `CNY`.
- `BankAccount` (`account.py`) — account implementation with `deposit`, `withdraw`, `get_account_info`, and `update_account_status`. Validates owner/currency and blocks operations for frozen or closed.
- `errors.py` — `AccountErrors` base exception, with `AccountFrozenError`, `AccountClosedError`, `InvalidOperationError`, `InsufficientFundsError` as subclasses.

## Requirements

Python 3.10+

## Example usage

```python
from src.clients.account import BankAccount
from src.clients.customer import Customer
from src.clients.base_classes import Currency, AccountStatus

customer = Customer("Ivan", "Ivanov", "1990-01-01")
account = BankAccount(customer, Currency.USD)

account.deposit(100)
account.withdraw(40)
print(account)

account.update_account_status(AccountStatus.FROZEN)
account.deposit(10)  # raises AccountFrozenError
```

## Testing

```bash
python3 -m unittest tests.test_account -v
```