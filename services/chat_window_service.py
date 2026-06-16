from datetime import datetime, timedelta
from sqlmodel import Session, select

from models.ChatWindow import ChatWindow, ChatWindowCreateRequest, ChatWindowListResponse, ChatWindowResponse

def get_chat_windows(session: Session, user_id: int):
    """
    Retrieves all chat windows for a specific user from the database.

    Args:
        session (Session): The SQLAlchemy session for database interaction.
        user_id (int): The ID of the user whose chat windows are to be retrieved.   
    """
    statement = select(ChatWindow).where(ChatWindow.user_id == user_id)
    response = session.exec(statement).all()
    chat_windows_list = [ChatWindowResponse(id=resp.id, title=resp.title, created_at=resp.created_at) for resp in response]
    return ChatWindowListResponse(status="success",chat_windows=chat_windows_list)

def create_chat_window(session:Session, user_id:int, chat_window:ChatWindowCreateRequest):
    chat_window_contents = ChatWindow(user_id=user_id, title=chat_window.title)
    session.add(chat_window_contents)
    session.commit()
    session.refresh(chat_window_contents)
    return {
        "status":"success",
        "response":chat_window_contents
    }