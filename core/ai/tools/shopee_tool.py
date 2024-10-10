from typing import Optional

from langchain_core.tools import BaseTool
from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun
)
from pydantic import BaseModel, Field
from typing import Type
from core.ai.knowledge_base.shopee_kb import ShopeeKnowledgeBase


class ShopeeSearchInput(BaseModel):
    """Input for the Shopee tool."""
    query: str = Field(description="search query to look up")


class ShopeeSearch(BaseTool):
    name: str = "shopee_search"
    description: str = "Useful when you need to find a resturant, food and drink on Shopee"
    args_schema: Type[BaseModel] = ShopeeSearchInput
    verbose: bool = True

    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """Run Shopee search and get restaurant information, food and drink."""
        retriever = self.metadata['shopee_kb'].retriever
        documents = retriever.invoke(input=query)
        return "\n\n".join([document.page_content for document in documents])

    async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        return self._run(query=query, run_manager=run_manager.get_sync())


shopee_search = ShopeeSearch(metadata={"shopee_kb": ShopeeKnowledgeBase()})
