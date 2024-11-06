import csv
import os

class User_Account:
    def __init__(self, uid, filename="accounts.csv", auto_add=True):
        self.filename = filename
        self.uid = uid
        self.accounts = self.load_accounts()
        
        if auto_add and self.uid not in self.accounts:
            self.add_account(balance=0)  # Default balance is 0

    def load_accounts(self):
        accounts = {}
        if os.path.exists(self.filename):
            with open(self.filename, mode="r", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    accounts[row["uid"]] = float(row["balance"])
        else:
            with open(self.filename, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["uid", "balance"])
        return accounts

    def save_accounts(self):
        with open(self.filename, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["uid", "balance"])
            for uid, balance in self.accounts.items():
                writer.writerow([uid, balance])

    def add_account(self, balance=0):
        if self.uid not in self.accounts:
            self.accounts[self.uid] = balance
            self.save_accounts()

    def remove_account(self):
        if self.uid in self.accounts:
            if self.accounts[self.uid] > 0:
                raise ValueError("Withdraw balance first to close account")
            else:
                del self.accounts[self.uid]
                self.save_accounts()
        else:
            raise ValueError(f"No account found for {self.uid}")

    def get_balance(self):
        # Explicitly return None if the user does not exist in the accounts
        return self.accounts.get(self.uid, None)

    def update_balance(self, new_balance):
        if self.uid in self.accounts:
            self.accounts[self.uid] = new_balance
            self.save_accounts()
        else:
            print(f"Uid:{self.uid} not found, cannot update balance")

    def deposit(self, amount):
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Deposit amount must be positive")
            if self.uid not in self.accounts:
                raise ValueError(f"No account found for {self.uid}")
            
            self.accounts[self.uid] += amount
            print(f"Amount: {amount} deposited to account successfully. New balance: {self.accounts[self.uid]}")
            self.save_accounts()
        except ValueError as e:
            print(f"Invalid input: {e}")
            raise

    def withdraw(self, amount):
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Withdrawal amount must be positive")
            if self.uid not in self.accounts:
                raise ValueError(f"No account found for {self.uid}")
            
            if self.accounts[self.uid] < amount:
                raise ValueError("Insufficient balance")
            
            self.accounts[self.uid] -= amount
            print(f"Amount {amount} withdrawn. New balance: {self.accounts[self.uid]}")
            self.save_accounts()
        except ValueError as e:
            print(f"Invalid input: {e}")
            raise

    def check_account(self):
        return self.uid in self.accounts
