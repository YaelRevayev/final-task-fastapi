from typing import List
from fastapi import FastAPI, UploadFile, File
from datetime import datetime
import os
from encryption import read_key_from_file, sign_file
import configs.config as config
from logger import fastapi_logger

app = FastAPI()


def part_a_or_b(filename):
    index_of_underscore = filename.find("_")
    if index_of_underscore != -1 and index_of_underscore + 1 < len(filename):
        part = filename[index_of_underscore + 1]
        if part not in ["a", "b"]:
            return None
        return part
    else:
        raise SyntaxError("file name syntax is invalid.")


async def list_files_in_order(files):
    part_a = None
    part_b = None

    for file in files:
        file_content = await file.read()
        if file.filename.endswith("_a.jpg"):
            part_a = file_content
        elif file.filename.endswith("_b"):
            part_b = file_content
    return (part_a, part_b)


def write_to_merged_file(filename, merged_content, iv, encrypted_hash):
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    if filename.endswith("_a.jpg"):
        merged_filename = filename[:-6] + ".jpg"
    elif filename.endswith("_b"):
        merged_filename = filename[:-2] + ".jpg"
    with open("/{0}/merged_files/{1}".format(project_dir, merged_filename), "wb") as f:
        f.write(merged_content + iv + encrypted_hash)
    fastapi_logger.info("Merged file saved: %s", merged_filename)


@app.post("/merge_and_sign")
async def merge_files(files: List[UploadFile] = File(...)):
    try:
        part_a, part_b = await list_files_in_order(files)
        merged_content = part_a + part_b
        key = read_key_from_file(config.KEY_FILE_NAME)
        encrypted_hash, iv = sign_file(merged_content, key)

        write_to_merged_file(files[1].filename, merged_content, iv, encrypted_hash)
    except Exception as e:
        fastapi_logger.error("An error occurred: %s", str(e))
