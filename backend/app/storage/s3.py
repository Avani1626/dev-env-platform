import boto3
import json


class S3Storage:
    def __init__(self):
        self.s3 = boto3.client("s3", region_name="us-east-1")
        self.bucket_name = "dev-env-platform-scans-avani"

    # ---------------------------------------------------
    # Save full scan JSON to S3
    # ---------------------------------------------------
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
            print("🚨 S3 ERROR (SAVE):", str(e))
            raise

    # ---------------------------------------------------
    # Fetch full scan JSON from S3
    # ---------------------------------------------------
    def get_scan(self, user_id, scan_id):
        try:
            key = f"{user_id}/{scan_id}.json"

            response = self.s3.get_object(
                Bucket=self.bucket_name,
                Key=key
            )

            return json.loads(response["Body"].read())

        except Exception as e:
            print("🚨 S3 ERROR (GET):", str(e))
            raise
