import pytest
import warnings
warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL 1.1.1+")
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

def test_summarizer_custom_template(tmp_path):
    """Verify the Summarizer handles prompt templates and NoteManager formatting."""
    nm = NoteManager(workspace_path=tmp_path)
    content = "AI info"
    nm.create_note("summarize_me", content)
    
    model = DummyModel()
    # Using a simple template to ensure content remains in the DummyModel's 2-line preview
    custom_template = "{content}" 
    summarizer = Summarizer(model=model, prompt_template=custom_template)
    
    import App_models.Summarizer_file
    App_models.Summarizer_file.WORKSPACE_PATH = str(tmp_path)
    
    result = summarizer.summarize_text("summarize_me")
    
    # Assertions check for DummyModel prefix, NoteManager borders, and actual content
    assert "[DUMMY OUTPUT]" in result
    assert "---" in result
    assert "AI info" in result

# ---------- IdeaGenerator tests ----------

def test_idea_generator_with_dummy_model(tmp_path):
    note_path = tmp_path / "note.md"
    note_path.write_text("Some content for ideas")
    
    import App_models.IdeaGenerator_file
    App_models.IdeaGenerator_file.WORKSPACE_PATH = str(tmp_path)
    
    model = DummyModel()
    generator = IdeaGenerator(model=model)
    ideas = generator.generate_ideas("note.md", n=2)
    
    # If it returns a list, check the first element
    if isinstance(ideas, list):
        assert "DUMMY OUTPUT" in ideas[0]
    else:
        assert "DUMMY OUTPUT" in ideas

# ---------- TaskPrioritizer tests ----------

def test_task_prioritizer_with_dummy_model():
    model = DummyModel()
    prioritizer = TaskPrioritizer(model=model)
    
    # Keyword 'urgent' increases priority score
    urgent_score = prioritizer._score_task("urgent homework")
    normal_score = prioritizer._score_task("buy groceries")
    assert urgent_score > normal_score
