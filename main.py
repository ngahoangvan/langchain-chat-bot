from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from openai import APIError
from pydantic import ValidationError
# from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
# from slack_bolt.adapter.socket_mode import SocketModeHandler
# from slack_bolt.async_app import AsyncApp
from starlette.middleware.cors import CORSMiddleware

# from bots.slack_bot import SlackBot
# from configs.common_config import settings
from core.exceptions.exception_handler import (
    openai_request_error_handle,
    unexpected_error_handle,
    unexpected_exception_handle,
    validation_error_handler,
)
from core.loggers import configure_logging

logger = configure_logging(__name__)
load_dotenv(override=True)

# Initialize FastAPI
app = FastAPI(
    swagger_ui_parameters={"syntaxHighlight": False},
    title="Langchain - Slack Bot API",
    description="API of Slack Bot for Langchain",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Base exception handler
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(ValidationError, validation_error_handler)
app.add_exception_handler(APIError, openai_request_error_handle)
app.add_exception_handler(HTTPException, unexpected_error_handle)
app.add_exception_handler(Exception, unexpected_exception_handle)


@app.get("/health", status_code=status.HTTP_200_OK, tags=["Health"])
async def health() -> dict[str, str]:
    """Check if the server is running

    Returns:
        dict[str, str]: server is running
    """
    logger.info("Health check")
    return {"status": "ok"}


# @app.post("/slack/events")
# async def endpoint(req: Request):
#     # Handle slack events
#     return await handler.handle(req)


# # Initialize Slack Bolt App
# slack_app = AsyncApp(
#     token=settings.SLACK_BOT_TOKEN,
#     signing_secret=settings.SLACK_SIGNING_SECRET
# )

# # Initialize the SlackRequestHandler
# handler = SocketModeHandler(slack_app)

# @slack_app.event("message")
# async def handle_message(body, say):
#     await say("Hi there! How can I help you?")


# @slack_app.event("app_mention")
# async def handle_message(body, say):
#     # React to messages
#     text = body["event"]["text"]
#     # result = process_llm(text)
#     await say("Hello World")
