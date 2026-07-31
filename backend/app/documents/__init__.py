from app.documents.service import document_service, DocumentProcessingService
from app.documents.detector import FileTypeDetector

__all__ = [
    "document_service",
    "DocumentProcessingService",
    "FileTypeDetector",
]
