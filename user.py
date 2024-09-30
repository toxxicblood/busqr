from validator_collection import checkers


class User:

    def __init__(self):
        user_type = input(print("1.Login",\n,"2.Regiser")).casefold()
        if "1" == user_type == "login":
            self.user = self.user_logins()

        elif "2" == user_type == "register":
            self.user = self.user_registration()
        else:
            print("Usage: input")

    def user_registration(self):
        self.name = input_name()
        self.email = input_loop("Email: ")
        password = input_loop("Password: ")


    def input_name():
        while true:
            name = input("Name: ")
            if name:
                return name
    
    def input_email:
        while true:
            if checkers.is_email(input("Email: "):
                return email


