from os import path, makedirs, devnull, system, name
from gpt4all import GPT4All
from .log_config import setup_logger
import sys

logger = setup_logger()


def setupModel():
    MODEL_DIR = "models"
    MODEL_NAME = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"
    MODEL_PATH = path.join(MODEL_DIR, MODEL_NAME)

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
