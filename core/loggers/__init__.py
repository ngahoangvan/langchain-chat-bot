"""Define Logger for log message."""
import logging
import os.path

from .config import DEBUG


class UvicornFormatter(logging.Formatter):
    """Uvicorn Formatter."""

    FORMAT = (
        "\033[38;5;244m%(asctime)s\033[0m"
        " | "
        "%(levelname)-7s"
        " | "
        "\033[38;5;214m%(name)s\033[0m"
        " : "
        "\033[38;5;111m%(message)s\033[0m"
    )

    LEVEL_COLORS = {
        "DEBUG": "\033[38;5;32m",
        "INFO": "\033[38;5;36m",
        "WARNING": "\033[38;5;221m",
        "ERROR": "\033[38;5;196m",
        "CRITICAL": "\033[48;5;196;38;5;231m",
    }


def configure_logging(name):
    """Initialize logging defaults for Project.

    This function does:
    - Assign INFO and DEBUG level to logger file handler and console handler.

    Returns:
        Logger.
    """
    logging_level = os.getenv("LOGGING_LEVEL", logging.DEBUG if DEBUG else logging.INFO)
    logger = logging.getLogger(name)
    logger.setLevel(logging_level)

    return logger
