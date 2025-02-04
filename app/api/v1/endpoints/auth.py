from fastapi import APIRouter, Depends
from app.services.auth_service import AuthService, get_auth_service
from app.schemas.user import UserCreate, UserLogin

router = APIRouter()

@router.post("/register")
async def register_user(user: UserCreate, service: AuthService = Depends(get_auth_service)):
    return await service.register_user(user)

@router.post("/login")
async def login_user(user: UserLogin, service: AuthService = Depends(get_auth_service)):
    return await service.authenticate_user(user)
