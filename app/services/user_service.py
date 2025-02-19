from typing import Any, List, Optional
from app.database.base import BaseRepository
from app.services.base_service import BaseService

class UserService(BaseService):
    """Service layer handling user operations."""

    def __init__(self, repository: BaseRepository):
        super().__init__(repository)

    async def create(self, data: dict) -> Any:
        # Example: Additional business logic before saving
        data["username"] = data.get("username").lower()
        return await self.repository.create(data)

    async def get_by_id(self, id: Any) -> Optional[Any]:
        return await self.repository.get_by_id(id)

    async def get_all(self) -> List[Any]:
        return await self.repository.get_all()

    async def update(self, id: Any, data: dict) -> Any:
        return await self.repository.update(id, data)

    async def delete(self, id: Any) -> Any:
        return await self.repository.delete(id)
