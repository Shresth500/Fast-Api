from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status
from typing import Annotated
from fastapi.params import Depends
from sqlmodel import Session
from dotenv import load_dotenv
from DbConnections import get_session
from services.auth_user import get_user_by_id

import os
import jwt
import logging

load_dotenv()  # ✅ load env variables first

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

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

    user = get_user_by_id(id, session=session)
    if user is None:
        raise credentials_exception

    return user