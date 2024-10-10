from typing import Optional

import wikipedia
from langchain_core.tools import BaseTool
from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun
)
from pydantic import BaseModel, Field
from typing import Type


class WikiSearchInput(BaseModel):
    """Input for the Tavily tool."""
    query: str = Field(description="search query to look up")


class WikiSearch(BaseTool):
    name: str = "wiki_search"
    description: str = "useful when you need an answer from Wikipedia"
    args_schema: Type[BaseModel] = WikiSearchInput
    verbose: bool = True
    # return_direct: bool = True # this option will return the result directly to the user

    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """Run Wikipedia search and get page summaries."""
        page_titles = wikipedia.search(query)
        summaries = []
        for page_title in page_titles[:5]:
            try:
                wiki_page =  wikipedia.page(title=page_title, auto_suggest=False)
                summaries.append(f"Page: {page_title}\nSummary: {wiki_page.summary}")
            except (
                wikipedia.exceptions.PageError,
                wikipedia.exceptions.DisambiguationError,
            ):
                pass
        if not summaries:
            return "No good Wikipedia Search Result was found"

        return "\n\n".join(summaries)

    async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        return self._run(query=query, run_manager=run_manager.get_sync())


wiki_tool = WikiSearch()
