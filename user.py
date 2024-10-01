from validator_collection import checkers
import password

class User:

    def __init__(self):
        self.user_type = input(print("1.Login","2.Regiser")).casefold()
        if "1" == self.user_type == "login":
            self.user = self.user_logins()

        elif "2" == self.user_type == "register":
            self.user = self.user_registration()
        else:
            print("Usage: input")

    def user_registration(self):
        self.name = input_name()
        self.email = input_email()
        self.password = input_password()


    def input_name():
        while true:
            name = input("Name: ")
            if name:
                return name
    
    def input_email():
        while true:
            email = input("Email: ")
            if checkers.is_email(email):
                return email
    
    def input_password():
        password = input("Password: ")
        password = password.Password(method='sha1', hash_encoding='base64')

