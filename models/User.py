from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Relationship, SQLModel, Field
from pydantic import EmailStr, field_validator, model_validator
import re
if TYPE_CHECKING:
    from models.ChatWindow import ChatWindow


# Input schema with validation
class UserRequest(SQLModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr  # validates email format automatically
    password: str = Field(..., min_length=8)
    confirm_password: str

    @field_validator("name")
    @classmethod
    def name_must_be_alpha(cls, v):
        if not re.match(r"^[a-zA-Z\s]+$", v):
            raise ValueError("Name must contain only letters and spaces.")
        return v.strip()

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character.")
        return v

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match.")
        return self


# DB model
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    password: str  # stores hashed password only
    chat_windows: List["ChatWindow"] = Relationship(back_populates="user")

class UserResponse(SQLModel):
    id: int
    name: str
    email: str

class UserListResponse(SQLModel):
    status: str
    users: List[UserResponse]

class TokenResponse(SQLModel):
    access_token: str

class LoginResponse(UserResponse):
    token: TokenResponse

class LoginRequest(SQLModel):
    email: EmailStr
    password: str