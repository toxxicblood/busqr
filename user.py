from validator_collection import checkers
import os
from cryptography.fernet import Fernet
import csv



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

    def user_logins():
        self.name = self.input_name()
        self.password = self.input_password()
        self.valid_user = self.validate_credentials()


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

    def decrypt_data(self):
        #this function decrypts data in the csv to authenticate user logins

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
            writer.writerow({"username": self.usertoken, "email":self.emailtoken, "password"=self.passwordtoken, "userID": self._UID


    def validate_credentials(self):
        #import the users csv or check api
        #check if usrname in csv
        #pick usrid to do all other functions


    def UID_generator():
        #this function generates 10 character long user ids
        #i use this to identify user sessions 
        return shortuuid.uuid(length=10)
        


class User_Account():
    def __init__(self,uid):
        #pass in the user id
        
        def deposit():
        
        def withdraw():

        def pay():

        def balance():

        def transactions():
            #open a txt file for all usrs transactions.
            #identified through uid
            



