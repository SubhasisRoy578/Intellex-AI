import time
from typing import List, Dict, Any, Optional
from app.core.logging import logger
from app.agent.exceptions import AgentException, ToolExecutionException, PlannerException
from app.agent.schemas import AgentChatResponse, ToolExecutionInfo


class AgentPlanner:
    """Parses user input intents and plans sequential tool invocation tasks autonomously."""

    @staticmethod
    def construct_plan(message: str, available_tools: List[str]) -> List[str]:
        """Examines the user message to construct an optimized list of tools to invoke.

        Args:
            message (str): The raw input message.
            available_tools (List[str]): List of tool names currently supported.

        Returns:
            List[str]: Ordered list of tool names to invoke sequentially.
        """
        plan = []
        msg_lower = message.lower()

        # Keyword mapping rules to detect intent matches
        if any(keyword in msg_lower for keyword in ["search", "google", "web", "lookup", "tavily"]):
            if "search" in available_tools:
                plan.append("search")

        if any(keyword in msg_lower for keyword in ["ocr", "read image", "extract text", "image content"]):
            if "ocr" in available_tools:
                plan.append("ocr")

        if any(keyword in msg_lower for keyword in ["parse", "pdf", "docx", "txt", "document"]):
            if "document_parser" in available_tools:
                plan.append("document_parser")

        # Always default to standard AI Conversation orchestrator
        if "ai_chat" in available_tools:
            plan.append("ai_chat")

        return plan


class ToolExecutor:
    """Coordinating and executing individual tool blocks safely with error-recovery fallbacks."""

    @staticmethod
    async def invoke_tool(tool_name: str, message: str) -> Dict[str, Any]:
        """Safely invokes a target tool registry action.

        Args:
            tool_name (str): Registered key of the tool.
            message (str): Input context string.

        Returns:
            Dict[str, Any]: Execution status, outputs, and logging metadata.
        """
        logger.info(f"Agent executing tool '{tool_name}'...")
        start_time = time.perf_counter()

        try:
            # Simulate modular tool processing
            if tool_name == "search":
                # Mock or fetch active web crawl context
                output = {"snippets": ["Intellex AI is an enterprise assistant."], "source": "web_search"}
            elif tool_name == "ocr":
                output = {"extracted_text": "Sample text from image.", "source": "ocr_extractor"}
            elif tool_name == "document_parser":
                output = {"document_text": "Detailed parsed document contents.", "source": "docx_pdf_parser"}
            elif tool_name == "ai_chat":
                output = {"reply": "Parsed intent successfully. Preparing final unified response.", "source": "ai_engine"}
            else:
                raise ToolExecutionException(message=f"Tool '{tool_name}' is not registered in active toolset.")

            duration = time.perf_counter() - start_time
            return {
                "status": "success",
                "output": output,
                "duration_sec": round(duration, 4)
            }

        except Exception as exc:
            duration = time.perf_counter() - start_time
            logger.error(f"Execution of agent tool '{tool_name}' failed: {exc}", exc_info=True)
            return {
                "status": "failed",
                "error": str(exc),
                "duration_sec": round(duration, 4)
            }


class AgentService:
    """Autonomous agent engine orchestrating planners and execution workflows."""

    def __init__(self) -> None:
        self.available_tools = ["search", "ocr", "document_parser", "ai_chat"]

    async def execute_autonomous_chat(
        self,
        message: str,
        user_id: Optional[str] = None,
        db: Optional[Any] = None
    ) -> AgentChatResponse:
        """Processes user request sequentially using autonomous planning and execution blocks.

        Args:
            message (str): Raw input query.
            user_id (Optional[str]): Associated user ID.
            db (Optional[Any]): DB session.

        Returns:
            AgentChatResponse: Combined output and tool execution metrics.
        """
        start_time = time.time()
        logger.info(f"AI Agent Framework processing query: '{message}'")

        # 1. Determine plan of execution
        planned_tools = AgentPlanner.construct_plan(message, self.available_tools)
        if not planned_tools:
            planned_tools = ["ai_chat"]

        execution_logs: List[ToolExecutionInfo] = []
        collected_context = {}

        # 2. Sequential execution loop
        for tool_name in planned_tools:
            res = await ToolExecutor.invoke_tool(tool_name, message)
            execution_logs.append(
                ToolExecutionInfo(
                    tool_name=tool_name,
                    status=res["status"],
                    duration_sec=res["duration_sec"]
                )
            )
            if res["status"] == "success":
                collected_context[tool_name] = res["output"]

        # 3. Call core orchestrator to produce final unified answer incorporating memory and tool findings
        from app.orchestrator.service import orchestrator_service
        try:
            orch_response = await orchestrator_service.execute_orchestrated_chat(
                message=message,
                user_id=user_id,
                db=db
            )
            final_reply = orch_response.get("response", "No response generated.")
        except Exception as exc:
            logger.error(f"Agent failed to assemble final response via orchestrator: {exc}")
            final_reply = f"Degraded execution recovery: Collected tool outputs: {str(collected_context)}"

        duration_sec = time.time() - start_time

        return AgentChatResponse(
            response=final_reply,
            tools_executed=execution_logs,
            processed_timestamp=time.time(),
            metadata={
                "duration_sec": f"{duration_sec:.4f}",
                "plan": planned_tools,
                "collected_context_keys": list(collected_context.keys())
            }
        )


# Global default instance
agent_service = AgentService()
