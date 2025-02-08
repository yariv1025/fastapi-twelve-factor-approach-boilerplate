from sqlalchemy import Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.base import BaseRepository
from typing import Any, List, Optional, Sequence


class PostgresRepository(BaseRepository):
    """Repository for PostgreSQL using SQLAlchemy"""

    def __init__(self, session: AsyncSession, model):
        self.session = session
        self.model = model

    async def create(self, data: dict) -> Any:
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def get_by_id(self, id: Any) -> Optional[Any]:
        result = await self.session.get(self.model, id)
        return result

    async def get_by_email(self, email: str) -> Optional[Any]:
        result = await self.session.execute(select(self.model).filter_by(email=email))
        return result.scalars().first()

    # async def get_all(self) -> List[Any]:
    async def get_all(self) -> Sequence[Row[Any] | RowMapping | Any]:
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def update(self, id: Any, data: dict) -> Any:
        instance = await self.get_by_id(id)
        if instance:
            for key, value in data.items():
                setattr(instance, key, value)
            await self.session.commit()
            await self.session.refresh(instance)
        return instance

    async def delete(self, id: Any) -> Any:
        instance = await self.get_by_id(id)
        if instance:
            await self.session.delete(instance)
            await self.session.commit()
        return instance
