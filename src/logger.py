import logging
from datetime import datetime
import os


def configure_logger(logger_name, handlers, log_level=logging.INFO):
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
    )
    for handler, level in handlers:
        handler = logging.FileHandler(handler)
        handler.setFormatter(formatter)
        handler.setLevel(level)
        logger.addHandler(handler)
    logger.setLevel(log_level)
    return logger


root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
logs_folder_path = os.path.join(root_path, "logs")

handlers = [
    (
        f"{logs_folder_path}/success_file_merging{datetime.now().strftime('%Y-%m-%d')}.log",
        logging.INFO,
    ),
    (f"{logs_folder_path}/error_fastapi.log", logging.ERROR),
]

fastapi_logger = configure_logger("fastapi_logger", handlers)
