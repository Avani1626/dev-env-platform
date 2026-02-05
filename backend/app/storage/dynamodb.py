import boto3
from boto3.dynamodb.conditions import Key


class DynamoDBStorage:
    """
    Handles scan metadata storage in DynamoDB.
    Stores only scan summary (not full scan data).
    """

    def __init__(self):
        # Connect to DynamoDB
        self.dynamodb = boto3.resource("dynamodb")

        # Connect to the table you created
        self.table = self.dynamodb.Table("scan_metadata")

    def save_scan_summary(self, user_id: str, scan_id: str, summary: dict):
        """
        Save one scan summary into DynamoDB
        """

        item = {
            "user_id": user_id,        # Partition Key
            "scan_id": scan_id,        # Sort Key
            "status": summary["status"],
            "os": summary["os"],
            "timestamp": summary["timestamp"]
        }

        self.table.put_item(Item=item)

    def get_scan_history(self, user_id: str):
        """
        Fetch all scans for a user
        """

        response = self.table.query(
            KeyConditionExpression=Key("user_id").eq(user_id)
        )

        return response["Items"]
