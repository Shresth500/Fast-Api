from fastapi import APIRouter, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from fastapi.params import Depends
from schemas import UserRequestDTO, UserResponseDTO, UserListResponseDTO, TokenResponseDTO, LoginResponseDTO, LoginRequestDTO
from database import get_session 
from service import AuthService
from repository import UserRepository


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register")
async def register(user:UserRequestDTO, session: Session = Depends(get_session)):
    # Implement user registration logic here
    # For example, you can call a service function to handle the registration
    # and return the appropriate response.
    repo = UserRepository(session)
    auth_service = AuthService(repo)
    response = await auth_service.register_user(user)
    return response

@router.get("/users", response_model=UserListResponseDTO)
def users(session: Session = Depends(get_session)):
    # Implement user retrieval logic here
    repo = UserRepository(session)
    auth_service = AuthService(repo)
    response = auth_service.get_users(session)
    return response

@router.post("/login")
async def login(
        user: LoginRequestDTO, 
        session: Session = Depends(get_session)):
    repo = UserRepository(session)
    auth_service = AuthService(repo)
    response = await auth_service.login_user(user)
    return response
    
@router.get("/me", response_model=UserResponseDTO)
def get_current_user(session: Session = Depends(get_session)):
    repo = UserRepository(session)
    auth_service = AuthService(repo)
    