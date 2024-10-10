from validator_collection import checkers
import os
from cryptography.fernet import Fernet
import csv
from cryptography.hazmat.primitives import constant_time
import json



class User:

    def __init__(self):
        print("1.Login","2.Regiser")
        user_type = input("choice: ").casefold()
        if  user_type == "login":
            self.user = self.user_logins()

        elif  user_type == "register":
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
        password = input("Password: ")
        return password
    

    def encrypt_data(self):
        #this function encrypts all data to be stored in the new users csv
        key = Fernet.generate_key()
        self.fernet = Fernet(key)
        self.usertoken = fernet.encrypt(self.name)
        self.emailtoken = fernet.encrypt(self.email)
        self.passwordtoken = fernet.encrypt(self.password)
        self.add_user()

    def decrypt_data(self, token):
        #this function decrypts data in the csv to authenticate user logins
        fernet = self.fernet
        return fernet.decrypt(token)


    def add_user(self):
        #here we add users to a csv file to help with local authentication 
        csv_file_path = "Users.csv"
        header = ["username", "email", "password", "userID"]
        
        #checking if csv file exists and if its empty
        if not os.path.exists(csv_file_path) or os.path.getsize(csv_file_path) == 0:
            with open(csv_file_path, mode = 'w', newline= '') as file:
                writer = csv.DictWriter(file, fieldnames=header)
                writer.writeheader()

        #appending to the csv file using dicts
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writerow({"username": self.usertoken, "email":self.emailtoken, "password"=self.passwordtoken, "userID": self._UID})
        
        self.user_login()


    def user_login():
        self.name = self.input_name()
        self.password = self.input_password()
        self.valid_user = self.validate_credentials()
        User_Account()

    def validate_credentials(self):
        #import the users csv or check api
        user_data = {}
        with open("Users.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                decrypted_username = decrypt_data(row['username'])
                user_data[decrypted_username] = row

        #check if usrname in csv
        user = user_data.get(self.user)
        if user:
            user_password = decrypt_data(user[password])
            if constant_time.bytes_eq(self.password, user_password):
                user_id = decrypt_data(row['userID'])
                return user_id

        #pick usrid to do all other functions


    def UID_generator():
        #this function generates 10 character long user ids
        #i use this to identify user sessions 
        return shortuuid.uuid(length=10)
        


class User_Account:
    def __init__(self, filename= 'accounts.json'):
        self.filename= filename
        self.accounts = self.load_accounts()


    def load_accounts(self):
        try:
            with open(self.filename) as f:
                return json.load(f)
        
        except (FileNotFoundError, json.JSONDecondeError):
            return{}

    def save_accounts(self): 
        with open(self.filenae, 'w') as f:
            json.dump(self.accounts, f)

            
    def add_account(self, uid, account):
        if uid in self.accounts:
            raise ValueError(f "account for {uid} allready exist)
        self.accounts[uid] = account
        self.save_accounts()


    def get_accounts(self, uid):
        return self.accounts.get(uid, None)


    def remove_accounts(self, uid):
        if uid in self.accounts:
            del self.accounts[uid]
            self.save_accounts()
        else:
            raise ValueError(f"No account found for {uid})



