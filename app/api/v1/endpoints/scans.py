from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencies import get_scan_service
from app.schemas.scan import ScanRequest, ScanResponse
from app.services.scan_service import ScanService

router = APIRouter()

@router.post("/", response_model=ScanResponse)
async def create_scan(scan_request: ScanRequest, scan_service: ScanService = Depends(get_scan_service)):
    """
    Create a scan task and run the Trivy scan.
    """
    try:
        scan = scan_service.run_scan(scan_request.target, scan_request.scan_type)
        return ScanResponse(
            id=scan.id,
            target=scan.target,
            scan_type=scan.scan_type,
            status=scan.status,
            result=scan.result
        )
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))
