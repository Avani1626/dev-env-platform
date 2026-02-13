from fastapi import FastAPI, Depends, HTTPException
from .auth import verify_token



from fastapi import FastAPI


from backend.app.models.scan import ScanRequest
from backend.app.services.scan_service import ScanService

app = FastAPI(title="Dev Env Platform")

scan_service = ScanService()

@app.get("/scan/history")
def get_scan_history(user=Depends(verify_token)):
    return {
        "message": "Access granted",
        "user_id": user["sub"],
        "groups": user.get("cognito:groups", [])
    }

def admin_required(user=Depends(verify_token)):
    groups = user.get("cognito:groups", [])
    if "admins" not in groups:
        raise HTTPException(status_code=403, detail="Admins only")
    return user


@app.post("/scan")
def submit_scan(scan: ScanRequest):
    scan_service = ScanService()

    # 🔥 THIS LINE IS THE FIX
    payload = scan.model_dump(mode="json")

    return scan_service.save_scan(payload)

