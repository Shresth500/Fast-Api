from fastapi import APIRouter, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from fastapi.params import Depends
from schemas import UserRequestDTO, UserResponseDTO, UserListResponseDTO, TokenResponseDTO, LoginResponseDTO, LoginRequestDTO
from database import get_session 
from service import AuthService
from repository import UserRepository
from core.security import verify_jwt


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
async def users(session: Session = Depends(get_session),
                page: int = Query(1, ge=1),
                page_size: int = Query(10, ge=1, le=100)):
    # Implement user retrieval logic here
    repo = UserRepository(session)
    auth_service = AuthService(repo)
    response = await auth_service.get_users(session, page, page_size)
    print("Users response:", response)
    return response

@router.post("/login")
async def login(
        user: LoginRequestDTO, 
        session: Session = Depends(get_session)):
    repo = UserRepository(session)
    auth_service = AuthService(repo)
    response = await auth_service.login_user(user)
    return response
    
@router.get("/me")
def get_current_user(session: Session = Depends(get_session), user = Depends(verify_jwt)):
    print("Current user:", user)
    return UserResponseDTO(**user)  # Return the user object, which contains the user info
    