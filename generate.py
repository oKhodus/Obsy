# import os
from gpt4all import GPT4All
import sys

model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")


class Model:
    def __init__(self, user_prompt: str):
        self.user_prompt = user_prompt

    @property
    def start_conversation(self) -> str:
        with model.chat_session():
            answer = model.generate(self.user_prompt, max_tokens=1024)
        model.close()
        return answer


# print("Prompt: ", end="", flush=True)
# prompt = input()
prompt = input("Prompt: ")
print(Model(prompt).start_conversation)
sys.exit(0)
