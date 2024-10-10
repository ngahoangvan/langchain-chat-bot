"""Logging."""
import inspect
import logging
from elasticsearch import Elasticsearch
from datetime import datetime
from loguru import logger
from configs.common_config import settings


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class ELKHandler(logging.Handler):
    def __init__(self, host, port, index, level):
        super().__init__(level)
        self.es = Elasticsearch(
            hosts=[
                {
                    'host': host,
                    'port': port,
                    'scheme': 'http'
                }
            ],
            basic_auth=(settings.ELK_USERNAME, settings.ELK_PASSWORD),
            verify_certs=False
        )
        self.index = index

    def emit(self, record):
        try:
            msg = self.format(record)
            now = datetime.now()
            doc = {
                'timestamp': now,
                'level': record.levelname,
                'message': msg,
                'logger': record.name,
                'path': record.pathname,
                'lineno': record.lineno,
                'func': record.funcName
            }
            self.es.index(index=self.index, body=doc)
        except Exception:
            self.handleError(record)
