from App_models.GPT4All_Model import BaseAIModel
from App_models.NoteManager_file import NoteManager
from tools.config import WORKSPACE_PATH

from typing import Optional, List, Dict, Any
import re

class TaskPrioritizer:
    """
    Sorts and prioritizes tasks based on simple AI evaluation
    Attributes:
        model: BaseAIModel (optional)
    Methods:
        prioritize_tasks(task_list) -> List[Dict]
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
    
    def prioritize_tasks(self, tasks: list[str]) -> str:
        """Prioritize a list of tasks directly (no file reading)."""
        scored = [{"task": t, "score": self._score_task(t)} for t in tasks]
        scored.sort(key=lambda x: x["score"], reverse=True)
        out = ""
        for elem in scored:
            out += f"{elem['task']} - {elem['score']}\n"
        return out