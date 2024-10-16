from validator_collection import checkers

def input_name():
    while True:
        name = input("Name: ").strip()
        if name:
            return name

def input_email():
    while True:
        email = input("Email: ")
        if checkers.is_email(email):
            return email

def input_password():
    while True:
        password = input("Password: ")
        if password:
            return password

