
from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from models import ChatWindow


class ChatConversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) # Changed default to None for auto-increment
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Foreign Key
    chat_window_id: int = Field(foreign_key="chatwindow.id")
    
    # Relationships
    chat_window: "ChatWindow" = Relationship(back_populates="conversations")
    