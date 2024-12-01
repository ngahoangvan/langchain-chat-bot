import asyncio

from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_bolt.async_app import AsyncApp

from configs.common_config import settings
from core.ai.agents.slack_agent import SlackAgent
from core.ai.memories.postgre_memory import PostgreChatMemoryMessage
from core.loggers import configure_logging

load_dotenv(override=True)
logger = configure_logging(__name__)

app = AsyncApp(token=settings.SLACK_BOT_TOKEN, name="slack-bot")
slack_agent = SlackAgent()


@app.event("message")
async def handle_message(body, say):
    """Handle incoming Slack messages.

    Args:
        body (dict): The message event data from Slack
        say (callable): Function to send a response to Slack
    """
    text = body["event"]["text"]
    channel = body["event"]["channel"]
    # Get memory instance for this channel
    memory = PostgreChatMemoryMessage.get_instance(channel)
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
    memory.update_memory()
    await say(result['output'])


@app.event("app_mention")
async def handle_app_mention(body, say):
    """Handle mentions of the bot in Slack.

    Args:
        body (dict): The mention event data from Slack
        say (callable): Function to send a response to Slack
    """
    text = body["event"]["text"]
    channel = body["event"]["channel"]
    # Get memory instance for this channel
    memory = PostgreChatMemoryMessage.get_instance(channel)
    chat_history = memory.get_chat_history()
    result = await slack_agent.ainvoke(
        input={
            "input": text,
            "chat_history": chat_history,
        },
    )
    memory.save_context(
        {"input": text},
        {"output": result['output']},
    )
    memory.update_memory()
    await say(result['output'])


async def main():
    """Start the Slack bot in socket mode."""
    handler = AsyncSocketModeHandler(app, settings.SLACK_APP_TOKEN)
    await handler.start_async()


if __name__ == "__main__":
    asyncio.run(main())
