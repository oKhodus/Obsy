from os import path, makedirs, devnull, system, name
from gpt4all import GPT4All
from tools.log_config import setup_logger
from tools.config import MODEL_DIR, MODEL_NAME, MODEL_PATH
import sys

logger = setup_logger()


def setupModel():
    stderr = sys.stderr
    sys.stderr = open(devnull, "w")

    if not path.exists(MODEL_PATH):
        makedirs(MODEL_DIR, exist_ok=True)
        logger.info("Model not found, downloading...")

    model = GPT4All(MODEL_NAME, model_path=MODEL_DIR)

    sys.stderr.close()
    sys.stderr = stderr

    logger.info("Model loaded successfully")
    system("cls" if name == "nt" else "clear")
    return model
