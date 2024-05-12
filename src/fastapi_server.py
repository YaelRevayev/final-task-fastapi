from typing import List
from fastapi import FastAPI, UploadFile, File
import os
import sys
import logging
from datetime import datetime

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(os.path.join(project_dir, "configs"))
sys.path.insert(0, os.path.join(project_dir, "src"))

import config
from encryption import read_key_from_file, sign_file
from logger import configure_logger


app = FastAPI()

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
logs_folder_path = os.path.join(root_path, "logs")
merged_files_logger = configure_logger(
    "merged_files_logger_logger",
    f"{logs_folder_path}/success_file_merging{datetime.now().strftime('%Y-%m-%d')}.log",
    logging.INFO,
)

error_logger = configure_logger(
    "error_fastapi_logger",
    f"{logs_folder_path}/error_fastapi.log",
    logging.ERROR,
)


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
    try:

        part_a, part_b = await list_files_in_order(files)
        merged_content = part_a + part_b

        key = read_key_from_file(config.KEY_FILE_NAME)
        encrypted_hash, iv = sign_file(merged_content, key)

        merged_filename = files[1].filename.replace("_b", ".jpg")
        with open("merged_files/" + merged_filename, "wb") as f:
            f.write(merged_content + iv + encrypted_hash)

        merged_files_logger.info("Merged file saved: %s", merged_filename)
    except Exception as e:
        error_logger.error("An error occurred: %s", str(e))
