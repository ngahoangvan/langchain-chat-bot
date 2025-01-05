from bots.base import Bot
from bots.slack_bot import SlackBot
from bots.telegram_bot import TelegramBot


class BotFactory:
    """Factory class for creating different types of bots"""

    @staticmethod
    def create_bot(bot_type: str, **kwargs) -> Bot:
        """
        Create a bot instance based on the specified type

        Args:
            bot_type: Type of bot to create ('slack' or 'telegram')
            **kwargs: Additional arguments needed for specific bot initialization

        Returns:
            Bot instance

        Raises:
            ValueError: If bot_type is not supported
        """
        bot_types = {
            'slack': SlackBot,
            'telegram': TelegramBot,
        }

        bot_class = bot_types.get(bot_type.lower())
        if not bot_class:
            raise ValueError(
                f"Unsupported bot type: {bot_type}. "
                f"Supported types are: {', '.join(bot_types.keys())}",
            )

        return bot_class(**kwargs)
