from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .auth import verify_token
from app.models.scan import ScanRequest
from app.services.scan_service import ScanService


app = FastAPI(title="Dev Env Platform")

# ✅ CORS CONFIGURATION (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scan_service = ScanService()


@app.get("/scan/history")
def get_scan_history(user=Depends(verify_token)):
    return [
        {
            "scan_id": "scan001",
            "timestamp": "2026-02-19",
            "status": "PASS",
            "os": "Windows"
        },
        {
            "scan_id": "scan002",
            "timestamp": "2026-02-18",
            "status": "FAIL",
            "os": "MacOS"
        }
    ]


def admin_required(user=Depends(verify_token)):
    groups = user.get("cognito:groups", [])
    if "admins" not in groups:
        raise HTTPException(status_code=403, detail="Admins only")
    return user


@app.post("/scan")
def submit_scan(scan: ScanRequest):
    payload = scan.model_dump(mode="json")
    return scan_service.save_scan(payload)
