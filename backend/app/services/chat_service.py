import time
from typing import Optional, Dict, Any
from app.ai.prompts import prompt_builder
from app.ai.context import context_manager
from app.services.ai_service import AIService


class ChatService:
    """Orchestration service linking session context management, prompting, and generation."""

    def __init__(self, ai_service: AIService) -> None:
        self.ai_service = ai_service

    async def process_chat(
        self,
        message: str,
        conversation_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Orchestrates the prompt execution, context updating, and metrics formatting.

        Args:
            message (str): Raw incoming user question.
            conversation_id (Optional[str]): Optional conversation ID.

        Returns:
            Dict[str, Any]: Payload containing AI text response, resolved thread ID, and usage.
        """
        # 1. Resolve or create unique thread session
        resolved_id = context_manager.get_or_create_session(conversation_id)

        # 2. Retrieve history context
        history = context_manager.retrieve_context(resolved_id)

        # 3. Construct prompt
        prompt = prompt_builder.build_conversation_prompt(message, history)

        # 4. Generate response through AI service
        response_text, tokens = await self.ai_service.execute_generation(
            prompt=prompt,
            system_instruction=prompt_builder.default_system_instruction
        )

        # 5. Append messages to short-lived context memory
        context_manager.append_message(resolved_id, role="user", content=message)
        context_manager.append_message(resolved_id, role="assistant", content=response_text)

        # 6. Format unified output payload
        return {
            "response": response_text,
            "conversation_id": resolved_id,
            "timestamp": time.time(),
            "provider": self.ai_service.provider.get_provider_name(),
            "model": self.ai_service.provider.get_model_name(),
            "tokens_used": tokens,
        }
