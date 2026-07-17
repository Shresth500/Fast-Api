from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, SQLModel


class ChatWindowCreateRequestDTO(SQLModel):
    title: str

class ChatWindowResponseDTO(SQLModel):
    id: int
    title: str
    created_at: datetime

class ChatWindowListResponseDTO(SQLModel):
    chat_windows: List[ChatWindowResponseDTO]
    status: str
    page_number: Optional[int] = Field(default=1)
    page_size: Optional[int] = Field(default=10)
