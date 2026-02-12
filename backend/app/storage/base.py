from abc import ABC, abstractmethod
from typing import Dict, Any


class ScanStorage(ABC):
    @abstractmethod
    def save_scan(self, developer_id: str, timestamp: str, data: Dict[str, Any]) -> None:
        pass
