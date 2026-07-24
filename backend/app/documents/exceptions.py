from typing import Any, Optional
from fastapi import status
from app.exceptions.exceptions import APIException


class DocumentProcessingException(APIException):
    """Exception raised when document processing or textual parsing fails."""

    def __init__(self, message: str = "Document parsing operation failed", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            details=details,
        )


class PasswordProtectedException(APIException):
    """Exception raised when a PDF or document is protected by a password and cannot be unlocked."""

    def __init__(self, message: str = "Password protected documents are not supported", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
            details=details,
        )


class DocumentCorruptedException(APIException):
    """Exception raised when document contents are unreadable or corrupted."""

    def __init__(self, message: str = "Uploaded document is corrupted or invalid", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
            details=details,
        )


class UnsupportedDocumentException(APIException):
    """Exception raised when the selected document type is unsupported by the pipeline."""

    def __init__(self, message: str = "Document format is not supported", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            message=message,
            details=details,
        )
