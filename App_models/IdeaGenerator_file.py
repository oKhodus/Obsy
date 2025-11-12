from .GPT4All_Model import DummyModel, BaseAIModel
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

    def generate_ideas(self, text: str, n: int = 5) -> List[str]:
        prompt = f"Based on the following note, generate {n} concise idea bullets (one per line):\n\n{text}"

        out = self.model.run(prompt, max_tokens=256)

        lines = [line.strip(" -*") for line in out.splitlines() if line.strip()]

        if len(lines) >= 1:
            return lines[:n]

        parts = re.split(r"[,\.;]\s", out)

        return [p for p in parts if p][:n]
