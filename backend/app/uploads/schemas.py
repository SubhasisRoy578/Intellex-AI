from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    """Unified API serialization model representing a completed file upload transaction."""

    upload_id: str = Field(..., description="Unique transaction ID for tracking file context")
    original_filename: str = Field(..., description="The original unsanitized name of the uploaded file")
    stored_filename: str = Field(..., description="The non-colliding, secured internal storage filename")
    file_type: str = Field(..., description="The validated extension or MIME category of the file")
    file_size: int = Field(..., description="The validated size of the file in bytes")
    upload_timestamp: float = Field(..., description="Epoch timestamp of file storage write completion")
    upload_status: str = Field(..., description="Status string of the upload ('stored', 'temporary', etc.)")


class UploadHealthSchema(BaseModel):
    """Metadata status validation model for the secure uploads module."""

    status: str = Field(..., description="Health status of the storage sub-system")
    storage_provider: str = Field(..., description="Type of storage active ('local', 's3', etc.)")
    upload_directory: str = Field(..., description="Active configured folder target")
    max_file_size_bytes: int = Field(..., description="Configured maximum file limit in bytes")
