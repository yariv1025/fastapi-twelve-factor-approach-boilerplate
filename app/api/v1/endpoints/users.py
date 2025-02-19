from fastapi import APIRouter, Depends

from app.schemas.user import UserCreate
from app.database.models.user import UserRole
from app.services.user_service import UserService
from app.core.dependencies import get_current_user
from app.core.dependencies import require_role, get_user_service

router = APIRouter()


@router.post("/", tags=["Users"])
async def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    """
    Endpoint to create a new user.

    :param user: User data to create the new user, which is validated using the UserCreate schema.
    :param service: The UserService used to handle business logic for user creation. It is injected as a dependency.
    :return: Returns a response containing the created user data.
    """
    return await service.create(user.model_dump())


@router.get("/{user_id}", tags=["Users"])
async def get_user(user_id: str, service: UserService = Depends(get_user_service)):
    """
    Endpoint to fetch a user by their unique user_id.

    :param user_id: The unique ID of the user to fetch.
    :param service: The UserService used to handle business logic for interacting with the database and retrieve the user.
    :return: Returns the user data corresponding to the provided user_id.
    """
    return await service.get_by_id(user_id)


@router.get("/me")
async def get_current_user_info(user: dict = Depends(get_current_user)):
    """
    Endpoint to fetch the current authenticated user's info.

    :param user: The currently authenticated user, extracted from the JWT token.
    :return: Returns the email of the authenticated user.
    """
    return {"email": user["sub"]}


@router.get("/admin-only")
async def admin_dashboard(user: dict = Depends(require_role(UserRole.ADMIN))):
    """
    Endpoint to access an admin-only dashboard.

    :param user: The current user, which validated to have an ADMIN role using the require_role dependency.
    :return: Returns a welcome message for the admin user.
    """
    return {"message": "Welcome, Admin!", "user": user}
