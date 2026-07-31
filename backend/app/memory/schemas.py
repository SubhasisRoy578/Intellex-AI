from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class MemoryBase(BaseModel):
    """Base schema containing fields shared across memory operations."""

    category: str = Field(
        ...,
        description="The category of memory: e.g., 'preferences', 'projects', 'long_term_facts'.",
        min_length=1,
        max_length=50,
        examples=["preferences", "projects", "long_term_facts"],
    )
    title: str = Field(
        ...,
        description="A short descriptive title for this memory record.",
        min_length=1,
        max_length=255,
        examples=["Preferred Coding Language", "Intellex AI Project Info"],
    )
    content: str = Field(
        ...,
        description="The detailed content of the memory or preference.",
        min_length=1,
        examples=["Prefers Python and FastAPI with strict type hints."],
    )
    importance_score: float = Field(
        default=0.5,
        description="Importance weighting from 0.0 (low) to 1.0 (critical importance).",
        ge=0.0,
        le=1.0,
    )
    source: str = Field(
        default="user",
        description="The origin source of the memory (e.g. 'user', 'ai_extracted').",
        max_length=100,
        examples=["user", "ai_extracted"],
    )
    tags: str = Field(
        default="",
        description="Comma-separated list of tags for searching or filtering.",
        max_length=255,
        examples=["python,backend,profile"],
    )
    is_active: bool = Field(
        default=True,
        description="Whether this memory is currently active and used for AI context.",
    )


class MemoryCreate(MemoryBase):
    """Schema for creating a new memory record."""
    pass


class MemoryUpdate(BaseModel):
    """Schema for updating an existing memory record. All fields are optional."""

    category: Optional[str] = Field(
        None,
        description="The category of memory.",
        min_length=1,
        max_length=50,
    )
    title: Optional[str] = Field(
        None,
        description="A short descriptive title.",
        min_length=1,
        max_length=255,
    )
    content: Optional[str] = Field(
        None,
        description="Detailed content.",
        min_length=1,
    )
    importance_score: Optional[float] = Field(
        None,
        description="Importance weight from 0.0 to 1.0.",
        ge=0.0,
        le=1.0,
    )
    source: Optional[str] = Field(
        None,
        description="Origin source of the memory.",
        max_length=100,
    )
    tags: Optional[str] = Field(
        None,
        description="Comma-separated tags.",
        max_length=255,
    )
    is_active: Optional[bool] = Field(
        None,
        description="Active status indicator.",
    )


class MemoryResponse(MemoryBase):
    """Schema representing a returned memory record including system-managed fields."""

    id: str = Field(..., description="Unique UUID identifier for the memory record.")
    user_id: str = Field(..., description="The Clerk user ID associated with the memory.")
    created_at: datetime = Field(..., description="Timestamp when the memory record was created.")
    updated_at: datetime = Field(..., description="Timestamp when the memory record was last updated.")
    last_accessed_at: datetime = Field(..., description="Timestamp of the most recent access/retrieval.")
    access_count: int = Field(..., description="Number of times this memory record has been accessed.")

    class Config:
        from_attributes = True


class MemoryCategoryStats(BaseModel):
    """Representing summary metrics for a specific memory category."""

    category: str
    count: int


class MemoryStats(BaseModel):
    """Detailed metadata and volume metrics for a user's memory utilization."""

    total_memories: int = Field(..., description="Total count of active and inactive memories.")
    active_memories: int = Field(..., description="Count of active memories currently injected as context.")
    categories: List[MemoryCategoryStats] = Field(default_factory=list, description="Distribution list of memories by category.")
