import asyncio

from dotenv import load_dotenv
from slack_bolt.async_app import AsyncApp

from bots.slack_bot import SlackBot
from configs.common_config import settings
from core.ai.agents import SlackAgent
from core.ai.memories.postgres_memory import PostgresChatMemoryMessage
from core.loggers import configure_logging

load_dotenv(override=True)
logger = configure_logging(__name__)


if __name__ == "__main__":
    bot = SlackBot(
        app=AsyncApp(token=settings.SLACK_BOT_TOKEN, name="slack-bot"),
        agent=SlackAgent,
        memory=PostgresChatMemoryMessage,
    )
    asyncio.run(bot.start())
