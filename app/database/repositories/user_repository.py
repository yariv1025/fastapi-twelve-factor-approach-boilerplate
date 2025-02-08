from typing import Any
from pydantic import EmailStr

from app.database.base import BaseRepository


class UserRepository(BaseRepository):
    """User-specific repository that wraps a database-agnostic repository"""

    def __init__(self, db_repo: BaseRepository):
        self.db_repo = db_repo

    async def create(self, data: dict):
        return await self.db_repo.create(data)

    async def get_by_id(self, id: Any):
        return await self.db_repo.get_by_id(id)

    async def get_by_email(self, email: EmailStr):
        return await self.db_repo.get_by_email(email)

    async def get_all(self):
        return await self.db_repo.get_all()

    async def update(self, id: Any, data: dict):
        return await self.db_repo.update(id, data)

    async def delete(self, id: Any):
        return await self.db_repo.delete(id)
