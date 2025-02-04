from fastapi import APIRouter

router = APIRouter()

@router.get("/", tags=["Health Check"])
async def health_status():
    return {"status": "healthy"}
