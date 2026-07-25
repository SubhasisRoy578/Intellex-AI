from typing import Any, Optional
from fastapi import status
from app.exceptions.exceptions import APIException


class ImageProcessingException(APIException):
    """Exception raised when general image analysis or Pillow manipulation operations fail."""

    def __init__(self, message: str = "Image processing operation failed", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            details=details,
        )


class ImageCorruptedException(APIException):
    """Exception raised when an uploaded image file is unreadable or corrupted."""

    def __init__(self, message: str = "Uploaded image file appears corrupted or unreadable", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
            details=details,
        )


class UnsupportedImageException(APIException):
    """Exception raised when the selected image format is unsupported by Pillow or our routes."""

    def __init__(self, message: str = "Image format is not supported", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            message=message,
            details=details,
        )


class OCRException(APIException):
    """Exception raised when the OCR engine or provider fails text extraction."""

    def __init__(self, message: str = "OCR text extraction operation failed", details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            message=message,
            details=details,
        )
