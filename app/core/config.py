import os

from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Twelve-Factor Boilerplate"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development" # TODO: move to .env
    DEBUG: bool = True # TODO: move to .env
    ENTRYPOINT: str = "main:app"

    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database settings
    DATABASE_URL: str = "postgresql+asyncpg://postgres:mysecretpassword@localhost:5432/mydatabase" # TODO: move to .env
    MONGODB_URL: str = "mongodb://root:example@localhost:27017/" # TODO: move to .env
    MONGO_DB_NAME: str ="test"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0" # TODO: move to .env + add redis

    # RabbitMQ
    RABBITMQ_URL: str = "amqp://user:password@localhost:5672/" # TODO: move to .env

    #Auth
    SECRET_KEY: str = "40fe47dd7563234bf9a66817fef6d45847962074899cf35a8e0412727d9e982a" # TODO: move to .env
    ALGORITHM: str = "HS256" # TODO: move to .env
    ACCESS_TOKEN_EXPIRE_MINUTES: str = "30" # TODO: move to .env

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
