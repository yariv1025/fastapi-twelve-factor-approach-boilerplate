import redis.asyncio as redis

from typing import Union
from pymongo import MongoClient
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.config import settings


class HealthService:
    """Service for checking system health, including databases and cache services."""

    def __init__(self, db: Union[AsyncSession, AsyncIOMotorDatabase, Redis]):
        self.db = db

    async def check_postgres(self):
        try:
            await self.db.execute("SELECT *")
            return True
        except Exception as e:
            return False

    async def check_mongo(self):
        try:
            client = MongoClient(settings.MONGO_URI)
            client.admin.command('ping')
            return True
        except Exception as e:
            return False

    async def check_redis(self):
        try:
            client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD)
            if await client.ping():
                return True
        except Exception as e:
            return False
