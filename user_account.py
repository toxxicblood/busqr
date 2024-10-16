import json


class User_Account:
    def __init__(self, uid, filename="accounts.json"):
        self.filename = filename
        self.accounts = self.load_accounts()
        self.uid = uid

    def load_accounts(self):
        try:
            with open(self.filename) as f:
                return json.load(f)

        except (FileNotFoundError, json.JSONDecondeError):
            return {}

    def save_accounts(self):
        with open(self.filenae, "w") as f:
            json.dump(self.accounts, f)

    def add_account(self, balance=0):
        if self.uid in self.accounts:
            raise ValueError(f"account for {self.uid} allready exists")
        else:
            self.accounts[self.uid] = balance
            self.save_accounts()

    def remove_accounts(self):
        if self.uid in self.accounts:
            if self.accounts[self.uid] > 0:
                raise ValueError("withdraw balance first to close account")
            else:
                del self.accounts[self.uid]
                self.save_accounts()
        else:
            raise ValueError(f"No account found for {self.uid}")

    def get_balance(self):
        return self.accounts.get(self.uid, None)

    def update_balance(self, new_balance):
        # update balance for an existing usr
        if self.uid in self.accounts:
            self.accounts[self.uid] = new_balance
        else:
            print(f"Uid:{self.uid} not found, cannot update balance")

    def deposit(self, ammount):
        # deposit a positive ammt into the users acct
        if self.uid in self.accounts:
            if ammount > 0:
                self.accounts[self.uid] += ammount
                print(
                    f"ammount:{ammount} deposited to account successfully. New balance: {self.accont[self.uid]}"
                )
            else:
                print("invalid deposit")
        else:
            print("uid not found")

    def withdraw(self, ammount):
        if self.uid in self.accounts:
            if ammount > 0:
                if self.accounts[self.uid] >= ammount:
                    self.accounts[self.uid] -= ammount
                    print(f"ammt{ammount} withdrawn. balance {self.accounts[self.uid]}")
                else:
                    print(f"insufficient bal")

            else:
                print("invalid withdrawal ammount")
        else:
            print("uid not found")

