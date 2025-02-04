from fastapi import APIRouter
from app.api.v1.endpoints import tasks, users, health

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(health.router, prefix="/health", tags=["Health Check"])
