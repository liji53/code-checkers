import os
from starlette.config import Config


config = Config(".env")
DEFAULT_STATIC_DIR = os.path.join(
    os.path.abspath(os.path.dirname(os.path.dirname(__file__))), os.path.join("frontend", "dist")
)
STATIC_DIR = config("STATIC_DIR", default=DEFAULT_STATIC_DIR)

FILES_DIR_NAME = "files"
DEFAULT_FILES_DIR = os.path.join(
    os.path.abspath(os.path.dirname(os.path.dirname(__file__))), FILES_DIR_NAME
)
FILES_DIR = config("FILES_DIR", default=DEFAULT_FILES_DIR)
