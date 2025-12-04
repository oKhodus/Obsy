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
        self._model = model or DummyModel()
        self._prompt_template = (
            prompt_template
            or "Summarize the following text in 3-5 short sentences:\n\n{content}"
        )

    @property
    def model(self) -> BaseAIModel:
        return self._model

    @model.setter
    def model(self, value: BaseAIModel):
        if not isinstance(value, BaseAIModel):
            raise TypeError("model must be a BaseAIModel")
        self._model = value

    @property
    def prompt_template(self) -> str:
        return self._prompt_template

    @prompt_template.setter
    def prompt_template(self, value: str):
        if not value:
            raise ValueError("prompt_template cannot be empty")
        self._prompt_template = value

    def summarize_text(self, file: str, additional_prompt=None) -> str:
        nm = NoteManager(WORKSPACE_PATH)
        text = nm.read_note(file)
        prompt = self._prompt_template.format(content=text)
        print("Loading...\n")
        return (
            self._model.run(prompt)
            if not additional_prompt
            else self._model.run(f"{additional_prompt}, {text}")
        )
