from typing import Any, Dict, List, Optional
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.core.logging import logger


class APIException(Exception):
    """Base API Exception for structured application error handling."""

    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        message: str = "An unexpected error occurred",
        details: Optional[Any] = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.message = message
        self.details = details


class BadRequestException(APIException):
    def __init__(self, message: str = "Bad Request", details: Optional[Any] = None) -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST, message, details)


class AuthenticationException(APIException):
    def __init__(self, message: str = "Authentication Failed", details: Optional[Any] = None) -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, message, details)


class ForbiddenException(APIException):
    def __init__(self, message: str = "Permission Denied", details: Optional[Any] = None) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, message, details)


class NotFoundException(APIException):
    def __init__(self, message: str = "Resource Not Found", details: Optional[Any] = None) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, message, details)


class DatabaseException(APIException):
    def __init__(self, message: str = "Database operation failed", details: Optional[Any] = None) -> None:
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, message, details)


def register_exception_handlers(app: FastAPI) -> None:
    """Register uniform custom JSON exception handlers for the FastAPI application."""

    @app.exception_handler(APIException)
    async def api_exception_handler(request: Request, exc: APIException) -> JSONResponse:
        request_id = getattr(request.state, "request_id", "N/A")
        logger.warning(
            f"API Exception: {exc.message} | Status: {exc.status_code}",
            extra={"extra": {"request_id": request_id, "details": exc.details}},
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.status_code,
                    "message": exc.message,
                    "details": exc.details,
                    "request_id": request_id,
                }
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        request_id = getattr(request.state, "request_id", "N/A")

        # Flatten validation errors into clean structured list
        errors: List[Dict[str, Any]] = []
        for error in exc.errors():
            errors.append({
                "field": " -> ".join(str(loc) for loc in error.get("loc", [])),
                "type": error.get("type"),
                "message": error.get("msg"),
            })

        logger.warning(
            f"Validation Exception: {len(errors)} fields failed validation.",
            extra={"extra": {"request_id": request_id, "errors": errors}},
        )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "error": {
                    "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                    "message": "Input validation failed",
                    "details": errors,
                    "request_id": request_id,
                }
            },
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        request_id = getattr(request.state, "request_id", "N/A")
        logger.error(
            f"Unhandled exception: {exc}",
            exc_info=True,
            extra={"extra": {"request_id": request_id}},
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": "An internal server error occurred",
                    "details": str(exc) if app.debug else None,
                    "request_id": request_id,
                }
            },
        )
