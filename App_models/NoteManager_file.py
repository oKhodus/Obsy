from pathlib import Path
from typing import List

class NoteManager:
    """
    handles creation, reading, and listing of markdown notes

    Attributes:
        workspace_path: Path to notes directory.
    Methods:
        create_note(name, content) -> Path
        read_note(name) -> str
        list_notes() -> list
    """

    def __init__(self, workspace_path: str):
        self._workspace = Path(workspace_path).expanduser()
        self._workspace.mkdir(parents=True, exist_ok=True)

    def create_note(self, name: str, content: str) -> Path:
        if not name.endswith(".md"):
            name = name + ".md"

        note = self._workspace / name
        note.write_text(content, encoding="utf-8")
        return note

    def read_note(self, name: str) -> str:
        if not name.endswith(".md"):
            name = name + ".md"

        note = self._workspace / name

        if not note.exists():
            raise FileNotFoundError(f"Note `{name}` not found in {self._workspace}")

        return f"\n{"-"*50}\n{note.read_text(encoding="utf-8")}\n{"-"*50}\n"

    def list_notes(self) -> List[str]:
        all_notes = sorted([note.name for note in self._workspace.glob("*.md")])
        return f"\nYou have {len(all_notes)} notes, sir:\n\n{all_notes}\n"
