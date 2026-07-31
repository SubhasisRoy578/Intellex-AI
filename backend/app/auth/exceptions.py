from typing import Any
from fastapi import status
from app.exceptions.exceptions import APIException


class InvalidTokenException(APIException):
    """Exception thrown when the authentication token fails signature or structure validation."""

    def __init__(self, message: str = "Invalid authentication token", details: Any = None) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
            details=details,
        )


class ExpiredTokenException(APIException):
    """Exception thrown when the authentication token signature is expired."""

    def __init__(self, message: str = "Authentication token has expired", details: Any = None) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
            details=details,
        )


class MissingTokenException(APIException):
    """Exception thrown when the authorization header is completely missing or malformed."""

    def __init__(self, message: str = "Missing or malformed authorization credentials", details: Any = None) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
            details=details,
        )


class AuthForbiddenException(APIException):
    """Exception thrown when the user is authenticated but lacks required permission scope."""

    def __init__(self, message: str = "Forbidden permission resource request", details: Any = None) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message=message,
            details=details,
        )
