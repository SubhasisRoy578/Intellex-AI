from typing import Optional
from pydantic import BaseModel, Field


class DocumentProcessRequest(BaseModel):
    """Input payload validation model for initiating a text extraction task."""

    upload_id: str = Field(..., min_length=1, description="The secure unique target filename/id stored on disk")


class DocumentProcessResponse(BaseModel):
    """Output serialization model containing extracted textual layers and computed counts."""

    status: str = Field(..., description="Processing status of the file ('processed', 'unsupported')")
    file_type: str = Field(..., description="Extracted extension structure")
    file_size: int = Field(..., description="Size of the parsed file in bytes")
    pages: Optional[int] = Field(None, description="Number of logical pages extracted (applicable to PDF)")
    character_count: int = Field(..., description="Total alphanumeric characters computed")
    word_count: int = Field(..., description="Total space-separated words computed")
    extracted_text: str = Field(..., description="Extracted full textual representation")
    processed_timestamp: float = Field(..., description="Epoch timestamp of extraction completion")


class DocumentHealthSchema(BaseModel):
    """Metadata status validation model for the document processing module."""

    status: str = Field(..., description="Availability status of parsing utilities")
    supported_formats: list[str] = Field(..., description="Permitted extraction extensions")
    libraries_active: list[str] = Field(..., description="Active backend rendering engines")
