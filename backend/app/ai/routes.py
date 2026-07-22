from fastapi import APIRouter, Depends, status
from app.auth.dependencies import get_current_user
from app.auth.schemas import ClerkUser
from app.ai.schemas import ChatRequest, ChatResponse, AIHealthSchema
from app.ai.provider import get_configured_ai_provider
from app.services.ai_service import AIService
from app.services.chat_service import ChatService
from app.config.config import settings

router = APIRouter(prefix="/chat", tags=["AI Conversation Engine"])


def get_chat_service() -> ChatService:
    """Dependency injection factory returning an initialized ChatService instance."""
    provider = get_configured_ai_provider()
    ai_service = AIService(provider)
    return ChatService(ai_service)


@router.post(
    "",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate AI Conversation Response",
    description="Processes an incoming prompt, maintaining thread history context, and returns a verified AI reply.",
)
async def generate_chat_response(
    request: ChatRequest,
    current_user: ClerkUser = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service),
) -> ChatResponse:
    """Processes chat prompt through the decoupled AI Conversation Engine."""
    # Process user query safely
    result = await chat_service.process_chat(
        message=request.message,
        conversation_id=request.conversation_id
    )
    
    return ChatResponse(
        response=result["response"],
        conversation_id=result["conversation_id"],
        timestamp=result["timestamp"],
        provider=result["provider"],
        model=result["model"],
        tokens_used=result["tokens_used"],
    )


@router.get(
    "/health",
    response_model=AIHealthSchema,
    status_code=status.HTTP_200_OK,
    summary="Verify AI Engine Status",
    description="Reports the configured and running provider service and defaults.",
)
async def check_ai_health() -> AIHealthSchema:
    """Verifies configurations for the AI sub-systems."""
    provider = get_configured_ai_provider()
    return AIHealthSchema(
        status="healthy" if settings.AI_PROVIDER else "unconfigured",
        provider=provider.get_provider_name(),
        default_model=provider.get_model_name(),
    )
