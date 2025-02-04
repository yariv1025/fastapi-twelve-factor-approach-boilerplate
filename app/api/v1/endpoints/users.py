from fastapi import APIRouter, Depends
from app.services.user_service import UserService
from app.database.session import get_pg_session, get_mongo_db
from app.database.repositories.postgres_repository import PostgresRepository
from app.database.repositories.mongo_repository import MongoRepository
from app.database.models.user import User
from pydantic import BaseModel
from app.core.dependencies import get_current_user
from app.database.models.user import UserRole
from app.core.dependencies import require_role

router = APIRouter()

# Dependency Injection: Choose PostgreSQL or MongoDB dynamically
async def get_user_service(db_type: str = "postgres", session=Depends(get_pg_session), db=Depends(get_mongo_db)):
    if db_type == "postgres":
        return UserService(PostgresRepository(session, User))
    else:
        return UserService(MongoRepository(db, "users"))

# Pydantic schema
class UserCreate(BaseModel):
    username: str
    email: str

@router.post("/", tags=["Users"])
async def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    return await service.create(user.dict())

@router.get("/{user_id}", tags=["Users"])
async def get_user(user_id: str, service: UserService = Depends(get_user_service)):
    return await service.get_by_id(user_id)

@router.get("/me")
async def get_current_user_info(user: dict = Depends(get_current_user)):
    return {"email": user["sub"]}

@router.get("/admin-only")
async def admin_dashboard(user: dict = Depends(require_role(UserRole.ADMIN))):
    return {"message": "Welcome, Admin!", "user": user}
