import unittest

from src.clients.account import BankAccount
from src.clients.customer import Customer
from src.clients.base_classes import AccountStatus, Currency
from src.clients.errors import (
    AccountFrozenError,
    AccountClosedError,
    InsufficientFundsError,
)


class BankAccountTestCase(unittest.TestCase):
    def setUp(self, ):
        self.owner_info = Customer('Ivan', 'Ivanov', '1990-01-01')

    def _make_account(self, ) -> BankAccount:
        return BankAccount(self.owner_info, Currency.USD)

    def test_create_active_account(self, ):
        account = self._make_account()

        self.assertEqual(account.account_status, AccountStatus.ACTIVE)
        self.assertFalse(account.operations_is_banned)
        self.assertEqual(account._balance, .0)

    def test_create_frozen_account(self, ):
        account = self._make_account()
        account.update_account_status(AccountStatus.FROZEN)

        self.assertEqual(account.account_status, AccountStatus.FROZEN)
        self.assertTrue(account.operations_is_banned)

    def test_deposit_on_frozen_account_is_rejected(self, ):
        account = self._make_account()
        account.update_account_status(AccountStatus.FROZEN)

        with self.assertRaises(AccountFrozenError):
            account.deposit(100)

    def test_withdraw_on_frozen_account_is_rejected(self, ):
        account = self._make_account()
        account.deposit(100)
        account.update_account_status(AccountStatus.FROZEN)

        with self.assertRaises(AccountFrozenError):
            account.withdraw(50)

    def test_operations_on_closed_account_are_rejected(self, ):
        account = self._make_account()
        account.update_account_status(AccountStatus.CLOSED)

        with self.assertRaises(AccountClosedError):
            account.deposit(100)

    def test_valid_deposit(self, ):
        account = self._make_account()
        account.deposit(150)

        self.assertEqual(account._balance, 150)

    def test_valid_withdraw(self, ):
        account = self._make_account()
        account.deposit(150)
        account.withdraw(60)

        self.assertEqual(account._balance, 90)

    def test_withdraw_more_than_balance_raises(self, ):
        account = self._make_account()
        account.deposit(50)

        with self.assertRaises(InsufficientFundsError):
            account.withdraw(100)


if __name__ == '__main__':
    unittest.main()
