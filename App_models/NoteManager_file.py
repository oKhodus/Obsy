from pathlib import Path
from typing import List


class NoteManager:
    """
    Handles creation, reading, and listing of markdown notes.

    Attributes:
        _workspace: Path to notes directory (private).
    Methods:
        create_note(name, content) -> Path
        read_note(name) -> str
        list_notes() -> List[str]
    """

    def __init__(self, workspace_path: str):
        self._workspace = Path(workspace_path).expanduser()
        self._workspace.mkdir(parents=True, exist_ok=True)

    def _normalize_name(self, name: str) -> str:
        """Ensure the note filename ends with .md"""
        return name if name.endswith(".md") else f"{name}.md"

    def _note_path(self, name: str) -> Path:
        """Return the full Path for a note."""
        normalized_name = self._normalize_name(name)
        return self._workspace / normalized_name

    def create_note(self, name: str, content: str) -> Path:
        """Create a new note with the given content"""
        note_path = self._note_path(name)
        note_path.write_text(content, encoding="utf-8")
        return note_path

    def read_note(self, name: str) -> str:
        """Read a note. Raises FileNotFoundError if note doesn't exist"""
        note_path = self._note_path(name)
        if not note_path.exists():
            raise FileNotFoundError(f"Note `{note_path.name}` not found")
        text = note_path.read_text(encoding="utf-8")
        border = "-" * 50
        return f"\n{border}\n{text}\n{border}\n"

    def list_notes(self) -> List[str]:
        """Return a sorted list of all note filenames"""
        return sorted(n.name for n in self._workspace.glob("*.md"))
