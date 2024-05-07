import sys
import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
src_dir = os.path.join(project_dir, "configs")
sys.path.append(project_dir)
sys.path.insert(0, src_dir)
import configs.config as config


def read_key_from_file(file_path):
    with open(file_path, "rb") as file:
        key = file.read()
    if len(key) != config.AES_KEY_LENGTH:
        raise ValueError("Key length is not equal to the AES key length")
    return key


def sign_file(content, key):
    sha512_hash = hashlib.sha512(content).hexdigest()
    iv = get_random_bytes(config.IV_BYTES_LENGTH)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    encrypted_hash = cipher.encrypt(sha512_hash.encode())
    return encrypted_hash, iv
