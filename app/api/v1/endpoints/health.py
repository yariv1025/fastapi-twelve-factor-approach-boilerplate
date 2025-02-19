from http import HTTPStatus
from fastapi import APIRouter, Depends

from app.core.config import settings
from app.services.health_service import HealthService
from app.database.db_instance import get_db

router = APIRouter()
db_type = settings.DB_TYPE.lower()


@router.get("/", tags=["Health Check"])
async def health_status(
        db = Depends(get_db),
):
    """
    Health check endpoint that verifies:
    - PostgreSQL connectivity
    - MongoDB connectivity
    - Redis connectivity (if enabled)

    Returns a JSON response with the health status.
    """
    health_service = HealthService(db)  # Explicitly passing dependency

    if db_type == "postgresql":
        db_ok = await health_service.check_postgres()
    elif db_type == "mongodb":
        db_ok = await health_service.check_mongo()
    elif db_type == "redis":
        db_ok = await health_service.check_redis()
    else:
        raise ValueError(f"Unsupported database type: {db_type}")

    health_data = {
        "status": "healthy" if db_ok else "unhealthy",
        "database": "OK" if db_ok else "DOWN",
    }

    return (health_data, HTTPStatus.OK) if db_ok \
        else (health_data, HTTPStatus.SERVICE_UNAVAILABLE)
