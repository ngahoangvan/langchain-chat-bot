from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_openai import ChatOpenAI

from core.ai.tools.forecast_temperature import get_current_temperature
from core.ai.tools.tavily_search import tavily_tool
from core.ai.tools.wiki_search import wiki_tool
from core.callbacks.langfuse_handler import langfuse_callback
from core.ai.tools.shopee_tool import shopee_search
from core.enumerate import OpenAIModel


class SlackAgent:
    def __init__(self, model: str=None) -> None:
        self.model = ChatOpenAI(
            temperature=0,
            max_retries=10,
            request_timeout=600,
            model=model or OpenAIModel.GPT_4O_MINI,
        )
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are helpful but sassy assistant"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        self.tools = [
            get_current_temperature,
            tavily_tool,
            wiki_tool,
            shopee_search
        ]
        self.functions = [convert_to_openai_function(f) for f in self.tools]
        self.model_with_tools = self.model.bind(functions=self.functions)
        self.chain = self.prompt | self.model_with_tools | OpenAIFunctionsAgentOutputParser()
        self.agent_chain = RunnablePassthrough.assign(
            agent_scratchpad= lambda x: format_to_openai_functions(x["intermediate_steps"])
        ) | self.chain
        self.agent_executor = AgentExecutor(agent=self.agent_chain, tools=self.tools, verbose=True)

    def invoke(self, input: dict) -> dict:
        return self.agent_executor.invoke(input=input, config={"callbacks": [langfuse_callback]})
    
    async def ainvoke(self, input: dict) -> dict:
        return await self.agent_executor.ainvoke(input=input, config={"callbacks": [langfuse_callback]})
