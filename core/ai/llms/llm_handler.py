from langchain_openai import ChatOpenAI

from core.enumerate import OpenAIModel


class LLMHandler:
    def __init__(self, model: str=None) -> None:
        self.model = ChatOpenAI(
            temperature=0,
            max_retries=10,
            request_timeout=600,
            model=model or OpenAIModel.GPT_4O_MINI,
        )
