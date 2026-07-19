import os
import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


load_dotenv()  # Load environment variables from .env file
# ---------------------------------------------------------------------------
# 2. Auth — simple API key check (swap for JWT/OAuth in production)
# ---------------------------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")  # Default to HS256 if not set
bearer_scheme = HTTPBearer()
 
 
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> dict:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
 
    id,name,email = int(payload.get("sub")), payload.get("name"), payload.get("email")
    if not id:
        raise HTTPException(status_code=401, detail="Token missing subject claim")
 
    return {
        "id": id,
        "name": name,
        "email": email
    }