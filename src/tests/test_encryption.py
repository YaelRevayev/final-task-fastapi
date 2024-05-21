import unittest
from unittest.mock import MagicMock, patch, mock_open
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from encryption import sign_file, read_key_from_file
import configs as config


class TestFileFunctions(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data=b"short_key")
    def test_key_length_given_shorter_key_should_add_empty_spaces(self, mock_open_file):
        key = read_key_from_file("dummy_file_path")
        expected_key = b"short_key" + b" " * (config.AES_KEY_LENGTH - len(b"short_key"))
        self.assertEqual(key, expected_key)

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=b"this_is_a_longer_key_than_32_bytes",
    )
    def test_key_length_longer(self, mock_open_file):
        with self.assertRaises(ValueError):
            read_key_from_file("dummy_file_path")

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=b"9a4b5e2c8f1d6a7b3c4e2f9a4b5e2c8f",
    )
    def test_key_length_given_exact_key_length_return_the_same_key(
        self, mock_open_file
    ):
        key = read_key_from_file("dummy_file_path")
        self.assertEqual(len(key), 32)
        self.assertEqual(key, b"9a4b5e2c8f1d6a7b3c4e2f9a4b5e2c8f")

    @patch("hashlib.sha512")
    @patch("Crypto.Cipher.AES.new")
    def test_sign_file_given_valid_values_should_return_hash_and_iv(
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
