import json
import os
from datetime import datetime
from typing import Dict, Any

import boto3

from backend.app.storage.base import ScanStorage


class S3Storage(ScanStorage):
    """
    Stores scan data as JSON objects in AWS S3.
    """

    def __init__(self):
        self.bucket_name = os.getenv("S3_BUCKET_NAME")
        self.region = os.getenv("AWS_REGION")

        if not self.bucket_name:
            raise ValueError("S3_BUCKET_NAME environment variable is not set")

        self.s3_client = boto3.client("s3", region_name=self.region)

    def save_scan(self, scan_data: Dict[str, Any]) -> Dict[str, Any]:
        developer_id = scan_data["developer_id"]
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

        s3_key = f"scans/{developer_id}/{timestamp}.json"

        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=s3_key,
            Body=json.dumps(scan_data, indent=2),
            ContentType="application/json"
        )

        return {
            "storage_type": "s3",
            "bucket": self.bucket_name,
            "region": self.region,
            "developer_id": developer_id,
            "timestamp": timestamp,
            "s3_key": s3_key,
        }
