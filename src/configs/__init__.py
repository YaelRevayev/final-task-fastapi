import yaml
import os


def load_config(config_file):
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    os.chdir(project_dir)
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)
    return config


config_file = "configs/config.yaml"
config = load_config(config_file)


LOGS_FOLDER_NAME = config["LOGS_FOLDER_NAME"]
AES_KEY_LENGTH = config["AES_KEY_LENGTH"]
IV_BYTES_LENGTH = config["IV_BYTES_LENGTH"]
KEY_FILE_NAME = config["KEY_FILE_NAME"]
