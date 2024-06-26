import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from configs import config
from typing import Tuple
from logger import fastapi_logger


def read_key_from_file(file_path: str):
    fastapi_logger.debug("Reading key from file..")
    with open(file_path, "rb") as file:
        key = file.read()

    if len(key) < config.AES_KEY_LENGTH:
        key += b" " * (config.AES_KEY_LENGTH - len(key))
    elif len(key) > config.AES_KEY_LENGTH:
        raise ValueError("Key length is longer than the AES key length")

    return key

def sign_file(content: bytes, key: bytes) -> Tuple[bytes, bytes]:
    fastapi_logger.debug("Signing file..")
    sha512_hash = hashlib.sha512(content).hexdigest()
    iv = get_random_bytes(config.IV_BYTES_LENGTH)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    encrypted_hash = cipher.encrypt(sha512_hash.encode())
    return encrypted_hash, iv
