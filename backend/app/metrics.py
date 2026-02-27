from fastapi import APIRouter
import boto3

router = APIRouter()

client = boto3.client("dynamodb", region_name="us-east-1")


# ---------------------------------------
# SUMMARY ENDPOINT
# ---------------------------------------
@router.get("/metrics/summary")
def get_metrics_summary():
    response = client.scan(TableName="scan_metadata")
    items = response.get("Items", [])

    total_scans = len(items)
    processed = 0
    failed = 0
    total_score = 0

    for item in items:
        status = item.get("status", {}).get("S")
        score = item.get("score", {}).get("N")

        if status == "COMPLETED":
            processed += 1
            if score:
                total_score += int(score)

        elif status == "FAILED":
            failed += 1

    average_score = total_score // processed if processed > 0 else 0

    return {
        "total_scans": total_scans,
        "processed": processed,
        "failed": failed,
        "average_score": average_score
    }


# ---------------------------------------
# TRENDS ENDPOINT
# ---------------------------------------
@router.get("/metrics/trends")
def get_metrics_trends():
    response = client.scan(TableName="scan_metadata")
    items = response.get("Items", [])

    daily_scans = {}
    daily_failures = {}

    for item in items:
        status = item.get("status", {}).get("S")
        timestamp = item.get("timestamp", {}).get("S")

        if not timestamp or len(timestamp) < 8 or not timestamp.isdigit():
            continue

        raw_date = timestamp[:8]
        formatted_date = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:8]}"

        if formatted_date not in daily_scans:
            daily_scans[formatted_date] = 0
            daily_failures[formatted_date] = 0

        daily_scans[formatted_date] += 1

        if status == "FAILED":
            daily_failures[formatted_date] += 1

    return {
        "daily_scans": daily_scans,
        "daily_failures": daily_failures
    }