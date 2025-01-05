from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI

from core.ai.agents.slack.base import BaseSlackAgent
from core.ai.tools.forecast_temperature import get_current_temperature
from core.ai.tools.shopee_tool import shopee_search
from core.ai.tools.tavily_search import tavily_tool
from core.ai.tools.wiki_search import wiki_tool
from core.enumerate import OpenAIModel


class SlackReactAgent(BaseSlackAgent):
    def __init__(self, model: str = None) -> None:
        super().__init__()
        self.model = ChatOpenAI(
            temperature=0,
            max_retries=10,
            request_timeout=600,
            model=model or OpenAIModel.GPT_4O_MINI,
        )
        self.tools = [
            get_current_temperature,
            tavily_tool,
            wiki_tool,
            shopee_search,
        ]
        self.prompt = hub.pull("hwchase17/react")
        self.agent = self._gen_react_agent_chain()
        self.agent_executor = self._gen_react_agent_executror()

    def _gen_react_agent_chain(self):
        return create_react_agent(self.model, self.tools, self.prompt)

    def _gen_react_agent_executror(self):
        return AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)

    def invoke(self, input: dict) -> dict:
        return self.agent_executor.invoke(input=input, config=self.invoke_config)

    async def ainvoke(self, input: dict) -> dict:
        return await self.agent_executor.ainvoke(input=input, config=self.invoke_config)
