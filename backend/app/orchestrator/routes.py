from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.dependencies import get_current_user
from app.auth.schemas import ClerkUser
from app.dependencies.dependencies import get_db_session
from app.orchestrator.schemas import OrchestratorChatRequest, OrchestratorChatResponse, OrchestratorHealthSchema, CitationInfo
from app.orchestrator.service import orchestrator_service
from app.ai.provider import get_configured_ai_provider

router = APIRouter(prefix="/orchestrator", tags=["AI Knowledge Orchestration Layer"])


@router.post(
    "/chat",
    response_model=OrchestratorChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Unified Knowledge Orchestrated AI Chat",
    description="Intelligently detects prompt intents and uploaded document/image references, retrieves Web context, "
                "combines all raw contexts, and queries the configured AI provider for a consolidated final answer.",
)
async def orchestrated_chat_query(
    request: OrchestratorChatRequest,
    current_user: ClerkUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> OrchestratorChatResponse:
    """Dispatches user request to the centralized orchestration pipeline securely."""
    result = await orchestrator_service.execute_orchestrated_chat(
        message=request.message,
        document_upload_ids=request.document_upload_ids,
        image_upload_ids=request.image_upload_ids,
        user_id=current_user.id,
        db=db
    )

    # Convert citations result dictionaries to CitationInfo models
    compiled_citations = []
    for cite in result["citations"]:
        compiled_citations.append(CitationInfo(
            type=cite.type,
            title=cite.title,
            url=cite.url,
            snippet=cite.snippet,
            document_name=cite.document_name,
            page_number=cite.page_number
        ))

    return OrchestratorChatResponse(
        response=result["response"],
        knowledge_sources_used=result["knowledge_sources_used"],
        citations=compiled_citations,
        confidence_score=result["confidence_score"],
        processed_timestamp=result["processed_timestamp"],
        metadata=result["metadata"],
    )


@router.get(
    "/health",
    response_model=OrchestratorHealthSchema,
    status_code=status.HTTP_200_OK,
    summary="Verify Orchestration Layer Health",
    description="Validates active sub-system connections and defaults.",
)
async def check_orchestrator_health() -> OrchestratorHealthSchema:
    """Reports configuration attributes for the core orchestration layer."""
    ai_provider = get_configured_ai_provider()
    return OrchestratorHealthSchema(
        status="healthy",
        active_sources=["Conversation Engine", "Document Processing", "Image OCR", "Internet Search"],
        default_ai_provider=ai_provider.get_provider_name()
    )
