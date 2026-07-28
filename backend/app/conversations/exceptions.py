from typing import Any, Optional
from fastapi import status
from app.exceptions.exceptions import APIException


class ConversationNotFoundException(APIException):
    """Exception raised when a requested conversation session cannot be located."""

    def __init__(self, message: str = "Conversation thread session not found", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=message,
            details=details,
        )


class ConversationForbiddenException(APIException):
    """Exception raised when an authenticated user attempts to access another user's conversation."""

    def __init__(self, message: str = "Access to this conversation session is forbidden", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message=message,
            details=details,
        )


class ConversationException(APIException):
    """Exception raised on unexpected database or logical conversation operations failures."""

    def __init__(self, message: str = "Internal conversation operation failed", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            details=details,
        )
