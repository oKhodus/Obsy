from os import path, makedirs
from log_config import setup_logger


def init_workspace():
    PROJECT_ROOT = path.dirname(path.dirname(path.abspath(__file__)))

    logger = setup_logger(project_root=PROJECT_ROOT)

    OBSY_WORKDIR = path.join(PROJECT_ROOT, "ObsyNotes")

    makedirs(OBSY_WORKDIR, exist_ok=True)

    note_name = "example_note.md"
    note_path = path.join(OBSY_WORKDIR, note_name)

    with open(note_path, "w", encoding="utf-8") as f:
        f.write("# My note\n\nHere will be text.")

    logger.info(f"Note created: {note_path}")


init_workspace()
