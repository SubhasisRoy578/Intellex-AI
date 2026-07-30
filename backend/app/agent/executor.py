import time
from typing import List, Dict, Any, Optional, Tuple
from app.core.logging import logger
from app.agent.tools import tool_registry
from app.agent.schemas import ToolExecutionInfo
from app.agent.exceptions import ToolExecutionException


class ToolExecutor:
    """Safe dispatcher running individual planned tools sequentially and recording performance metrics."""

    @staticmethod
    async def execute_plan(
        plan: List[Dict[str, Any]],
        **context_kwargs: Any
    ) -> Tuple[List[ToolExecutionInfo], List[Dict[str, Any]]]:
        """Iterates over a plan list, runs matching registered tools, and records stats.

        Returns:
            Tuple[List[ToolExecutionInfo], List[Dict[str, Any]]]: Tuple of executed statistics and raw outputs.
        """
        execution_stats: List[ToolExecutionInfo] = []
        raw_outputs: List[Dict[str, Any]] = []

        for stage in plan:
            name = stage["tool_name"]
            params = stage.get("params", {}).copy()
            
            # Merge extra shared contexts (e.g. active DB sessions, Clerk user ID)
            params.update(context_kwargs)

            tool_instance = tool_registry.get_tool(name)
            if not tool_instance:
                logger.error(f"ToolExecutor: Planned tool '{name}' is not registered.")
                execution_stats.append(ToolExecutionInfo(
                    tool_name=name,
                    status="failed",
                    duration_sec=0.0
                ))
                continue

            start_time = time.perf_counter()
            logger.info(f"ToolExecutor: Invoking tool '{name}' with parameter blocks...")

            try:
                # Dispatch execution asynchronously
                result = await tool_instance.run(**params)
                duration = time.perf_counter() - start_time
                
                execution_stats.append(ToolExecutionInfo(
                    tool_name=name,
                    status="success",
                    duration_sec=round(duration, 4)
                ))
                
                raw_outputs.append({
                    "tool_name": name,
                    "result": result
                })
                logger.info(f"ToolExecutor: Tool '{name}' succeeded in {duration:.4f}s.")

            except Exception as exc:
                duration = time.perf_counter() - start_time
                logger.error(f"ToolExecutor: Tool '{name}' failed: {exc}", exc_info=True)
                
                execution_stats.append(ToolExecutionInfo(
                    tool_name=name,
                    status="failed",
                    duration_sec=round(duration, 4)
                ))
                
                # Recover gracefully rather than crashing the entire pipeline (robust error recovery)
                raw_outputs.append({
                    "tool_name": name,
                    "error": str(exc),
                    "result": {"output": f"Error running tool '{name}': {str(exc)}"}
                })

        return execution_stats, raw_outputs
