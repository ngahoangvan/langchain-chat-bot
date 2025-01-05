import asyncio

from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_bolt.async_app import AsyncApp

from configs.common_config import settings
from core.ai.agents import SlackAgent
from core.ai.memories.postgres_memory import PostgresChatMemoryMessage
from core.loggers import configure_logging

load_dotenv(override=True)
logger = configure_logging(__name__)

app = AsyncApp(token=settings.SLACK_BOT_TOKEN, name="slack-bot")
slack_agent = SlackAgent()


async def handle_chat_interaction(text: str, channel: str) -> None:
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
    memory = PostgresChatMemoryMessage.get_instance(session_id=channel)
    chat_history = memory.get_chat_history()
    result = await slack_agent.ainvoke(
        input={
            "input": text,
            "chat_history": chat_history,
        },
    )
    memory.get_memory().save_context(
        {"input": text},
        {"output": result['output']},
    )


# Then modify the event handlers to use this function
@app.event("message")
async def handle_message(body, say):
    """Handle incoming Slack messages."""
    text = body["event"]["text"]
    channel = body["event"]["channel"]
    result = await handle_chat_interaction(text, channel)
    await say(result['output'])


@app.event("app_mention")
async def handle_app_mention(body, say):
    """Handle mentions of the bot in Slack."""
    text = body["event"]["text"]
    channel = body["event"]["channel"]
    result = await handle_chat_interaction(text, channel)
    await say(result['output'])


async def main():
    """Start the Slack bot in socket mode."""
    handler = AsyncSocketModeHandler(app, settings.SLACK_APP_TOKEN)
    await handler.start_async()


if __name__ == "__main__":
    asyncio.run(main())
