import time
from pathlib import Path
from typing import Dict, Any, Optional
from app.config.config import settings
from app.core.logging import logger
from app.documents.detector import FileTypeDetector
from app.documents.utils import clean_extracted_text
from app.documents.exceptions import DocumentCorruptedException, DocumentProcessingException


class DocumentProcessingService:
    """Core orchestrator service coordinating the document parsing, text cleansing, and count analytics."""

    def __init__(self, upload_dir: Optional[str] = None) -> None:
        self.upload_dir = Path(upload_dir or settings.UPLOAD_DIR)

    def process_stored_document(self, upload_id: str) -> Dict[str, Any]:
        """Loads a stored file by its upload ID/filename, triggers parsing, and returns metadata metrics.

        Args:
            upload_id (str): Unique secured internal name of file stored on disk.

        Returns:
            Dict[str, Any]: Structured map of extraction analytics.
        """
        # Resolve target physical path
        target_path = self.upload_dir / upload_id
        
        # Security check: prevent breakout path traversal
        if not target_path.resolve().is_relative_to(self.upload_dir.resolve()):
            raise DocumentProcessingException(message="Invalid document path lookup block")

        if not target_path.exists():
            logger.warning(f"File lookup failed for: {upload_id}")
            raise DocumentCorruptedException(message="The specified document could not be located in storage")

        # 1. Detect file type and match processor
        processor = FileTypeDetector.get_processor_for_file(target_path)
        file_size = target_path.stat().st_size

        logger.info(
            f"Processing document {upload_id} using {processor.__class__.__name__}...",
            extra={"extra": {"file_size_bytes": file_size}}
        )

        # 2. Execute parsing pipeline
        result = processor.extract_text(target_path)

        # 3. Securely sanitize and clean the extracted output
        dirty_text = result["text"] or ""
        clean_text = clean_extracted_text(dirty_text)

        # 4. Re-calculate precise clean counts
        final_char_count = len(clean_text)
        final_word_count = len(clean_text.split())

        return {
            "status": "processed",
            "file_type": target_path.suffix.lower(),
            "file_size": file_size,
            "pages": result["pages"],
            "character_count": final_char_count,
            "word_count": final_word_count,
            "extracted_text": clean_text,
            "processed_timestamp": time.time()
        }


# Global default instance
document_service = DocumentProcessingService()
