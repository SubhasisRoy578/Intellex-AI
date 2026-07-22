from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseAIProvider(ABC):
    """Abstract base interface defining interface boundaries for interchangeable LLM providers."""

    @abstractmethod
    async def generate_response(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        """Asynchronously dispatches a textual prompt query to the target provider.

        Args:
            prompt (str): Prepared user text or conversation prompt.
            system_instruction (Optional[str]): Operational instructions defining LLM persona.

        Returns:
            str: Raw generated textual string.
        """
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Returns the registered name of this provider (e.g. 'openai', 'gemini')."""
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """Returns the active config model name of this provider."""
        pass
