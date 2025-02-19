import os
from redis.asyncio import Redis
from app.core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

db_type = settings.DB_TYPE.lower()

# PostgreSQL Connection
pg_engine = create_async_engine(settings.POSTGRES_URL, echo=False, future=True)
PostgresSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=pg_engine, class_=AsyncSession)

# MongoDB Connection
mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)
mongo_db = mongo_client.get_database(settings.MONGO_DB_NAME)

# Redis Connection
redis_client = Redis.from_url(settings.REDIS_URL)


async def get_pg_session() -> AsyncSession:
    """Dependency for PostgreSQL"""
    async with PostgresSessionLocal() as session:
        yield session


async def get_mongo_db():
    """Dependency for MongoDB"""
    yield mongo_db


async def get_redis_db():
    """Dependency for Redis"""
    yield redis_client


async def get_db():
    """
    Database session generator (handler) that yields a database session
    based on environment variable, and ensures that the database session
    lifecycle is properly managed (e.g., automatically closing sessions after use).
    """
    if db_type == "postgresql":
        async with PostgresSessionLocal() as session:
            yield session
    elif db_type == "mongodb":
        yield mongo_db
    elif db_type == "redis":
        yield redis_client
    else:
        raise ValueError(f"Unsupported database type: {db_type}")


# TODO: Delete the explanation below
"""
Purpose of using yield:

Context Management:
In asynchronous applications, the yield statement is used to provide a session 
object to the caller (e.g., a route handler) while maintaining control of the 
session's lifecycle. It ensures that the session is properly cleaned up after the caller is done with it.
This is similar to using with for synchronous context managers, but adapted for asynchronous code.

Asynchronous Iteration:
Since FastAPI and SQLAlchemy (via async_sessionmaker) work with asynchronous code, 
yield allows the session to be yielded asynchronously to the calling function 
(in this case, route handlers like create_user, get_user, etc.). 
This avoids blocking other requests while the database session is open.

Releasing Resources:
After the caller finishes using the session (i.e., after the endpoint function finishes executing), 
the control returns to the yield statement, and the session can be properly closed or cleaned up. 
The async with statement ensures that the session is automatically closed at the end of the function scope.

Why not just return the session?
We could technically return the session, but using yield offers the following advantages:
1. It allows for resource management (like closing sessions) automatically at the end of the function.
2. It supports asynchronous contexts, which are necessary when dealing with I/O-bound operations (like database interactions) without blocking other requests.
"""
