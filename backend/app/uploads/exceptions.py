from typing import Any, Optional
from fastapi import status
from app.exceptions.exceptions import APIException


class InvalidFileExtensionException(APIException):
    """Exception raised when the uploaded file extension is not permitted."""

    def __init__(self, message: str = "File extension is not allowed", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
            details=details,
        )


class InvalidMimeTypeException(APIException):
    """Exception raised when the uploaded file MIME type is not permitted."""

    def __init__(self, message: str = "File MIME type is not allowed", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
            details=details,
        )


class FileTooLargeException(APIException):
    """Exception raised when the uploaded file exceeds maximum payload boundaries."""

    def __init__(self, message: str = "Uploaded file exceeds maximum permissible size limit", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            message=message,
            details=details,
        )


class EmptyFileException(APIException):
    """Exception raised when an uploaded file is empty."""

    def __init__(self, message: str = "Uploaded file cannot be empty", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
            details=details,
        )


class CorruptedFileException(APIException):
    """Exception raised when the uploaded file is corrupted or unreadable."""

    def __init__(self, message: str = "Uploaded file appears to be corrupted or invalid", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
            details=details,
        )


class UploadStorageException(APIException):
    """Exception raised when storage transactions or write operations fail."""

    def __init__(self, message: str = "Internal storage operation failed", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            details=details,
        )
