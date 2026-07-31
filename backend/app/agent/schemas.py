from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class AgentChatRequest(BaseModel):
    """Input payload validation model for initiating an autonomous agent chat query."""

    message: str = Field(..., min_length=1, description="Raw user prompt query or command")
    document_upload_ids: Optional[List[str]] = Field(default=None, description="Optional uploaded file list")
    image_upload_ids: Optional[List[str]] = Field(default=None, description="Optional uploaded image list")


class ToolExecutionInfo(BaseModel):
    """Execution statistics details for a single invoked agent tool."""

    tool_name: str = Field(..., description="The registered identifier code of the tool")
    status: str = Field(..., description="Execution status outcome ('success', 'failed')")
    duration_sec: float = Field(..., description="Execution duration in seconds")


class AgentChatResponse(BaseModel):
    """Output serialization response containing final orchestrated text replies and execution details."""

    response: str = Field(..., description="Generated unified answer from the autonomous agent")
    tools_executed: List[ToolExecutionInfo] = Field(default_factory=list, description="Statistics logs of all executing tool blocks")
    processed_timestamp: float = Field(..., description="Epoch timestamp of complete execution path")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata logs of the executed agent planner stages")


class AgentHealthSchema(BaseModel):
    """Metadata status validation model for the autonomous agent framework."""

    status: str = Field(..., description="Operational status of the agent pipeline")
    registered_tools: List[str] = Field(..., description="List of registered tools available to the planner")
    active_planner: str = Field(..., description="Registered planner class name")
