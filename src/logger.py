import logging
import os
from datetime import datetime
import sys
import shutil

from utils import setup_project_directories

setup_project_directories("configs")
import configs.config as config


def reset_folder(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
        os.makedirs(directory)
    elif not os.path.exists(directory):
        os.makedirs(directory)


def configure_logger(logger_name, log_file_name):
    logger = logging.getLogger(logger_name)
    handler = logging.FileHandler(log_file_name)
    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def create_loggers():
    merged_files_logger = configure_logger(
        "merged_files_logger_logger",
        os.path.join(
            config.LOGS_FOLDER_NAME,
            f"success_file_merging{datetime.now().strftime('%Y-%m-%d')}.log",
        ),
    )
    merged_files_logger.setLevel(logging.INFO)

    error_logger = configure_logger(
        "error_fastapi_logger",
        os.path.join(config.LOGS_FOLDER_NAME, "error_fastapi.log"),
    )
    error_logger.setLevel(logging.ERROR)

    return (merged_files_logger, error_logger)
