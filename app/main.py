import logging
import uvicorn

from fastapi import FastAPI
from typing import AsyncGenerator, Any
from contextlib import asynccontextmanager

from app.core.config import get_settings
from app.api.v1.routers import api_router
from app.utils.init_db_containers import initialize_databases

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    """
    A lifespan event handler that manage startup and shutdown events.
    :return: AsyncGenerator[None, Any]
    """
    # startup code here
    initialize_databases()

    logging.info("App is starting up...")
    yield

    # shutdown code here
    logging.info("App is shutting down...")


# Initialize FastAPI App
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A FastAPI boilerplate following the Twelve-Factor App methodology",
    version=settings.VERSION,
    docs_url="/docs",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Include API routes
app.include_router(api_router, prefix=f"/api/{settings.VERSION}")

if __name__ == "__main__":
    uvicorn.run(
        app=settings.ENTRYPOINT,
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
