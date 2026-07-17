from datetime import datetime
from typing import List, Optional
from alembic.environment import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:   
    from models.ChatWindow import ChatWindow

class ChatConversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) # Changed default to None for auto-increment
    user_message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    bot_response: str
    # Foreign Key
    chat_window_id: int = Field(foreign_key="chatwindow.id")
    # Relationships
    chat_window: "ChatWindow" = Relationship(back_populates="conversations")