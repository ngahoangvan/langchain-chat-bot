import asyncio
import argparse

from dotenv import load_dotenv
from slack_bolt.async_app import AsyncApp

from bots.factory import BotFactory
from configs.common_config import settings
from core.ai.agents import SlackAgent
from core.ai.memories.postgres_memory import PostgresChatMemoryMessage
from core.loggers import configure_logging

load_dotenv(override=True)
logger = configure_logging(__name__)


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Start a chat bot')
    parser.add_argument(
        '--type_bot',
        type=str,
        required=True,
        choices=['slack', 'telegram'],
        default='slack',
        help='Type of bot to start (slack or telegram)',
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    try:
        bot_kwargs = {
            'slack': {
                'app': AsyncApp(token=settings.SLACK_BOT_TOKEN, name="slack-bot"),
                'agent': SlackAgent,
                'memory': PostgresChatMemoryMessage,
            },
            'telegram': {
                # Add telegram specific kwargs here
            },
        }
        bot = BotFactory.create_bot(args.type_bot, **bot_kwargs[args.type_bot])
    except Exception as e:
        print(f"Error starting bot: {e}")
        raise

    asyncio.run(bot.start())
