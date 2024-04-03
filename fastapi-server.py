import logging
from fastapi import FastAPI, UploadFile, File
import hashlib
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from typing import List

app = FastAPI()
logging.basicConfig(filename='fast-api-server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

@app.post("/merge_and_sign")
async def merge_and_sign(files: List[UploadFile] = File(...)):
    try:
        merged_content = await merge_files(files)
        sha512_hash = hashlib.sha512(merged_content).hexdigest()
        iv = get_random_bytes(16)
        aes_cipher = AES.new(read_key_from_file("tornado.key"), AES.MODE_CFB, iv)
        encrypted_content = aes_cipher.encrypt(sha512_hash)

        filename = create_new_file_name(files[1].filename)
        with open("./final-files/{name}".format(name=filename), "wb") as f:
            f.write(iv)

        with open("./final-files/{name}".format(name=filename), "ab") as f:
            f.write(encrypted_content)

        logging.info("Files merged, signed, and encrypted successfully.: %s", filename)
    
    except Exception as e:
        logging.error("An error occurred: %s", str(e))
    
def read_key_from_file(filepath):
    key_file = open(filepath, "rb")
    data = key_file.read() 
    key_file.close()
    return data

def create_new_file_name(second_file_name):
    return second_file_name[:2] + '.jpg'

async def merge_files(files):
    file_contents = []
    for file in files:
        file_contents.append(await file.read())
    return b"".join(file_contents)


def main():
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)