import io
import pytest
from fastapi import UploadFile
from app.utils.file_handler import validate_upload_file
from app.exceptions.exceptions import BadRequestException


def test_validate_upload_file_valid() -> None:
    """Test validating a valid uploaded file."""
    file_content = b"Some dummy textual content"
    dummy_file = io.BytesIO(file_content)
    upload_file = UploadFile(file=dummy_file, filename="test_document.txt")

    filename, extension = validate_upload_file(upload_file)
    assert filename == "test_document.txt"
    assert extension == ".txt"


def test_validate_upload_file_no_extension() -> None:
    """Test validating an uploaded file without an extension."""
    file_content = b"Some dummy textual content"
    dummy_file = io.BytesIO(file_content)
    upload_file = UploadFile(file=dummy_file, filename="test_document")

    with pytest.raises(BadRequestException) as exc_info:
        validate_upload_file(upload_file)
    assert "extension" in str(exc_info.value.message)
