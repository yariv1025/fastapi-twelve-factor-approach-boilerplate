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

    # Postgres
    POSTGRES_URL: str = os.getenv("POSTGRES_URL")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_DOMAIN: str = os.getenv("POSTGRES_DOMAIN")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB_NAME: str = os.getenv("POSTGRES_DB_NAME")

    # Mongo DB
    MONGO_USER: str = os.getenv("MONGO_USER")
    MONGO_PASSWORD: str = os.getenv("MONGO_PASSWORD")
    MONGO_ADMIN_USER: str = os.getenv("MONGO_ADMIN_USER")
    MONGO_ADMIN_PASSWORD: str = os.getenv("MONGO_ADMIN_PASSWORD")
    MONGO_DOMAIN: str = os.getenv("MONGO_DOMAIN")
    MONGO_PORT: str = os.getenv("MONGO_PORT")
    MONGODB_URL: str = os.getenv("MONGODB_URL")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME")

    # Redis
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD")
    REDIS_DOMAIN: str = os.getenv("REDIS_DOMAIN")
    REDIS_PROT: str = os.getenv("REDIS_PROT")
    REDIS_URL: str = os.getenv("REDIS_URL")

    # RabbitMQ
    RABBITMQ_USERNAME: str = os.getenv("RABBITMQ_USERNAME")
    RABBITMQ_PASSWORD: str = os.getenv("RABBITMQ_PASSWORD")
    RABBITMQ_DOMAIN: str = os.getenv("RABBITMQ_DOMAIN")
    RABBITMQ_PORT: str = os.getenv("RABBITMQ_PORT")
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
