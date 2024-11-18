import customtkinter as ctk
import qrcode
from PIL import Image, ImageTk
from pyzbar.pyzbar import decode
import sqlite3
from tkinter import filedialog, messagebox

# Initialize SQLite database
def initialize_db():
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT,
            amount TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Save transaction to database
def save_transaction(phone_number, amount):
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (phone_number, amount) VALUES (?, ?)", (phone_number, amount))
    conn.commit()
    conn.close()

# Fetch transaction history
def fetch_transactions():
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT phone_number, amount, timestamp FROM transactions ORDER BY timestamp DESC")
    data = cursor.fetchall()
    conn.close()
    return data

# QR Code Generator Function
def generate_qr_code(phone_number):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(phone_number)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    img.save("driver_qr_code.png")
    return "driver_qr_code.png"

# Main Application
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pochi La Biashara QR Code App")
        self.geometry("700x500")
        self.configure(padx=20, pady=20)

        # Initialize database
        initialize_db()

        # Tabs
        self.tabview = ctk.CTkTabview(self, width=680, height=450)
        self.tabview.pack(pady=20)
        
        self.generator_tab = self.tabview.add("QR Code Generator")
        self.scanner_tab = self.tabview.add("QR Code Scanner")

        # Generator Tab
        self.generator_frame = ctk.CTkFrame(self.generator_tab)
        self.generator_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(self.generator_frame, text="Driver's Phone Number:").pack(pady=10)
        self.phone_entry = ctk.CTkEntry(self.generator_frame, placeholder_text="Enter Phone Number")
        self.phone_entry.pack(pady=5)

        self.generate_button = ctk.CTkButton(self.generator_frame, text="Generate QR Code", command=self.generate_qr)
        self.generate_button.pack(pady=10)

        self.qr_image_label = ctk.CTkLabel(self.generator_frame, text="Generated QR Code will appear here")
        self.qr_image_label.pack(pady=10)

        # Scanner Tab
        self.scanner_frame = ctk.CTkFrame(self.scanner_tab)
        self.scanner_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.upload_button = ctk.CTkButton(self.scanner_frame, text="Upload QR Code to Scan", command=self.scan_qr)
        self.upload_button.pack(pady=10)

        self.result_label = ctk.CTkLabel(self.scanner_frame, text="Scanned Information Will Appear Here", wraplength=500)
        self.result_label.pack(pady=10)

        self.history_button = ctk.CTkButton(self.scanner_frame, text="Show Transaction History", command=self.show_history)
        self.history_button.pack(pady=10)

    # QR Code Generator Logic
    def generate_qr(self):
        phone_number = self.phone_entry.get().strip()
        if not phone_number:
            messagebox.showerror("Error", "Please enter a phone number")
            return
        
        # Generate and display the QR code
        img_path = generate_qr_code(phone_number)
        img = Image.open(img_path)
        img.thumbnail((200, 200))
        img_tk = ImageTk.PhotoImage(img)
        self.qr_image_label.configure(image=img_tk, text="")
        self.qr_image_label.image = img_tk
        messagebox.showinfo("Success", f"QR Code generated and saved as {img_path}")

    # QR Code Scanner Logic
    def scan_qr(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if not file_path:
            return
        
        img = Image.open(file_path)
        decoded_objects = decode(img)

        if decoded_objects:
            phone_number = decoded_objects[0].data.decode("utf-8")
            amount = messagebox.askstring("Amount", "Enter the payment amount:")

            if amount:
                save_transaction(phone_number, amount)
                self.result_label.configure(text=f"Transaction Saved:\nPhone: {phone_number}\nAmount: {amount}")
        else:
            messagebox.showerror("Error", "No QR Code detected in the image")

    # Show Transaction History
    def show_history(self):
        history = fetch_transactions()
        if history:
            history_text = "\n".join([f"Phone: {row[0]}, Amount: {row[1]}, Date: {row[2]}" for row in history])
        else:
            history_text = "No transactions recorded yet."
        messagebox.showinfo("Transaction History", history_text)


if __name__ == "__main__":
    app = App()
    app.mainloop()
