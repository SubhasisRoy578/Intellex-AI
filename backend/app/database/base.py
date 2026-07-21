# Import all models here so that Alembic can discover them
from app.database.database import Base
from app.models.conversation import Conversation, Message

# Export Base and any models for clean imports
__all__ = ["Base", "Conversation", "Message"]
