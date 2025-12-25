"""
error_handler.py
Custom exception handling for FastAPI.
Provides structured error responses and logging.
"""

import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError

# Initialize logger
logger = logging.getLogger("clarivox.error_handler")


# Custom Exception Classes
class ClarivoxException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class AudioValidationError(ClarivoxException):
    pass


class TranscriptionError(ClarivoxException):
    pass


class IntentExtractionError(ClarivoxException):
    pass


class FHIRGenerationError(ClarivoxException):
    pass


class RoutingError(ClarivoxException):
    pass


class PIISanitizationError(ClarivoxException):
    pass


# Global Exception Handlers
async def clarivox_exception_handler(request: Request, exc: ClarivoxException):
    logger.error(f"{exc.__class__.__name__}: {exc.message}", extra={"path": request.url.path})
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message, "error_type": exc.__class__.__name__},
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error: {exc.errors()}", extra={"path": request.url.path})
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "error_type": "ValidationError"},
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(f"HTTP error: {exc.detail}", extra={"path": request.url.path})
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error_type": "HTTPException"},
    )


async def generic_exception_handler(request: Request, exc: Exception):
    logger.critical(f"Unhandled exception: {str(exc)}", extra={"path": request.url.path})
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred.", "error_type": "InternalServerError"},
    )


def register_exception_handlers(app):
    """
    Register all exception handlers with the FastAPI app.
    
    Usage in main.py:
        from error_handler import register_exception_handlers
        register_exception_handlers(app)
    """
    app.add_exception_handler(ClarivoxException, clarivox_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
