import tkinter as tk
import customtkinter as ctk
import credentials_input as cred
from validator_collection import checkers
import os
import csv
from cryptography.hazmat.primitives import constant_time
import shortuuid


ctk.set_appearance_mode("system")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('BusQr')
        self.geometry('600*500')
        self.startapp()

    def startapp(self):
        self.clear_page()
        self.bus_button = ctk.CTkButton(self, text='Bus' )
        self.bus_button.pack(pady=20, padx=20)
        self.user_button = ctk.CTkButton(self, text=  'User', command = self.launch_user )
        self.user_button.pack(pady=20, padx=20)

    def launch_user(self):
        self.clear_page()
        #self.user_button.destroy()
        #self.bus_button.destroy()
        #label welcomes users
        self.welcome_label = ctk.CTkLabel(self, text='Karibu User')
        self.welcome_label.grid(row=0, column=0, pady=20)

        self.login_button = ctk.CTkButton(self, text='Login' ,command = self.login)
        self.login_button.grid(row=1, column=0, padx=10)

        self.register_button = ctk.CTkButton(self, text= 'Register', command = self.register)
        self.register_button.grid(row=1, column=1, padx=10)

        self.back_button = ctk.CTkButton(self, text = 'Back', command = self.startapp)
        self.back_button.grid(row=2, column=0, pady=20)
    
    def clear_page(self):
        #this function clears the page of widgets
        for widget in self.winfo_children():
            widget.destroy()


    def  login(self):
        self.welcome_label.configure(text='Please enter your details to log in')
        self.login_button.destroy()
        self.register_button.destroy()
        self.back_button.configure(command = self.launch_user)

    def register(self):
        self.welcome_label.configure(text="please enter the following details to sign up")
        self.login_button.destroy()
        self.register_button.destroy()
        self.back_button.configure(command=self.launch_user)
        self.data_input()

        #self.name_label= ctk.CTkLabel(self, text='input email:')
        #self.name_label.grid(row=0, column=0, padx=10, pady=10)
    def data_input(self):
        self.name_entry = ctk.CTkEntry(self, placeholder_text= "Name:")
        self.name_entry.grid(row=0, column=0, padx=10, pady=10)

        self.email_entry = ctk.CTkEntry(self, placeholder_text= "Email:")
        self.email_entry.grid(row=1, column=0, padx=10, pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text= "Password:")
        self.password_entry.grid(row=2, column=0, padx=10, pady=10)

        self.submit_button =ctk.CTkButton(self, text= 'Submit', command = self.verify_inputs)
        self.submit_button.grid(row=3, column=0, pady=15)

    def verify_inputs(self):#to do
        #check if user has inputted a name
        if not self.name_entry.get():
            raise ValueError("input name")

        
        #check if user has inputted an email and verify email
        if not self.email_entry.get():
            raise ValueError("input email")

        elif not checkers.is_email(self.email_entry.get()):
            raise ValueError("input a correct email")

        #check the inputted passwords 
        if not self.password_entry.get():
            raise ValueError("input a password")

        self.clear_page()
        self.confirm_registration = ctk.CTkButton(self, text = 'confirm registration', command = self.add_user)
        self.confirm_registration.pack(pady = 20)


    def add_user(self):#to do
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



        

        






app = App()
app.mainloop()