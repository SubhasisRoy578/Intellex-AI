from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List, Dict, Any

from app.auth.dependencies import get_current_user
from app.auth.schemas import ClerkUser
from app.dependencies.dependencies import get_db_session

from app.agent.schemas import AgentChatRequest, AgentChatResponse, AgentHealthSchema
from app.agent.service import agent_service

router = APIRouter(prefix="/agent", tags=["AI Agent Framework & Tool Calling"])


@router.post(
    "/chat",
    response_model=AgentChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Initiate Autonomous Agent Chat Request",
    description="Invokes the AI Agent Planner to autonomously select, order, and execute specific helper tools.",
)
async def execute_agent_chat(
    payload: AgentChatRequest,
    current_user: ClerkUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> AgentChatResponse:
    """Triggers the autonomous agent execution pipeline with full security checking."""
    return await agent_service.execute_autonomous_chat(
        message=payload.message,
        user_id=current_user.id,
        db=db
    )


@router.get(
    "/health",
    response_model=AgentHealthSchema,
    status_code=status.HTTP_200_OK,
    summary="Verify Agent Framework Operational Integrity",
    description="Loads a list of registered tools and active planner schemas available.",
)
async def retrieve_agent_health() -> AgentHealthSchema:
    """Returns active configurations and integrity stats of the autonomous planner."""
    return AgentHealthSchema(
        status="healthy",
        registered_tools=agent_service.available_tools,
        active_planner="AgentPlanner"
    )
