from typing import List
from fastapi import FastAPI, UploadFile, File
from datetime import datetime
import os
from encryption import read_key_from_file, sign_file
import configs as config
from logger import fastapi_logger

app = FastAPI()


def part_a_or_b(filename):
    _, sep, suffix = filename.partition("_")
    if suffix and suffix[0] in ["a", "b"]:
        return suffix[0]
    raise SyntaxError("file name syntax is invalid.")


async def list_files_in_order(files):
    parts = {"_a.jpg": None, "_b": None}

    for file in files:
        file_content = await file.read()
        if file.filename.endswith("_a.jpg"):
            parts["_a.jpg"] = file_content
        elif file.filename.endswith("_b"):
            parts["_b"] = file_content

    return (parts["_a.jpg"], parts["_b"])


def write_to_merged_file(filename, merged_content, iv, encrypted_hash):
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    SUFFIX_A = "_a.jpg"
    SUFFIX_B = "_b"
    EXTENSION = ".jpg"

    if filename.endswith(SUFFIX_A):
        merged_filename = filename[: -len(SUFFIX_A)] + EXTENSION
    elif filename.endswith(SUFFIX_B):
        merged_filename = filename[: -len(SUFFIX_B)] + EXTENSION
    else:
        raise ValueError("Filename does not end with a recognized suffix.")

    merged_file_path = os.path.join(project_dir, "merged_files", merged_filename)

    with open(merged_file_path, "wb") as f:
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
