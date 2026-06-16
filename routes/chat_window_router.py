from fastapi import APIRouter, Query
from sqlmodel import Session
from fastapi.params import Depends

from DbConnections import get_session
from models.ChatWindow import ChatWindowCreateRequest, ChatWindowListResponse
from services.access_token_service import get_current_user
from services.chat_window_service import create_chat_window, get_chat_windows

router = APIRouter(
    prefix="/chat-window",
    tags=["ChatWindow"]
)

@router.post("/create-new-chat")
def CreateChatWindow(chat_window: ChatWindowCreateRequest, 
                       session: Session = Depends(get_session),
                       current_user = Depends(get_current_user)):
    response = create_chat_window(session,current_user.id,chat_window)
    return response

@router.get("/chat-windows", response_model=ChatWindowListResponse)
def get_chat_list(session: Session = Depends(get_session),
                     current_user = Depends(get_current_user)):
    
    response = get_chat_windows(session=session,user_id=current_user.id)
    return response

@router.get("/chat-windows/{chat_window_id}")
def get_chat_window(chat_window_id: int, session: Session = Depends(get_session),
                    current_user = Depends(get_current_user)):
    pass


@router.post("/chat-windows/{chat_window_id}")
def post_chat_question(chat_window_id:int, 
                       session:Session = Depends(get_session),
                       current_user = Depends(get_current_user)):
    pass