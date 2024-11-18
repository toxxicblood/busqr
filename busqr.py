import re
import os
import csv
import json
import qrcode
import shortuuid
import crypt_data
import user_account
import customtkinter as ctk
from datetime import datetime
from cryptography.hazmat.primitives import constant_time
from validator_collection import checkers, validators, errors


#configure ctk appearance
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("dark-blue")


#set file paths as global constants
USER_FILE = 'Users.csv'
BOOKING_FILE = 'Bookings.csv'
VEHICLE_FILE = 'Vehicles.json'
DRIVER_FILE = 'Drivers.json'

class BusQr(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("BusQr")
        self.geometry("600x800")
        self.configure(fg_color = "#1e1e2f")#set main window bg color
        
        #initialize the data encryptor
        self.crypt = crypt_data.DataEncryptor()

        #set theme colors
        self.primary_color = "#3b8ed0"  # Blue for button highlights
        self.secondary_color = "#2c2c54"  # Dark purple for background elements
        #this line calls the startapp method to start the app
        self.startapp()

    #this function creates tabview when called
    def tab_create(self):
        # Create tabs for different sections
        self.tabview = ctk.CTkTabview(self, width=600, height=800)
        self.tabview.pack(fill="both", expand=True)
        self.tabview.configure(fg_color="#1e1e2f")  # Tab background color

    #this function clears the page by deleting all widgets
    def clear_page(self):
        for widget in self.winfo_children():
            widget.destroy()

    #this function creates a back button in the specified location with a specified command
    def back_button(self,text,location,command):
        self.back_btn = ctk.CTkButton(location,
                                         text =text , command=command,
            fg_color=self.primary_color, hover_color="#2a6a9a", width=150
        )
        self.back_btn.pack(pady=10)

    #this function displays the buttons to select whether you are a use or a bus operator
    def startapp(self):
        self.clear_page()
        self.bus_button = ctk.CTkButton(self, text="Bus",command = self.bus)
        self.bus_button.pack(pady=20, padx=20)
        self.user_button = ctk.CTkButton(self, text="User ", command=self.user)
        self.user_button.pack(pady=20)

    def bus(self):
        self.clear_page()
        self.tab_create()
        self.add_driver_registration_tab()
        self.add_driver_login_tab()

    def add_driver_registration_tab(self):
        driver_tab = self.tabview.add("Register Driver")
        driver_tab.configure(fg_color=self.secondary_color)
        self.welcome_label = ctk.CTkLabel(driver_tab, text="Karibu Pilot")
        self.welcome_label.pack(pady=20)

        self.registration_number_entry = ctk.CTkEntry(driver_tab, placeholder_text="Vehicle Registration Number", width=250)
        self.registration_number_entry.pack(pady=(20, 5))

        self.registration_number_error = ctk.CTkLabel(driver_tab, text="", text_color="red", font=("Arial", 10))
        self.registration_number_error.pack()

        self.vehicle_type_entry = ctk.CTkComboBox(driver_tab, values=["Bus", "Taxi"], width=250)
        self.vehicle_type_entry.set("Bus")
        self.vehicle_type_entry.pack(pady=(10, 5))

        self.capacity_entry = ctk.CTkEntry(driver_tab, placeholder_text="Capacity", width=250)
        self.capacity_entry.pack(pady=(10, 5))

        self.capacity_error = ctk.CTkLabel(driver_tab, text="", text_color="red", font=("Arial", 10))
        self.capacity_error.pack()

        self.driver_contact_entry = ctk.CTkEntry(driver_tab, placeholder_text="Driver Contact", width=250)
        self.driver_contact_entry.pack(pady=(10, 5))

        self.driver_contact_error = ctk.CTkLabel(driver_tab, text="", text_color="red", font=("Arial", 10))
        self.driver_contact_error.pack()

        self.driver_name_entry = ctk.CTkEntry(driver_tab, placeholder_text="Driver Name", width=250)
        self.driver_name_entry.pack(pady=(20, 5))

        self.driver_name_error = ctk.CTkLabel(driver_tab, text="", text_color="red", font=("Arial", 10))
        self.driver_name_error.pack()

        self.driver_email_entry = ctk.CTkEntry(driver_tab, placeholder_text="Email", width=250)
        self.driver_email_entry.pack(pady=(10, 5))

        self.driver_email_error = ctk.CTkLabel(driver_tab, text="", text_color="red", font=("Arial", 10))
        self.driver_email_error.pack()

        self.driver_password_entry = ctk.CTkEntry(driver_tab, placeholder_text="Password", show="*", width=250)
        self.driver_password_entry.pack(pady=(10, 5))

        self.driver_password_error = ctk.CTkLabel(driver_tab, text="", text_color="red", font=("Arial", 10))
        self.driver_password_error.pack()


        self.register_driver_button = ctk.CTkButton(
            driver_tab, text="Register Vehicle", command=self.register_driver,
            fg_color=self.primary_color, hover_color="#2a6a9a", width=150
        )
        self.register_driver_button.pack(pady=20)

        self.back_button("Back", driver_tab, self.startapp)

    def register_driver(self):
        registration_number = self.registration_number_entry.get()
        vehicle_type = self.vehicle_type_entry.get()
        capacity = self.capacity_entry.get()
        driver_contact = self.driver_contact_entry.get()
        self.registration_number_error.configure(text="")
        self.capacity_error.configure(text="")
        self.driver_contact_error.configure(text="")

        if not registration_number:
            self.registration_number_error.configure(text="Please enter vehicle registration number.")
        elif not self.validate_numeric(capacity):
            self.capacity_error.configure(text="Capacity must be a number.")
        elif not self.validate_contact(driver_contact):
            self.driver_contact_error.configure(text="Invalid contact number.")
        elif not self.save_vehicle(registration_number, vehicle_type, capacity, driver_contact):
            self.registration_number_error.configure(text="Vehicle already registered.")
        else:
            print("Vehicle registered successfully!")

        username = self.driver_name_entry.get()
        email = self.driver_email_entry.get()
        password = self.driver_password_entry.get()
        self.driver_name_error.configure(text="")
        self.driver_email_error.configure(text="")
        self.driver_password_error.configure(text="")

        if not username:
            self.driver_name_error.configure(text="Please enter your name.")
        elif not self.validate_email(email):
            self.driver_email_error.configure(text="Invalid email format.")
        elif not self.validate_password(password):
            self.driver_password_error.configure(text="Password should be at least 8 characters long with letters and numbers.")
        elif not self.save_user(username, email, password, DRIVER_FILE):
            self.driver_email_error.configure(text="Driver already exists.")
        else:
            print("Driver registration successful!")

    
    def save_vehicle(self, registration_number, vehicle_type, capacity, driver_contact):
        with open(VEHICLE_FILE, 'r+') as f:
            vehicles = json.load(f)
            if registration_number in vehicles:
                return False  # Vehicle already registered
            vehicles[registration_number] = {
                "vehicle_type": vehicle_type,
                "capacity": capacity,
                "driver_contact": driver_contact
            }
            f.seek(0)
            json.dump(vehicles, f, indent=4)
        return True

    def add_driver_login_tab(self):
        driver_login_tab = self.tabview.add("Driver Login")
        driver_login_tab.configure(fg_color=self.secondary_color)

        self.driver_login_email_entry = ctk.CTkEntry(driver_login_tab, placeholder_text="Email", width=250)
        self.driver_login_email_entry.pack(pady=(20, 5))

        self.driver_login_email_error = ctk.CTkLabel(driver_login_tab, text="", text_color="red", font=("Arial", 10))
        self.driver_login_email_error.pack()

        self.driver_login_password_entry = ctk.CTkEntry(driver_login_tab, placeholder_text="Password", show="*", width=250)
        self.driver_login_password_entry.pack(pady=(10, 5))

        self.driver_login_password_error = ctk.CTkLabel(driver_login_tab, text="", text_color="red", font=("Arial", 10))
        self.driver_login_password_error.pack()

        self.driver_login_button = ctk.CTkButton(
            driver_login_tab, text="Log In as Driver", command=self.driver_login,
            fg_color=self.primary_color, hover_color="#2a6a9a", width=150
        )
        self.driver_login_button.pack(pady=20)

    def driver_login(self):
        username = self.driver_login_email_entry.get()
        password = self.driver_login_password_entry.get()
        self.driver_login_email_error.configure(text="")
        self.driver_login_password_error.configure(text="")

        if not username or not password:
            self.driver_login_email_error.configure(text="Please enter both email and password.")
        elif not self.check_json_user_credentials(username, password, DRIVER_FILE):
            self.driver_login_password_error.configure(text="Invalid email or password.")
        else:
            print("Driver login successful!")
            self.driver_UI()

    def driver_UI(self):
        self.clear_page()
        self.tab_create()
        self.qr_code_generator_tab()

    def qr_code_generator_tab(self):
        qr_gen_tab = self.tabview.add("QR Code Generator")
        qr_gen_tab.configure(fg_color=self.secondary_color)

        



    def user(self):
        self.clear_page()
        self.tab_create()
        self.create_login_tab()
        self.create_registration_tab()

    def create_login_tab(self):
        login_tab = self.tabview.add("Login")
        login_tab.configure(fg_color=self.secondary_color)

        self.login_email_entry = ctk.CTkEntry(login_tab, placeholder_text="Email", width=250)
        self.login_email_entry.pack(pady=(10, 5))

        self.login_email_error = ctk.CTkLabel(login_tab, text="", text_color="red", font=("Arial", 10))
        self.login_email_error.pack()

        self.password_entry = ctk.CTkEntry(login_tab, placeholder_text="Password", show="*", width=250)
        self.password_entry.pack(pady=(10, 5))

        self.password_error = ctk.CTkLabel(login_tab, text="", text_color="red", font=("Arial", 10))
        self.password_error.pack()

        self.login_button = ctk.CTkButton(
            login_tab, text="Log In", command=self.login,
            fg_color=self.primary_color, hover_color="#2a6a9a", width=150
        )
        self.login_button.pack(pady=20)

        self.back_button("Back",login_tab,self.startapp)

    # Button event functions
    def login(self):
        email = self.login_email_entry.get()
        password = self.password_entry.get()
        self.login_email_error.configure(text="")
        self.password_error.configure(text="")

        if not email :
            self.login_email_error.configure(text="Please enter an email.")
        elif not password:
            self.password_error.configure(text="Please enter a password")
        elif not self.check_user_credentials(email, password):
            self.password_error.configure(text="Invalid username or password.")
        else:
            print("Login successful!")

    def check_user_credentials(self,email,password):
        user_data = {}
        try:
            with open(USER_FILE) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    decrypted_email = self.crypt.decrypt(row["email"])

                    if decrypted_email is not None:
                        user_data[decrypted_email] = row
        except FileNotFoundError:
            print("No user data found.")
            return {}
        

        user = user_data.get(email)
        if user:
            user_password = self.crypt.decrypt(user["password"])
            if user_password is not None and constant_time.bytes_eq(
                password.encode(), user_password.encode()
            ):
                self.user_id = self.crypt.decrypt(user["userID"])
                self.username = self.crypt.decrypt(user["username"])
                self.user_interface()  # Call the user interface method
            else:
                print("Password does not match.")
        else:
            print("User  not found.")
    
    def create_registration_tab(self):
        registration_tab = self.tabview.add("Register")
        registration_tab.configure(fg_color=self.secondary_color)

        self.name_entry = ctk.CTkEntry(registration_tab, placeholder_text="Full Name", width=250)
        self.name_entry.pack(pady=(20, 5))

        self.name_error = ctk.CTkLabel(registration_tab, text="", text_color="red", font=("Arial", 10))
        self.name_error.pack()

        self.email_entry = ctk.CTkEntry(registration_tab, placeholder_text="Email", width=250)
        self.email_entry.pack(pady=(10, 5))

        self.email_error = ctk.CTkLabel(registration_tab, text="", text_color="red", font=("Arial", 10))
        self.email_error.pack()

        self.password_reg_entry = ctk.CTkEntry(registration_tab, placeholder_text="Password", show="*", width=250)
        self.password_reg_entry.pack(pady=(10, 5))

        self.password_reg_error = ctk.CTkLabel(registration_tab, text="", text_color="red", font=("Arial", 10))
        self.password_reg_error.pack()

        self.register_button = ctk.CTkButton(
            registration_tab, text="Register", command=self.register,
            fg_color=self.primary_color, hover_color="#2a6a9a", width=150
        )
        self.register_button.pack(pady=20)

        self.back_button("Back",registration_tab,self.startapp)

    #the following is the user registration function
    def register(self):
        username = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_reg_entry.get()
        self.name_error.configure(text="")
        self.email_error.configure(text="")
        self.password_reg_error.configure(text="")

        if not username:
            self.name_error.configure(text="Please enter your name.")
        elif not email:
            self.email_error.configure(text="Please enter your email")
        elif not self.validate_email(email):
            self.email_error.configure(text="Invalid email format.")
        elif not self.validate_password(password):
            self.password_reg_error.configure(text="Password should be at least 8 characters long with letters and numbers.")
        elif self.email_exists(email):
            self.email_error.configure(text="User already exists.")
        else:
            print("adding user")
            self.add_user(username,email,password)
            

    def add_user(self,username,email,password):
        
        header = ["username", "email", "password", "userID"]

        if not os.path.exists(USER_FILE) or os.path.getsize(USER_FILE) == 0:
            with open(USER_FILE, mode="w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=header)
                writer.writeheader()

        encrypted_username = self.crypt.encrypt(username)
        encrypted_email = self.crypt.encrypt(email)
        encrypted_password = self.crypt.encrypt(password)
        encrypted_userID = self.crypt.encrypt(shortuuid.uuid())

        print("data encrypted")
        # add user since email doesnt exist
        with open(USER_FILE, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writerow(
                {
                    "username": encrypted_username,
                    "email": encrypted_email,
                    "password": encrypted_password,
                    "userID": encrypted_userID,
                }
            )
        print("User  added to CSV:") 
        print("login")   # Debugging line
        # print(f"Username: {encrypted_username}, Email: {encrypted_email}, Password: {encrypted_password}, UserID: {encrypted_userID}")  # Debugging line

    #the following are validation functions
    def email_exists(self, email):
        if os.path.exists(USER_FILE) and os.path.getsize(USER_FILE) > 0:
            with open(USER_FILE, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    decrypted_email = self.crypt.decrypt(row["email"])  # Decrypt the email in the CSV
                    if decrypted_email == email:  # Compare decrypted email
                        return True
        return False
    
    def validate_email(self, email):
        try:
            validators.email(email)
            return True
        except errors.InvalidEmailError:
            return False

    def validate_password(self, password):
        return bool(re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@#$%^&+=_-]{8,}$'
, password))

    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def validate_numeric(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def validate_contact(self, contact):
        return bool(re.match(r'^\+?[0-9]{10,15}$', contact))  # Contact must be a valid phone number
    
    def save_user(self, username, email, password, file_path):
        with open(file_path, 'r+') as f:
            users = json.load(f)
            if username in users:
                return False
            users[username] = {"email": email, "password": password}
            f.seek(0)
            json.dump(users, f, indent=4)
        return True
    

    def check_json_user_credentials(self, username, password, file_path):
        with open(file_path, 'r') as f:
            users = json.load(f)
            return username in users and users[username]["password"] == password

    def user_interface(self):
        self.clear_page()
        self.tab_create()
        self.add_accouns_tab()
        self.add_scan_tab()
        self.add_bookings_tab()

    def add_accouns_tab(self):
        account_tab = self.tabview.add("Account")
        account_tab.configure(fg_color=self.secondary_color)


        self.success_label = ctk.CTkLabel(account_tab, text="Login successful")
        self.success_label.pack(pady=20)

        self.hello_user = ctk.CTkLabel(account_tab, text=f"Hello {self.username}")
        self.hello_user.pack(pady=10)

        self.usr_acct = user_account.User_Account(self.user_id)
        self.usr_acct.add_account()

        self.balance = ctk.CTkLabel(
            account_tab, text=f"Balance: {self.usr_acct.get_balance()}"
        )
        self.balance.pack(pady=10)

        self.deposit = ctk.CTkButton(account_tab, text="Deposit", command=self.depositor)
        self.deposit.pack(pady=10)

        self.withdraw = ctk.CTkButton(account_tab, text="Withdraw", command=self.withdrawer)
        self.withdraw.pack(pady=10)

        self.remove_acct = ctk.CTkButton(
            account_tab, text="Remove Account", command=self.usr_acct.remove_account
        )
        self.remove_acct.pack(pady=10)

        self.back_button("Log Out",account_tab,self.startapp)
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
                self.user_interface()
            # self.balance.configure(text=f"Balance: {self.usr_acct.get_balance()}")
            else:
                print("Invalid input: Please enter a numeric value for the deposit.")

        self.submit_button = ctk.CTkButton(self, text="Submit", command=submit_deposit)
        self.submit_button.pack(pady=10)

        self.back_button = ctk.CTkButton(self, text="Back", command=self.user_interface)
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
                self.user_interface()
                # self.balance.configure(text=f"Balance: {self.usr_acct.get_balance()}")
            else:
                print("Invalid input: Please enter a numeric value for the withdrawal.")

        self.submit_button = ctk.CTkButton(self, text="Submit", command=submit_withdraw)
        self.submit_button.pack(pady=10)

        self.back_button = ctk.CTkButton(self, text="Back", command=self.user_interface)
        self.back_button.pack(pady=10)


    def add_scan_tab(self):#to do
        scan_tab = self.tabview.add("Scan n Pay")
        scan_tab.configure(fg_color=self.secondary_color)

        self.back_button("Log Out",scan_tab,self.startapp)


    def add_bookings_tab(self):
        booking_tab = self.tabview.add("Bookings")
        booking_tab.configure(fg_color=self.secondary_color)

        self.route_entry = ctk.CTkEntry(booking_tab, placeholder_text="Route (From - To)", width=250)
        self.route_entry.pack(pady=(20, 5))

        self.route_error = ctk.CTkLabel(booking_tab, text="", text_color="red", font=("Arial", 10))
        self.route_error.pack()

        self.date_of_travel_entry = ctk.CTkEntry(booking_tab, placeholder_text="Date of Travel (YYYY-MM-DD)", width=250)
        self.date_of_travel_entry.pack(pady=(10, 5))

        self.date_of_travel_error = ctk.CTkLabel(booking_tab, text="", text_color="red", font=("Arial", 10))
        self.date_of_travel_error.pack()

        self.passenger_count_entry = ctk.CTkEntry(booking_tab, placeholder_text="Number of Passengers", width=250)
        self.passenger_count_entry.pack(pady=(10, 5))

        self.passenger_count_error = ctk.CTkLabel(booking_tab, text="", text_color="red", font=("Arial", 10))
        self.passenger_count_error.pack()

        self.book_button = ctk.CTkButton(
            booking_tab, text="Book Now", command=self.book,
            fg_color=self.primary_color, hover_color="#2a6a9a", width=150
        )
        self.book_button.pack(pady=20)

        self.back_button("Log Out",booking_tab,self.startapp)

    def book(self):
        route = self.route_entry.get()
        date = self.date_of_travel_entry.get()
        passenger_count = self.passenger_count_entry.get()
        self.route_error.configure(text="")
        self.date_of_travel_error.configure(text="")
        self.passenger_count_error.configure(text="")

        if not route:
            self.route_error.configure(text="Please enter the route.")
        elif not self.validate_date(date):
            self.date_of_travel_error.configure(text="Invalid date format. Use YYYY-MM-DD.")
        elif not self.validate_numeric(passenger_count):
            self.passenger_count_error.configure(text="Enter a valid passenger count.")
        else:
            self.save_booking(route, date, passenger_count)
            print("Booking successful!")


    def save_booking(self, route, date, passenger_count):
        with open(BOOKING_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([route, date, passenger_count])

if __name__ == "__main__":
    app = BusQr()
    app.mainloop()
