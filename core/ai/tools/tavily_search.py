from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper


search = TavilySearchAPIWrapper()
description = """A search engine optimized for comprehensive accurate, \
and trusted resutls. Useful for when you need to answer question \
about current events or about recent information. \
Input should be a search query. \
If the user is asking about somthing that you don't have information about, \
you should probably use this tool to see if that can provide any information.
"""
tavily_tool = TavilySearchResults(api_wrapper=search, description=description, verbose=True)
