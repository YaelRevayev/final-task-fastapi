import unittest
from unittest.mock import MagicMock, patch
import os
import sys
from Crypto.Cipher import AES

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(project_dir)
from src.encryption import sign_file, read_key_from_file
import configs.config as config


class TestFileFunctions(unittest.TestCase):

    @patch("builtins.open", create=True)
    def test_read_key_from_file_given_exact_length_key_returns_the_same_key(
        self, mock_open
    ):
        key_32_bytes = "12345678901234567890123456789012"
        mock_open.return_value.__enter__.return_value.read.return_value = key_32_bytes

        key = read_key_from_file("test_key_file")

        self.assertEqual(len(key), config.AES_KEY_LENGTH)
        self.assertEqual(key, key_32_bytes)

    @patch("builtins.open", create=True)
    def test_read_key_from_file_given_longer_key_returns_error(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = (
            b"test_key123456789012345678900000000000000000000000000"
        )
        with self.assertRaises(ValueError) as context:
            read_key_from_file("test_key_file")
        self.assertEqual(
            str(context.exception), "Key length is not equal to the AES key length"
        )

    @patch("builtins.open", create=True)
    def test_read_key_from_file_given_shorter_key_returns_error(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"short_key"
        with self.assertRaises(ValueError) as context:
            read_key_from_file("test_key_file")
        self.assertEqual(
            str(context.exception), "Key length is not equal to the AES key length"
        )

    @patch("hashlib.sha512")
    @patch("Crypto.Cipher.AES.new")
    def test_sign_file_given_valid_values_returns_hash_and_iv(
        self, mock_aes_new, mock_sha512
    ):
        content = b"test_content"
        key = b"test_key"

        mock_aes_instance = MagicMock()
        mock_aes_new.return_value = mock_aes_instance
        mock_aes_instance.encrypt.return_value = b"test_encrypted_hash"
        mock_sha512.return_value.hexdigest.return_value = "test_sha512_hash"

        result = sign_file(content, key)

        self.assertEqual(result[0], b"test_encrypted_hash")
        mock_sha512.assert_called_once_with(content)
        mock_aes_instance.encrypt.assert_called_once_with(b"test_sha512_hash")


if __name__ == "__main__":
    unittest.main()
