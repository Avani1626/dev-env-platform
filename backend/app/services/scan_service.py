from datetime import datetime
import os
import boto3
import json

from app.storage.local import LocalStorage
from app.storage.s3 import S3Storage
from app.storage.dynamodb import DynamoDBStorage


# ✅ Create EventBridge client (outside class)
eventbridge = boto3.client("events", region_name="us-east-1")


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

        # ✅ Safe timestamp for filenames (also used as scan_id)
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")

        scan_data["timestamp"] = timestamp

        scan_id = timestamp

        # ---------------------------------------------
        # 1️⃣ Save full scan JSON (S3 or local)
        # ---------------------------------------------
        self.storage.save_scan(
            user_id=developer_id,
            scan_id=scan_id,
            scan_data=scan_data,
        )

        environment = scan_data.get("environment", {})

        summary = {
            "status": "PENDING",
            "os": environment.get("os", "UNKNOWN"),
            "timestamp": timestamp,
        }

        # ---------------------------------------------
        # 2️⃣ Save metadata to DynamoDB
        # ---------------------------------------------
        self.dynamodb.save_scan_summary(
            user_id=developer_id,
            scan_id=scan_id,
            summary=summary,
        )

        # ---------------------------------------------
        # 3️⃣ Publish Event to EventBridge
        # ---------------------------------------------
        try:
            response = eventbridge.put_events(
                Entries=[
                    {
                        "Source": "dev.env.platform",
                        "DetailType": "ScanUploaded",
                        "Detail": json.dumps({
                            "scan_id": scan_id,
                            "user_id": developer_id,
                            "timestamp": timestamp
                        }),
                        "EventBusName": "default"
                    }
                ]
            )

            print("EventBridge response:", response)

        except Exception as e:
            print("Error publishing event to EventBridge:", str(e))

        # ---------------------------------------------
        return {"message": "Scan saved successfully", "scan_id": scan_id}

    # ---------------------------------------------------
    # Get Full Scan
    # ---------------------------------------------------
    def get_full_scan(self, user_id, scan_id):
        return self.storage.get_scan(user_id, scan_id)