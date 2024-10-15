from validator_collection import checkers
import os
from cryptography.fernet import Fernet
import csv
from cryptography.hazmat.primitives import constant_time
import json
import shortuuid


class User:
    def __init__(self):
        print("1.Login", "2.Regiser")
        user_type = input("choice: ").casefold()
        if user_type == "login":
            self.user = self.user_logins()

        elif user_type == "register":
            self.user = self.user_registration()
        else:
            print("Usage: input")

    def user_registration(self):
        self.name = self.input_name()
        self.email = self.input_email()
        self.password = self.input_password()
        self._UID = self.UID_generator()
        self.encrypt_data()

    def input_name(self):
        while True:
            name = input("Name: ")
            if name:
                return name

    def input_email(self):
        while True:
            email = input("Email: ")
            if checkers.is_email(email):
                return email

    def input_password(self):
        while True:
            password = input("Password: ")
            if password:
                return password

    def encrypt_data(self):
        # this function encrypts all data to be stored in the new users csv
        key = Fernet.generate_key()
        self.fernet = Fernet(key)

        self.usertoken = self.fernet.encrypt(self.name)
        self.emailtoken = self.fernet.encrypt(self.email)
        self.passwordtoken = self.fernet.encrypt(self.password)
        self.add_user()

    def decrypt_data(self, token):
        # this function decrypts data in the csv to authenticate user logins
        fernet = self.fernet
        return fernet.decrypt(token)

    def add_user(self):
        # here we add users to a csv file to help with local authentication
        csv_file_path = "Users.csv"
        header = ["username", "email", "password", "userID"]

        # checking if csv file exists and if its empty
        if not os.path.exists(csv_file_path) or os.path.getsize(csv_file_path) == 0:
            with open(csv_file_path, mode="w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=header)
                writer.writeheader()

        # appending to the csv file using dicts
        with open(csv_file_path, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writerow(
                {
                    "username": self.usertoken,
                    "email": self.emailtoken,
                    "password": self.passwordtoken,
                    "userID": self._UID,
                }
            )

        self.user_login()

    def user_login(self):
        self.name = self.input_name()
        self.password = self.input_password()
        self.valid_user = self.validate_credentials()
        User_Account(self.valid_user)

    def validate_credentials(self):
        # import the users csv or check api
        user_data = {}
        with open("Users.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                decrypted_username = self.decrypt_data(row["username"])
                user_data[decrypted_username] = row

        # check if usrname in csv
        user = user_data.get(self.user)
        if user:
            user_password = self.decrypt_data(user['password'])
            if constant_time.bytes_eq(self.password, user_password):
                user_id = self.decrypt_data(row["userID"])
                return user_id

        # pick usrid to do all other functions

    def UID_generator():
        # this function generates 10 character long user ids
        # i use this to identify user sessions
        return shortuuid.uuid(length=10)


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


def main():
    user = User()


if __name__ == "__main__":
    main()
