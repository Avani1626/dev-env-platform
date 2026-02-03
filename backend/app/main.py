from fastapi import FastAPI
from app.models.scan import ScanRequest

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/scan")
def receive_scan(scan: ScanRequest):
    return {
        "message": "Scan received successfully",
        "developer_id": scan.developer_id
    }

