from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List, Dict, Any

from app.auth.dependencies import get_current_user
from app.auth.schemas import ClerkUser
from app.dependencies.dependencies import get_db_session

from app.memory.schemas import (
    MemoryCreate,
    MemoryUpdate,
    MemoryResponse,
    MemoryStats
)
from app.memory.service import MemoryService

router = APIRouter(prefix="/memories", tags=["Personalization and Long-Term Memory"])


@router.post(
    "",
    response_model=MemoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a New Memory/Preference Record",
    description="Saves a new long-term fact, project, or preference associated with the current user.",
)
async def create_memory_record(
    payload: MemoryCreate,
    current_user: ClerkUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> MemoryResponse:
    """Saves a new user preference or fact."""
    record = await MemoryService.create_memory(db, user_id=current_user.id, payload=payload)
    return MemoryResponse.model_validate(record)


@router.get(
    "",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="List User Memories with Advanced Filtering",
    description="Loads a paginated list of long-term facts and preferences with filter constraints.",
)
async def list_memories(
    page: int = Query(default=1, ge=1, description="Page index"),
    limit: int = Query(default=20, ge=1, le=100, description="Page limit scale"),
    category: Optional[str] = Query(default=None, description="Filter by category"),
    is_active: Optional[bool] = Query(default=None, description="Filter by active state"),
    search: Optional[str] = Query(default=None, description="Optional keyword search string"),
    tags: Optional[str] = Query(default=None, description="Comma-separated list of tags to match"),
    sort_by: str = Query(default="last_accessed_at", description="Sort field ('last_accessed_at', 'title', 'created_at', 'importance_score')"),
    sort_order: str = Query(default="desc", description="Sort direction ('desc', 'asc')"),
    current_user: ClerkUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> Dict[str, Any]:
    """Fetches user preferences and facts with advanced search queries."""
    skip = (page - 1) * limit
    total_count, items = await MemoryService.list_memories(
        db,
        user_id=current_user.id,
        category=category,
        is_active=is_active,
        search_query=search,
        tags=tags,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order
    )

    mapped_items = [MemoryResponse.model_validate(item) for item in items]

    return {
        "total": total_count,
        "page": page,
        "limit": limit,
        "items": mapped_items
    }


@router.get(
    "/stats",
    response_model=MemoryStats,
    status_code=status.HTTP_200_OK,
    summary="Get Scoped User Memory Statistics",
    description="Loads descriptive metrics regarding total memories, active constraints, and categorical distribution.",
)
async def get_memory_stats(
    current_user: ClerkUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> MemoryStats:
    """Generates analytics for user dashboard memory utilization."""
    stats = await MemoryService.retrieve_metrics(db, user_id=current_user.id)
    return MemoryStats(
        total_memories=stats["total_memories"],
        active_memories=stats["active_memories"],
        categories=stats["categories"]
    )


@router.get(
    "/{memory_id}",
    response_model=MemoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve Detailed Memory Context",
    description="Retrieves a specific memory item, verifying that it belongs to the authenticated user.",
)
async def retrieve_memory(
    memory_id: str,
    current_user: ClerkUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> MemoryResponse:
    """Finds a single owned memory record."""
    record = await MemoryService.get_memory(db, memory_id=memory_id, user_id=current_user.id)
    return MemoryResponse.model_validate(record)


@router.put(
    "/{memory_id}",
    response_model=MemoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Modify Memory Properties",
    description="Updates attributes of an existing user-owned memory record.",
)
async def update_memory(
    memory_id: str,
    payload: MemoryUpdate,
    current_user: ClerkUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> MemoryResponse:
    """Updates attributes of a selected memory record."""
    record = await MemoryService.update_memory(
        db,
        memory_id=memory_id,
        user_id=current_user.id,
        payload=payload
    )
    return MemoryResponse.model_validate(record)


@router.delete(
    "/{memory_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete Single Memory",
    description="Deletes a specific memory record from database permanently.",
)
async def delete_memory(
    memory_id: str,
    current_user: ClerkUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    """Removes a single memory record securely."""
    await MemoryService.delete_memory(db, memory_id=memory_id, user_id=current_user.id)
    return {"success": True, "message": "Memory record successfully removed."}


@router.delete(
    "",
    status_code=status.HTTP_200_OK,
    summary="Clear All User Memories",
    description="Purges/deletes all memories and preferences associated with the current user.",
)
async def clear_all_memories(
    current_user: ClerkUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    """Triggers bulk clean removal of all long-term user memories."""
    count = await MemoryService.clear_memories(db, user_id=current_user.id)
    return {"success": True, "message": f"Successfully cleared all {count} long-term memories."}
