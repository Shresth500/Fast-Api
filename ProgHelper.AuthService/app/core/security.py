from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status
from typing import Annotated
from fastapi.params import Depends
from sqlmodel import Session
from dotenv import load_dotenv
from database import get_session
from repository import UserRepository
from service import AuthService

import os
import jwt
import logging


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt





oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")  # ✅ no leading slash

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        repo = UserRepository(session)
        auth_service = AuthService(repo)
        logger.info(f"DECODING TOKEN: {token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id = payload.get("sub")
        logger.info(f"FETCHED ID: {id}")

        if id is None:
            raise credentials_exception

        id = int(id)  # ✅ convert to int

    except jwt.InvalidTokenError as e:
        logger.error(f"TOKEN ERROR: {e}")  # ✅ log actual error
        raise credentials_exception

    user = auth_service.get_user_by_id(id, session=session)
    if user is None:
        raise credentials_exception

    return user