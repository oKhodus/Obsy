from App_models.GPT4All_Model import DummyModel, BaseAIModel
from App_models.NoteManager_file import NoteManager
from tools.config import WORKSPACE_PATH
from typing import Optional, List
import re


class IdeaGenerator:
    """
    Generates new ideas based on user notes.
    Attributes:
        model: BaseAIModel
    Methods:
        generate_ideas(text, n=5) -> List[str]
    """

    def __init__(self, model: Optional[BaseAIModel] = None):
        self.model = model or DummyModel()

    def generate_ideas(self, file: str, n: int = 5) -> str: # Changed return hint to str
        nm = NoteManager(WORKSPACE_PATH)
        text = nm.read_note(file)
        prompt = f"Based on the following note, generate {n} laconic idea bullets (one per line) which can help to handle with the tasks:\n\n{text}"
        print("Loading...")
        out = self.model.run(prompt, max_tokens=256)

        lines = [line.strip(" -*") for line in out.splitlines() if line.strip()]

        # If we have multiple lines (real model output), return them joined
        if len(lines) > 1:
            return "\n".join(lines[:n])

        # If we have one line (like DummyModel), treat it as a single idea string
        if len(lines) == 1:
            return lines[0]

        return "No ideas generated."
