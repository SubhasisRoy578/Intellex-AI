from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class MessageBase(BaseModel):
    role: str = Field(..., description="Role of the message sender (user, assistant, system)")
    content: str = Field(..., description="The textual content of the message")


class MessageCreate(MessageBase):
    pass


class MessageResponse(MessageBase):
    id: str
    conversation_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationBase(BaseModel):
    title: str = Field(..., max_length=255, description="Conversational thread title")


class ConversationCreate(ConversationBase):
    id: str = Field(..., description="Unique client-side generated UUID identifier")


class ConversationResponse(ConversationBase):
    id: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True


class StandardResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
