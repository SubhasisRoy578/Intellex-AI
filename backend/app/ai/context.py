from typing import Dict, List, Any, Optional
import uuid


class ConversationContextManager:
    """Manages short-lived active conversation context and memory frames in-memory."""

    def __init__(self) -> None:
        # Maps conversation_id -> List of message dictionaries representing active context
        self._active_sessions: Dict[str, List[Dict[str, str]]] = {}

    def get_or_create_session(self, conversation_id: Optional[str] = None) -> str:
        """Retrieves an existing conversation ID or creates a fresh one.

        Args:
            conversation_id (Optional[str]): Client provided thread reference.

        Returns:
            str: Resolved conversation ID.
        """
        resolved_id = conversation_id or str(uuid.uuid4())
        if resolved_id not in self._active_sessions:
            self._active_sessions[resolved_id] = []
        return resolved_id

    def retrieve_context(self, conversation_id: str) -> List[Dict[str, str]]:
        """Fetch past messages in context for the given conversation session."""
        return self._active_sessions.get(conversation_id, [])

    def append_message(self, conversation_id: str, role: str, content: str) -> None:
        """Appends a new role-content message block to the given session context."""
        if conversation_id not in self._active_sessions:
            self._active_sessions[conversation_id] = []
        
        self._active_sessions[conversation_id].append({
            "role": role,
            "content": content
        })

    def clear_session(self, conversation_id: str) -> None:
        """Flushes context memory for the given session ID."""
        if conversation_id in self._active_sessions:
            del self._active_sessions[conversation_id]


# Shared instance
context_manager = ConversationContextManager()
