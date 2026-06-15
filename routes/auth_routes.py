from fastapi import APIRouter, Query
from sqlmodel import Session
from fastapi.params import Depends

from DbConnections import get_session
from models.User import LoginRequest, User, UserListResponse, UserRequest, UserResponse
from services.auth_user import get_users, login_user, register_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register")
async def register(user:UserRequest, session: Session = Depends(get_session)):
    # Implement user registration logic here
    # For example, you can call a service function to handle the registration
    # and return the appropriate response.
    resposne = await register_user(user,session)
    return resposne

@router.get("/users", response_model=UserListResponse)
def users(session: Session = Depends(get_session)):
    # Implement user retrieval logic here
    response = get_users(session)
    return response

@router.post("/login")
def login(user: LoginRequest, session: Session = Depends(get_session)):
    # Implement user login logic here
    response = login_user(user, session)
    return response
    