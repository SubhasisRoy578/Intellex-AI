from typing import List, Dict, Any, Optional

DEFAULT_SYSTEM_PROMPT = (
    "You are Intellex AI, a premium, lightweight, and highly capable AI Assistant. "
    "Your design system features dark-gold elements to represent premium quality. "
    "You provide clear, accurate, and professional answers. "
    "Be direct and objective while maintaining an intellectual, friendly tone."
)


class PromptBuilder:
    """Utility class to construct, sanitize, and manage structured prompts for LLM consumption."""

    def __init__(self, default_system_instruction: str = DEFAULT_SYSTEM_PROMPT) -> None:
        self.default_system_instruction = default_system_instruction

    def build_simple_prompt(self, user_message: str) -> str:
        """Sanitizes and bundles a raw user query with basic framing."""
        return user_message.strip()

    def build_conversation_prompt(
        self,
        user_message: str,
        history: List[Dict[str, str]],
    ) -> str:
        """Formats an in-context chat thread of past messages into a single parsed prompt string.

        Args:
            user_message (str): Latest user prompt.
            history (List[Dict[str, str]]): List of past role/content dictionaries.

        Returns:
            str: Single formatted conversational prompt.
        """
        formatted_segments = []
        for message in history:
            role = message.get("role", "user").capitalize()
            content = message.get("content", "").strip()
            formatted_segments.append(f"{role}: {content}")

        # Append latest prompt
        formatted_segments.append(f"User: {user_message.strip()}")
        formatted_segments.append("Assistant:")

        return "\n\n".join(formatted_segments)


# Shared instance
prompt_builder = PromptBuilder()
