from fastapi import APIRouter, Query

from models.User import User


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register")
async def register_user(user:User):
    # Implement user registration logic here
    # For example, you can call a service function to handle the registration
    # and return the appropriate response.
    return {
        "status": "success",
        "message": f"User {user.name} registered successfully."
    }