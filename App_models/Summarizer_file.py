from App_models.GPT4All_Model import DummyModel, BaseAIModel
from App_models.NoteManager_file import NoteManager
from tools.config import WORKSPACE_PATH
from typing import Optional


class Summarizer:
    """
    Summarizes note content using an AI model.
    Attributes:
        model: BaseAIModel
        prompt_template: str (optional)
    Methods:
        summarize_text(text) -> str
    """

    def __init__(
        self, model: Optional[BaseAIModel] = None, prompt_template: Optional[str] = None
    ):
        self.model = model or DummyModel()
        self.prompt_template = (
            prompt_template
            or "Summarize the following text in 3-5 short sentences:\n\n{content}"
        )

    def summarize_text(self, file: str, additional_prompt=None) -> str:
        nm = NoteManager(WORKSPACE_PATH)
        text = nm.read_note(file)
        prompt = self.prompt_template.format(content=text)
        return (
            self.model.run(prompt)
            if not additional_prompt
            else self.model.run(f"{additional_prompt}, {text}")
        )
