from cryptography.fernet import Fernet
import os

class DataEncryptor:
    def __init__(self, key_file='encryption_key.key'):
        self.key_file = key_file
        self.key = self._load_or_generate_key()
        self.cipher = Fernet(self.key)

    def _load_or_generate_key(self):
        """Loads the encryption key from a file or generates a new one if it doesn't exist."""
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
        """Encrypts the given data."""
        if isinstance(data, str):
            data = data.encode()  # Convert string to bytes
        encrypted_data = self.cipher.encrypt(data)
        return encrypted_data

    def decrypt(self, encrypted_data):
        """Decrypts the given data."""
        decrypted_data = self.cipher.decrypt(encrypted_data)
        return decrypted_data.decode()  # Convert bytes back to string

# Example Usage
if __name__ == "__main__":
    encryptor = DataEncryptor()

    # Encrypt some data
    encrypted = encryptor.encrypt("This is a secret message")
    print(f"Encrypted: {encrypted}")

    # Decrypt the data
    decrypted = encryptor.decrypt(encrypted)
    print(f"Decrypted: {decrypted}")
