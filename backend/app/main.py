from fastapi import FastAPI

from backend.app.models.scan import ScanRequest
from backend.app.services.scan_service import save_scan




app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/scan")
def ingest_scan(scan: ScanRequest):
    result = save_scan(scan)
    return {
        "message": "Scan received and stored successfully",
        "data": result
    }

