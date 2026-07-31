import time
import math
from typing import List, Optional, Dict, Any

from app.core.logging import logger
from app.ai.provider import get_configured_ai_provider
from app.services.ai_service import AIService
from app.search.service import search_service
from app.documents.service import document_service
from app.images.service import image_service

from app.orchestrator.decision import DecisionEngine
from app.orchestrator.prompts import PromptComposer, ORCHESTRATOR_SYSTEM_INSTRUCTION
from app.orchestrator.context import ContextBuilder
from app.orchestrator.citations import CitationManager
from app.orchestrator.exceptions import OrchestratorException, SourceUnavailableException


class OrchestratorService:
    """The central brain orchestrating decision analysis, document/image parsing, web crawlers, and AI provider calls."""

    def __init__(self, ai_service: Optional[AIService] = None) -> None:
        # Resolve active AI worker dependency
        provider = get_configured_ai_provider()
        self.ai_service = ai_service or AIService(provider)

    async def execute_orchestrated_chat(
        self,
        message: str,
        document_upload_ids: Optional[List[str]] = None,
        image_upload_ids: Optional[List[str]] = None,
        user_id: Optional[str] = None,
        db: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """Runs the complete AI Knowledge Orchestration pipeline.

        Args:
            message (str): Primary user prompt.
            document_upload_ids (Optional[List[str]]): Target document IDs.
            image_upload_ids (Optional[List[str]]): Target image IDs.
            user_id (Optional[str]): Optional user ID for memory mapping.
            db (Optional[Any]): Optional DB session.

        Returns:
            Dict[str, Any]: Consolidated chat metrics and responses.
        """
        start_time = time.time()
        logger.info(f"Initiating AI Knowledge Orchestration pipeline for user query...")

        # 1. Intent Detection & Decision Analysis
        decision = DecisionEngine.detect_intents(
            message=message,
            document_upload_ids=document_upload_ids,
            image_upload_ids=image_upload_ids
        )

        sources_used = []
        web_results = None
        processed_docs = []
        processed_imgs = []

        # 2. Gather Document Context
        if decision["use_documents"] and document_upload_ids:
            sources_used.append("document")
            for doc_id in document_upload_ids:
                try:
                    result = document_service.process_stored_document(doc_id)
                    processed_docs.append({
                        "document_name": doc_id,
                        "pages": result.get("pages"),
                        "extracted_text": result.get("extracted_text")
                    })
                except Exception as exc:
                    logger.error(f"Failed to gather document context for {doc_id}: {exc}")
                    raise SourceUnavailableException(
                        message=f"Referenced document '{doc_id}' is corrupted or unreadable"
                    )

        # 3. Gather Image OCR Context
        if decision["use_ocr"] and image_upload_ids:
            sources_used.append("ocr")
            for img_id in image_upload_ids:
                try:
                    result = image_service.process_stored_image(img_id)
                    processed_imgs.append({
                        "image_name": img_id,
                        "width": result.get("width"),
                        "height": result.get("height"),
                        "ocr_text": result.get("ocr_text")
                    })
                except Exception as exc:
                    logger.error(f"Failed to gather image OCR context for {img_id}: {exc}")
                    raise SourceUnavailableException(
                        message=f"Referenced image '{img_id}' is corrupted or unreadable"
                    )

        # 4. Gather Web Search Context
        if decision["use_web"]:
            sources_used.append("web_search")
            try:
                search_res = await search_service.execute_web_search(message)
                web_results = search_res.get("results", [])
            except Exception as exc:
                # Recover gracefully on web search failure (answer using fallback general knowledge)
                logger.warning(f"Web search crawling degraded: {exc}. Recovering with fallback AI chat.")
                web_results = []

        if not sources_used:
            sources_used.append("chat_only")

        # 5. Format Context Blocks
        web_context_str = ContextBuilder.format_search_context(web_results) if web_results else None
        doc_context_str = ContextBuilder.format_document_context(processed_docs) if processed_docs else None
        ocr_context_str = ContextBuilder.format_ocr_context(processed_imgs) if processed_imgs else None

        # 6. Compose Unified Prompt
        final_prompt = PromptComposer.compose_unified_prompt(
            user_message=message,
            web_context=web_context_str,
            document_context=doc_context_str,
            ocr_context=ocr_context_str
        )

        # Retrieve and merge long-term personalization context
        system_inst = ORCHESTRATOR_SYSTEM_INSTRUCTION
        if db and user_id:
            try:
                from app.memory.context import MemoryContextComposer
                memory_addition = await MemoryContextComposer.get_system_prompt_addition(
                    db=db,
                    user_id=user_id,
                    user_query=message
                )
                if memory_addition:
                    system_inst = f"{system_inst}\n\n{memory_addition}"
            except Exception as exc:
                logger.error(f"Failed to load user memory context: {exc}")

        # 7. Execute AI Generation Pipeline
        try:
            response_text, tokens = await self.ai_service.execute_generation(
                prompt=final_prompt,
                system_instruction=system_inst
            )
        except Exception as exc:
            logger.error(f"AI Provider execution failed: {exc}", exc_info=True)
            raise OrchestratorException(message="Underlying AI generation failed")

        # Automatically extract new long-term facts/preferences in the background
        if db and user_id:
            try:
                from app.memory.service import MemoryService
                await MemoryService.trigger_extraction(db=db, user_id=user_id, dialogue=message)
            except Exception as exc:
                logger.error(f"Failed to auto-extract memory facts from chat flow: {exc}")

        # 8. Compile Unified Citations
        citations = CitationManager.compile_citations(
            web_results=web_results,
            processed_documents=processed_docs,
            processed_images=processed_imgs
        )

        # 9. Compute Confidence Scoring
        confidence = 0.85  # Default base confidence
        if processed_docs or processed_imgs:
            confidence = min(0.98, confidence + 0.10)  # High confidence with direct upload references
        if web_results:
            confidence = min(0.95, confidence + 0.05)  # Moderate confidence boost with search citations

        duration = time.time() - start_time
        logger.info(f"AI Knowledge Orchestration pipeline succeeded in {duration:.4f}s.")

        return {
            "response": response_text,
            "knowledge_sources_used": sources_used,
            "citations": citations,
            "confidence_score": confidence,
            "processed_timestamp": time.time(),
            "metadata": {
                "duration_sec": f"{duration:.4f}",
                "tokens_used": tokens,
                "ai_provider": self.ai_service.provider.get_provider_name(),
                "ai_model": self.ai_service.provider.get_model_name(),
            }
        }


# Global default instance
orchestrator_service = OrchestratorService()
