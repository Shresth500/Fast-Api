from datetime import datetime
from typing import List, Optional
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

class ChatConversationDTO(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True) # Changed default to None for auto-increment
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    # Foreign Key
    chat_window_id: int = Field(foreign_key="chatwindow.id")
    # Relationships
    chat_window: "ChatWindow" = Relationship(back_populates="conversations")

class ChatConversationResponseDTO(SQLModel):
    chat_list:List[ChatConversationDTO]
    status:str
    page_number: Optional[int] = Field(default=1)
    page_size: Optional[int] = Field(default=10)