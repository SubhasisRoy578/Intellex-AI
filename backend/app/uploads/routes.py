from fastapi import APIRouter, Depends, UploadFile, status, File
from app.auth.dependencies import get_current_user
from app.auth.schemas import ClerkUser
from app.uploads.schemas import UploadResponse, UploadHealthSchema
from app.uploads.service import storage_service, LocalStorageProvider
from app.config.config import settings

router = APIRouter(prefix="/uploads", tags=["Secure File Upload Infrastructure"])


@router.post(
    "",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Securely Upload a File",
    description="Validates type, extension, size, and header characteristics of the file, sanitizes its naming structure, and persists it securely.",
)
async def upload_document(
    file: UploadFile = File(..., description="Multipart document file"),
    current_user: ClerkUser = Depends(get_current_user),
) -> UploadResponse:
    """Processes, validates, and stores a document file securely."""
    metadata = await storage_service.save_file(file)
    
    return UploadResponse(
        upload_id=metadata["upload_id"],
        original_filename=metadata["original_filename"],
        stored_filename=metadata["stored_filename"],
        file_type=metadata["file_type"],
        file_size=metadata["file_size"],
        upload_timestamp=metadata["upload_timestamp"],
        upload_status=metadata["upload_status"],
    )


@router.get(
    "/health",
    response_model=UploadHealthSchema,
    status_code=status.HTTP_200_OK,
    summary="Verify Upload Module Health",
    description="Validates and reports status of the backing file storage sub-systems.",
)
async def check_uploads_health() -> UploadHealthSchema:
    """Verifies and reports status of configured disk storage layers."""
    return UploadHealthSchema(
        status="healthy" if settings.UPLOAD_DIR else "degraded",
        storage_provider="local",
        upload_directory=str(storage_service.storage_dir),
        max_file_size_bytes=settings.MAX_UPLOAD_SIZE,
    )
