import unittest
from unittest.mock import MagicMock, patch, mock_open
import csv
from app import App
import shortuuid

# Define a mock encryptor for simplifying cryptographic function mocking
class MockEncryptor:
    def encrypt(self, x):
        return f"encrypted_{x}"

    def decrypt(self, x):
        return x.replace('encrypted_', '')

class TestApp(unittest.TestCase):
    
    # Set up common mock data and app instance
    def setUp(self):
        self.app = App()
        self.app.crypt = MockEncryptor()
        self.mock_name = "Test User"
        self.mock_email = "testuser@example.com"
        self.mock_password = "securepassword"

        # Mock entries for name, email, and password inputs
        self.mock_name_entry = MagicMock()
        self.mock_name_entry.get.return_value = self.mock_name
        self.mock_email_entry = MagicMock()
        self.mock_email_entry.get.return_value = self.mock_email
        self.mock_password_entry = MagicMock()
        self.mock_password_entry.get.return_value = self.mock_password

        # Attach mocked entries to the app instance
        self.app.name_entry = self.mock_name_entry
        self.app.email_entry = self.mock_email_entry
        self.app.password_entry = self.mock_password_entry

        # Mock the submit button and back button to prevent AttributeError
        self.app.submit_button = MagicMock()
        self.app.back_button = MagicMock()  # Add this line for back_button


    @patch('app.shortuuid.uuid', return_value='1234567890')  # Mock the UUID generation to return a fixed value
    @patch('app.csv.DictWriter')
    @patch('app.csv.DictReader')
    @patch('app.open', new_callable=mock_open, read_data="email,password,username,userID\n")
    def test_register_user(self, mock_open, MockDictReader, MockDictWriter, mock_uuid):
        # Mock the encryption function to return a fixed encrypted value
        # mock_crypt.encrypt.return_value = 'encrypted_1234567890'  # Uncomment if needed

        # Mock CSV reading to simulate no existing email
        MockDictReader.return_value = iter([])  # Simulate an empty CSV

        # Mock the CSV writer
        mock_csv_writer = MagicMock()
        MockDictWriter.return_value = mock_csv_writer

        # Run the registration process
        self.app.verify_inputs()  # Ensure input verification passes
        self.app.add_user()  # Add a user to the CSV

        # Verify that the user data is correctly written to the CSV
        mock_csv_writer.writerow.assert_called_with({
            'username': 'encrypted_Test User',
            'email': 'encrypted_testuser@example.com',
            'password': 'encrypted_securepassword',
            'userID': 'encrypted_1234567890'  # Simulated UUID
        })


    @patch('app.csv.DictReader')
    @patch('app.open', new_callable=mock_open)
    def test_login_user_success(self, mock_open, MockDictReader):
        # Simulate the CSV read operation with an existing user
        MockDictReader.return_value = iter([
            {'email': 'encrypted_testuser@example.com', 'password': 'encrypted_securepassword', 'username': 'Test User', 'userID': 'encrypted_1234567890'}
        ])

        # Mock entries for email and password inputs
        self.app.email_entry = MagicMock()
        self.app.email_entry.get.return_value = self.mock_email
        self.app.password_entry = MagicMock()
        self.app.password_entry.get.return_value = self.mock_password

        # Run the login process
        self.app.login_user()

        # Verify that the login was successful and user attributes were set
        self.assertEqual(self.app.username, 'Test User')
        self.assertEqual(self.app.user_id, '1234567890')

    @patch('app.ctk.CTkButton')  # Mock all CTkButton widgets
    @patch('app.ctk.CTkEntry')  # Mock all CTkEntry widgets
    @patch('app.csv.DictReader')  # Mock CSV reading
    @patch('app.open', new_callable=MagicMock)  # Mock file operations
    def test_login_user_fail(self, mock_open, MockDictReader, MockEntry, MockButton):
        # Initialize the app and mock the cryptographic functions
        app = App()
        app.crypt = MagicMock()
        app.crypt.encrypt.side_effect = lambda x: f"encrypted_{x}"
        app.crypt.decrypt.side_effect = lambda x: x.replace('encrypted_', '')

        # Simulate an incorrect login (user not found)
        mock_email = "wronguser@example.com"
        mock_password = "wrongpassword"

        # Simulate the CSV read operation (no matching user)
        MockDictReader.return_value = iter([])

        # Mock entries to return the inputs when 'get' is called
        mock_email_entry = MagicMock()
        mock_email_entry.get.return_value = mock_email
        mock_password_entry = MagicMock()
        mock_password_entry.get.return_value = mock_password

        # Set the mock entries to the app's instance
        app.email_entry = mock_email_entry
        app.password_entry = mock_password_entry

        # Mock the username and user_id attributes
        app.username = None
        app.user_id = None

        # Run login logic
        app.login_user()

        # Assert that the app handled the user not being found and did not crash
        self.assertIsNone(app.username)
        self.assertIsNone(app.user_id)



    @patch('app.csv.DictReader')
    @patch('app.open', new_callable=mock_open)
    def test_email_not_exists(self, mock_open, MockDictReader):
        # Simulate an empty CSV, meaning no matching user
        MockDictReader.return_value = iter([])

        # Check if email_exists returns False for a non-existent email
        result = self.app.email_exists("nonexistentuser@example.com")
        self.assertFalse(result)

    # Additional test to validate inputs (edge cases)
    def test_verify_inputs_invalid_email(self):
        # Mock invalid email
        self.app.email_entry.get.return_value = "invalid-email"
        
        with self.assertRaises(ValueError):
            self.app.verify_inputs()  # Should raise ValueError for invalid email

    def test_verify_inputs_empty_name(self):
        # Mock empty name
        self.app.name_entry.get.return_value = ""
        
        with self.assertRaises(ValueError):
            self.app.verify_inputs()  # Should raise ValueError for empty name

if __name__ == '__main__':
    unittest.main()
