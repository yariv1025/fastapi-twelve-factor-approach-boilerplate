from fastapi import FastAPI
from app.core.config import get_settings
from app.api.v1.routers import api_router

settings = get_settings()

# Initialize FastAPI App
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A FastAPI boilerplate following the Twelve-Factor App methodology",
    version=settings.VERSION,
    docs_url="/docs",
    openapi_url="/openapi.json",
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=settings.PORT, reload=True)
    uvicorn.run(app=settings.ENTRYPOINT, host="0.0.0.0", port=settings.PORT, reload=True)
