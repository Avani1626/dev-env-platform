import json
import os
from typing import Dict, Any

import boto3

from backend.app.storage.base import ScanStorage


class S3Storage(ScanStorage):
    def __init__(self):
        self.bucket_name = os.getenv("S3_BUCKET_NAME")
        self.client = boto3.client("s3")

    def save_scan(self, developer_id: str, timestamp: str, data: Dict[str, Any]) -> None:
        if not self.bucket_name:
            raise RuntimeError("S3_BUCKET_NAME environment variable not set")

        key = f"scans/{developer_id}/{timestamp}.json"

        self.client.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=json.dumps(data, indent=2),
            ContentType="application/json",
        )
