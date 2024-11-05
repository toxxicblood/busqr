from cryptography.fernet import Fernet, InvalidToken
import os
import base64

class DataEncryptor:
    def __init__(self, key_file='encryption_key.key'):
        self.key_file = key_file
        self.key = self._load_or_generate_key()
        self.cipher = Fernet(self.key)

    def _load_or_generate_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as key_file:
                key = key_file.read()
                print(f"Key loaded from {self.key_file}.")
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as key_file:
                key_file.write(key)
                print(f"New key generated and saved to {self.key_file}.")
        return key

    def encrypt(self, data):
        if isinstance(data, str):
            data = data.encode()  # Convert string to bytes
        encrypted_data = self.cipher.encrypt(data)
        encoded_data = base64.urlsafe_b64encode(encrypted_data).decode()  # Convert bytes to string
        print(f"Encrypted data: {encoded_data}")  # Debugging line
        return encoded_data

    def decrypt(self, encrypted_data):
        try:
            print(f"Decrypting data: {encrypted_data}")  # Debugging line
            encrypted_data = base64.urlsafe_b64decode(encrypted_data.encode())  # Convert string back to bytes
            decrypted_data = self.cipher.decrypt(encrypted_data)
            return decrypted_data.decode()  # Convert bytes back to string
        except (InvalidToken, ValueError) as e:
            print(f"Decryption failed: {e}")  # Debugging line
            return None

    def is_valid_encrypted_data(self, encrypted_data):
        return isinstance(encrypted_data, str)  # Expecting string for CSV storage

    def check_key_consistency(self):
        """Checks if the current key matches the key stored in the key file."""
        current_key = self.key
        with open(self.key_file, 'rb') as key_file:
            stored_key = key_file.read()
        if current_key == stored_key:
            print("Key consistency check passed.")
            return True
        else:
            print("Key consistency check failed.")
            return False

# Example Usage
if __name__ == "__main__":
    encryptor = DataEncryptor()

    # Encrypt some data
    encrypted = encryptor.encrypt("This is a secret message")
    print(f"Encrypted: {encrypted}")

    # Check key consistency
    encryptor.check_key_consistency()

    # Decrypt the data
    decrypted = encryptor.decrypt(encrypted)
    if decrypted is not None:
        print(f"Decrypted: {decrypted}")
    else:
        print("Failed to decrypt the data.")