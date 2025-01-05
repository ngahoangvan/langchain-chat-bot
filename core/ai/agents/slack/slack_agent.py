from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough
from langchain_openai import ChatOpenAI

from core.ai.agents.slack.base import BaseSlackAgent
from core.enumerate import OpenAIModel


class SlackAgent(BaseSlackAgent):
    def __init__(self, model: str = None) -> None:
        super().__init__()
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
        self.agent_chain = self._gen_agent_chain()
        self.agent_executor = self._gen_agent_executror()

    def _gen_agent_chain(self):
        model_with_tools = self.model.bind(functions=self.functions)
        chain = self.prompt | model_with_tools | OpenAIFunctionsAgentOutputParser()
        agent_chain = RunnablePassthrough.assign(
            agent_scratchpad=lambda x: format_to_openai_functions(x["intermediate_steps"]),
        ) | chain
        return agent_chain

    def _gen_agent_executror(self):
        return AgentExecutor(agent=self.agent_chain, tools=self.tools, verbose=True)

    def invoke(self, input: dict) -> dict:
        return self.agent_executor.invoke(input=input, config=self.invoke_config)

    async def ainvoke(self, input: dict) -> dict:
        return await self.agent_executor.ainvoke(input=input, config=self.invoke_config)
