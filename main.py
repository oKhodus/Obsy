from App_models.GPT4All_Model import BaseAIModel, GPT4AllModel, DummyModel
from App_models.NoteManager_file import NoteManager
from App_models.Summarizer_file import Summarizer
from App_models.IdeaGenerator_file import IdeaGenerator
from App_models.TaskPrioritizer_file import TaskPrioritizer

from typing import Optional, List, Any
import json


class ObsyApp:
    """
    Central controller connecting all features.
    Attributes:
        note_manager, summarizer, idea_generator, task_prioritizer
    Methods:
        run() -> simple CLI loop
        handle_command(cmd, args) -> perform actions
    """

    def __init__(
        self, workspace_path: str = "./notes", model: Optional[BaseAIModel] = None
    ):
        self.note_manager = NoteManager(workspace_path)
        self.summarizer = Summarizer(model=model)
        self.idea_generator = IdeaGenerator(model=model)
        self.task_prioritizer = TaskPrioritizer(model=model)

    def handle_command(self, cmd: str, args: Optional[List[str]] = None) -> Any:
        args = args or []

        cmds = {
            "list": self.note_manager.list_notes,
            "read": self.note_manager.read_note,
            "create": self.note_manager.create_note,
            # next not work, needa refactor
            "summz": self.summarizer.summarize_text,
            "ideas": self.idea_generator.generate_ideas,
            "prioz": self.task_prioritizer.prioritize_tasks,
        }

        if cmd not in cmds:
            raise ValueError(f"Unknown command: {cmd}")

        func = cmds[cmd]
        if not args:
            return func()
        elif len(args) == 1:
            return func(args[0])
        else:
            return func(args[0], args[1])

    def run(self):
        print(
            "ObsyApp CLI — commands:\n"
            "list, "
            "read <name>, "
            "create <name> <content>, "
            "summarize <name>, "
            "ideas <name>, "
            "prioritize <name or tasks...>, exit"
        )
        while True:
            try:
                raw = input(">> ").strip()
                if not raw:
                    continue
                if raw in {"exit", "quit"}:
                    break
                parts = raw.split(maxsplit=2)
                cmd = parts[0]
                args = parts[1:] if len(parts) > 1 else []

                if cmd == "create" and len(parts) == 3:

                    res = self.handle_command("create", [parts[1], parts[2]])
                    print(f"Created: {res}")
                else:
                    res = self.handle_command(cmd, args)
                    print(
                        json.dumps(res, indent=2)
                        if isinstance(res, (list, dict))
                        else res
                    )
            except Exception as e:
                print("Error:", e)


if __name__ == "__main__":
    # app = ObsyApp(workspace_path="./demo_notes", model=GPT4AllModel())
    app = ObsyApp(workspace_path="./demo_notes", model=DummyModel())
    app.note_manager.create_note(
        "meeting.md",
        "# Meeting notes\nDiscuss project timeline. Deadline 2025-11-20.\nTasks:\n- Finish report\n- Email team (urgent)\n- Prepare slides",
    )
    print("Notes:", app.note_manager.list_notes())
    print("Read:", app.note_manager.read_note("meeting.md"))
    print(
        "Summary:",
        app.summarizer.summarize_text(app.note_manager.read_note("meeting.md")),
    )
    print(
        "Ideas:",
        app.idea_generator.generate_ideas(
            app.note_manager.read_note("meeting.md"), n=3
        ),
    )
    print(
        "Prioritized:",
        app.task_prioritizer.prioritize_tasks(
            ["Finish report", "Email team (urgent)", "Prepare slides by 20/11"]
        ),
    )
