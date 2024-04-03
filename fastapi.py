import logging
from fastapi import FastAPI, UploadFile, File
import hashlib
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
import os

app = FastAPI()

logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

KEY = b'Sixteen byte key'
MODE = AES.MODE_CFB

@app.post("/merge_and_sign")
async def merge_and_sign(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    try:
        content1 = await file1.read()
        content2 = await file2.read()

        merged_content = content1 + content2
        sha512_hash = hashlib.sha512(merged_content).hexdigest()
        iv = get_random_bytes(16)
        aes_cipher = AES.new(KEY, MODE, iv)
        encrypted_content = aes_cipher.encrypt(merged_content)
        filename = "merged_file.jpg"

        with open(filename, "wb") as f:
            f.write(encrypted_content)

        with open(filename, "ab") as f:
            f.write(sha512_hash.encode())

        logging.info("United file saved: %s", filename)

        return {"message": "Files merged, signed, and encrypted successfully.", "sha512_hash": sha512_hash}
    except Exception as e:
        logging.error("An error occurred: %s", str(e))
        return {"error": "An error occurred while processing the files."}

