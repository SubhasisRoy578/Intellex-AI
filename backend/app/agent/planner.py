import re
from typing import List, Dict, Any, Optional
from app.core.logging import logger


class AgentPlanner:
    """Intelligent autonomous planner resolving user commands and planning a sequential tools execution queue."""

    SEARCH_KEYWORDS = {"search", "browse", "news", "current", "latest", "weather", "online", "web", "internet"}
    CONV_KEYWORDS = {"list conversations", "show chats", "create thread", "new conversation", "history"}

    @classmethod
    def generate_execution_plan(
        cls,
        message: str,
        document_upload_ids: Optional[List[str]] = None,
        image_upload_ids: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Analyzes query parameters and text intents to construct a sequential execution plan of tools.

        Args:
            message (str): User prompt query.
            document_upload_ids (Optional[List[str]]): Target document IDs.
            image_upload_ids (Optional[List[str]]): Target image IDs.

        Returns:
            List[Dict[str, Any]]: List of dictionary plans, e.g., [{"tool_name": "...", "params": {...}}].
        """
        prompt_lower = message.lower()
        words = set(re.findall(r"\b[a-z]{2,}\b", prompt_lower))
        plan = []

        logger.info(f"AgentPlanner: Constructing execution plan for user message...")

        # 1. Plan Document Processing if physical documents are attached
        if document_upload_ids:
            for doc_id in document_upload_ids:
                plan.append({
                    "tool_name": "document_processing",
                    "params": {"upload_id": doc_id}
                })

        # 2. Plan OCR Processing if physical images are attached
        if image_upload_ids:
            for img_id in image_upload_ids:
                plan.append({
                    "tool_name": "ocr_processing",
                    "params": {"upload_id": img_id}
                })

        # 3. Plan Internet Search if search keywords are matched
        if not words.isdisjoint(cls.SEARCH_KEYWORDS):
            plan.append({
                "tool_name": "internet_search",
                "params": {"query": message, "limit": 3}
            })

        # 4. Plan Conversation Management if history keywords match
        if any(keyword in prompt_lower for keyword in cls.CONV_KEYWORDS):
            action = "create" if "create" in prompt_lower or "new" in prompt_lower else "list"
            plan.append({
                "tool_name": "conversation_management",
                "params": {"action": action}
            })

        # 5. Append final orchestrator or conversation worker to summarize and answer the user query
        if document_upload_ids or image_upload_ids or not words.isdisjoint(cls.SEARCH_KEYWORDS):
            plan.append({
                "tool_name": "knowledge_orchestration",
                "params": {
                    "message": message,
                    "document_upload_ids": document_upload_ids,
                    "image_upload_ids": image_upload_ids
                }
            })
        else:
            plan.append({
                "tool_name": "ai_conversation",
                "params": {"message": message}
            })

        logger.info(f"AgentPlanner: Successfully constructed execution plan with {len(plan)} tool stages.")
        return plan
