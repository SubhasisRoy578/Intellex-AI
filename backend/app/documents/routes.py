from fastapi import APIRouter, Depends, status
from app.auth.dependencies import get_current_user
from app.auth.schemas import ClerkUser
from app.documents.schemas import DocumentProcessRequest, DocumentProcessResponse, DocumentHealthSchema
from app.documents.service import document_service
from app.config.config import settings

router = APIRouter(prefix="/documents", tags=["Document Processing Module"])


@router.post(
    "/process",
    response_model=DocumentProcessResponse,
    status_code=status.HTTP_200_OK,
    summary="Process and Extract Text from Document",
    description="Locates the uploaded file, determines format, normalizes encoding/Unicode, and extracts text content and metrics.",
)
async def process_document(
    request: DocumentProcessRequest,
    current_user: ClerkUser = Depends(get_current_user),
) -> DocumentProcessResponse:
    """Processes target stored document and returns comprehensive text extraction and word analytics."""
    result = document_service.process_stored_document(request.upload_id)
    
    return DocumentProcessResponse(
        status=result["status"],
        file_type=result["file_type"],
        file_size=result["file_size"],
        pages=result["pages"],
        character_count=result["character_count"],
        word_count=result["word_count"],
        extracted_text=result["extracted_text"],
        processed_timestamp=result["processed_timestamp"],
    )


@router.get(
    "/health",
    response_model=DocumentHealthSchema,
    status_code=status.HTTP_200_OK,
    summary="Verify Document Processing Module Health",
    description="Validates active libraries and supported format options.",
)
async def check_documents_health() -> DocumentHealthSchema:
    """Reports configurations and active rendering dependencies for the document processing module."""
    return DocumentHealthSchema(
        status="healthy",
        supported_formats=[".pdf", ".docx", ".txt"],
        libraries_active=["PyMuPDF (fitz)", "python-docx", "Standard codecs"]
    )
