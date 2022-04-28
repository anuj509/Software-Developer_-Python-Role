"""Remote host configuration."""
from os import getenv, path

from dotenv import load_dotenv

import logging
logging = logging.getLogger("config-logger")

# Load environment variables from .env
BASE_DIR = path.abspath(path.dirname(__file__))
# print("path ",BASE_DIR)
# load_dotenv(".env")
load_dotenv(path.join(BASE_DIR, ".env"))
# SSH Connection Variables
ENVIRONMENT = getenv("ENVIRONMENT")
SSH_REMOTE_HOST = getenv("SSH_REMOTE_HOST")
SSH_USERNAME = getenv("SSH_USERNAME")
SSH_PASSWORD = getenv("SSH_PASSWORD")
SSH_KEY_FILEPATH = getenv("SSH_KEY_FILEPATH")
SCP_DESTINATION_FOLDER = getenv("SCP_DESTINATION_FOLDER")
SSH_CONFIG_VALUES = [
    {"host": SSH_REMOTE_HOST},
    {"user": SSH_USERNAME},
    {"password": SSH_PASSWORD},
    {"ssh": SSH_KEY_FILEPATH},
    {"path": SCP_DESTINATION_FOLDER},
]


# Verify all config values are present
for config in SSH_CONFIG_VALUES + SSH_CONFIG_VALUES:
    if None in config.values():
        logging.warning(f"Config value not set: {config.popitem()}")
        raise Exception("Please set your environment variables via a `.env` file.")

# Local file directory (no trailing slashes)
LOCAL_FILE_DIRECTORY = getenv('LOCAL_FILE_DIRECTORY')
