from datetime import timedelta
from http.client import HTTPException

from sqlmodel import Session, select
from pwdlib import PasswordHash
from models.User import LoginRequest, LoginResponse, TokenResponse, User, UserListResponse, UserRequest, UserResponse
import os

from services.jwt_service import create_access_token

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

password_hash = PasswordHash.recommended()


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)

async def register_user(
        user_data: UserRequest,
        session: Session):
    """
    Registers a new user with the provided user data.

    Args:
        user_data (dict): A dictionary containing user registration data.

    Returns:
        dict: A dictionary containing the status and result of the registration process.
    """
    statement = select(User).where(User.email == user_data.email)
    existing_user = session.exec(statement).first()
    if existing_user:
        return {"status": "error", "message": "User already exists."}
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=get_password_hash(user_data.password) 
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"status": "success", "message": f"User {user_data.name} registered successfully."}


def get_users(session: Session):
    """
    Retrieves all users from the database.

    Args:
        session (Session): The SQLAlchemy session for database interaction.

    Returns:
        List[User]: A list of all users in the database.
    """
    statement = select(User)
    return UserListResponse(
        status="success",
        users=[UserResponse(id=user.id, name=user.name, email=user.email) for user in session.exec(statement).all()]
    )


def login_user(user: LoginRequest, session: Session):
    statement = select(User).where(User.email == user.email)
    existing_user = session.exec(statement).first()

    if not existing_user:
        raise HTTPException(status_code=404, detail="User does not exist.")   # ✅ use HTTPException

    if not verify_password(user.password, existing_user.password):
        raise HTTPException(status_code=401, detail="Incorrect password.")    # ✅ use HTTPException

    access_token = create_access_token(
        data={
            "sub": str(existing_user.id),
            "name": existing_user.name,
            "email": existing_user.email
        },
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token,   # ✅ top level
        "token_type": "bearer",         # ✅ required by OAuth2 spec
        "user": {
            "id": existing_user.id,
            "name": existing_user.name,
            "email": existing_user.email
        }
    }
def get_user_by_id(user_id: int, session: Session):
    """
    Retrieves a user from the database based on their ID.

    Args:
        user_id (int): The ID of the user to retrieve.
    Returns:
        UserResponse: A Pydantic model containing the user's information, or None if the user does not exist.
    """
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    if user:
        return UserResponse(id=user.id, name=user.name, email=user.email)
    return None