from typing import List
from fastapi import FastAPI, UploadFile, File
import hashlib
from logger import create_loggers
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
import config

app = FastAPI()


def read_key_from_file(filepath):
    with open(filepath, "rb") as key_file:
        key = key_file.read()
    if len(key) == config.AES_KEY_LENGTH:
        return key
    elif len(key) > config.AES_KEY_LENGTH:
        return key[: config.AES_KEY_LENGTH]
    else:
        return key.ljust(config.AES_KEY_LENGTH, b"\0")


def sign_file(content, key):
    sha512_hash = hashlib.sha512(content).hexdigest()
    iv = get_random_bytes(config.IV_BYTES_LENGTH)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    encrypted_hash = cipher.encrypt(sha512_hash.encode())
    return encrypted_hash, iv


@app.post("/merge_and_sign")
async def merge_and_sign(files: List[UploadFile] = File(...)):
    try:
        merged_files_logger, error_logger = create_loggers()
        content1 = await files[0].read()
        content2 = await files[1].read()

        merged_content = content1 + content2
        key = read_key_from_file(config.KEY_FILE_NAME)
        encrypted_hash, iv = sign_file(merged_content, key)

        merged_filename = files[1].filename.replace("_b", ".jpg")
        with open("merged_files/" + merged_filename, "wb") as f:
            f.write(merged_content + iv + encrypted_hash)

        merged_files_logger.info("Merged file saved: %s", merged_filename)
    except Exception as e:
        error_logger.error("An error occurred: %s", str(e))
