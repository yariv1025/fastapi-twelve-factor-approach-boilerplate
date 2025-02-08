from enum import Enum
from pydantic import BaseModel

class ScanType(str, Enum):
    IMAGE = "image"
    FILESYSTEM = "filesystem"
    REPOSITORY = "repository"

class ScanRequest(BaseModel):
    target: str
    scan_type: ScanType

class ScanResponse(BaseModel):
    id: int
    target: str
    scan_type: ScanType
    status: str
    result: str = None
