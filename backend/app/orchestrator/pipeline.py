from typing import List, Optional, Dict, Any
from app.orchestrator.service import orchestrator_service


class AIKnowledgePipeline:
    """Interface wrapper aligning execution contexts for Orchestrator transactions."""

    @staticmethod
    async def run_pipeline(
        message: str,
        document_upload_ids: Optional[List[str]] = None,
        image_upload_ids: Optional[List[str]] = None,
        user_id: Optional[str] = None,
        db: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """Convenience method triggering the orchestrated service.

        Args:
            message (str): User prompt query.
            document_upload_ids (Optional[List[str]]): Document file IDs.
            image_upload_ids (Optional[List[str]]): Image file IDs.
            user_id (Optional[str]): Optional user ID for memory mapping.
            db (Optional[Any]): Optional DB session.

        Returns:
            Dict[str, Any]: Consolidated chat metrics.
        """
        return await orchestrator_service.execute_orchestrated_chat(
            message=message,
            document_upload_ids=document_upload_ids,
            image_upload_ids=image_upload_ids,
            user_id=user_id,
            db=db
        )
