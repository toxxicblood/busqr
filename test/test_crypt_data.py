import unittest
import os
from cryptography.fernet import Fernet, InvalidToken
from crypt_data import DataEncryptor  # Replace with the actual module name

class TestDataEncryptor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_key_file = "test_encryption_key.key"

    def setUp(self):
        # Ensure we start with a fresh DataEncryptor instance before each test
        if os.path.exists(self.test_key_file):
            os.remove(self.test_key_file)
        self.encryptor = DataEncryptor(key_file=self.test_key_file)

    @classmethod
    def tearDownClass(cls):
        # Clean up key file after all tests complete
        if os.path.exists(cls.test_key_file):
            os.remove(cls.test_key_file)

    def test_key_generation(self):
        # Verify that a new key file is created and that it matches the encryptor's key
        self.assertTrue(os.path.exists(self.test_key_file), "Key file should be created")
        
        with open(self.test_key_file, "rb") as f:
            key = f.read()
        
        self.assertEqual(key, self.encryptor.key, "Loaded key should match encryptor's key")

    def test_key_consistency(self):
        # Check that the key consistency test passes with a valid key
        self.assertTrue(self.encryptor.check_key_consistency(), "Key consistency check should pass with matching keys")

    def test_inconsistent_key(self):
        # Modify the key file to simulate an inconsistent key
        with open(self.test_key_file, "wb") as f:
            f.write(b"InvalidKeyData")

        # Ensure key consistency check fails due to the modified key
        self.assertFalse(self.encryptor.check_key_consistency(), "Key consistency check should fail with mismatched keys")

    def test_encrypt_and_decrypt(self):
        data = "This is a test message"
        encrypted_data = self.encryptor.encrypt(data)
        decrypted_data = self.encryptor.decrypt(encrypted_data)
        self.assertEqual(data, decrypted_data, "Decrypted data should match original")

    def test_invalid_decrypt(self):
        # Test decryption with invalid data
        invalid_data = "InvalidEncryptedData"
        decrypted_data = self.encryptor.decrypt(invalid_data)
        self.assertIsNone(decrypted_data, "Decryption should fail and return None for invalid data")

    def test_is_valid_encrypted_data(self):
        # Check the validity of encrypted data
        encrypted_data = self.encryptor.encrypt("test")
        self.assertTrue(self.encryptor.is_valid_encrypted_data(encrypted_data), "Valid encrypted data should be identified correctly")
        self.assertFalse(self.encryptor.is_valid_encrypted_data(123), "Non-string data should return False")

if __name__ == "__main__":
    unittest.main()
