from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.storage.dynamodb import DynamoDBStorage

from .auth import verify_token
from app.models.scan import ScanRequest
from app.services.scan_service import ScanService
from app.auth import verify_token


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
    user_id = user["sub"]

    dynamodb = DynamoDBStorage()

    items = dynamodb.get_scan_history(user_id)

    return items



def admin_required(user=Depends(verify_token)):
    groups = user.get("cognito:groups", [])
    if "admins" not in groups:
        raise HTTPException(status_code=403, detail="Admins only")
    return user


@app.post("/scan")
def submit_scan(payload: dict, current_user: dict = Depends(verify_token)):
    # Force developer_id from JWT
    payload["developer_id"] = current_user["sub"]

    return scan_service.save_scan(payload)

@app.get("/scan/{scan_id}")
def get_scan(scan_id: str, current_user: dict = Depends(verify_token)):
    user_id = current_user["sub"]
    return scan_service.get_full_scan(user_id, scan_id)

