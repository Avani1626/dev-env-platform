from datetime import datetime
import os

from app.storage.local import LocalStorage
from app.storage.s3 import S3Storage
from app.storage.dynamodb import DynamoDBStorage


class ScanService:
    def __init__(self):
        backend = os.getenv("STORAGE_BACKEND", "local")

        self.storage = S3Storage() if backend == "s3" else LocalStorage()
        self.dynamodb = DynamoDBStorage()

    # ---------------------------------------------------
    # Save Scan
    # ---------------------------------------------------
    def save_scan(self, scan_data: dict):
        developer_id = scan_data["developer_id"]

        # ✅ Safe timestamp for filenames
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")

        scan_data["timestamp"] = timestamp

        # Save full scan JSON (S3 or local)
        self.storage.save_scan(
            user_id=developer_id,
            scan_id=timestamp,
            scan_data=scan_data,
        )

        environment = scan_data.get("environment", {})

        scan_id = timestamp

        summary = {
            "status": "COMPLETED",
            "os": environment.get("os", "UNKNOWN"),
            "timestamp": timestamp,
        }

        # Save metadata to DynamoDB
        self.dynamodb.save_scan_summary(
            user_id=developer_id,
            scan_id=scan_id,
            summary=summary,
        )

        return {"message": "Scan saved successfully"}

    # ---------------------------------------------------
    # Get Full Scan (NEW)
    # ---------------------------------------------------
    def get_full_scan(self, user_id, scan_id):
        return self.storage.get_scan(user_id, scan_id)
