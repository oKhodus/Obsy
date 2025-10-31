from pathlib import Path
from editor import NoteEditor

if __name__ == "__main__":
    notes_dir = Path(__file__).resolve().parent / "ObsyNotes"
    editor = NoteEditor(notes_dir)

    notes = editor.list_notes()
    if not notes:
        print("Dir ObsyNotes doesn't have any notes.")
        exit()

    print("📂 Found notes:")
    for i, note in enumerate(notes, 1):
        print(f"{i}. {note.name}")

    idx = int(input("Choose number of notes: ")) - 1
    instruction = input("What to make with note? ")

    editor.edit(notes[idx].name, instruction)
