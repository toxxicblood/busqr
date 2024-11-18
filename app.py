import customtkinter as ctk
from validator_collection import checkers
import os
import csv
from cryptography.hazmat.primitives import constant_time
import shortuuid
import crypt_data
import user_account

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("dark-blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("BusQr")
        self.geometry("600x500")
        self.configure(bg="800080")
        self.crypt = crypt_data.DataEncryptor()
        self.startapp()
#
    def startapp(self):
        self.clear_page()
        self.bus_button = ctk.CTkButton(self, text="Bus",command = self.launch_bus)
        self.bus_button.pack(pady=20, padx=20)
        self.user_button = ctk.CTkButton(self, text="User ", command=self.launch_user)
        self.user_button.pack(pady=20)


    def launch_bus(self):
        self.clear_page()
        self.welcome_label = ctk.CTkLabel(self, text="Karibu Pilot")
        self.welcome_label.pack(pady=20)

        self.login_button = ctk.CTkButton(self, text="Login to bus account", command=self.bus_login)
        self.login_button.pack(pady=20)

        self.register_button = ctk.CTkButton(
            self, text="Register a new bus or taxi", command=self.bus_register
        )
        self.register_button.pack(pady=20)

        self.back_button = ctk.CTkButton(self, text="Back", command=self.startapp)
        self.back_button.pack(pady=20)

    def bus_register(self):
        self.clear_page()
        self.label = ctk.CTkLabel(self, text="Enter the following details to register.")
        self.label.pack(pady=20)


    def bus_login(self):
        pass
        
    def launch_user(self):
        self.clear_page()
        self.welcome_label = ctk.CTkLabel(self, text="Karibu User")
        self.welcome_label.pack(pady=20)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.pack(pady=20)

        self.register_button = ctk.CTkButton(
            self, text="Register", command=self.register
        )
        self.register_button.pack(pady=20)

        self.back_button = ctk.CTkButton(self, text="Back", command=self.startapp)
        self.back_button.pack(pady=20)

    def clear_page(self):
        for widget in self.winfo_children():
            widget.destroy()

    def register(self):
        self.clear_page()
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Name:", corner_radius=10)
        self.name_entry.pack(pady=20)

        self.email_entry = ctk.CTkEntry(
            self, placeholder_text="Email:", corner_radius=10
        )
        self.email_entry.pack(pady=20)

        self.password_entry = ctk.CTkEntry(
            self, placeholder_text="Password:", corner_radius=10, show="*"
        )
        self.password_entry.pack(pady=20)

        self.submit_button = ctk.CTkButton(
            self, text="Submit", command=self.verify_inputs
        )
        self.submit_button.pack(pady=20)

        self.back_button = ctk.CTkButton(self, text="Back", command=self.launch_user)
        self.back_button.pack(pady=20)

    def verify_inputs(self):
        if not self.name_entry.get():
            self.name_entry.configure(
                placeholder_text_color="#F31604", fg_color=("#F61B09", "#383838")
            )
            raise ValueError("Input name")

        if not self.email_entry.get():
            self.email_entry.configure(
                placeholder_text_color="#F31604", fg_color=("#F61B09", "#383838")
            )
            raise ValueError("Input email")

        elif not checkers.is_email(self.email_entry.get()):
            self.email_entry.configure(
                text_color="#F31604",
                placeholder_text_color="#F31604",
                fg_color=("#F61B09", "#383838"),
            )
            raise ValueError("Input a correct email")
        else:
            # Check for existing email before proceeding to add user
            encrypted_email = self.crypt.encrypt(self.email_entry.get())
            if self.email_exists(encrypted_email):
                self.email_entry.configure(
                    text_color="#F31604", fg_color=("#F61B09", "#383838")
                )
                print("Error: An account with this email already exists.")
                return  # Stop further processing and don't proceed to add the user

            else:
                self.email_entry.configure(text_color="white")

        if not self.password_entry.get():
            self.password_entry.configure(
                placeholder_text_color="#F31604", fg_color=("#F61B09", "#383838")
            )
            raise ValueError("Input a password")

        self.submit_button.configure(text="Confirm Registration", command=self.add_user)
        self.back_button.configure(command=self.register)

    def email_exists(self, encrypted_email):
        csv_file_path = "Users.csv"
        if os.path.exists(csv_file_path) and os.path.getsize(csv_file_path) > 0:
            with open(csv_file_path, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    decrypted_email = self.crypt.decrypt(row["email"])  # Decrypt the email in the CSV
                    if decrypted_email == self.email_entry.get():  # Compare decrypted email
                        return True
        return False

    def add_user(self):
        csv_file_path = "Users.csv"
        header = ["username", "email", "password", "userID"]

        if not os.path.exists(csv_file_path) or os.path.getsize(csv_file_path) == 0:
            with open(csv_file_path, mode="w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=header)
                writer.writeheader()

        encrypted_username = self.crypt.encrypt(self.name_entry.get())
        encrypted_email = self.crypt.encrypt(self.email_entry.get())
        encrypted_password = self.crypt.encrypt(self.password_entry.get())
        encrypted_userID = self.crypt.encrypt(shortuuid.uuid())


        # add user since email doesnt exist
        with open(csv_file_path, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writerow(
                {
                    "username": encrypted_username,
                    "email": encrypted_email,
                    "password": encrypted_password,
                    "userID": encrypted_userID,
                }
            )
        print("User  added to CSV:")    # Debugging line
        # print(f"Username: {encrypted_username}, Email: {encrypted_email}, Password: {encrypted_password}, UserID: {encrypted_userID}")  # Debugging line

        self.login()

    def login(self):
        self.clear_page()

        self.email_entry = ctk.CTkEntry(
            self, placeholder_text="Email:", corner_radius=10
        )
        self.email_entry.pack(pady=20)

        self.password_entry = ctk.CTkEntry(
            self, placeholder_text="Password:", corner_radius=10, show="*"
        )
        self.password_entry.pack(pady=20)

        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.login_user)
        self.submit_button.pack(pady=20)

        self.back_button = ctk.CTkButton(self, text="Back", command=self.launch_user)
        self.back_button.pack(pady=20)

    def login_user(self):
        if not self.email_entry.get():
            self.email_entry.configure(
                text_color="#F31604",
                placeholder_text_color="#F31604",
                fg_color=("#F61B09", "#383838"),
            )
            raise ValueError("Input email")

        if not self.password_entry.get():
            self.password_entry.configure(
                placeholder_text_color="#F31604", fg_color=("#F61B09", "#383838")
            )
            raise ValueError("Input password")

        user_data = {}
        try:
            with open("Users.csv") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    decrypted_email = self.crypt.decrypt(row["email"])

                    if decrypted_email is not None:
                        user_data[decrypted_email] = row
        except FileNotFoundError:
            self.register()
        
        input_value = self.email_entry.get()
        user = user_data.get(input_value)
        if user:
            user_password = self.crypt.decrypt(user["password"])
            if user_password is not None and constant_time.bytes_eq(
                self.password_entry.get().encode(), user_password.encode()
            ):
                self.user_id = self.crypt.decrypt(user["userID"])
                self.username = self.crypt.decrypt(row["username"])
                self.Accounts()  # Call the Accounts method
            else:
                print("Password does not match.")
        else:
            print("User  not found.")
            self.register()

    def Accounts(self):
        self.clear_page()

        self.success_label = ctk.CTkLabel(self, text="Login successful")
        self.success_label.pack(pady=20)

        self.hello_user = ctk.CTkLabel(self, text=f"Hello {self.username}")
        self.hello_user.pack(pady=10)

        self.usr_acct = user_account.User_Account(self.user_id)
        self.usr_acct.add_account()

        self.balance = ctk.CTkLabel(
            self, text=f"Balance: {self.usr_acct.get_balance()}"
        )
        self.balance.pack(pady=10)

        self.deposit = ctk.CTkButton(self, text="Deposit", command=self.depositor)
        self.deposit.pack(pady=10)

        self.withdraw = ctk.CTkButton(self, text="Withdraw", command=self.withdrawer)
        self.withdraw.pack(pady=10)

        self.remove_acct = ctk.CTkButton(
            self, text="Remove Account", command=self.usr_acct.remove_account
        )
        self.remove_acct.pack(pady=10)

        self.logout_button = ctk.CTkButton(self, text="Logout", command=self.login)
        self.logout_button.pack(pady=20)

        # Additional functionality for user accounts can be added here

    def depositor(self):
        self.clear_page()
        self.input_amount = ctk.CTkEntry(
            self, placeholder_text="Enter Amount:", corner_radius=10
        )
        self.input_amount.pack(pady=10)

        def submit_deposit():
            amount = self.input_amount.get().strip()
            if amount.isnumeric():  # Simple validation
                self.usr_acct.deposit(float(amount))
                self.Accounts()
            # self.balance.configure(text=f"Balance: {self.usr_acct.get_balance()}")
            else:
                print("Invalid input: Please enter a numeric value for the deposit.")

        self.submit_button = ctk.CTkButton(self, text="Submit", command=submit_deposit)
        self.submit_button.pack(pady=10)

        self.back_button = ctk.CTkButton(self, text="Back", command=self.Accounts)
        self.back_button.pack(pady=10)

    def withdrawer(self):
        self.clear_page()

        self.input_amount = ctk.CTkEntry(
            self, placeholder_text="Enter Amount:", corner_radius=10
        )
        self.input_amount.pack(pady=10)

        def submit_withdraw():
            amount = self.input_amount.get().strip()
            if amount.isnumeric():  # Simple validation
                self.usr_acct.withdraw(float(amount))
                self.Accounts()
                # self.balance.configure(text=f"Balance: {self.usr_acct.get_balance()}")
            else:
                print("Invalid input: Please enter a numeric value for the withdrawal.")

        self.submit_button = ctk.CTkButton(self, text="Submit", command=submit_withdraw)
        self.submit_button.pack(pady=10)

        self.back_button = ctk.CTkButton(self, text="Back", command=self.Accounts)
        self.back_button.pack(pady=10)


app = App()
app.mainloop()
