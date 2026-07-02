from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Relationship, SQLModel, Field

from models.ChatConversation import ChatConversation
if TYPE_CHECKING:
    from models.User import User

class ChatWindow(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Foreign Key
    user_id: int = Field(foreign_key="user.id")
    
    # Relationships
    user: "User" = Relationship(back_populates="chat_windows")
    conversations: List["ChatConversation"] = Relationship(back_populates="chat_window")

class ChatWindowCreateRequest(SQLModel):
    title: str

class ChatWindowResponse(SQLModel):
    id: int
    title: str
    created_at: datetime

class ChatWindowListResponse(SQLModel):
    chat_windows: List[ChatWindowResponse]
    status: str
