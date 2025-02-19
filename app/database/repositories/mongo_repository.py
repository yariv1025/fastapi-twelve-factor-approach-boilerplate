from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database.base import BaseRepository
from typing import Any, List, Optional
from bson.objectid import ObjectId

class MongoRepository(BaseRepository):
    """Repository for MongoDB using Motor"""

    def __init__(self, db: AsyncIOMotorDatabase, collection_name: str):
        self.collection = db[collection_name]
        # self.collection = db.get(collection_name)

    async def create(self, data: dict) -> Any:
        result = await self.collection.insert_one(data)
        return {**data, "_id": str(result.inserted_id)}

    async def get_by_id(self, id: Any) -> Optional[Any]:
        result = await self.collection.find_one({"_id": ObjectId(id)})
        return result if result else None

    async def get_by_email(self, email: str) -> Optional[Any]:
        result = await self.collection.find_one({"email": email})
        return result if result else None

    async def get_all(self) -> List[Any]:
        return await self.collection.find().to_list(None)

    async def update(self, id: Any, data: dict) -> Any:
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": data}, return_document=True
        )
        return result

    async def delete(self, id: Any) -> Any:
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
