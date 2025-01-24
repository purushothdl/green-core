# core/error_handler.py
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from loguru import logger
import traceback

from app.core.exceptions import UserNotFoundError, InvalidCredentialsError

async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global exception handler for standardized error responses.
    """
    # Handle your custom exceptions first
    if isinstance(exc, UserNotFoundError):
        return JSONResponse(
            status_code=404,
            content={
                "error_type": "UserNotFoundError",
                "message": str(exc),
                "details": None
            }
        )
    elif isinstance(exc, InvalidCredentialsError):
        return JSONResponse(
            status_code=401,
            content={
                "error_type": "InvalidCredentialsError",
                "message": str(exc),
                "details": None
            }
        )
    # Handle FastAPI's validation errors
    elif isinstance(exc, RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "error_type": "ValidationError",
                "message": "Invalid request payload",
                "details": exc.errors()
            }
        )
    # Handle all other exceptions
    else:
        logger.critical(f"Unexpected error: {exc}\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={
                "error_type": "InternalServerError",
                "message": "An unexpected error occurred",
                "details": None
            }
        )