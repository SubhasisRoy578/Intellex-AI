from typing import Any, Optional
from fastapi import status
from app.exceptions.exceptions import APIException


class OrchestratorException(APIException):
    """Exception raised when the core AI Knowledge Orchestration pipeline crashes."""

    def __init__(self, message: str = "Knowledge orchestration operation failed", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            details=details,
        )


class SourceUnavailableException(APIException):
    """Exception raised when a referenced knowledge source (document/image) is unreadable or deleted."""

    def __init__(self, message: str = "Referenced knowledge source is unavailable", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
            details=details,
        )
