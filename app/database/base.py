from abc import ABC, abstractmethod
from typing import Any, List, Optional

class BaseRepository(ABC):
    """Abstract Base Repository to enforce a common interface"""

    @abstractmethod
    async def create(self, data: dict) -> Any:
        pass

    @abstractmethod
    async def get_by_id(self, id: Any) -> Optional[Any]:
        pass

    @abstractmethod
    async def get_by_email(self, email: Any) -> Optional[Any]:
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
