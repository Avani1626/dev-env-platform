from fastapi import FastAPI

from backend.app.models.scan import ScanRequest
from backend.app.services.scan_service import ScanService

app = FastAPI(title="Dev Env Platform")

scan_service = ScanService()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/scan")
def submit_scan(scan: ScanRequest):
    scan_service = ScanService()

    # 🔥 THIS LINE IS THE FIX
    payload = scan.model_dump(mode="json")

    return scan_service.save_scan(payload)

