from functools import partial

from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_bolt.async_app import AsyncApp

from bots.base import Bot
from configs.common_config import settings
from core.ai.agents.slack.base import BaseSlackAgent
from core.ai.memories.postgres_memory import PostgresChatMemoryMessage


class SlackBot(Bot):
    def __init__(self, app: AsyncApp, agent: partial[BaseSlackAgent,], memory: partial[PostgresChatMemoryMessage]):
        self.app = app
        self.agent = agent()
        self.memory = memory
        self.setup_event_handlers()

    def setup_event_handlers(self):
        """Set up event handlers for Slack messages and mentions."""
        self.app.event("message")(self.handle_message)
        self.app.event("app_mention")(self.handle_app_mention)

    def get_memory(self):
        return self.memory().get_memory()

    async def handle_chat_interaction(self, text: str, channel: str) -> None:
        """
        Handles chat interactions by processing the input text and updating the chat history.

        This function retrieves the chat history from a Postgres-backed memory, invokes the Slack agent
        to process the input text, and saves the context of the interaction.

        Args:
            text (str): The input text from the user.
            channel (str): The Slack channel ID where the interaction is taking place.

        Returns:
            None
        """
        session_memory = self.memory.get_instance(session_id=channel)
        chat_history = session_memory.get_chat_history()
        result = await self.agent.ainvoke(
            input={
                "input": text,
                "chat_history": chat_history,
            },
        )
        session_memory.memory.save_context(
            {"input": text},
            {"output": result['output']},
        )
        return result

    async def handle_message(self, body, say):
        """Handle incoming Slack messages."""
        text = body["event"]["text"]
        channel = body["event"]["channel"]
        result = await self.handle_chat_interaction(text, channel)
        await say(result['output'])

    async def handle_app_mention(self, body, say):
        """Handle mentions of the bot in Slack."""
        text = body["event"]["text"]
        channel = body["event"]["channel"]
        result = await self.handle_chat_interaction(text, channel)
        await say(result['output'])

    async def start(self):
        """Start the Slack bot in socket mode."""
        handler = AsyncSocketModeHandler(self.app, settings.SLACK_APP_TOKEN)
        await handler.start_async()
