from typing import List, Dict, Any, Optional


class AgentContextBuilder:
    """Aggregates and formats intermediate outputs from diverse executed tools into a unified structured context string."""

    @staticmethod
    def compile_tool_contexts(raw_outputs: List[Dict[str, Any]]) -> str:
        """Processes tool output dictionaries and formats structured context blocks.

        Args:
            raw_outputs (List[Dict[str, Any]]): Collected list of executed tools results.

        Returns:
            str: Consolidated textual context string.
        """
        if not raw_outputs:
            return ""

        formatted_blocks = []
        for idx, stage in enumerate(raw_outputs, 1):
            name = stage["tool_name"]
            
            # Check for error states
            if "error" in stage:
                formatted_blocks.append(
                    f"[{idx}] Tool executed: '{name}'\n"
                    f"    Outcome: failed\n"
                    f"    Error: {stage['error']}\n"
                )
                continue

            result = stage.get("result", {})
            output_val = result.get("output", "")
            
            # Convert lists/dicts to strings nicely
            if isinstance(output_val, list):
                output_str = "\n".join(f"  - {str(item)}" for item in output_val)
            else:
                output_str = str(output_val)

            formatted_blocks.append(
                f"[{idx}] Tool executed successfully: '{name}'\n"
                f"    Extracted Content:\n"
                f"    \"\"\"\n{output_str.strip()}\n    \"\"\"\n"
            )

        return "\n\n".join(formatted_blocks)
