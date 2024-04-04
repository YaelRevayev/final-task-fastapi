from typing import List
from logger import configure_error_logger, configure_success_logger, reset_folder
from fastapi import FastAPI, UploadFile, File
import hashlib
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

app = FastAPI()
info_logger = configure_success_logger()
error_logger= configure_error_logger()

def read_key_from_file(filepath):
    with open(filepath, "rb") as key_file:
        key = key_file.read()
    if len(key) == 32:
        return key
    elif len(key) > 32:
        return key[:32]
    else:
        return key.ljust(32, b'\0')

def sign_file(content, key):
    sha512_hash = hashlib.sha512(content).hexdigest()
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    encrypted_hash = cipher.encrypt(sha512_hash.encode())
    return encrypted_hash, iv

@app.post("/merge_and_sign")
async def merge_and_sign(files: List[UploadFile] = File(...)):
    try:
        content1 = await files[0].read()
        content2 = await files[1].read()

        merged_content = content1 + content2
        key = read_key_from_file("tornado.key")
        encrypted_hash, iv = sign_file(merged_content, key)

        merged_filename = files[1].filename.replace("_b", ".jpg")
        with open("merged_files/" + merged_filename, "wb") as f:
            f.write(merged_content + encrypted_hash + iv)

        info_logger.info("Consolidated file saved: %s", merged_filename)
    except Exception as e:
        error_logger.error("An error occurred: %s", str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
