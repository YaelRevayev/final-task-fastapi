from typing import List
from fastapi import FastAPI, UploadFile, File
import os
import sys
import logging
import secrets
from datetime import datetime

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(os.path.join(project_dir, "configs"))
sys.path.insert(0, os.path.join(project_dir, "src"))
from encryption import read_key_from_file, sign_file

app = FastAPI()


def part_a_or_b(filename):
    index_of_underscore = filename.find("_")
    if index_of_underscore != -1 and index_of_underscore + 1 < len(filename):
        part = filename[index_of_underscore + 1]
        if part not in ["a", "b"]:
            return None
        return part
    else:
        return None


async def list_files_in_order(files):
    part_a = None
    part_b = None

    for file in files:
        file_content = await file.read()
        part = part_a_or_b(file.filename)
        if part == "a":
            part_a = file_content
        elif part == "b":
            part_b = file_content
    return (part_a, part_b)


@app.post("/merge_and_sign")
async def merge_files(files: List[UploadFile] = File(...)):
    from logger import merged_files_logger, error_logger

    try:
        part_a, part_b = await list_files_in_order(files)
        merged_content = part_a + part_b
        # key = read_key_from_file(config.KEY_FILE_NAME)
        key = secrets.token_bytes(32)
        encrypted_hash, iv = sign_file(merged_content, key)

        filename = files[1].filename
        if filename.endswith("_a.jpg"):
            merged_filename = filename[:-6] + ".jpg"
        elif filename.endswith("_b"):
            merged_filename = filename[:-2] + ".jpg"
        print(merged_filename)
        with open(
            "/{0}/merged_files/{1}".format(project_dir, merged_filename), "wb"
        ) as f:
            f.write(merged_content + iv + encrypted_hash)

        merged_files_logger.info("Merged file saved: %s", merged_filename)
    except Exception as e:
        error_logger.error("An error occurred: %s", str(e))
