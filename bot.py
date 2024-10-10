import asyncio

from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_bolt.async_app import AsyncApp

from configs.common_config import settings
from core.ai.agents.slack_agent import SlackAgent
from core.loggers import configure_logging
from core.ai.memories import get_message_history

load_dotenv(override=True)
logger = configure_logging(__name__)

app = AsyncApp(token=settings.SLACK_BOT_TOKEN, name="slack-bot")
slack_agent = SlackAgent()

@app.event("message")
async def handle_message(body, say):
    text = body["event"]["text"]
    channel = body["event"]["channel"]
    chat_history, memory = get_message_history(channel)
    result = await slack_agent.ainvoke(
        input={
            "input": text,
            "chat_history": chat_history,
        },
    )
    memory.save_context(
        {"input": text},
        {"output": result['output']}
    )
    await say(result['output'])


@app.event("app_mention")
async def handle_message(body, say):
    # React to messages
    text = body["event"]["text"]
    channel = body["event"]["channel"]
    chat_history, memory = get_message_history(channel)
    result = await slack_agent.ainvoke(
        input={
            "input": text,
            "chat_history": chat_history,
        },
    )
    memory.save_context(
        {"input": text},
        {"output": result['output']}
    )
    await say(result['output'])


async def main():
    handler = AsyncSocketModeHandler(app, settings.SLACK_APP_TOKEN)
    await handler.start_async()


if __name__ == "__main__":
    asyncio.run(main())
