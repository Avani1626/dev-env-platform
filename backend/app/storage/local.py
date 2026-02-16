import json
from pathlib import Path
from typing import Dict, Any

from app.storage.base import ScanStorage


class LocalStorage(ScanStorage):
    def __init__(self, base_path: str = "storage/scans"):
        self.base_path = Path(base_path)

    def save_scan(self, developer_id: str, timestamp: str, data: Dict[str, Any]) -> None:
        developer_dir = self.base_path / developer_id
        developer_dir.mkdir(parents=True, exist_ok=True)

        file_path = developer_dir / f"{timestamp}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
