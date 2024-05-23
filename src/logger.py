import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
import os


def configure_logger(logger_name: str, log_files: dict):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
    )

    for file_name, level in log_files.items():
        handler = TimedRotatingFileHandler(
            file_name, when="midnight", interval=1, backupCount=7
        )
        handler.setFormatter(formatter)
        handler.setLevel(level)
        logger.addHandler(handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
logs_folder_path = os.path.join(root_path, "logs")

handlers = [
    (
        os.path.join(
            logs_folder_path,
            f"success_file_merging_{datetime.now().strftime('%Y-%m-%d')}.log",
        ),
        logging.INFO,
    ),
    (os.path.join(logs_folder_path, "error_fastapi.log"), logging.ERROR),
    (
        os.path.join(logs_folder_path, "debug_fastapi.log"),
        logging.DEBUG,
    ),
]

fastapi_logger = configure_logger("fastapi_logger", handlers)
