from typing import Set

# Storage & File Upload constraints
SUPPORTED_DOCUMENT_EXTENSIONS: Set[str] = {".pdf", ".docx", ".txt"}
SUPPORTED_IMAGE_EXTENSIONS: Set[str] = {".jpg", ".jpeg", ".png"}

# Conversation constraints
MAX_CONVERSATIONS_MEMORY: int = 10

# API standard message responses
SUCCESS_MESSAGE: str = "Operation completed successfully"
INTERNAL_ERROR_MESSAGE: str = "An unexpected server error occurred. Please contact system administrators."
