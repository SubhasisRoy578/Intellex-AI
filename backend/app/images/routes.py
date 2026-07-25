from fastapi import APIRouter, Depends, status
from app.auth.dependencies import get_current_user
from app.auth.schemas import ClerkUser
from app.images.schemas import ImageProcessRequest, ImageProcessResponse, ImageHealthSchema
from app.images.service import image_service, ImageProcessingService
from app.images.provider import get_configured_ocr_provider

router = APIRouter(prefix="/images", tags=["Image Analysis & OCR Module"])


@router.post(
    "/process",
    response_model=ImageProcessResponse,
    status_code=status.HTTP_200_OK,
    summary="Process and Perform OCR on Image",
    description="Validates target uploaded image, parses width, height, format properties, executes contrast grayscale preprocessing, and extracts OCR textual strings.",
)
async def process_image(
    request: ImageProcessRequest,
    current_user: ClerkUser = Depends(get_current_user),
) -> ImageProcessResponse:
    """Processes target stored image file and returns metadata and extracted OCR texts."""
    result = image_service.process_stored_image(request.upload_id)
    
    return ImageProcessResponse(
        status=result["status"],
        width=result["width"],
        height=result["height"],
        format=result["format"],
        file_size=result["file_size"],
        ocr_text=result["ocr_text"],
        processed_timestamp=result["processed_timestamp"],
    )


@router.get(
    "/health",
    response_model=ImageHealthSchema,
    status_code=status.HTTP_200_OK,
    summary="Verify Image Analysis Module Health",
    description="Validates and reports status of active image parsing and OCR utility engines.",
)
async def check_images_health() -> ImageHealthSchema:
    """Reports configurations and active rendering dependencies for the image processing module."""
    provider = get_configured_ocr_provider()
    return ImageHealthSchema(
        status="healthy",
        ocr_provider=provider.get_provider_name(),
        supported_formats=[".png", ".jpg", ".jpeg"]
    )
