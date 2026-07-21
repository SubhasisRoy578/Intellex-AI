from fastapi import APIRouter
from app.routes import health
from app.auth import routes as auth_routes

api_router = APIRouter()

# Include versioned routers
api_router.include_router(health.router, tags=["System Health"])
api_router.include_router(auth_routes.router, tags=["Clerk Authentication"])
