from tools.log_config import setup_logger
from tools.setup_model import setupModel
from pathlib import Path

logger = setup_logger()
model = setupModel()

class NoteEditor:
    def __init__(self, notes_dir, edit_model=model):
        self.notes_dir = notes_dir
        self.model = edit_model
    
    def list_notes(self):
        notes = list(self.notes_dir.glob("*.md"))
        return notes

    def edit(self, note_name: str, instruction: str):
        note_path = self.notes_dir / note_name
        if not note_path.exists():
            print("Didn't find this note")
            return

        text = note_path.read_text(encoding="utf-8")
        prompt = f"You are an editor of the notes. {instruction}\n\nText:\n{text}\n\nCorrect variant:"
        output = self.model.generate(prompt, max_tokens=300)

        new_path = note_path.with_name(f"{note_path.stem}_edited.md")
        new_path.write_text(output, encoding="utf-8")

        print(f" New version saved as {new_path.name}")
        return