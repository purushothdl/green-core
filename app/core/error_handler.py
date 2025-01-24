# core/error_handler.py
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from loguru import logger
import traceback

from app.core.exceptions import (
    OrgNotFoundError,
    UserNotFoundError,
    InvalidCredentialsError,
    DuplicateRatingError
)

async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global exception handler for standardized error responses.
    """
    if isinstance(exc, UserNotFoundError):
        return await handle_user_not_found_error(exc)
    elif isinstance(exc, InvalidCredentialsError):
        return await handle_invalid_credentials_error(exc)
    elif isinstance(exc, DuplicateRatingError):
        return await handle_duplicate_rating_error(exc)
    elif isinstance(exc, RequestValidationError):
        return await handle_validation_error(exc)
    elif isinstance(exc, OrgNotFoundError):
        return await handle_org_not_found_error(exc)
    else:
        return await handle_unexpected_error(exc)

# --- Helper functions ---

async def handle_user_not_found_error(exc: UserNotFoundError) -> JSONResponse:
    logger.error(f"User not found: {str(exc)}")
    return JSONResponse(
        status_code=404,
        content={
            "error_type": "UserNotFoundError",
            "message": str(exc),
            "details": None
        }
    )

async def handle_invalid_credentials_error(exc: InvalidCredentialsError) -> JSONResponse:
    logger.error(f"Invalid credentials: {str(exc)}")
    return JSONResponse(
        status_code=401,
        content={
            "error_type": "InvalidCredentialsError",
            "message": str(exc),
            "details": None
        }
    )

async def handle_duplicate_rating_error(exc: DuplicateRatingError) -> JSONResponse:
    logger.error(f"Duplicate rating error: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={
            "error_type": "DuplicateRatingError",
            "message": str(exc),
            "details": None
        }
    ) 

async def handle_validation_error(exc: RequestValidationError) -> JSONResponse:
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "error_type": "ValidationError",
            "message": "Invalid request payload",
            "details": exc.errors()
        }
    )

async def handle_org_not_found_error(exc: RequestValidationError) -> JSONResponse:
    logger.error(f"Org not found: {str(exc)}")
    return JSONResponse(
        status_code=404,
        content={
            "error_type": "OrgNotFoundError",
            "message": str(exc),
            "details": None
        }
    )

async def handle_unexpected_error(exc: Exception) -> JSONResponse:
    logger.critical(f"Unexpected error: {exc}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={
            "error_type": "InternalServerError",
            "message": "An unexpected error occurred",
            "details": None
        }
    )
