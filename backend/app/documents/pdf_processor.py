import fitz  # PyMuPDF
from pathlib import Path
from typing import Dict, Any
from app.core.logging import logger
from app.documents.base_processor import BaseDocumentProcessor
from app.documents.exceptions import (
    PasswordProtectedException,
    DocumentCorruptedException,
    DocumentProcessingException,
)


class PDFProcessor(BaseDocumentProcessor):
    """Memory-efficient PDF document parser using PyMuPDF (fitz)."""

    def extract_text(self, file_path: Path) -> Dict[str, Any]:
        logger.info(f"Initiating PDF extraction pipeline for: {file_path.name}")
        
        try:
            # Open PDF with PyMuPDF
            doc = fitz.open(file_path)
        except Exception as exc:
            logger.error(f"Failed to open PDF document: {exc}", exc_info=True)
            raise DocumentCorruptedException(message="PDF document appears corrupted or unreadable")

        # Check for password encryption/protection
        if doc.is_encrypted:
            doc.close()
            logger.warning(f"Encrypted PDF document blocked: {file_path.name}")
            raise PasswordProtectedException(message="Password-protected PDF files cannot be processed")

        extracted_pages = []
        char_count = 0
        word_count = 0
        page_count = len(doc)

        try:
            # Loop through pages (low memory buffering)
            for page_num in range(page_count):
                page = doc[page_num]
                text = page.get_text("text") or ""
                
                # Compute counters
                char_count += len(text)
                word_count += len(text.split())
                extracted_pages.append(text)

            full_text = "\n\n--- Page Break ---\n\n".join(extracted_pages)
            
            logger.info(
                f"Successfully parsed PDF: {file_path.name}",
                extra={
                    "extra": {
                        "pages": page_count,
                        "character_count": char_count,
                        "word_count": word_count
                    }
                }
            )

            return {
                "text": full_text,
                "pages": page_count,
                "character_count": char_count,
                "word_count": word_count,
            }

        except Exception as exc:
            logger.error(f"Error extracting text from PDF page: {exc}", exc_info=True)
            raise DocumentProcessingException(message="Internal PDF text extraction failed")
        finally:
            doc.close()
