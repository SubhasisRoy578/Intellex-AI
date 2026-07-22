import httpx
from typing import Any, Optional, Dict
from app.ai.base import BaseAIProvider
from app.config.config import settings
from app.core.logging import logger
from app.ai.exceptions import AIProviderException, AITimeoutException


class MockAIProvider(BaseAIProvider):
    """Reliable, lightweight Mock AI provider returning intelligent predefined responses."""

    def __init__(self, model_name: str = "mock-gpt-4") -> None:
        self.model_name = model_name

    async def generate_response(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        # Predefined mock replies based on keywords for rich conversation flows
        prompt_lower = prompt.lower()
        if "hello" in prompt_lower or "hi" in prompt_lower:
            return "Hello! I am Intellex AI, your premium personal assistant. How can I help you achieve great things today?"
        elif "help" in prompt_lower:
            return "I am here to help you analyze documents, perform internet searches, write clean code, or chat about any ideas you have!"
        elif "premium" in prompt_lower:
            return "My system is configured with dark-gold styling to represent top-tier capability, speed, and intelligence."
        
        return f"Intellex AI received your query: '{prompt}'. As your lightweight assistant, I stand ready to assist you!"

    def get_provider_name(self) -> str:
        return "mock"

    def get_model_name(self) -> str:
        return self.model_name


class OpenAIProvider(BaseAIProvider):
    """Asynchronous production-ready OpenAI API Provider using raw httpx queries."""

    def __init__(self, api_key: str, model_name: str = "gpt-4o") -> None:
        self.api_key = api_key
        self.model_name = model_name
        self.api_url = "https://api.openai.com/v1/chat/completions"

    async def generate_response(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        data = {
            "model": self.model_name,
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.7),
        }

        async with httpx.AsyncClient(timeout=settings.AI_TIMEOUT_SECONDS) as client:
            try:
                response = await client.post(self.api_url, headers=headers, json=data)
                
                if response.status_code != 200:
                    logger.error(f"OpenAI error reply: {response.text}")
                    raise AIProviderException(
                        message="OpenAI provider failed to generate response",
                        details={"status_code": response.status_code, "error": response.text}
                    )
                
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
                
            except httpx.TimeoutException as e:
                logger.warning(f"OpenAI request timed out: {e}")
                raise AITimeoutException(message="OpenAI request timed out")
            except Exception as e:
                if isinstance(e, (AIProviderException, AITimeoutException)):
                    raise e
                logger.error(f"Error querying OpenAI: {e}", exc_info=True)
                raise AIProviderException(message="Failed to communicate with OpenAI API")

    def get_provider_name(self) -> str:
        return "openai"

    def get_model_name(self) -> str:
        return self.model_name


class GeminiProvider(BaseAIProvider):
    """Asynchronous production-ready Google Gemini API Provider using raw httpx queries."""

    def __init__(self, api_key: str, model_name: str = "gemini-1.5-pro") -> None:
        self.api_key = api_key
        self.model_name = model_name
        # Gemini Generative AI endpoints
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

    async def generate_response(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        headers = {"Content-Type": "application/json"}
        
        # Build contents structure
        contents = []
        if system_instruction:
            contents.append({
                "role": "user",
                "parts": [{"text": f"SYSTEM DIRECTIVE: {system_instruction}"}]
            })
        contents.append({
            "role": "user",
            "parts": [{"text": prompt}]
        })

        data = {"contents": contents}

        async with httpx.AsyncClient(timeout=settings.AI_TIMEOUT_SECONDS) as client:
            try:
                response = await client.post(self.api_url, headers=headers, json=data)
                
                if response.status_code != 200:
                    logger.error(f"Gemini error reply: {response.text}")
                    raise AIProviderException(
                        message="Gemini provider failed to generate response",
                        details={"status_code": response.status_code, "error": response.text}
                    )
                
                result = response.json()
                return result["candidates"][0]["content"]["parts"][0]["text"].strip()
                
            except httpx.TimeoutException as e:
                logger.warning(f"Gemini request timed out: {e}")
                raise AITimeoutException(message="Gemini request timed out")
            except Exception as e:
                if isinstance(e, (AIProviderException, AITimeoutException)):
                    raise e
                logger.error(f"Error querying Gemini: {e}", exc_info=True)
                raise AIProviderException(message="Failed to communicate with Gemini API")

    def get_provider_name(self) -> str:
        return "gemini"

    def get_model_name(self) -> str:
        return self.model_name


def get_configured_ai_provider() -> BaseAIProvider:
    """Dependency resolver returning the active configured BaseAIProvider instance."""
    provider_name = settings.AI_PROVIDER.lower()
    
    if provider_name == "openai" and settings.OPENAI_API_KEY:
        return OpenAIProvider(
            api_key=settings.OPENAI_API_KEY,
            model_name=settings.AI_DEFAULT_MODEL or "gpt-4o"
        )
    elif provider_name == "gemini" and settings.GEMINI_API_KEY:
        return GeminiProvider(
            api_key=settings.GEMINI_API_KEY,
            model_name=settings.AI_DEFAULT_MODEL or "gemini-1.5-pro"
        )
    
    # Defaults/Fallbacks to extremely safe Mock provider
    return MockAIProvider(model_name=settings.AI_DEFAULT_MODEL or "mock-gpt-4")
