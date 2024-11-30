from __future__ import annotations

from typing import Text

from fastapi import HTTPException
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from core.loggers import configure_logging


logger = configure_logging(__name__)


async def validation_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """HTTP 400 Error handler.

    Args:
        exc: Exception.

    Returns:
        Json response
    """
    logger.debug(request)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "message_code": str(exc),
            "message": "Bad Request!",
        },
    )


async def openai_request_error_handle(request: Request, exc: Exception):
    logger.debug(request)

    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "message_code": str(exc),
            "message": "Too many request to OpenAI API, please try again later!",
        },
    )


async def unexpected_error_handle(request: Request, exc: HTTPException):
    logger.debug(request)

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message_code": exc.status_code,
            "message": exc.detail,
        },
        headers=exc.headers,
    )


async def unexpected_exception_handle(request: Request, exc: Exception):
    logger.debug(request)
    logger.debug(exc)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "API Error! We encountered an unexpected error. We are working on a fix.",
        },
    )


async def retry_error_handle(request: Request, exc: Exception):
    logger.debug(request)
    logger.debug(exc)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "API Error! We encountered an unexpected error. We are working on a fix.",
        },
    )


def handle_validation_error(message_code: Text, message: Text) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message_code": message_code,
            "message": message,
        },
    )


def handle_unexpected_error(message_code: Text, message: Text) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message_code": message_code,
            "message": message,
        },
    )
