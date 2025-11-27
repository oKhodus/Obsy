import pytest
from pathlib import Path
from App_models.NoteManager_file import NoteManager
from App_models.GPT4All_Model import DummyModel
from App_models.Summarizer_file import Summarizer
from App_models.IdeaGenerator_file import IdeaGenerator
from App_models.TaskPrioritizer_file import TaskPrioritizer

# ---------- NoteManager tests ----------


@pytest.fixture
def note_manager(tmp_path):
    return NoteManager(workspace_path=tmp_path)


def test_create_and_read_note(note_manager):
    note_manager.create_note("test_note", "Hello World")
    content = note_manager.read_note("test_note")
    assert "Hello World" in content


def test_list_notes(note_manager):
    note_manager.create_note("note1", "Text1")
    note_manager.create_note("note2", "Text2")
    notes = note_manager.list_notes()
    assert "note1.md" in notes
    assert "note2.md" in notes


# ---------- Summarizer tests ----------


def test_summarizer_with_dummy_model(tmp_path):
    note_path = tmp_path / "test_note.md"
    note_path.write_text("Some content")

    model = DummyModel()
    summarizer = Summarizer(model=model, prompt_template="{content}")

    summary = summarizer.summarize_text(str(note_path))
    assert isinstance(summary, str)
    assert "dummy" in summary.lower()


# ---------- IdeaGenerator tests ----------


def test_idea_generator_with_dummy_model(tmp_path):
    note_path = tmp_path / "note.md"
    note_path.write_text("Some content for ideas")
    model = DummyModel()
    generator = IdeaGenerator(model=model)
    ideas = generator.generate_ideas(str(note_path), n=2)
    assert isinstance(ideas, list)
    assert all(isinstance(i, str) for i in ideas)


# ---------- TaskPrioritizer tests ----------


def test_task_prioritizer_with_dummy_model():
    model = DummyModel()
    tasks = ["Do homework ASAP", "Buy groceries", "Read book"]
    prioritizer = TaskPrioritizer(model=model)

    ranked = prioritizer.prioritize_tasks(tasks)
    assert isinstance(ranked, str)
    assert "Do homework" in ranked
