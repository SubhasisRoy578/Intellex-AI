import os
import time
import secrets
import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, List, Optional
from fastapi import UploadFile
from app.config.config import settings
from app.core.logging import logger
from app.uploads.exceptions import UploadStorageException
from app.uploads.validators import validate_file_metadata, sanitize_filename


class BaseStorageProvider(ABC):
    """Abstract interface defining required storage mutations for handling user documents."""

    @abstractmethod
    async def save_file(self, file: UploadFile) -> Dict[str, Any]:
        """Saves file context into the active storage and returns metadata."""
        pass

    @abstractmethod
    async def delete_file(self, filename: str) -> None:
        """Removes the file from active storage."""
        pass

    @abstractmethod
    def list_files(self) -> List[str]:
        """Lists active stored files names."""
        pass


class LocalStorageProvider(BaseStorageProvider):
    """Production local disk storage provider with thread-safe file streams."""

    def __init__(self, storage_dir: Optional[str] = None) -> None:
        self.storage_dir = Path(storage_dir or settings.UPLOAD_DIR)
        # Ensure targeted storage directory is live
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    async def save_file(self, file: UploadFile) -> Dict[str, Any]:
        # 1. Trigger strict metadata validations (size, extension, MIME type, stream)
        validate_file_metadata(file)

        # 2. Sanitize and secure naming schemas
        original_name = file.filename or "unnamed"
        clean_name = sanitize_filename(original_name)
        
        # Non-colliding hash-based internal name (prevents path collisions or injections)
        extension = Path(clean_name).suffix.lower()
        secure_internal_name = f"{secrets.token_hex(16)}{extension}"
        target_path = self.storage_dir / secure_internal_name

        try:
            # 3. Read size and write chunks to disk in a thread-safe manner
            file_size = 0
            with open(target_path, "wb") as buffer:
                while chunk := file.file.read(8192):
                    buffer.write(chunk)
                    file_size += len(chunk)

            logger.info(
                f"File successfully written to disk: {secure_internal_name}",
                extra={
                    "extra": {
                        "original_name": original_name,
                        "stored_name": secure_internal_name,
                        "file_size": file_size,
                        "path": str(target_path)
                    }
                }
            )

            return {
                "upload_id": secrets.token_urlsafe(12),
                "original_filename": clean_name,
                "stored_filename": secure_internal_name,
                "file_type": extension,
                "file_size": file_size,
                "upload_timestamp": time.time(),
                "upload_status": "stored"
            }

        except Exception as exc:
            # Cleanup partially written files on error
            if target_path.exists():
                target_path.unlink()
            logger.error(f"Failed to store file on disk: {exc}", exc_info=True)
            raise UploadStorageException(message="Could not save file to disk storage")

    async def delete_file(self, filename: str) -> None:
        target_path = self.storage_dir / filename
        # Prevent directory traversal breakout deletions
        if not target_path.resolve().is_relative_to(self.storage_dir.resolve()):
            raise UploadStorageException(message="Attempted directory traversal deletion blocked")

        if target_path.exists():
            try:
                target_path.unlink()
                logger.info(f"Storage deleted file: {filename}")
            except Exception as exc:
                logger.error(f"Failed to delete file {filename}: {exc}", exc_info=True)
                raise UploadStorageException(message="Could not delete file from local storage")

    def list_files(self) -> List[str]:
        """Lists active stored files within the upload folder."""
        return [f.name for f in self.storage_dir.iterdir() if f.is_file() and f.name != ".gitkeep"]

    def perform_automatic_cleanup(self, max_age_hours: float = 24.0) -> int:
        """Prunes old temporary files to protect disk storage boundaries.

        Args:
            max_age_hours (float): Maximum age in hours before a file is pruned.

        Returns:
            int: Number of files successfully pruned.
        """
        cleaned_count = 0
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600

        logger.info(f"Initiating automatic upload storage cleanup (pruning files older than {max_age_hours}h)...")

        for file_path in self.storage_dir.iterdir():
            if file_path.is_file() and file_path.name != ".gitkeep":
                try:
                    file_mtime = file_path.stat().st_mtime
                    if (current_time - file_mtime) > max_age_seconds:
                        file_path.unlink()
                        cleaned_count += 1
                        logger.info(f"Cleanup: Pruned aged upload file: {file_path.name}")
                except Exception as exc:
                    logger.error(f"Failed to prune file {file_path.name} during cleanup: {exc}")

        logger.info(f"Automatic cleanup complete. Total files pruned: {cleaned_count}")
        return cleaned_count


# Export a global default instance
storage_service = LocalStorageProvider()
