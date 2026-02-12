import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

from backend.app.storage.base import ScanStorage


class LocalStorage(ScanStorage):
    """
    Stores scan data as JSON files on the local filesystem.
    """

    def __init__(self, base_path: Path | None = None):
        if base_path is None:
            project_root = Path(__file__).resolve().parents[3]
            self.base_path = project_root / "storage" / "scans"
        else:
            self.base_path = base_path

    def save_scan(self, scan_data: Dict[str, Any]) -> Dict[str, Any]:
        developer_id = scan_data["developer_id"]

        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

        developer_dir = self.base_path / developer_id
        developer_dir.mkdir(parents=True, exist_ok=True)

        file_path = developer_dir / f"{timestamp}.json"

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(scan_data, f, indent=2)

        return {
            "storage_type": "local",
            "developer_id": developer_id,
            "timestamp": timestamp,
            "path": str(file_path),
        }
