from datetime import datetime
from typing import Dict, Any, List

from pydantic import BaseModel, Field


class EnvironmentInfo(BaseModel):
    os: str
    os_version: str
    python_version: str


class ToolInfo(BaseModel):
    name: str
    version: str


class ScanRequest(BaseModel):
    developer_id: str = Field(..., description="Unique developer identifier")

    scan_time: datetime = Field(
        default_factory=datetime.utcnow,
        description="Time when scan was generated"
    )

    environment: EnvironmentInfo

    tools: List[ToolInfo]

    metadata: Dict[str, Any] = Field(default_factory=dict)
