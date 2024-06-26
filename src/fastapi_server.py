from typing import List, Tuple
from fastapi import FastAPI, UploadFile, File
import os
from encryption import read_key_from_file, sign_file
from logger import fastapi_logger
from configs import config

app = FastAPI()
key = read_key_from_file(config.KEY_FILE_NAME)


def get_project_dir() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def split_filename(filename: str) -> str:
    if filename.endswith(config.SUFFIX_A):
        return filename[: -len(config.SUFFIX_A)] + config.EXTENSION
    elif filename.endswith(config.SUFFIX_B):
        return filename[: -len(config.SUFFIX_B)] + config.EXTENSION
    else:
        fastapi_logger.debug(filename)
        raise ValueError("Filename does not end with a recognized suffix.")


async def extract_files_in_order(files: List[UploadFile]) -> Tuple[bytes, bytes]:
    parts = {config.SUFFIX_A: None, config.SUFFIX_B: None}

    for file in files:
        file_content = await file.read()
        suffix = get_file_suffix(file.filename)
        if suffix in parts:
            parts[suffix] = file_content

    return parts[config.SUFFIX_A], parts[config.SUFFIX_B]


def get_file_suffix(filename: str) -> str:
    if filename.endswith(config.SUFFIX_A):
        return config.SUFFIX_A
    elif filename.endswith(config.SUFFIX_B):
        return config.SUFFIX_B
    else:
        raise ValueError("Filename does not end with a recognized suffix.")


def write_to_merged_file(
    filename: str, merged_content: bytes, iv: bytes, encrypted_hash: bytes
):
    fastapi_logger.debug("writing merged content to new file..")
    merged_filename = split_filename(filename)
    project_dir = get_project_dir()
    merged_file_path = os.path.join(
        project_dir, config.MERGED_FILES_DIR_NAME, merged_filename
    )

    os.makedirs(os.path.dirname(merged_file_path), exist_ok=True)

    with open(merged_file_path, "wb") as f:
        f.write(merged_content + iv + encrypted_hash)

    fastapi_logger.info("Merged file saved: %s", merged_filename)


@app.post("/merge_and_sign")
async def merge_files(files: List[UploadFile] = File(...)):
    try:
        part_a, part_b = await extract_files_in_order(files)
        if isinstance(part_a, bytes) and isinstance(part_b, bytes):
            merged_content = part_a + part_b
            encrypted_hash, iv = sign_file(merged_content, key)

            write_to_merged_file(files[1].filename, merged_content, iv, encrypted_hash)
        else:
            fastapi_logger.error("One or both parts are missing.")
    except Exception as e:
        fastapi_logger.error("An error occurred: %s", str(e))
