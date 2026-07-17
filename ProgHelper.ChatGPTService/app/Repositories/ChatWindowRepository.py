from typing import Optional

from sqlmodel import Session, select

from models.ChatConversation import ChatConversation
from models.ChatWindow import ChatWindow
from schemas.ChatWindowDTO import ChatWindowResponseDTO, ChatWindowListResponseDTO, ChatWindowCreateRequestDTO
from schemas.ChatConversationDTO import ChatConversationDTO, ChatConversationResponseDTO


class ChatWindowRepository:
    def __init__(self, session: Session):
        self.session = session

    async def get_chat_windows(self, user_id: int, page_size: int, page_number: int) -> ChatWindowListResponseDTO:
        statement = select(ChatWindow).order_by(ChatWindow.created_at.desc()).where(ChatWindow.user_id == user_id).offset((page_number - 1) * page_size).limit(page_size)  # Adjust offset and limit as needed
        response = self.session.exec(statement).all()
        chat_windows_list = [ChatWindowResponseDTO(id=resp.id, title=resp.title, created_at=resp.created_at) for resp in response]
        return ChatWindowListResponseDTO(status="success",chat_windows=chat_windows_list, page_number=page_number, page_size=page_size)
    
    async def create_chat_window(self, user_id:int, chat_window:ChatWindowCreateRequestDTO):
        chat_window_contents = ChatWindow(user_id=user_id, title=chat_window.title)
        self.session.add(chat_window_contents)
        self.session.commit()
        self.session.refresh(chat_window_contents)
        return {
            "status":"success",
            "response":chat_window_contents
        }

