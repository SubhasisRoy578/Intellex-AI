from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.dependencies import get_current_user
from app.auth.schemas import ClerkUser
from app.dependencies.dependencies import get_db_session
from app.agent.schemas import AgentChatRequest, AgentChatResponse, AgentHealthSchema, ToolExecutionInfo
from app.agent.service import agent_service
from app.agent.tools import tool_registry

router = APIRouter(prefix="/agent", tags=["AI Agent Framework & Tool Calling"])


@router.post(
    "/chat",
    response_model=AgentChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Autonomous Agent Chat Completion",
    description="Intelligently plans sequential tool selections (crawls, document parsers, database statistics queries), "
                "executes them asynchronously, bundles outputs, and returns a unified cited LLM reply.",
)
async def agent_chat_query(
    request: AgentChatRequest,
    current_user: ClerkUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> AgentChatResponse:
    """Dispatches user prompt request to the centralized autonomous agent loop securely."""
    result = await agent_service.execute_agent_chat(
        message=request.message,
        document_upload_ids=request.document_upload_ids,
        image_upload_ids=request.image_upload_ids,
        db=db,
        user_id=current_user.id
    )

    # Convert execution stats dictionaries to ToolExecutionInfo Pydantic models
    tool_stats = []
    for stat in result["tools_executed"]:
        tool_stats.append(ToolExecutionInfo(
            tool_name=stat.tool_name,
            status=stat.status,
            duration_sec=stat.duration_sec
        ))

    return AgentChatResponse(
        response=result["response"],
        tools_executed=tool_stats,
        processed_timestamp=result["processed_timestamp"],
        metadata=result["metadata"]
    )


@router.get(
    "/health",
    response_model=AgentHealthSchema,
    status_code=status.HTTP_200_OK,
    summary="Verify Agent Framework Health",
    description="Validates and reports status of registered tool capabilities and active planners.",
)
async def check_agent_health() -> AgentHealthSchema:
    """Reports configuration attributes for the autonomous agent module."""
    return AgentHealthSchema(
        status="healthy",
        registered_tools=tool_registry.list_tool_names(),
        active_planner="AgentPlanner"
    )
