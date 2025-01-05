from typing import Optional

from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_core.runnables.utils import Input
from langchain_openai import ChatOpenAI

from core.ai.llms.base_ai_handler import BaseAIHandler
from core.enumerate import OpenAIModel
from langchain.schema.runnable import Runnable


class LangchainAIHandler(BaseAIHandler):
    def __init__(self, model: str = None) -> None:
        super().__init__()

        self.model = ChatOpenAI(
            temperature=0,
            max_retries=10,
            request_timeout=600,
            model=model or OpenAIModel.GPT_4O_MINI,
        )
        self.chain: Runnable = None

    def create_default_chain(self, prompt_template: ChatPromptTemplate) -> Runnable:
        self.chain = prompt_template | self.model
        return self.chain

    async def invoke(self, input: Input, config: Optional[RunnableConfig], prompt_template: ChatPromptTemplate):
        if not self.chain:
            self.create_default_chain(prompt_template)

        return self.chain.ainvoke(
            input=input,
            config=config,
        )
