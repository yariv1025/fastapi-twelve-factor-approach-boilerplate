from app.services.scan_service import ScanService
from app.database.repositories.scan_repository import ScanRepository
from unittest.mock import MagicMock
import pytest


@pytest.fixture
def mock_scan_repo():
    mock_repo = MagicMock(spec=ScanRepository)
    return mock_repo


def test_run_scan(mock_scan_repo):
    scan_service = ScanService(mock_scan_repo)

    # Test scanning an image
    mock_scan_repo.create.return_value = None  # Simulate saving to the DB
    scan = scan_service.run_scan("ubuntu:latest", "image")

    assert scan.status == "completed"
    assert "vulnerabilities found" in scan.result  # Example assertion, adjust as needed

    # Check if the repository methods were called
    mock_scan_repo.create.assert_called_once()
    mock_scan_repo.update.assert_called_once()
