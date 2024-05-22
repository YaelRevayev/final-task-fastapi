import yaml
import os
from dataclasses import dataclass


@dataclass
class AppConfig:
    LOGS_FOLDER_NAME: str
    AES_KEY_LENGTH: int
    IV_BYTES_LENGTH: int
    KEY_FILE_NAME: str
    HTTP_PORT: int

    @classmethod
    def load(cls, config_file):
        with open(config_file, "r") as file:
            config_data = yaml.safe_load(file)
        return cls(**config_data)


config_file = "configs/config.yaml"
config = AppConfig.load(config_file)
