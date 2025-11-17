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

        if re.search(r"\b\d{1,2}[/.-]\d{1,2}\b|\b\d{4}\b", task):
            score += 0.5
        return score
    
    def prioritize_tasks(self, note_name: str) -> List[Dict[str, Any]]:
        nm = NoteManager(WORKSPACE_PATH)
        text = nm.read_note(note_name)

        tasks = [
            line[2:].strip()
            for line in text.splitlines()
            if line.strip().startswith("- ")
        ]

        scored = [{"task": t, "score": self._score_task(t)} for t in tasks]
        scored.sort(key=lambda x: x["score"], reverse=True)
        out = ""
        for elem in scored:
            out += f"{elem["task"]} - {elem["score"]}\n"
        return out