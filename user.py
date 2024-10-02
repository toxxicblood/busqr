from validator_collection import checkers
import password

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
        self.add_user()

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

    def add_user():
        ... to do
        #usr details to be appended to the csv
        #generate user id
        #how to implement api tokens in normal python apps
        #hot to store user credentials.

    def validate_credentials(self):
        #import the users csv or check api
        #check if usrname in csv
        #pick usrid to do all other functions

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
            



