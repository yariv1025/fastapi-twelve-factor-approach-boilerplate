from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class TaskCreate(BaseModel):
    title: str
    description: str

@router.post("/", tags=["Tasks"])
async def create_task(task: TaskCreate):
    return {"message": "Task created", "task": task}

@router.get("/{task_id}", tags=["Tasks"])
async def get_task(task_id: int):
    return {"task_id": task_id, "title": "Example Task"}
