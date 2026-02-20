import boto3
import json


class S3Storage:
    def __init__(self):
        self.s3 = boto3.client("s3", region_name="us-east-1")
        self.bucket_name = "dev-env-platform-scans-avani"

    def save_scan(self, user_id, scan_id, scan_data):
        try:
            key = f"{user_id}/{scan_id}.json"

            print("---- S3 DEBUG START ----")
            print("Bucket:", self.bucket_name)
            print("Key:", key)

            self.s3.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=json.dumps(scan_data, default=str),
                ContentType="application/json"
            )

            print("S3 upload successful")
            print("---- S3 DEBUG END ----")

        except Exception as e:
            print("🚨 S3 ERROR:", str(e))
            raise
