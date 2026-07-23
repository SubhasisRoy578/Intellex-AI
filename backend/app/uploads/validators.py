import os
import re
from pathlib import Path
from fastapi import UploadFile
from app.config.config import settings
from app.uploads.exceptions import (
    InvalidFileExtensionException,
    InvalidMimeTypeException,
    FileTooLargeException,
    EmptyFileException,
    CorruptedFileException,
)


def sanitize_filename(filename: str) -> str:
    """Sanitizes a user uploaded filename to prevent path traversal and arbitrary executions.

    Args:
        filename (str): Unsanitized original user input name.

    Returns:
        str: Secured, clean filename with non-alphanumeric characters stripped.
    """
    # 1. Strip directories path (prevent traversal)
    base_name = os.path.basename(filename)
    
    # 2. Extract suffix
    path_obj = Path(base_name)
    suffix = path_obj.suffix.lower()
    stem = path_obj.stem
    
    # 3. Clean filename stem: keep alphanumeric, dashes, and underscores
    clean_stem = re.sub(r"[^a-zA-Z0-9_\-]", "", stem)
    if not clean_stem:
        clean_stem = "secured_file"
        
    return f"{clean_stem}{suffix}"


def validate_file_metadata(file: UploadFile) -> None:
    """Performs strict validation checks against file extensions, sizes, and headers.

    Args:
        file (UploadFile): Raw uploaded multipart file.
    """
    original_name = file.filename or ""
    if not original_name:
        raise EmptyFileException(message="Uploaded filename is missing or empty")

    path_obj = Path(original_name)
    extension = path_obj.suffix.lower()

    # 1. Validate File Extension
    if extension not in settings.ALLOWED_EXTENSIONS:
        raise InvalidFileExtensionException(
            message=f"File extension '{extension}' is not supported",
            details={"allowed_extensions": settings.ALLOWED_EXTENSIONS}
        )

    # 2. Validate MIME Type
    content_type = file.content_type
    if not content_type or content_type not in settings.ALLOWED_MIME_TYPES:
        raise InvalidMimeTypeException(
            message=f"File MIME type '{content_type}' is not supported",
            details={"allowed_mime_types": settings.ALLOWED_MIME_TYPES}
        )

    # 3. Validate File Size & Empty constraints
    try:
        # Seek end of file to measure actual stream size
        file.file.seek(0, os.SEEK_END)
        size = file.file.tell()
        file.file.seek(0)  # Always reset stream pointer
    except Exception as exc:
        raise CorruptedFileException(message="File stream is unreadable or corrupted")

    if size == 0:
        raise EmptyFileException(message="Uploaded file content cannot be empty")

    if size > settings.MAX_UPLOAD_SIZE:
        max_mb = settings.MAX_UPLOAD_SIZE / (1024 * 1024)
        raise FileTooLargeException(
            message=f"File size exceeds the limit of {max_mb:.1f} MB",
            details={"file_size_bytes": size, "max_limit_bytes": settings.MAX_UPLOAD_SIZE}
        )
