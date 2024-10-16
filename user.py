import os
import csv
from cryptography.hazmat.primitives import constant_time
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



def main():
    user = User()


if __name__ == "__main__":
    main()
