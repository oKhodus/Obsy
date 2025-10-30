import logging
from os import path


def setup_logger(log_file_name="app.log", project_root=None):
    if project_root is None:
        project_root = path.dirname(path.abspath(__file__))

    log_path = path.join(project_root, log_file_name)

    logger = logging.getLogger("ObsyLogger")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.FileHandler(log_path, encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
