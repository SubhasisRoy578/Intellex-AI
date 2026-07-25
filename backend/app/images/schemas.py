from pydantic import BaseModel, Field


class ImageProcessRequest(BaseModel):
    """Input payload validation model for initiating an image analysis or OCR task."""

    upload_id: str = Field(..., min_length=1, description="The secure unique target filename/id stored on disk")


class ImageProcessResponse(BaseModel):
    """Output serialization model containing image metadata and extracted OCR text."""

    status: str = Field(..., description="Processing status of the image ('processed', 'failed')")
    width: int = Field(..., description="Width of the image in pixels")
    height: int = Field(..., description="Height of the image in pixels")
    format: str = Field(..., description="Format of the image (PNG, JPEG, etc.)")
    file_size: int = Field(..., description="Size of the image file in bytes")
    ocr_text: str = Field(..., description="Extracted OCR text from the image")
    processed_timestamp: float = Field(..., description="Epoch timestamp of processing completion")


class ImageHealthSchema(BaseModel):
    """Metadata status validation model for the image processing module."""

    status: str = Field(..., description="Availability status of image processing sub-system")
    ocr_provider: str = Field(..., description="Active backend OCR provider")
    supported_formats: list[str] = Field(..., description="Permitted image extensions")
