from App_models.GPT4All_Model import BaseAIModel, GPT4AllModel, DummyModel
from App_models.NoteManager_file import NoteManager
from App_models.Summarizer_file import Summarizer
from App_models.IdeaGenerator_file import IdeaGenerator
from App_models.TaskPrioritizer_file import TaskPrioritizer

from tools.autocomplete import md_completer
from tools.config import MODEL_PATH, WORKSPACE_PATH

from typing import Optional, List, Any
from os import system, name, path
import json
import readline


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
            "Hello Sir, It's a pleasure to make your day ^_^\n\n"
            "If you are newbie and wanna check all commands, just write command <man>\n"
        )
        while True:
            try:
                raw = input(">> ").strip()

                if not raw:
                    continue
                if raw in {"exit", "quit"}:
                    return f"Have a nice and calm day, sir."

                if raw in {"clear", "cls", "cl"}:
                    system("cls" if name == "nt" else "clear")
                    continue
    
                parts = raw.split(maxsplit=2)
                cmd = parts[0]
                args = parts[1:] if len(parts) > 1 else []

                if cmd == "man":
                    manual = (
                        "\nObsyApp CLI — commands:\n"
                        "list, \n"
                        "read <name>, \n"
                        "create <name> <content>, \n"
                        "summz <name>, \n"
                        "ideas <name>, \n"
                        "prioritize <name or tasks...>,\n"
                        "exit/quit,\n"
                        "clear/cls/cl\n"
                    )
                    print(manual)
                    continue

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


def main():
    if not path.exists(MODEL_PATH):
        model = DummyModel()

    model = GPT4AllModel()

    app = ObsyApp(workspace_path=WORKSPACE_PATH, model=model)

    readline.set_completer(md_completer)
    readline.parse_and_bind("tab: complete")

    print(
        app.run()
    )

if __name__ == "__main__":
    main()
