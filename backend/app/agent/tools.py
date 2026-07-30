import time
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from app.core.logging import logger
from app.ai.provider import get_configured_ai_provider
from app.services.ai_service import AIService
from app.services.chat_service import ChatService
from app.documents.service import document_service
from app.images.service import image_service
from app.search.service import search_service
from app.orchestrator.service import orchestrator_service
from app.conversations.service import conversation_service


class BaseAgentTool(ABC):
    """Abstract interface defining standard schemas for autonomous agent tools."""

    @abstractmethod
    async def run(self, **kwargs: Any) -> Dict[str, Any]:
        """Runs the tool with parameters and returns structured result logs.

        Returns:
            Dict[str, Any]: Mapping of tool outputs and metrics.
        """
        pass

    @abstractmethod
    def get_tool_name(self) -> str:
        """Returns the identifier code name of this tool."""
        pass

    @abstractmethod
    def get_tool_description(self) -> str:
        """Returns description explaining tool capabilities to the planner."""
        pass


class AIConversationTool(BaseAgentTool):
    """Tool allowing autonomous text completions using the active LLM."""

    def __init__(self) -> None:
        provider = get_configured_ai_provider()
        self.chat_svc = ChatService(AIService(provider))

    async def run(self, **kwargs: Any) -> Dict[str, Any]:
        message = kwargs.get("message", "")
        conv_id = kwargs.get("conversation_id")
        logger.info(f"Agent executing AIConversationTool for query...")
        result = await self.chat_svc.process_chat(message, conv_id)
        return {"output": result["response"], "conversation_id": result["conversation_id"]}

    def get_tool_name(self) -> str:
        return "ai_conversation"

    def get_tool_description(self) -> str:
        return "Generates responsive, intelligent AI prompt replies based on general knowledge."


class DocumentProcessingTool(BaseAgentTool):
    """Tool wrapping the Phase 5 Document Processing Service."""

    async def run(self, **kwargs: Any) -> Dict[str, Any]:
        upload_id = kwargs.get("upload_id", "")
        logger.info(f"Agent executing DocumentProcessingTool on file: {upload_id}")
        result = document_service.process_stored_document(upload_id)
        return {"output": result["extracted_text"], "metadata": result}

    def get_tool_name(self) -> str:
        return "document_processing"

    def get_tool_description(self) -> str:
        return "Parses and extracts full text layers and counting metrics from uploaded PDF, Word, or TXT documents."


class OCRProcessingTool(BaseAgentTool):
    """Tool wrapping the Phase 6 Image Analysis and OCR Service."""

    async def run(self, **kwargs: Any) -> Dict[str, Any]:
        upload_id = kwargs.get("upload_id", "")
        logger.info(f"Agent executing OCRProcessingTool on image: {upload_id}")
        result = image_service.process_stored_image(upload_id)
        return {"output": result["ocr_text"], "metadata": result}

    def get_tool_name(self) -> str:
        return "ocr_processing"

    def get_tool_description(self) -> str:
        return "Opens uploaded PNG/JPG image snapshots, executes PIL enhancements, and extracts OCR text strings."


class InternetSearchTool(BaseAgentTool):
    """Tool wrapping the Phase 7 Latest Internet Search Service."""

    async def run(self, **kwargs: Any) -> Dict[str, Any]:
        query = kwargs.get("query", "")
        limit = kwargs.get("limit")
        logger.info(f"Agent executing InternetSearchTool for query: '{query}'")
        result = await search_service.execute_web_search(query, limit)
        return {"output": result["results"], "metadata": result}

    def get_tool_name(self) -> str:
        return "internet_search"

    def get_tool_description(self) -> str:
        return "Crawls and queries standard web engines to fetch ranked, deduplicated, and sourced up-to-date web articles."


class OrchestratorTool(BaseAgentTool):
    """Tool wrapping the Phase 8 AI Knowledge Orchestration Layer."""

    async def run(self, **kwargs: Any) -> Dict[str, Any]:
        message = kwargs.get("message", "")
        doc_ids = kwargs.get("document_upload_ids")
        img_ids = kwargs.get("image_upload_ids")
        logger.info(f"Agent executing OrchestratorTool for query...")
        result = await orchestrator_service.execute_orchestrated_chat(
            message=message,
            document_upload_ids=doc_ids,
            image_upload_ids=img_ids
        )
        return {"output": result["response"], "metadata": result}

    def get_tool_name(self) -> str:
        return "knowledge_orchestration"

    def get_tool_description(self) -> str:
        return "Intelligently decides automatically to combine web search, document parsing, and OCR texts to generate unified answers."


class ConversationManagementTool(BaseAgentTool):
    """Tool wrapping the Phase 9 Conversation Management Services."""

    async def run(self, **kwargs: Any) -> Dict[str, Any]:
        action = kwargs.get("action", "list").lower()
        user_id = kwargs.get("user_id", "")
        db = kwargs.get("db")
        
        logger.info(f"Agent executing ConversationManagementTool action: {action}")
        if not db or not user_id:
            return {"error": "Missing database connection or user session scopes"}

        if action == "list":
            skip = kwargs.get("skip", 0)
            limit = kwargs.get("limit", 10)
            total, items = await conversation_service.list_user_threads(db, user_id, skip=skip, limit=limit)
            return {"output": [item.id for item in items], "total": total}
        elif action == "create":
            title = kwargs.get("title")
            created = await conversation_service.create_new_conversation(db, user_id, title)
            return {"output": created.id, "title": created.title}
            
        return {"output": "Unsupported conversation action"}

    def get_tool_name(self) -> str:
        return "conversation_management"

    def get_tool_description(self) -> str:
        return "Allows list summaries, thread creation, rerenames, or removals of conversation history."


class ToolRegistry:
    """Central registry tracking all registered BaseAgentTool instances."""

    def __init__(self) -> None:
        self._tools: Dict[str, BaseAgentTool] = {}
        # Auto register native tool blocks
        self.register_tool(AIConversationTool())
        self.register_tool(DocumentProcessingTool())
        self.register_tool(OCRProcessingTool())
        self.register_tool(InternetSearchTool())
        self.register_tool(OrchestratorTool())
        self.register_tool(ConversationManagementTool())

    def register_tool(self, tool: BaseAgentTool) -> None:
        self._tools[tool.get_tool_name()] = tool

    def get_tool(self, name: str) -> Optional[BaseAgentTool]:
        return self._tools.get(name)

    def list_tools(self) -> List[BaseAgentTool]:
        return list(self._tools.values())

    def list_tool_names(self) -> List[str]:
        return list(self._tools.keys())


# Singleton instance
tool_registry = ToolRegistry()
