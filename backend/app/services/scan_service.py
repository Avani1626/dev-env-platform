import json
from pathlib import Path
from datetime import datetime

from backend.app.models.scan import ScanRequest

# Resolve project root and storage path
BASE_DIR = Path(__file__).resolve().parents[3]
STORAGE_PATH = BASE_DIR / "storage" / "scans"


def save_scan(scan: ScanRequest) -> dict:
    """
    Persist a validated scan request as raw JSON.
    Storage layout is S3-ready:
    storage/scans/<developer_id>/<timestamp>.json
    """

    # Ensure base storage directory exists
    STORAGE_PATH.mkdir(parents=True, exist_ok=True)

    # Create developer-specific directory
    developer_dir = STORAGE_PATH / scan.developer_id
    developer_dir.mkdir(parents=True, exist_ok=True)

    # Generate immutable timestamp-based filename
    filename = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S.json")
    file_path = developer_dir / filename

    # Serialize using Pydantic's JSON-safe dump
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(scan.model_dump(mode="json"), f, indent=2)

    return {
        "status": "stored",
        "developer_id": scan.developer_id,
        "file": filename
    }
