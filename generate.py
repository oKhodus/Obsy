from tools.setup_model import setupModel
from tools.log_config import setup_logger

logger = setup_logger()
logger.info("Starting model...")

model = setupModel()


class Model:
    def __init__(self, user_prompt: str):
        self.user_prompt = user_prompt

    @property
    def get_answer(self) -> str:
        with model.chat_session():
            answer = model.generate(self.user_prompt, max_tokens=1024)
        model.close()
        return answer


if __name__ == "__main__":
    try:
        prompt = input("Prompt: ")
        response = Model(prompt).get_answer
        print(response)
    except KeyboardInterrupt:
        logger.info("User interrupted the program.")
