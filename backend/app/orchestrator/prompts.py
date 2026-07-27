from typing import List, Dict, Any, Optional

ORCHESTRATOR_SYSTEM_INSTRUCTION = (
    "You are Intellex AI, a premium, lightweight, and highly capable AI Assistant. "
    "Your user interface elements are designed in a premium dark-gold style. "
    "You have access to structured reference context retrieved from various knowledge modules "
    "(such as real-time web searches, uploaded documents, or image OCR text extractions). "
    "Use the provided context to answer the user's question directly, accurately, and objectively. "
    "Always cite your sources where applicable. "
    "If the context is insufficient or unhelpful, state that clearly and answer using your general knowledge."
)


class PromptComposer:
    """Orchestrator prompt composer formatting system directives and referenced context blocks."""

    @staticmethod
    def compose_unified_prompt(
        user_message: str,
        web_context: Optional[str] = None,
        document_context: Optional[str] = None,
        ocr_context: Optional[str] = None,
    ) -> str:
        """Constructs a consolidated prompt, clearly demarcating different knowledge context frames.

        Args:
            user_message (str): User prompt question.
            web_context (Optional[str]): Standard formatted web context.
            document_context (Optional[str]): Consolidated documents text.
            ocr_context (Optional[str]): Consolidated image OCR text.

        Returns:
            str: Single consolidated prompt context.
        """
        prompt_segments = []

        # 1. Inject Web Search context if present
        if web_context:
            prompt_segments.append(
                f"=== [KNOWLEDGE SOURCE: LATEST INTERNET SEARCH] ===\n"
                f"{web_context}\n"
                f"===================================================\n"
            )

        # 2. Inject Documents context if present
        if document_context:
            prompt_segments.append(
                f"=== [KNOWLEDGE SOURCE: UPLOADED DOCUMENTS] ===\n"
                f"{document_context}\n"
                f"===============================================\n"
            )

        # 3. Inject Image OCR context if present
        if ocr_context:
            prompt_segments.append(
                f"=== [KNOWLEDGE SOURCE: IMAGE OCR TEXT EXTRACTS] ===\n"
                f"{ocr_context}\n"
                f"===================================================\n"
            )

        # 4. Inject Primary User Question
        prompt_segments.append(
            f"User Question: {user_message.strip()}\n\n"
            f"Intellex AI Response:"
        )

        return "\n\n".join(prompt_segments)
