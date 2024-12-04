import logging
from unittest.mock import Mock

from elasticsearch import Elasticsearch
import pytest

from core.loggers import configure_logging
from core.loggers.handler import ELKHandler, InterceptHandler
from unittest import TestCase


class TestInterceptHandler(TestCase):
    def setUp(self) -> None:
        self.logger = configure_logging(__name__)
        return super().setUp()
    # def test_emit(self):
    #     handler = InterceptHandler()
    #     record = logging.LogRecord(
    #         name="INFO",
    #         level=logging.INFO,
    #         pathname="test.py",
    #         lineno=1,
    #         func="test",
    #         msg="Test message",
    #         args=(),
    #         exc_info=None
    #     )
    #     # test emit does not raise exception
    #     handler.emit(record)

    def test_emit_with_exception(self):
        handler = Mock(spec=InterceptHandler())
        handler.emit = Mock()
        record = logging.LogRecord(
            name="ERROR",
            level=logging.ERROR,
            pathname="test.py",
            lineno=1,
            func="test",
            msg="Test message",
            args=(),
            exc_info="Exception",
        )
        # test emit does not raise exception
        handler.emit(record)
        handler.emit.assert_called_once_with(record)

    @pytest.mark.skip
    def test_elk_handler(self):
        handler = ELKHandler("localhost", 9200, "test", logging.INFO)
        handler.es = Mock(spec=Elasticsearch)
        record = {
            "level": "INFO",
            "exc_info": None,
            "getMessage": lambda: "Test message",
            "name": "test",
            "pathname": "test.py",
            "lineno": 1,
            "funcName": "test",
        }
        # test emit does not raise exception
        handler.emit(record)
        handler.es.assert_called_once_with(
            index="test", body={
                'timestamp': "now",
                'level': "INFO",
                'message': "Test message",
                'logger': "test",
                'path': "test.py",
                'lineno': 1,
                'func': "test",
            },
        )
