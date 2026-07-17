from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class ChatConversationDTO(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True) # Changed default to None for auto-increment
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    chat_window_id: int = Field(foreign_key="chatwindow.id")

class ChatConversationResponseDTO(SQLModel):
    chat_list:List[ChatConversationDTO]
    status:str
    page_number: Optional[int] = Field(default=1)
    page_size: Optional[int] = Field(default=10)