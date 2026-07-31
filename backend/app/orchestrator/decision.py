import re
from typing import List, Optional, Set, Dict, Any


class DecisionEngine:
    """Intelligent decision engine analyzing prompt intents and references to select active knowledge pipelines."""

    # Keywords mapping standard online search intents
    SEARCH_INTENT_KEYWORDS: Set[str] = {
        "search", "browse", "news", "current", "latest", "weather",
        "today", "now", "recent", "online", "price of", "how is", "website",
        "google", "bing", "internet", "web"
    }

    @classmethod
    def detect_intents(
        cls,
        message: str,
        document_upload_ids: Optional[List[str]] = None,
        image_upload_ids: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Analyzes incoming prompt parameters and text structures to resolve knowledge source selections.

        Args:
            message (str): Raw user query string.
            document_upload_ids (Optional[List[str]]): Stored file references.
            image_upload_ids (Optional[List[str]]): Stored image references.

        Returns:
            Dict[str, Any]: Mapping of determined decision triggers (e.g., "use_web", "use_documents", "use_ocr").
        """
        prompt_lower = message.lower()

        # 1. Check for physical references
        use_documents = bool(document_upload_ids)
        use_ocr = bool(image_upload_ids)

        # 2. Match search intent keywords
        # Split into alphanumeric words to prevent partial substring matches (e.g. "now" inside "known")
        words = set(re.findall(r"\b[a-z]{2,}\b", prompt_lower))
        use_web = not words.isdisjoint(cls.SEARCH_INTENT_KEYWORDS)

        # 3. Always include core conversation fallback
        use_chat = True

        return {
            "use_chat": use_chat,
            "use_web": use_web,
            "use_documents": use_documents,
            "use_ocr": use_ocr
        }
