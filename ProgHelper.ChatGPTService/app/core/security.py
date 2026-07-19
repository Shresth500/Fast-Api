from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.params import Depends
from sqlmodel import Session
from dotenv import load_dotenv
from database import get_session

import os
import jwt
import logging


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
security = HTTPBearer()



def verify_jwt(credentials: HTTPAuthorizationCredentials = Depends(security),
               session: Session = Depends(get_session)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "id": payload.get("sub"),
            "name": payload.get("name"),
            "email": payload.get("email")
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


import json
from fastapi import Header, HTTPException

def get_gateway_user(x_authenticated_user: str = Header(...)) -> dict:
    try:
        user = json.loads(x_authenticated_user)
    except (json.JSONDecodeError, TypeError):
        raise HTTPException(status_code=400, detail="Invalid x-authenticated-user header")

    # optional but recommended: validate shape
    if not isinstance(user, dict) or "id" not in user:
        raise HTTPException(status_code=400, detail="Malformed authenticated-user payload")

    return user