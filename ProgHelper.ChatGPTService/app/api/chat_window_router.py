from fastapi import APIRouter, Query
from sqlmodel import Session
from fastapi.params import Depends
from schemas.ChatWindowDTO import ChatWindowCreateRequestDTO, ChatWindowListResponseDTO, ChatWindowResponseDTO
from database import get_session
from core.security import verify_jwt
from Repositories.ChatWindowRepository import ChatWindowRepository
from services.chat_window_service import ChatWindowService


router = APIRouter(
    prefix="/chat-window",
    tags=["ChatWindow"]
)

@router.post("/create-new-chat")
async def CreateChatWindow(chat_window: ChatWindowCreateRequestDTO, 
                       session: Session = Depends(get_session),
                       current_user = Depends(verify_jwt)):
    chat_window_repository = ChatWindowRepository(session)
    chat_window_service = ChatWindowService(chat_window_repository)
    new_chat_window = await chat_window_service.create_chat_window(current_user['id'], chat_window)
    return new_chat_window

@router.get("/chat-windows", response_model=ChatWindowListResponseDTO)
async def get_chat_list( page_limit:int= Query(default=10, description="Number of chat windows to retrieve per page"),
                    page_number:int= Query(default=1, description="Page number to retrieve"),
                    session: Session = Depends(get_session),
                    current_user = Depends(verify_jwt),
                ):
    chat_window_repository = ChatWindowRepository(session)
    chat_window_service = ChatWindowService(chat_window_repository)
    chat_windows = await chat_window_service.get_chat_windows(int(current_user['id']),page_limit,page_number)
    return chat_windows

