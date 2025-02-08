from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.services.health_service import HealthService
from app.database.db_instance import get_pg_session, get_mongo_db

router = APIRouter()


@router.get("/", tags=["Health Check"])
async def health_status(
        pg_session: AsyncSession = Depends(get_pg_session),
        mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db),
):
    """
    Health check endpoint that verifies:
    - PostgreSQL connectivity
    - MongoDB connectivity
    - Redis connectivity (if enabled)

    Returns a JSON response with the health status.
    """
    postgres_ok = await HealthService.check_postgres(pg_session)
    mongo_ok = await HealthService.check_mongo(mongo_db)
    redis_ok = await HealthService.check_redis()

    health_data = {
        "status": "healthy" if all([postgres_ok, mongo_ok, redis_ok]) else "unhealthy",
        "databases": {
            "postgres": "OK" if postgres_ok else "DOWN",
            "mongodb": "OK" if mongo_ok else "DOWN",
            "redis": "OK" if redis_ok else "DOWN",
        },
    }

    return health_data if all([postgres_ok, mongo_ok, redis_ok]) else (health_data, 503)
