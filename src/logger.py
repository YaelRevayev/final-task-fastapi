import logging
from datetime import datetime
import os


def configure_logger(logger_name: str, handlers: list, log_level=logging.INFO):
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
    )
    logger.setLevel(log_level)

    for handler_path, level in handlers:
        # Ensure the directory for log files exists
        os.makedirs(os.path.dirname(handler_path), exist_ok=True)
        handler = logging.FileHandler(handler_path)
        handler.setFormatter(formatter)
        handler.setLevel(level)
        logger.addHandler(handler)

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
]

fastapi_logger = configure_logger("fastapi_logger", handlers)
