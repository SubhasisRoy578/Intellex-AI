from typing import Any, Optional
from fastapi import status
from app.exceptions.exceptions import APIException


class AgentException(APIException):
    """Exception raised when the core AI Agent Framework operations fail."""

    def __init__(self, message: str = "AI Agent execution failed", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            details=details,
        )


class ToolExecutionException(APIException):
    """Exception raised when an autonomous tool execution fails or returns invalid states."""

    def __init__(self, message: str = "Agent tool execution failed", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
            details=details,
        )


class PlannerException(APIException):
    """Exception raised when the autonomous planning pipeline encounters inconsistent intent matches."""

    def __init__(self, message: str = "Agent planning pipeline failed", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
            details=details,
        )
