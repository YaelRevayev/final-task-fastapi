import yaml
import os


def load_config(config_file):
    print(os.getcwd())
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)
    return config


config_file = "./src/configs/config.yaml"
config = load_config(config_file)


LOGS_FOLDER_NAME = config["LOGS_FOLDER_NAME"]
AES_KEY_LENGTH = config["AES_KEY_LENGTH"]
IV_BYTES_LENGTH = config["IV_BYTES_LENGTH"]
KEY_FILE_NAME = config["KEY_FILE_NAME"]
