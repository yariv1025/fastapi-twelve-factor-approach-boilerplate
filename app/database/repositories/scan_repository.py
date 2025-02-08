from app.database.models.scan import Scan
from app.database.base import BaseRepository


class ScanRepository:
    def __init__(self, db_repo: BaseRepository):
        self.db_repo = db_repo

    def create(self, scan: Scan):
        return self.db_repo.create(scan)

    def get_by_id(self, scan_id: int):
        return self.db_repo.get_by_id(scan_id)

    def update(self, scan: Scan):
        return self.db_repo.update(scan)
