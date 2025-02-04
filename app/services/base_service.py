from abc import ABC, abstractmethod
from typing import Any, List, Optional
from app.database.base import BaseRepository

class BaseService(ABC):
    """Abstract Base Service providing a common interface for all services."""

    def __init__(self, repository: BaseRepository):
        self.repository = repository

    @abstractmethod
    async def create(self, data: dict) -> Any:
        pass

    @abstractmethod
    async def get_by_id(self, id: Any) -> Optional[Any]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Any]:
        pass

    @abstractmethod
    async def update(self, id: Any, data: dict) -> Any:
        pass

    @abstractmethod
    async def delete(self, id: Any) -> Any:
        pass
