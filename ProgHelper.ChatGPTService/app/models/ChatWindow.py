from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Relationship, SQLModel, Field
if TYPE_CHECKING:
    from models.ChatConversation import ChatConversation

class ChatWindow(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Foreign Key
    user_id: int
    
    # Relationships
    conversations: List["ChatConversation"] = Relationship(back_populates="chat_window")
