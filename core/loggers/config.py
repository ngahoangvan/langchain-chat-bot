"""Define config for project."""
from __future__ import annotations

import logging
import os
import sys
from enum import Enum

from loguru import logger

from .handler import ELKHandler, InterceptHandler
from configs.common_config import settings


class LoggingTarget(Enum):
    TERMINAL = "terminal"
    ELK = "elk"


DEBUG: bool = os.getenv("DEBUG", False) in ("True", "true", "1")
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", logging.DEBUG if DEBUG else logging.ERROR)
LOGGERS = ("uvicorn.asgi", "uvicorn.access")
LOGGING_TARGET = os.getenv("LOGGING_TARGET", LoggingTarget.TERMINAL.value)

# ELK configuration
ELK_HOST = settings.ELK_HOST
ELK_PORT = settings.ELK_PORT
ELK_INDEX = settings.ELK_INDEX


# logging configuration
def configure_logging():
    logging.getLogger().handlers = [InterceptHandler()]
    for logger_name in LOGGERS:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

    handlers = [{"sink": sys.stderr, "level": LOGGING_LEVEL}]
    if LOGGING_TARGET == LoggingTarget.ELK.value:
        elk_handler = ELKHandler(ELK_HOST, ELK_PORT, ELK_INDEX, level=LOGGING_LEVEL)
        handlers += [{"sink": elk_handler, "level": LOGGING_LEVEL}]

    logger.configure(handlers=handlers)

configure_logging()
