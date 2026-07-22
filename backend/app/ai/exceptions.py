from typing import Any, Optional
from fastapi import status
from app.exceptions.exceptions import APIException


class AIProviderException(APIException):
    """Exception raised when the selected AI provider returns an error response."""

    def __init__(self, message: str = "AI Provider encountered an error", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            message=message,
            details=details,
        )


class AITimeoutException(APIException):
    """Exception raised when the request to the AI Provider times out."""

    def __init__(self, message: str = "AI Provider request timed out", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            message=message,
            details=details,
        )


class AIRateLimitException(APIException):
    """Exception raised when the request hits the AI Provider's rate limits."""

    def __init__(self, message: str = "AI Provider rate limits exceeded", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            message=message,
            details=details,
        )
