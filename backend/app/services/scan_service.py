from datetime import datetime
import os

from backend.app.storage.local import LocalStorage
from backend.app.storage.s3 import S3Storage


class ScanService:
    def __init__(self):
        backend = os.getenv("STORAGE_BACKEND", "local")
        self.storage = S3Storage() if backend == "s3" else LocalStorage()

    def save_scan(self, scan_data: dict):
        developer_id = scan_data["developer_id"]

        timestamp = datetime.utcnow().isoformat()

        # Optional metadata
        scan_data["timestamp"] = timestamp

        self.storage.save_scan(
            developer_id=developer_id,
            timestamp=timestamp,
            data=scan_data,
        )

        return {"message": "Scan saved successfully"}
