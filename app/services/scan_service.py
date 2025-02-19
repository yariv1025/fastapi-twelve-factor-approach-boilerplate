import subprocess

from app.database.models.scan import Scan, ScanType
from app.database.repositories.scan_repository import ScanRepository


class ScanService:
    def __init__(self, scan_repository: ScanRepository):
        self.scan_repository = scan_repository

    def run_scan(self, target: str, scan_type: ScanType) -> Scan:
        """Run a scan on the specified target."""
        scan = Scan(target=target, scan_type=scan_type, status="running", result="")
        self.scan_repository.create(scan)

        try:
            # Depending on the scan type, we execute the appropriate Trivy command
            if scan_type == ScanType.IMAGE:
                result = self._scan_image(target)
            elif scan_type == ScanType.FILESYSTEM:
                result = self._scan_filesystem(target)
            elif scan_type == ScanType.REPOSITORY:
                result = self._scan_repository(target)
            else:
                raise ValueError("Invalid scan type.")

            scan.status = "completed"
            scan.result = result
            self.scan_repository.update(scan)

        except Exception as e:
            scan.status = "failed"
            scan.result = str(e)
            self.scan_repository.update(scan)

        return scan

    def _scan_image(self, image_name: str) -> str:
        """Run a Trivy scan on a Docker image."""
        command = ["trivy", "image", image_name]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Trivy scan failed: {result.stderr}")
        return result.stdout

    def _scan_filesystem(self, directory_path: str) -> str:
        """Run a Trivy scan on a filesystem."""
        command = ["trivy", "fs", directory_path]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Trivy scan failed: {result.stderr}")
        return result.stdout

    def _scan_repository(self, repo_url: str) -> str:
        """Run a Trivy scan on a Git repository."""
        command = ["trivy", "repo", repo_url]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Trivy scan failed: {result.stderr}")
        return result.stdout
