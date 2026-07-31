from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List, Dict, Any

from app.auth.dependencies import get_current_user
from app.auth.schemas import ClerkUser
from app.dependencies.dependencies import get_db_session

from app.conversations.schemas import (
    ConversationCreateRequest,
    ConversationUpdateRequest,
    ConversationResponse,
    ConversationListResponse,
    ConversationStatsResponse,
    ConversationHealthSchema
)
from app.conversations.service import conversation_service

router = APIRouter(prefix="/conversations", tags=["Conversation Management Module"])


@router.post(
    "",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a New Conversation Thread",
    description="Initiates a new conversation session, automatically checking and enforcing the newest-10 retention policy.",
)
async def create_conversation_thread(
    request: ConversationCreateRequest,
    current_user: ClerkUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> ConversationResponse:
    """Trigger creation of a new thread under the user's Clerk ID."""
    thread = await conversation_service.create_new_conversation(
        db,
        user_id=current_user.id,
        title=request.title
    )
    return ConversationResponse.model_validate(thread)


@router.get(
    "",
    response_model=ConversationListResponse,
    status_code=status.HTTP_200_OK,
    summary="List Scoped Conversations with Filters",
    description="Loads a paginated and sorted list of the user's conversation threads, supporting ilike keyword text search.",
)
async def list_conversation_threads(
    page: int = Query(default=1, ge=1, description="Page index"),
    limit: int = Query(default=10, ge=1, le=100, description="Page limit scale"),
    search: Optional[str] = Query(default=None, description="Optional keyword search string"),
    sort_by: str = Query(default="last_activity_at", description="Sort field ('last_activity_at', 'title', 'created_at')"),
    sort_order: str = Query(default="desc", description="Sort order direction ('desc', 'asc')"),
    current_user: ClerkUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> ConversationListResponse:
    """Fetches user threads list with paging and keyword filters."""
    skip = (page - 1) * limit
    total_count, items = await conversation_service.list_user_threads(
        db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        search_query=search,
        sort_by=sort_by,
        sort_order=sort_order
    )

    # Map models
    mapped_items = [ConversationResponse.model_validate(item) for item in items]

    return ConversationListResponse(
        total=total_count,
        page=page,
        limit=limit,
        items=mapped_items
    )


@router.get(
    "/stats",
    response_model=ConversationStatsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Scoped User Conversations Statistics",
    description="Aggregates and computes statistical metrics (total threads, message count sums, average depth) for the current user.",
)
async def get_conversations_stats(
    current_user: ClerkUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> ConversationStatsResponse:
    """Generates analytical aggregates for the user's dashboard."""
    stats = await conversation_service.calculate_user_statistics(db, user_id=current_user.id)
    return ConversationStatsResponse(
        total_conversations=stats["total_conversations"],
        active_conversations=stats["active_conversations"],
        archived_conversations=stats["archived_conversations"],
        total_messages=stats["total_messages"],
        average_messages_per_conversation=stats["average_messages_per_conversation"]
    )


@router.get(
    "/health",
    response_model=ConversationHealthSchema,
    status_code=status.HTTP_200_OK,
    summary="Verify Conversations Module Health",
    description="Validates active parameters of the conversations retention manager.",
)
async def check_conversations_health() -> ConversationHealthSchema:
    """Reports configuration attributes for the conversations retention module."""
    return ConversationHealthSchema(
        status="healthy",
        retention_limit_per_user=10
    )


@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve Detailed Conversation Context",
    description="Loads a single conversation thread with nested message bubbles, strictly verifying owner permissions.",
)
async def retrieve_conversation_thread(
    conversation_id: str,
    current_user: ClerkUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> ConversationResponse:
    """Locates and maps a single owned thread context."""
    thread = await conversation_service.get_conversation_details(
        db,
        conversation_id=conversation_id,
        user_id=current_user.id
    )
    return ConversationResponse.model_validate(thread)


@router.put(
    "/{conversation_id}",
    response_model=ConversationResponse,
    status_code=status.HTTP_200_OK,
    summary="Modify Conversation Properties",
    description="Updates the title and/or active status properties of the user's conversation thread.",
)
async def update_conversation_thread(
    conversation_id: str,
    request: ConversationUpdateRequest,
    current_user: ClerkUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> ConversationResponse:
    """Updates thread title or status scoped to owner."""
    thread = await conversation_service.rename_thread(
        db,
        conversation_id=conversation_id,
        user_id=current_user.id,
        title=request.title,
        status=request.status
    )
    return ConversationResponse.model_validate(thread)


@router.delete(
    "/{conversation_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete Single Conversation",
    description="Deletes a single conversation thread, cascading deletions down to nested messages.",
)
async def delete_conversation_thread(
    conversation_id: str,
    current_user: ClerkUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    """Removes a single owned thread from the database."""
    await conversation_service.remove_thread(
        db,
        conversation_id=conversation_id,
        user_id=current_user.id
    )
    return {"success": True, "message": "Conversation thread removed successfully"}


@router.delete(
    "",
    status_code=status.HTTP_200_OK,
    summary="Delete All Scoped Conversations",
    description="Prunes the entire list of conversation threads and messages belonging to the current user.",
)
async def delete_all_conversations(
    current_user: ClerkUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    """Deletes all owned threads from the database."""
    pruned = await conversation_service.clear_all_user_threads(db, user_id=current_user.id)
    return {
        "success": True,
        "message": f"Successfully cleared all {pruned} conversation threads"
    }
