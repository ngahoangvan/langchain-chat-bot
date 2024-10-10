import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from core.loggers import configure_logging


logger = configure_logging(__name__)


class SlackBot:
    def __init__(self, token=None):
        self.token = token
        if not self.token:
            raise ValueError("Slack bot token is required")
        self.client = WebClient(token=self.token)

    def send_message(self, channel: str, text: str):
        """
        Send a message to a channel.
        """
        try:
            response = self.client.chat_postMessage(channel=channel, text=text)
            return response
        except SlackApiError as e:
            logger.error(f"Error sending message: {e}")
    
    def upload_file(self, channel: str, file, initial_comment: str) -> dict:
        """
        Upload a file to a channel.
        """
        try:
            response = self.client.files_upload_v2(channels=channel, file=file, initial_comment=initial_comment,)
            return response
        except SlackApiError as e:
            logger.error(f"Error uploading file: {e}")

    def on_message(self, pattern=None):
        def decorator(func):
            @self.app.message(pattern)
            def wrapper(message, say):
                func(message, say)
            return wrapper
        return decorator

    def on_mention(self):
        def decorator(func):
            @self.app.event("app_mention")
            def wrapper(event, say):
                func(event, say)
            return wrapper
        return decorator

    def on_reaction(self):
        def decorator(func):
            @self.app.event("reaction_added")
            def wrapper(event, say):
                func(event, say)
            return wrapper
        return decorator
