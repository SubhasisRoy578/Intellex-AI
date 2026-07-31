from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field


class OrchestratorChatRequest(BaseModel):
    """Input payload validation model for initiating a unified orchestrated prompt transaction."""

    message: str = Field(..., min_length=1, description="Raw user prompt keywords or question")
    document_upload_ids: Optional[List[str]] = Field(default=None, description="List of securely uploaded PDF/DOCX/TXT file IDs")
    image_upload_ids: Optional[List[str]] = Field(default=None, description="List of securely uploaded PNG/JPG/JPEG file IDs")


class CitationInfo(BaseModel):
    """Standardized citation descriptor mapping specific sources that contributed to the answer."""

    type: str = Field(..., description="Type of knowledge source ('web', 'document', 'ocr')")
    title: Optional[str] = Field(None, description="Title of the citation (for web)")
    url: Optional[str] = Field(None, description="Absolute URL link of resource (for web)")
    snippet: Optional[str] = Field(None, description="Brief snippet containing context")
    document_name: Optional[str] = Field(None, description="File name of referenced document (for document)")
    page_number: Optional[int] = Field(None, description="Referenced page index if available (for PDF document)")


class OrchestratorChatResponse(BaseModel):
    """Unified API response model containing structured final text answers, source lists, and metadata."""

    response: str = Field(..., description="Generated unified answer from the orchestrated AI provider")
    knowledge_sources_used: List[str] = Field(..., description="List of modules queried ('chat_only', 'web_search', 'document', 'ocr')")
    citations: List[CitationInfo] = Field(default_factory=list, description="List of exact citations used in generating reply")
    confidence_score: float = Field(..., description="Computed confidence accuracy score (0.0 to 1.0)")
    processed_timestamp: float = Field(..., description="Epoch timestamp of completion")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata logs of the executed pipeline stages")


class OrchestratorHealthSchema(BaseModel):
    """Status reporting model for the knowledge orchestration layer."""

    status: str = Field(..., description="Operational status of the orchestrator pipeline")
    active_sources: List[str] = Field(..., description="Connected modules detected by orchestration layer")
    default_ai_provider: str = Field(..., description="The main LLM worker provider connected")
