import asyncio
from typing import Any, Optional
from app.ai.base import BaseAIProvider
from app.ai.utils import estimate_token_count
from app.config.config import settings
from app.core.logging import logger
from app.ai.exceptions import AIProviderException, AITimeoutException


class AIService:
    """Business service handling execution metrics, token estimation, and transient retry loops."""

    def __init__(self, provider: BaseAIProvider) -> None:
        self.provider = provider

    async def execute_generation(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        **kwargs: Any,
    ) -> tuple[str, int]:
        """Dispatches prompt to the active provider with built-in retry and token usage estimation.

        Args:
            prompt (str): Textual prompt context.
            system_instruction (Optional[str]): Persona directives.

        Returns:
            tuple[str, int]: Tuple of generated text response and computed token usage metrics.
        """
        max_retries = settings.AI_MAX_RETRIES
        delay = 1.0
        last_exception = None

        logger.info(
            f"Dispatching prompt to AI Provider '{self.provider.get_provider_name()}'...",
            extra={
                "extra": {
                    "provider": self.provider.get_provider_name(),
                    "model": self.provider.get_model_name(),
                    "prompt_length_chars": len(prompt)
                }
            }
        )

        for attempt in range(1, max_retries + 1):
            try:
                # Call abstract generation
                response_text = await self.provider.generate_response(
                    prompt=prompt,
                    system_instruction=system_instruction,
                    **kwargs
                )
                
                # Compute token usage
                prompt_tokens = estimate_token_count(prompt)
                completion_tokens = estimate_token_count(response_text)
                total_tokens = prompt_tokens + completion_tokens

                logger.info(
                    "AI generation succeeded",
                    extra={
                        "extra": {
                            "provider": self.provider.get_provider_name(),
                            "model": self.provider.get_model_name(),
                            "prompt_tokens": prompt_tokens,
                            "completion_tokens": completion_tokens,
                            "total_tokens": total_tokens,
                            "attempt": attempt
                        }
                    }
                )

                return response_text, total_tokens

            except (AIProviderException, AITimeoutException) as exc:
                last_exception = exc
                logger.warning(
                    f"AI generation attempt {attempt}/{max_retries} failed: {exc.message}",
                    extra={"extra": {"attempt": attempt, "error": str(exc)}}
                )
                if attempt < max_retries:
                    await asyncio.sleep(delay)
                    delay *= 2  # Exponential backoff
            except Exception as exc:
                last_exception = exc
                logger.error(
                    f"Unexpected error in execute_generation attempt {attempt}/{max_retries}: {exc}",
                    exc_info=True
                )
                if attempt < max_retries:
                    await asyncio.sleep(delay)
                    delay *= 2

        # If we exhausted all retries, raise the final exception
        raise last_exception or AIProviderException(message="AI Generation exhausted all retries")
