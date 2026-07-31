from typing import Any, Optional
from fastapi import status
from app.exceptions.exceptions import APIException


class SearchProviderException(APIException):
    """Exception raised when the active Search provider returns an error response."""

    def __init__(self, message: str = "Search provider encountered an error", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            message=message,
            details=details,
        )


class SearchTimeoutException(APIException):
    """Exception raised when search HTTP queries hit client timeout limits."""

    def __init__(self, message: str = "Search provider request timed out", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            message=message,
            details=details,
        )


class SearchQueryException(APIException):
    """Exception raised when search query parameters or validation filters are malformed."""

    def __init__(self, message: str = "Malformed search query request", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
            details=details,
        )
