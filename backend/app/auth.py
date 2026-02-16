from jose import jwt, jwk
from jose.utils import base64url_decode
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests


# ==============================
# Cognito Configuration
# ==============================

COGNITO_REGION = "us-east-1"
USER_POOL_ID = "us-east-1_65b7DDtg2"
APP_CLIENT_ID = "3ag53fg3iotu032h6tohf5c5pt"


ISSUER = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USER_POOL_ID}"
JWKS_URL = f"{ISSUER}/.well-known/jwks.json"

security = HTTPBearer()


# ==============================
# Token Verification Function
# ==============================

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        # 1️⃣ Fetch JWKS (public keys from Cognito)
        jwks = requests.get(JWKS_URL).json()

        # 2️⃣ Get token header
        header = jwt.get_unverified_header(token)
        kid = header["kid"]

        # 3️⃣ Find matching public key
        key = next(k for k in jwks["keys"] if k["kid"] == kid)

        # 4️⃣ Construct public key
        public_key = jwk.construct(key)

        # 5️⃣ Verify signature manually
        message, encoded_signature = token.rsplit(".", 1)
        decoded_signature = base64url_decode(encoded_signature.encode())

        if not public_key.verify(message.encode(), decoded_signature):
            raise HTTPException(status_code=401, detail="Invalid signature")

        # 6️⃣ Get claims (payload)
        payload = jwt.get_unverified_claims(token)

        # 7️⃣ Validate issuer
        if payload.get("iss") != ISSUER:
            raise HTTPException(status_code=401, detail="Invalid issuer")

        # 8️⃣ Ensure this is an access token
        if payload.get("token_use") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")

        # 9️⃣ Validate client ID
        if payload.get("client_id") != APP_CLIENT_ID:
            raise HTTPException(status_code=401, detail="Invalid client")

        return payload

    except Exception as e:
        print("JWT ERROR:", str(e))
        raise HTTPException(status_code=401, detail="Invalid or expired token")
