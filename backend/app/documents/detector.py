from pathlib import Path
from typing import Type
from app.documents.base_processor import BaseDocumentProcessor
from app.documents.pdf_processor import PDFProcessor
from app.documents.docx_processor import DOCXProcessor
from app.documents.txt_processor import TXTProcessor
from app.documents.exceptions import UnsupportedDocumentException


class FileTypeDetector:
    """Utility to map file extensions to correct format-specific document processing instances."""

    @staticmethod
    def get_processor_for_file(file_path: Path) -> BaseDocumentProcessor:
        """Determines and returns the matching document processor instance.

        Args:
            file_path (Path): Path to physical file.

        Returns:
            BaseDocumentProcessor: Extractor instance.
        """
        extension = file_path.suffix.lower()

        if extension == ".pdf":
            return PDFProcessor()
        elif extension == ".docx":
            return DOCXProcessor()
        elif extension == ".txt":
            return TXTProcessor()
            
        raise UnsupportedDocumentException(
            message=f"Document extension '{extension}' is not supported by parser engines"
        )
