from fastapi import APIRouter
from app.routes import health
from app.auth import routes as auth_routes
from app.ai import routes as ai_routes
from app.uploads import routes as upload_routes
from app.documents import routes as document_routes

api_router = APIRouter()

# Include versioned routers
api_router.include_router(health.router, tags=["System Health"])
api_router.include_router(auth_routes.router, tags=["Clerk Authentication"])
api_router.include_router(ai_routes.router, tags=["AI Conversation Engine"])
api_router.include_router(upload_routes.router, tags=["Secure File Upload Infrastructure"])
api_router.include_router(document_routes.router, tags=["Document Processing Module"])
