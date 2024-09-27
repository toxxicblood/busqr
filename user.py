



class User:
    def __init__(self, name,address):
        self.name = name
        self.address = address

    def __str__(self):
        return f"Username:{self.name} User address:{self.address}"
    
    @classmethod
    def get(cls):
        name = input("Input your name: ")
        address = input("Where do you live: ")

        return cls(name, address)


def main():
    user = User.get()
    print(user)

if __name__ == "__main__":
    main()