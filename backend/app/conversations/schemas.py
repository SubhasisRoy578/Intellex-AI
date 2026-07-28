from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class MessageResponse(BaseModel):
    """Simplified serialization model for nested conversation messages."""

    id: str = Field(..., description="Unique ID of message")
    role: str = Field(..., description="user, assistant, system")
    content: str = Field(..., description="Text content")
    created_at: datetime = Field(..., description="Creation timestamp")

    model_config = ConfigDict(from_attributes=True)


class ConversationCreateRequest(BaseModel):
    """Payload to initiate a new conversation thread."""

    title: Optional[str] = Field(default=None, max_length=255, description="Custom conversation title")


class ConversationUpdateRequest(BaseModel):
    """Payload to modify properties of an existing conversation thread."""

    title: str = Field(..., min_length=1, max_length=255, description="New title for the conversation")
    status: Optional[str] = Field(default=None, description="active, archived")


class ConversationResponse(BaseModel):
    """Full detail serialization model representing a single active conversation context."""

    id: str = Field(..., description="Unique conversation UUID")
    user_id: str = Field(..., description="Owner Clerk user ID")
    title: str = Field(..., description="Thread title")
    messages: List[MessageResponse] = Field(default_factory=list, description="Nested message bubbles")
    message_count: int = Field(..., description="Calculated total of nested messages")
    status: str = Field(..., description="Current status of the conversation")
    created_at: datetime = Field(..., description="Thread creation timestamp")
    updated_at: datetime = Field(..., description="Last database modification timestamp")
    last_activity_at: datetime = Field(..., description="Last conversation activity timestamp")

    model_config = ConfigDict(from_attributes=True)


class ConversationListResponse(BaseModel):
    """Standardized paginated list response wrapper."""

    total: int = Field(..., description="Total count of matches")
    page: int = Field(..., description="Current index page")
    limit: int = Field(..., description="Current limits scale")
    items: List[ConversationResponse] = Field(default_factory=list, description="List of conversations")


class ConversationStatsResponse(BaseModel):
    """Statistical summary analysis of user conversations."""

    total_conversations: int = Field(..., description="Total conversations created by this user")
    active_conversations: int = Field(..., description="Total active threads")
    archived_conversations: int = Field(..., description="Total archived threads")
    total_messages: int = Field(..., description="Sum total of messages across all user conversations")
    average_messages_per_conversation: float = Field(..., description="Average depth of conversation threads")


class ConversationHealthSchema(BaseModel):
    """Module health check reporting validation model."""

    status: str = Field(..., description="Module state")
    retention_limit_per_user: int = Field(..., description="Configured maximum number of concurrent threads")
