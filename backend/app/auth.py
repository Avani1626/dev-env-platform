from jose import jwt
from jose.exceptions import JWTError
import requests
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

COGNITO_REGION = "us-east-1"
USER_POOL_ID = "us-east-1_65b7DDtg2"
APP_CLIENT_ID = "4pqs7gkmc0soa0r7t6p7b91611"

ISSUER = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USER_POOL_ID}"
JWKS_URL = f"{ISSUER}/.well-known/jwks.json"

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        # Fetch JWKS fresh each time
        jwks = requests.get(JWKS_URL).json()

        header = jwt.get_unverified_header(token)
        kid = header["kid"]

        key = next(k for k in jwks["keys"] if k["kid"] == kid)

        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            issuer=ISSUER,
        )

        if payload.get("token_use") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")

        if payload.get("client_id") != APP_CLIENT_ID:
            raise HTTPException(status_code=401, detail="Invalid client")

        return payload

    except Exception as e:
        print("JWT ERROR:", str(e))
        raise HTTPException(status_code=401, detail="Invalid or expired token")
