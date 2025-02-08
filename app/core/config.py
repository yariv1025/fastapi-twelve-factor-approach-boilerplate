import os

from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    VERSION: str = os.getenv("VERSION")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT")
    DEBUG: bool = os.getenv("DEBUG")
    ENTRYPOINT: str = "main:app"

    # Server settings
    HOST: str = os.getenv("HOST")
    PORT: int = os.getenv("PORT")

    # Database settings
    DB_TYPE: str = os.getenv("DB_TYPE", "postgresql")  # Default to PostgreSQL if not set

    POSTGRES_URL: str = os.getenv("POSTGRES_URL")
    MONGODB_URL: str = os.getenv("MONGODB_URL")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME")

    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL")

    # RabbitMQ
    RABBITMQ_URL: str = os.getenv("RABBITMQ_URL")

    # Auth
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: str = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

    # OAuth
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET")
    GITHUB_CLIENT_ID: str = os.getenv("GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET: str = os.getenv("GITHUB_CLIENT_SECRET")
    OAUTH_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/callback"

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
