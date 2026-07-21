from fastapi import APIRouter
from app.routes import health

api_router = APIRouter()

# Include versioned routers
api_router.include_router(health.router, tags=["System Health"])
