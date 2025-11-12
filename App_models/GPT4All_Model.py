
from tools.setup_model import setupModel

class BaseAIModel:
    """Minimal interface for AI backends used by Summarizer/IdeaGenerator/Prioritizer."""

    def run(self, prompt: str, max_tokens: int = 256) -> str:
        raise NotImplementedError


class DummyModel(BaseAIModel):
    """Fallback model for local testing: returns a simple transformation."""

    def run(self, prompt: str, max_tokens: int = 256) -> str:
        lines = [line.strip() for line in prompt.splitlines() if line.strip()]

        if not lines:
            return "No content."
        preview = " ".join(lines[:2])
        if len(preview) > 200:
            preview = preview[:197] + "..."
        return f"[DUMMY OUTPUT] {preview}"


class GPT4AllModel(BaseAIModel):
    def __init__(self):
        self.g = setupModel()

    def run(self, prompt: str, max_tokens: int = 256) -> str:
        with self.g.chat_session():
            response = self.g.generate(prompt, max_tokens=max_tokens)
        return response
