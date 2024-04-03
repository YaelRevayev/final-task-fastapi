
from typing import List
import logging
from fastapi import FastAPI, UploadFile, File
import hashlib
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

app = FastAPI()
logging.basicConfig(filename='fastapi_server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

def read_key_from_file(filepath):
    # Read the key from the file
    with open(filepath, "rb") as key_file:
        key = key_file.read()

    # Check if the key length is valid for AES-256 (32 bytes)
    if len(key) == 32:
        return key
    elif len(key) > 32:
        # If the key is longer than 32 bytes, truncate it
        return key[:32]
    else:
        # If the key is shorter than 32 bytes, pad it with zeros
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

        # Merge file contents
        merged_content = content1 + content2

        # Read the secret key from file
        key = read_key_from_file("tornado.key")

        # Sign the merged content
        encrypted_hash, iv = sign_file(merged_content, key)

        merged_filename = files[1].filename.replace("_b", ".jpg")
        with open("merged_files/" + merged_filename, "wb") as f:
            f.write(merged_content + encrypted_hash + iv)

        logging.info("Consolidated file saved: %s", merged_filename)
        return {"message": "Consolidated file saved successfully."}
    except Exception as e:
        logging.error("An error occurred: %s", str(e))
        return {"error": "An error occurred while processing the request."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
