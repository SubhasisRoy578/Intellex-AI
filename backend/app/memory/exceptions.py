from typing import Any, Optional
from fastapi import status
from app.exceptions.exceptions import APIException


class MemoryNotFoundException(APIException):
    """Exception raised when a requested memory item cannot be located."""

    def __init__(self, message: str = "Memory record not found", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=message,
            details=details,
        )


class MemoryForbiddenException(APIException):
    """Exception raised when an authenticated user attempts to access another user's memories."""

    def __init__(self, message: str = "Access to this memory record is forbidden", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message=message,
            details=details,
        )


class MemoryException(APIException):
    """Exception raised on unexpected database or logical memory operation failures."""

    def __init__(self, message: str = "Internal memory operation failed", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            details=details,
        )
