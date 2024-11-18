import customtkinter as ctk
from validator_collection import validators, errors
import re
from datetime import datetime
import json
import csv
import os

# Configure customtkinter appearance
ctk.set_appearance_mode("Dark")  # Set overall theme to Dark
ctk.set_default_color_theme("blue")  # Set theme color

# File paths
USER_FILE = 'users.json'
BOOKING_FILE = 'bookings.csv'
VEHICLE_FILE = 'vehicles.json'  # Store driver vehicle information in a JSON file

class BusRegistrationApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Bus Registration Portal")
        self.geometry("600x800")
        self.configure(fg_color="#1e1e2f")  # Set main window background color

        # Create tabs for different sections
        self.tabview = ctk.CTkTabview(self, width=600, height=800)
        self.tabview.pack(fill="both", expand=True)
        self.tabview.configure(fg_color="#1e1e2f")  # Tab background color

        # Set theme colors
        self.primary_color = "#3b8ed0"  # Blue for button highlights
        self.secondary_color = "#2c2c54"  # Dark purple for background elements
#
        # Create tabs
        self.create_login_tab()
        self.create_registration_tab()
        self.create_booking_tab()
        self.create_driver_registration_tab()  # Add driver registration tab

        # Initialize files if they don't exist
        self.initialize_files()

    def initialize_files(self):
        if not os.path.isfile(USER_FILE):
            with open(USER_FILE, 'w') as f:
                json.dump({}, f)
        if not os.path.isfile(BOOKING_FILE):
            with open(BOOKING_FILE, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Route', 'Date of Travel', 'Passenger Count'])
        if not os.path.isfile(VEHICLE_FILE):
            with open(VEHICLE_FILE, 'w') as f:
                json.dump({}, f)

    def create_login_tab(self):
        login_tab = self.tabview.add("Login")
        login_tab.configure(fg_color=self.secondary_color)

        self.username_entry = ctk.CTkEntry(login_tab, placeholder_text="Username or Email", width=250)
        self.username_entry.pack(pady=(20, 5))

        self.username_error = ctk.CTkLabel(login_tab, text="", text_color="red", font=("Arial", 10))
        self.username_error.pack()

        self.password_entry = ctk.CTkEntry(login_tab, placeholder_text="Password", show="*", width=250)
        self.password_entry.pack(pady=(10, 5))

        self.password_error = ctk.CTkLabel(login_tab, text="", text_color="red", font=("Arial", 10))
        self.password_error.pack()

        self.login_button = ctk.CTkButton(
            login_tab, text="Log In", command=self.login,
            fg_color=self.primary_color, hover_color="#2a6a9a", width=150
        )
        self.login_button.pack(pady=20)

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

    def create_booking_tab(self):
        booking_tab = self.tabview.add("Book a Bus")
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

    def create_driver_registration_tab(self):
        driver_tab = self.tabview.add("Register Driver")
        driver_tab.configure(fg_color=self.secondary_color)

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

        self.register_driver_button = ctk.CTkButton(
            driver_tab, text="Register Vehicle", command=self.register_driver,
            fg_color=self.primary_color, hover_color="#2a6a9a", width=150
        )
        self.register_driver_button.pack(pady=20)

    # Validation functions
    def validate_email(self, email):
        try:
            validators.email(email)
            return True
        except errors.InvalidEmailError:
            return False

    def validate_password(self, password):
        return bool(re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password))

    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def validate_numeric(self, value):
        return value.isdigit()

    def validate_contact(self, contact):
        return bool(re.match(r'^\+?[0-9]{10,15}$', contact))  # Contact must be a valid phone number

    # JSON and CSV interaction functions
    def save_user(self, username, email, password):
        with open(USER_FILE, 'r+') as f:
            users = json.load(f)
            if username in users:
                return False  # User already exists
            users[username] = {"email": email, "password": password}
            f.seek(0)
            json.dump(users, f, indent=4)
        return True

    def check_user_credentials(self, username, password):
        with open(USER_FILE, 'r') as f:
            users = json.load(f)
            return username in users and users[username]["password"] == password

    def save_booking(self, route, date, passenger_count):
        with open(BOOKING_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([route, date, passenger_count])

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

    # Button event functions
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.username_error.configure(text="")
        self.password_error.configure(text="")

        if not username or not password:
            self.username_error.configure(text="Please enter both username and password.")
        elif not self.check_user_credentials(username, password):
            self.password_error.configure(text="Invalid username or password.")
        else:
            print("Login successful!")

    def register(self):
        username = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_reg_entry.get()
        self.name_error.configure(text="")
        self.email_error.configure(text="")
        self.password_reg_error.configure(text="")

        if not username:
            self.name_error.configure(text="Please enter your name.")
        elif not self.validate_email(email):
            self.email_error.configure(text="Invalid email format.")
        elif not self.validate_password(password):
            self.password_reg_error.configure(text="Password should be at least 8 characters long with letters and numbers.")
        elif not self.save_user(username, email, password):
            self.email_error.configure(text="User already exists.")
        else:
            print("Registration successful!")

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

if __name__ == "__main__":
    app = BusRegistrationApp()
    app.mainloop()
