import json
from pathlib import Path
from typing import Dict, Any

from app.storage.base import ScanStorage


class LocalStorage(ScanStorage):
    def __init__(self, base_path: str = "storage/scans"):
        self.base_path = Path(base_path)

    # ---------------------------------------------------
    # Save full scan locally
    # ---------------------------------------------------
    def save_scan(
        self,
        user_id: str,
        scan_id: str,
        scan_data: Dict[str, Any]
    ) -> None:
        user_dir = self.base_path / user_id
        user_dir.mkdir(parents=True, exist_ok=True)

        file_path = user_dir / f"{scan_id}.json"

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(scan_data, f, indent=2)

    # ---------------------------------------------------
    # Get full scan locally
    # ---------------------------------------------------
    def get_scan(self, user_id: str, scan_id: str):
        file_path = self.base_path / user_id / f"{scan_id}.json"

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
