import os
import secrets
from pathlib import Path
from typing import Tuple
from fastapi import UploadFile
from app.config.config import settings
from app.exceptions.exceptions import BadRequestException


def validate_upload_file(file: UploadFile) -> Tuple[str, str]:
    """Validates the uploaded file size and file extension.

    Args:
        file (UploadFile): FastAPI uploaded file object.

    Returns:
        Tuple[str, str]: Sanitized filename and extracted extension.
    """
    filename = file.filename or "unnamed_file"
    file_path = Path(filename)
    extension = file_path.suffix.lower()

    # Check for empty file extension
    if not extension:
        raise BadRequestException(message="Uploaded file must have an extension")

    # Read size implicitly (ensure small memory footprint)
    try:
        file.file.seek(0, os.SEEK_END)
        size = file.file.tell()
        file.file.seek(0)  # Reset pointer to start
    except Exception:
        raise BadRequestException(message="Could not read upload file properties")

    if size > settings.MAX_UPLOAD_SIZE:
        max_mb = settings.MAX_UPLOAD_SIZE / (1024 * 1024)
        raise BadRequestException(
            message=f"File exceeds maximum permissible size of {max_mb:.1f} MB"
        )

    return filename, extension


def save_uploaded_file(file: UploadFile, sub_dir: str = "") -> str:
    """Saves the uploaded file to the local storage target inside uploads directory.

    Args:
        file (UploadFile): Sanitized uploaded file.
        sub_dir (str, optional): Target subfolder under local storage.

    Returns:
        str: Absolute or relative resolved path of the saved file.
    """
    filename, extension = validate_upload_file(file)

    # Ensure save directory exists
    target_dir = Path(settings.UPLOAD_DIR) / sub_dir
    target_dir.mkdir(parents=True, exist_ok=True)

    # Secure random filename to avoid collisions and path injection
    unique_name = f"{secrets.token_hex(16)}{extension}"
    save_path = target_dir / unique_name

    with open(save_path, "wb") as buffer:
        while chunk := file.file.read(8192):
            buffer.write(chunk)

    return str(save_path)
