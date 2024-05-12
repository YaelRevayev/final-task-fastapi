import logging
from datetime import datetime
import os


def configure_logger(logger_name, log_file_name, log_level=logging.INFO):
    logger = logging.getLogger(logger_name)
    handler = logging.FileHandler(log_file_name)
    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(log_level)
    return logger


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
