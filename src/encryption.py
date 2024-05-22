import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from configs import config


def read_key_from_file(file_path: str):
    with open(file_path, "rb") as file:
        key = file.read()

    if len(key) < config.AES_KEY_LENGTH:
        key += b" " * (config.AES_KEY_LENGTH - len(key))
    elif len(key) > config.AES_KEY_LENGTH:
        raise ValueError("Key length is longer than the AES key length")

    return key


def sign_file(content, key):
    sha512_hash = hashlib.sha512(content).hexdigest()
    iv = get_random_bytes(config.IV_BYTES_LENGTH)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    encrypted_hash = cipher.encrypt(sha512_hash.encode())
    return encrypted_hash, iv
