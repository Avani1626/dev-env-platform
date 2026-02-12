from abc import ABC, abstractmethod
from typing import Dict, Any


class ScanStorage(ABC):
    """
    Abstract base class that defines how scan data is stored.
    """

    @abstractmethod
    def save_scan(self, scan_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Persist scan data and return metadata about the stored scan.

        Args:
            scan_data: Validated scan data (JSON-serializable)

        Returns:
            Metadata such as storage location, developer_id, timestamp
        """
        pass
