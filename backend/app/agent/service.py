import time
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logging import logger
from app.ai.provider import get_configured_ai_provider
from app.services.ai_service import AIService
from app.agent.planner import AgentPlanner
from app.agent.executor import ToolExecutor
from app.agent.context import AgentContextBuilder
from app.agent.prompts import AgentPromptBuilder, AGENT_SYSTEM_INSTRUCTION
from app.agent.exceptions import AgentException


class AgentService:
    """The central orchestrator brain coordinating the full Agentic autonomous tool selection and execution loop."""

    def __init__(self, ai_service: Optional[AIService] = None) -> None:
        provider = get_configured_ai_provider()
        self.ai_service = ai_service or AIService(provider)

    async def execute_agent_chat(
        self,
        message: str,
        document_upload_ids: Optional[List[str]] = None,
        image_upload_ids: Optional[List[str]] = None,
        db: Optional[AsyncSession] = None,
        user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Runs the complete AI Agent Autonomous planning and execution loop.

        Args:
            message (str): Primary user query command.
            document_upload_ids (Optional[List[str]]): Target document IDs.
            image_upload_ids (Optional[List[str]]): Target image IDs.
            db (Optional[AsyncSession]): SQL database session.
            user_id (Optional[str]): Clerk authenticated user reference.

        Returns:
            Dict[str, Any]: Consolidated metrics, executed stats lists, and unified response.
        """
        start_time = time.time()
        logger.info(f"Initiating autonomous AI Agent loop for query...")

        # 1. Autonomous Planning
        plan = AgentPlanner.generate_execution_plan(
            message=message,
            document_upload_ids=document_upload_ids,
            image_upload_ids=image_upload_ids
        )

        # 2. Autonomous Tool Execution
        executed_stats, raw_outputs = await ToolExecutor.execute_plan(
            plan=plan,
            db=db,
            user_id=user_id
        )

        # 3. Context Aggregation
        tool_contexts = AgentContextBuilder.compile_tool_contexts(raw_outputs)

        # 4. Prompt Composition
        final_prompt = AgentPromptBuilder.compose_final_prompt(
            user_message=message,
            tool_contexts=tool_contexts
        )

        # 5. LLM Synthesis & AI Provider Dispatching
        try:
            response_text, tokens = await self.ai_service.execute_generation(
                prompt=final_prompt,
                system_instruction=AGENT_SYSTEM_INSTRUCTION
            )
        except Exception as exc:
            logger.error(f"AgentService: Synthesis step failed: {exc}", exc_info=True)
            raise AgentException(message="Underlying LLM Agent synthesis failed")

        duration = time.time() - start_time
        logger.info(f"AgentService: AI Agent loop succeeded in {duration:.4f}s.")

        return {
            "response": response_text,
            "tools_executed": executed_stats,
            "processed_timestamp": time.time(),
            "metadata": {
                "duration_sec": f"{duration:.4f}",
                "tokens_used": tokens,
                "ai_provider": self.ai_service.provider.get_provider_name(),
                "ai_model": self.ai_service.provider.get_model_name(),
                "execution_plan_stages": [s["tool_name"] for s in plan]
            }
        }


# Global default instance
agent_service = AgentService()
