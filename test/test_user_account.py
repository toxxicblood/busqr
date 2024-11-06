import unittest
from unittest.mock import patch, mock_open
from user_account import User_Account  # Adjust the import based on your project structure


class TestUserAccount(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists", return_value=False)
    def test_load_accounts_file_does_not_exist(self, mock_exists, mock_open):
        user = User_Account(uid="user1", auto_add=False)
        self.assertEqual(user.accounts, {})  # Expect empty dict since file doesn't exist

    @patch("builtins.open", new_callable=mock_open, read_data="uid,balance\nuser1,100\n")
    @patch("os.path.exists", return_value=True)
    def test_load_accounts_file_exists(self, mock_exists, mock_open):
        user = User_Account(uid="user1", auto_add=False)
        self.assertEqual(user.accounts, {"user1": 100.0})  # Expect loaded data from file

    @patch("user_account.User_Account.save_accounts")
    def test_add_account(self, mock_save):
        user = User_Account(uid="user2", auto_add=False)
        user.add_account(balance=50)
        self.assertEqual(user.accounts["user2"], 50)
        mock_save.assert_called_once()  # Ensure save_accounts is called once

    def test_get_balance_existing_user(self):
        user = User_Account(uid="user3", auto_add=False)
        user.accounts["user3"] = 75.0
        balance = user.get_balance()
        self.assertEqual(balance, 75.0)  # Expect the balance for an existing user

    def test_get_balance_non_existing_user(self):
        user = User_Account(uid="user47", auto_add=False)
        balance = user.get_balance()
        self.assertIsNone(balance)  # Expect None for non-existing user

    @patch("user_account.User_Account.save_accounts")
    def test_remove_account_with_zero_balance(self, mock_save):
        user = User_Account(uid="user5", auto_add=False)
        user.accounts["user5"] = 0
        user.remove_account()
        self.assertNotIn("user5", user.accounts)  # User5 should be removed
        mock_save.assert_called_once()  # Ensure save_accounts is called once

    def test_remove_account_with_positive_balance(self):
        user = User_Account(uid="user6", auto_add=False)
        user.accounts["user6"] = 100
        with self.assertRaises(ValueError):
            user.remove_account()  # Removing should raise an error due to positive balance

    @patch("user_account.User_Account.save_accounts")
    def test_update_balance_existing_user(self, mock_save):
        user = User_Account(uid="user7", auto_add=False)
        user.accounts["user7"] = 20.0
        user.update_balance(50.0)
        self.assertEqual(user.accounts["user7"], 50.0)  # Expect updated balance
        mock_save.assert_called_once()  # Ensure save_accounts is called once

    @patch("user_account.User_Account.save_accounts")
    def test_deposit_positive_amount(self, mock_save):
        user = User_Account(uid="user8", auto_add=False)
        user.accounts["user8"] = 10.0
        user.deposit(20)
        self.assertEqual(user.accounts["user8"], 30.0)  # Balance should reflect deposit
        mock_save.assert_called_once()  # Ensure save_accounts is called once

    def test_deposit_invalid_amount(self):
        user = User_Account(uid="user9", auto_add=False)
        with self.assertRaises(ValueError):
            user.deposit(-10)  # Negative amount should raise ValueError

    @patch("user_account.User_Account.save_accounts")
    def test_withdraw_valid_amount(self, mock_save):
        user = User_Account(uid="user10", auto_add=False)
        user.accounts["user10"] = 50.0
        user.withdraw(20)
        self.assertEqual(user.accounts["user10"], 30.0)  # Balance should reflect withdrawal
        mock_save.assert_called_once()  # Ensure save_accounts is called once

    def test_withdraw_invalid_amount(self):
        user = User_Account(uid="user11", auto_add=False)
        user.accounts["user11"] = 30.0
        with self.assertRaises(ValueError):
            user.withdraw(-10)  # Negative amount should raise ValueError

    def test_withdraw_insufficient_balance(self):
        user = User_Account(uid="user12", auto_add=False)
        user.accounts["user12"] = 10.0
        with self.assertRaises(ValueError):
            user.withdraw(20)  # Exceeds balance, should raise ValueError

    def test_check_account_existing(self):
        user = User_Account(uid="user13", auto_add=False)
        user.accounts["user13"] = 0
        self.assertTrue(user.check_account())  # Account exists, should return True

    def test_check_account_non_existing(self):
        user = User_Account(uid="user14", auto_add=False)
        self.assertFalse(user.check_account())  # Account does not exist, should return False


if __name__ == "__main__":
    unittest.main()
