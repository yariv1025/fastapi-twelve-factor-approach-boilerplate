from typing import Any, List, Optional
from bcrypt import hashpw, gensalt

from app.database.base import BaseRepository
from app.services.base_service import BaseService

class UserService(BaseService):
    """Service layer handling user operations."""

    def __init__(self, repository: BaseRepository):
        super().__init__(repository)

    async def create(self, data: dict) -> Any:
        """
        Create a new user with hashed password and store it securely.

        :param data: Dictionary containing user details.
        :return: The created user object (excluding password).
        """
        data["username"] = data.get("username").lower()
        data["password"] = hashpw(data["password"].encode(), gensalt()).decode()  # Hash password
        user = await self.repository.create(data)
        user.pop("password", None)  # Remove password from response
        return user

    async def get_by_id(self, id: Any) -> Optional[Any]:
        """
        Retrieve a user by their ID, ensuring the password is not exposed.

        :param id: The unique identifier of the user.
        :return: The user object without the password.
        """
        user = await self.repository.get_by_id(id)
        if user:
            user.pop("password", None)  # Remove password from response
        return user

    async def get_all(self) -> List[Any]:
        """
        Retrieve all users while ensuring passwords are not exposed.

        :return: List of user objects without passwords.
        """
        users = await self.repository.get_all()
        for user in users:
            user.pop("password", None)  # Remove password from response
        return users

    async def update(self, id: Any, data: dict) -> Any:
        """
        Update user details securely.

        - If a password is provided, hash it before storing.
        - Ensure the updated user does not expose their password.

        :param id: The unique identifier of the user.
        :param data: The updated user data.
        :return: The updated user object without the password.
        """
        if "password" in data:
            data["password"] = hashpw(data["password"].encode(), gensalt()).decode()  # Hash new password

        updated_user = await self.repository.update(id, data)
        if updated_user:
            updated_user.pop("password", None)  # Remove password from response
        return updated_user

    async def delete(self, id: Any) -> Any:
        """
        Delete a user by their ID.

        :param id: The unique identifier of the user.
        :return: The deleted user object (without password) or None.
        """
        deleted_user = await self.repository.delete(id)
        if deleted_user:
            deleted_user.pop("password", None)  # Remove password from response
        return deleted_user

