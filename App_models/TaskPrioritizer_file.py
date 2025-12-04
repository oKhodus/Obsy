from App_models.GPT4All_Model import BaseAIModel
from App_models.NoteManager_file import NoteManager
from tools.config import WORKSPACE_PATH

from typing import Optional, List
import re

class TaskPrioritizer:
    """
    Sorts and prioritizes tasks based on simple AI evaluation.
    Attributes:
        model: BaseAIModel (optional)
    """

    def __init__(self, model: Optional[BaseAIModel] = None):
        self.model = model

    def _score_task(self, task: str) -> float:
        score = 0.0
        words = task.lower().split()
        keywords = {"urgent", "today", "asap", "deadline", "important", "now"}
        if any(k in words for k in keywords):
            score += 2.0
        score += max(0, 5 - len(words) * 0.2)
        return score

    def prioritize_tasks(self, file: str, n: int = 5) -> str:
        """Read tasks from a note file and prioritize them with optional AI explanations."""
        nm = NoteManager(WORKSPACE_PATH)
        text = nm.read_note(file)

        tasks_line = re.search(r"Tasks[:\s]*(.*)", text)
        tasks = []
        if tasks_line:
            tasks = [t.strip() for t in re.split(r"[;,]", tasks_line.group(1)) if t.strip()]

        if not tasks:
            return "No tasks found in the note."

        scored = [{"task": t, "score": self._score_task(t)} for t in tasks]
        scored.sort(key=lambda x: x["score"], reverse=True)
        top_tasks = [t["task"] for t in scored[:n]]

        if self.model:
            prompt = "Explain briefly why the following tasks are important:\n" + "\n".join(top_tasks)
            out = self.model.run(prompt, max_tokens=256)
            explanations = [line.strip(" -*") for line in out.splitlines() if line.strip()]
        else:
            explanations = ["No explanation (model not provided)"] * len(top_tasks)

        formatted = "Prioritized tasks:\n"
        for i, (task, explanation) in enumerate(zip(top_tasks, explanations), start=1):
            formatted += f"{i}. {task} - {explanation}\n"

        return formatted

