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

    def generate_ideas(self, file: str, n: int = 5) -> List[str]:
        nm = NoteManager(WORKSPACE_PATH)
        text = nm.read_note(file)
        prompt = f"Based on the following note, generate {n} laconic idea bullets (one per line) which can help to handle with the tasks:\n\n{text}"

        out = self.model.run(prompt, max_tokens=256)

        lines = [line.strip(" -*") for line in out.splitlines() if line.strip()]

        if len(lines) >= 1:
            return lines[: n + 1]

        parts = re.split(r"[,\.;]\s", out)

        ideas = [p for p in parts if p][:n]

        return ideas
