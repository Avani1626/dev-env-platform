from pydantic import BaseModel
from typing import List
from datetime import datetime


class Tool(BaseModel):
    name: str
    version: str


class SystemInfo(BaseModel):
    os: str
    os_version: str
    architecture: str


class ScanRequest(BaseModel):
    developer_id: str
    scan_time: datetime
    system: SystemInfo
    tools: List[Tool]
