from pathlib import Path
from tools.config import WORKSPACE_PATH

PATH = Path(WORKSPACE_PATH).expanduser()


def md_completer(text, state):
    try:
        files = [f.name for f in PATH.glob("*.md")]
        matches = [f for f in files if f.startswith(text)]
        return matches[state] if state < len(matches) else None
    except FileNotFoundError:
        return None
