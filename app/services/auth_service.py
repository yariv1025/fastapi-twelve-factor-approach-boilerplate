from datetime import timedelta
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.auth import verify_password, get_password_hash, create_access_token
from app.database.repositories.user_repository import UserRepository
from app.database.session import get_pg_session
from app.schemas.user import UserCreate, UserLogin
from app.database.models.user import UserRole

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register_user(self, user_data: UserCreate):
        existing_user = await self.user_repository.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = get_password_hash(user_data.password)
        user_data.password = hashed_password
        return await self.user_repository.create(user_data.dict())

    async def authenticate_user(self, user_data: UserLogin):
        user = await self.user_repository.get_by_email(user_data.email)
        if not user or not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # access_token = create_access_token({"sub": user.email}, timedelta(minutes=30))
        access_token = create_access_token({"sub": user.email, "role": user.role.value})  # Add role in JWT
        return {"access_token": access_token, "token_type": "bearer"}

# Dependency for authentication
async def get_auth_service(session: Session = Depends(get_pg_session)):
    return AuthService(UserRepository(session))


async def oauth_login(self, user_info: dict, provider: str):
    """Handles OAuth2 user login."""
    email = user_info["email"]
    user = await self.user_repository.get_by_email(email)

    if not user:
        user_data = {
            "email": email,
            "username": user_info.get("name", email.split("@")[0]),
            "hashed_password": None,  # No password for OAuth users
            "role": "user",
        }
        user = await self.user_repository.create(user_data)

    access_token = create_access_token({"sub": user.email, "role": user.role.value})
    return {"access_token": access_token, "token_type": "bearer"}
