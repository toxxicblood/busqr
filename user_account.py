import csv
import os

class User_Account:
    def __init__(self, uid, filename="accounts.csv"):
        self.filename = filename
        self.uid = uid
        self.accounts = self.load_accounts()
        
        # Automatically add the account if uid is not found
        if self.uid not in self.accounts:
            self.add_account(balance=0)  # Default balance is 0

    def load_accounts(self):
        accounts = {}
        # Check if the CSV file exists
        if os.path.exists(self.filename):
            with open(self.filename, mode='r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    accounts[row['uid']] = float(row['balance'])  # Convert balance to float
        else:
            # Create a new CSV file with the header if it doesn't exist
            with open(self.filename, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['uid', 'balance'])  # Write header
        return accounts

    def save_accounts(self):
        with open(self.filename, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['uid', 'balance'])  # Write header
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
        return self.accounts.get(self.uid, None)

    def update_balance(self, new_balance):
        if self.uid in self.accounts:
            self.accounts[self.uid] = new_balance
            self.save_accounts()  # Save changes to CSV
        else:
            print(f"Uid:{self.uid} not found, cannot update balance")

    def deposit(self, amount):
        try:
            amount = int(amount)  # Convert to integer
            if self.uid not in self.accounts:
                raise ValueError(f"No account found for {self.uid}")
            if amount > 0:
                self.accounts[self.uid] += amount
                print(f"Amount: {amount} deposited to account successfully. New balance: {self.accounts[self.uid]}")
                self.save_accounts()  # Save changes to CSV
            else:
                print("Invalid deposit amount")
        except ValueError:
            print("Invalid input: Please enter a numeric value for the deposit.")

    def withdraw(self, amount):
        try:
            amount = int(amount)  # Convert to integer
            if self.uid not in self.accounts:
                print("UID not found")
                return
            if amount <= 0:
                print("Invalid withdrawal amount")
                return

            if self.accounts[self.uid] >= amount:
                self.accounts[self.uid] -= amount
                print(f"Amount {amount} withdrawn. New balance: {self.accounts[self.uid]}")
                self.save_accounts()  # Save changes to CSV
            else:
                print("Insufficient balance")
        except ValueError:
            print("Invalid input: Please enter a numeric value for the withdrawal.")

    def check_account(self):
        if self.uid not in self.accounts:
            print(f"No account found for {self.uid}")
            return False
        return True