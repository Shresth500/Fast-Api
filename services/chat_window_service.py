from datetime import datetime, timedelta
from sqlmodel import Session, select

from models.ChatConversation import ChatConversation, ChatConversationDTO, ChatConversationDTO, ChatConversationResponseDTO
from models.ChatWindow import ChatWindow, ChatWindowCreateRequest, ChatWindowListResponse, ChatWindowResponse

def get_chat_windows(
        page_size:int, page_number:int,
        session: Session, user_id: int):
    """
    Retrieves all chat windows for a specific user from the database.

    Args:
        session (Session): The SQLAlchemy session for database interaction.
        user_id (int): The ID of the user whose chat windows are to be retrieved.   
    """
    statement = select(ChatWindow).where(ChatWindow.user_id == user_id).offset((page_number - 1) * page_size).limit(page_size)  # Adjust offset and limit as needed
    response = session.exec(statement).all()
    chat_windows_list = [ChatWindowResponse(id=resp.id, title=resp.title, created_at=resp.created_at) for resp in response]
    return ChatWindowListResponse(status="success",chat_windows=chat_windows_list, page_number=page_number, page_size=page_size)

def create_chat_window(session:Session, user_id:int, chat_window:ChatWindowCreateRequest):
    chat_window_contents = ChatWindow(user_id=user_id, title=chat_window.title)
    session.add(chat_window_contents)
    session.commit()
    session.refresh(chat_window_contents)
    return {
        "status":"success",
        "response":chat_window_contents
    }

def get_chat_history(session:Session, chat_window_id:int, page_size:int=10, page_number:int=1):
    statement = select(ChatConversation).where(ChatConversation.chat_window_id == chat_window_id).order_by(ChatConversation.timestamp.desc()).offset((page_number - 1) * page_size).limit(page_size)
    response = session.exec(statement).all()
    chat_history_list = [ChatConversationDTO(id=resp.id, message=resp.message, chat_window_id=resp.chat_window_id, timestamp=resp.timestamp) for resp in response]
    chat_history_response = ChatConversationResponseDTO(chat_list=chat_history_list, status="success", page_number=page_number, page_size=page_size)
    return chat_history_response