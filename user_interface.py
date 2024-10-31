import tkinter as tk
import customtkinter as ctk



ctk.set_appearance_mode("system")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('BusQr')
        self.geometry('600*500')

        self.bus_button = ctk.CTkButton(self, text='Bus' )
        self.bus_button.pack(pady=20, padx=20)
        self.user_button = ctk.CTkButton(self, text=  'User', command = self.launch_user )
        self.user_button.pack(pady=20, padx=20)

    def launch_user(self):
        self.user_button.destroy()
        self.bus_button.destroy()
        #label welcomes users
        self.welcome_label = ctk.CTkLabel(self, text='Karibu User')
        self.welcome_label.pack(pady=20)
        self.login_button = ctk.CTkButton(self, text='Login' ,command = self.login)
        self.login_button.grid(row=0, column=0, padx=10)

        self.register_button = ctk.CTkButton(self, text= 'Register', command = self.register)
        self.register_button.grid(row=0, column=1, padx=10)







app = App()
app.mainloop()