import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import settings

class HealthService:
    """Service for checking system health, including databases and cache services."""

    @staticmethod
    async def check_postgres(session: AsyncSession) -> bool:
        """Check if PostgreSQL database is available."""
        try:
            await session.execute("SELECT 1")
            return True
        except Exception:
            return False

    @staticmethod
    async def check_mongo(mongo_db: AsyncIOMotorDatabase) -> bool:
        """Check if MongoDB database is available."""
        try:
            await mongo_db.command("ping")
            return True
        except Exception:
            return False

    @staticmethod
    async def check_redis() -> bool:
        """Check if Redis is available."""
        try:
            redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
            pong = await redis_client.ping()
            await redis_client.close()
            return pong
        except Exception:
            return False
