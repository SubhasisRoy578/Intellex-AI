from pathlib import Path
from typing import Dict, Any, List
from app.core.logging import logger
from app.documents.base_processor import BaseDocumentProcessor
from app.documents.exceptions import DocumentCorruptedException, DocumentProcessingException


class TXTProcessor(BaseDocumentProcessor):
    """Memory-efficient plain text (.txt) parser supporting robust encoding fallbacks."""

    def extract_text(self, file_path: Path) -> Dict[str, Any]:
        logger.info(f"Initiating TXT extraction pipeline for: {file_path.name}")
        
        # Candidate encodings to test for successful decode
        encodings: List[str] = ["utf-8", "latin-1", "cp1252", "ascii"]
        full_text = ""
        success = False

        for enc in encodings:
            try:
                with open(file_path, mode="r", encoding=enc) as f:
                    full_text = f.read()
                success = True
                logger.info(f"Successfully decoded plain text using encoding: {enc}")
                break
            except UnicodeDecodeError:
                continue
            except Exception as exc:
                logger.error(f"Failed to read TXT file {file_path.name} with encoding {enc}: {exc}")
                raise DocumentCorruptedException(message="Plain text file is unreadable")

        if not success:
            raise DocumentCorruptedException(message="Could not decode plain text file. Unknown encoding.")

        char_count = len(full_text)
        word_count = len(full_text.split())

        logger.info(
            f"Successfully parsed Plain Text: {file_path.name}",
            extra={
                "extra": {
                    "character_count": char_count,
                    "word_count": word_count
                }
            }
        )

        return {
            "text": full_text,
            "pages": None,
            "character_count": char_count,
            "word_count": word_count,
        }
