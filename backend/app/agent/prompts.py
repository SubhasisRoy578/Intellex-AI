from typing import Optional

AGENT_SYSTEM_INSTRUCTION = (
    "You are Intellex AI Agent, an advanced autonomous context-aggregating assistant. "
    "Your user interface elements are designed in a premium dark-gold style. "
    "You decide which backend tool capabilities (web searches, document parsing, image OCR, etc.) "
    "should be invoked to answer questions. "
    "Below is the consolidated list of intermediate tool outputs executed for this specific query. "
    "Use the provided tool context to synthesize a complete, polished, and cited answer directly resolving the user's inquiry."
)


class AgentPromptBuilder:
    """Agent prompt composer formatting custom system instructions and collected tools context."""

    @staticmethod
    def compose_final_prompt(
        user_message: str,
        tool_contexts: str,
    ) -> str:
        """Constructs a consolidated prompt with embedded executed tool context.

        Args:
            user_message (str): User prompt query.
            tool_contexts (str): Clean compiled tools outputs.

        Returns:
            str: Single consolidated prompt text.
        """
        prompt_segments = []

        if tool_contexts:
            prompt_segments.append(
                f"=== [AUTONOMOUS AGENT TOOLS EXECUTION CONTEXT] ===\n"
                f"{tool_contexts}\n"
                f"===================================================\n"
            )

        prompt_segments.append(
            f"User Inquiry: {user_message.strip()}\n\n"
            f"Intellex AI Agent Synthesized Answer:"
        )

        return "\n\n".join(prompt_segments)
