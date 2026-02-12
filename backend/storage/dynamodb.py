import boto3
from boto3.dynamodb.conditions import Key


class DynamoDBStorage:
    """
    Handles scan metadata storage in DynamoDB.
    This is ONLY for scan summaries, not full scan data.
    """

    def __init__(self):
        # Create a DynamoDB resource (high-level AWS connection)
        self.dynamodb = boto3.resource("dynamodb")

        # Connect to the scan_metadata table
        self.table = self.dynamodb.Table("scan_metadata")

    def save_scan_summary(self, user_id: str, scan_id: str, summary: dict):
        """
        Save one scan summary into DynamoDB.
        """

        item = {
            "user_id": user_id,       # Partition Key
            "scan_id": scan_id,       # Sort Key
            "status": summary["status"],
            "os": summary["os"],
            "timestamp": summary["timestamp"]
        }

        # Write item to DynamoDB
        self.table.put_item(Item=item)

    def get_scan_history(self, user_id: str):
        """
        Fetch all scans for a given user.
        """

        response = self.table.query(
            KeyConditionExpression=Key("user_id").eq(user_id)
        )

        # Return only the actual data items
        return response["Items"]
