from datetime import timedelta

from sqlmodel import Session, select
from pwdlib import PasswordHash
from models.User import LoginRequest, LoginResponse, TokenResponse, User, UserListResponse, UserRequest, UserResponse
from dotenv import load_dotenv
import os

from services.access_token_service import create_access_token

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
    """
    Authenticates a user based on the provided login credentials.

    Args:
        user (LoginRequest): A Pydantic model containing the user's email and password.
    """
    statement = select(User).where(User.email == user.email)
    existing_user = session.exec(statement).first()
    if not existing_user:
        return {"status": "error", "message": "User does not exist."}
    if not verify_password(user.password, existing_user.password):
        return {"status": "error", "message": "Incorrect password."}
    # Here you would typically generate a JWT token or similar for the authenticated user
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": existing_user.id, "name": existing_user.name, "email": existing_user.email}, expires_delta=access_token_expires
    )
    return {
        "status": "success",
        "response": LoginResponse(
            id=existing_user.id,
            name=existing_user.name,
            email=existing_user.email,
            token=TokenResponse(
                access_token=access_token
            )
        )
    }