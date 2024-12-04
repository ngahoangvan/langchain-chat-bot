
from unittest import IsolatedAsyncioTestCase
from fastapi import HTTPException
from starlette.requests import Request
from starlette import status
import pytest

from core.exceptions.exception_handler import (
    validation_error_handler,
    openai_request_error_handle,
    unexpected_error_handle,
    unexpected_exception_handle,
    retry_error_handle,
    handle_validation_error,
    handle_unexpected_error,
)
from core.loggers import configure_logging

logger = configure_logging(__name__)


class TestExceptionHandler(IsolatedAsyncioTestCase):
    def setUp(self):
        self.request = Request({"type": "http", "method": "GET", "headers": []})

    @pytest.mark.asyncio
    async def test_validation_error_handler(self):
        exc = Exception("validation_error")
        response = await validation_error_handler(self.request, exc)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.body.decode(),
            '{"message_code":"validation_error","message":"Bad Request!"}',
        )

    @pytest.mark.asyncio
    async def test_openai_request_error_handle(self):
        exc = Exception("rate_limit_error")
        response = await openai_request_error_handle(self.request, exc)

        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertEqual(
            response.body.decode(),
            '{"message_code":"rate_limit_error","message":"Too many request to OpenAI API, please try again later!"}',
        )

    @pytest.mark.asyncio
    async def test_unexpected_error_handle(self):
        exc = HTTPException(status_code=404, detail="Not Found")
        response = await unexpected_error_handle(self.request, exc)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.body.decode(), '{"message_code":404,"message":"Not Found"}')

    @pytest.mark.asyncio
    async def test_unexpected_exception_handle(self):
        exc = Exception("unexpected_error")
        response = await unexpected_exception_handle(self.request, exc)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(
            response.body.decode(),
            '{"message_code":500,"message":"API Error! We encountered an unexpected error. We are working on a fix."}',
        )

    @pytest.mark.asyncio
    async def test_retry_error_handle(self):
        exc = Exception("retry_error")
        response = await retry_error_handle(self.request, exc)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(
            response.body.decode(),
            '{"message_code":500,"message":"API Error! We encountered an unexpected error. We are working on a fix."}',
        )

    def test_handle_validation_error(self):
        response = handle_validation_error("VALIDATION_ERROR", "Invalid input")

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(
            response.body.decode(),
            '{"message_code":"VALIDATION_ERROR","message":"Invalid input"}',
        )

    def test_handle_unexpected_error(self):
        response = handle_unexpected_error("UNEXPECTED_ERROR", "System error")

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.body.decode(), '{"message_code":"UNEXPECTED_ERROR","message":"System error"}')
