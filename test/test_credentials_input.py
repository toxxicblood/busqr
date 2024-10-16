import credentials_input
import unittest
from unittest.mock import patch
from validator_collection import checkers
# Assuming your module with the functions is named 'credentials_input'
# from credentials_input import input_name, input_email, input_password

class TestCredentialsInput(unittest.TestCase):

    @patch('builtins.input', return_value='John Doe')
    def test_input_name(self, mock_input):
        # Test input_name returns correct name
        self.assertEqual(credentials_input.input_name(), 'John Doe')

    @patch('builtins.input', side_effect=['', '  ', 'Jane Doe'])
    def test_input_name_with_empty_input(self, mock_input):
        # Test input_name handles empty or whitespace input
        self.assertEqual(credentials_input.input_name(), 'Jane Doe')

    @patch('builtins.input', return_value='jane@example.com')
    @patch('validator_collection.checkers.is_email', return_value=True)
    def test_input_email(self, mock_input, mock_is_email):
        # Test input_email with valid email
        self.assertEqual(credentials_input.input_email(), 'jane@example.com')
        mock_is_email.assert_called_with('jane@example.com')

    @patch('builtins.input', side_effect=['invalid', 'jane@example.com'])
    @patch('checkers.is_email', side_effect=[False, True])
    def test_input_email_invalid_then_valid(self, mock_input, mock_is_email):
        # Test input_email with invalid first input, then valid email
        self.assertEqual(credentials_input.input_email(), 'jane@example.com')
        self.assertEqual(mock_is_email.call_count, 2)  # Called twice, first invalid, then valid

    @patch('builtins.input', return_value='strongpassword123')
    def test_input_password(self, mock_input):
        # Test input_password returns correct password
        self.assertEqual(credentials_input.input_password(), 'strongpassword123')

    @patch('builtins.input', side_effect=['', 'mypassword'])
    def test_input_password_with_empty_input(self, mock_input):
        # Test input_password handles empty input
        self.assertEqual(credentials_input.input_password(), 'mypassword')


if __name__ == '__main__':
    unittest.main()
