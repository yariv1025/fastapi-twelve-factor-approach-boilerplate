from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

# PostgreSQL Connection
pg_engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
PostgresSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=pg_engine, class_=AsyncSession)

# MongoDB Connection
mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)
mongo_db = mongo_client.get_database(settings.MONGO_DB_NAME)

# Dependency for PostgreSQL
async def get_pg_session() -> AsyncSession:
    async with PostgresSessionLocal() as session:
        yield session

# Dependency for MongoDB
async def get_mongo_db():
    yield mongo_db
