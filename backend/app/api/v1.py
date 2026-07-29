from fastapi import APIRouter
from app.routes import health
from app.auth import routes as auth_routes
from app.ai import routes as ai_routes
from app.uploads import routes as upload_routes
from app.documents import routes as document_routes
from app.images import routes as image_routes
from app.search import routes as search_routes
from app.orchestrator import routes as orchestrator_routes
from app.conversations import routes as conversation_routes
from app.monitoring import routes as monitoring_routes

api_router = APIRouter()

# Include versioned routers
api_router.include_router(health.router, tags=["System Health"])
api_router.include_router(auth_routes.router, tags=["Clerk Authentication"])
api_router.include_router(ai_routes.router, tags=["AI Conversation Engine"])
api_router.include_router(upload_routes.router, tags=["Secure File Upload Infrastructure"])
api_router.include_router(document_routes.router, tags=["Document Processing Module"])
api_router.include_router(image_routes.router, tags=["Image Analysis & OCR Module"])
api_router.include_router(search_routes.router, tags=["Latest Internet Search Integration"])
api_router.include_router(orchestrator_routes.router, tags=["AI Knowledge Orchestration Layer"])
api_router.include_router(conversation_routes.router, tags=["Conversation Management Module"])
api_router.include_router(monitoring_routes.router, tags=["System Performance & Monitoring"])
