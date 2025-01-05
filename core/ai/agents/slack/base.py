
from abc import ABC, abstractmethod

from langchain_core.utils.function_calling import convert_to_openai_function

from core.ai.tools.forecast_temperature import get_current_temperature
from core.ai.tools.shopee_tool import shopee_search
from core.ai.tools.tavily_search import tavily_tool
from core.ai.tools.wiki_search import wiki_tool
from core.callbacks.langfuse_handler import langfuse_callback


class BaseSlackAgent(ABC):
    def __init__(self):
        self.invoke_config = {
            "callbacks": [langfuse_callback],
        }
        self.tools = [
            get_current_temperature,
            tavily_tool,
            wiki_tool,
            shopee_search,
        ]
        self.functions = [convert_to_openai_function(f) for f in self.tools]

    @abstractmethod
    def invoke(self, input: dict) -> dict:
        pass

    @abstractmethod
    async def ainvoke(self, input: dict) -> dict:
        pass
