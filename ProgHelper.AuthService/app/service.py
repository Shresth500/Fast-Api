from datetime import timedelta
from http.client import HTTPException

from sqlmodel import Session, select
from pwdlib import PasswordHash
from schemas import UserRequestDTO, UserResponseDTO, UserListResponseDTO, LoginRequestDTO
from models import User
import os

from core.security import create_access_token

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

password_hash = PasswordHash.recommended()


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)

from repository import UserRepository
class AuthService:
    def __init__(self,repo:UserRepository):
        self.repo = repo
    
    async def register_user(self, user_data: UserRequestDTO):
        existing_user = self.repo.get_by_email(user_data.email)
        if existing_user:
            return {"status": "error", "message": "User already exists."}
        
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            password=get_password_hash(user_data.password) 
        )
        self.repo.create(new_user)
        return {"status": "success", "message": f"User {user_data.name} registered successfully."}
    
    async def login_user(self, user: LoginRequestDTO):
        existing_user = self.repo.get_by_email(user.email)
        if not existing_user:
            raise HTTPException(status_code=404, detail="User does not exist.")
        
        if not verify_password(user.password, existing_user.password):
            raise HTTPException(status_code=401, detail="Incorrect password.")
        
        access_token = create_access_token(
            data={
                "sub": str(existing_user.id),
                "name": existing_user.name,
                "email": existing_user.email
            },
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": existing_user.id,
                "name": existing_user.name,
                "email": existing_user.email
            }
        }

    async def get_users(self, session: Session):
        users = self.repo.get_all()
        return UserListResponseDTO(
            status="success",
            users=[UserResponseDTO(id=user.id, name=user.name, email=user.email) for user in users]
        )
    
    async def get_user_by_id(self, user_id: int, session: Session):
        user = self.repo.get_by_id(user_id)
        if user:
            return UserResponseDTO(id=user.id, name=user.name, email=user.email)
        return None
