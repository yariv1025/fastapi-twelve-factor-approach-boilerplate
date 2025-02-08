from fastapi import APIRouter

from app.api.v1.endpoints import users, health, auth, scans

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(scans.router, prefix="/scans", tags=["Scans"])
api_router.include_router(health.router, prefix="/health", tags=["Health Check"])
