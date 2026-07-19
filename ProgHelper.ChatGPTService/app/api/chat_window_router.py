from typing import Annotated

from fastapi import APIRouter, File, Form, Query, UploadFile
from sqlmodel import Session
from fastapi.params import Depends
from schemas.ChatConversationDTO import ChatConversationDTO, ChatConversationResponseDTO
from schemas.ChatWindowDTO import ChatWindowCreateRequestDTO, ChatWindowListResponseDTO, ChatWindowResponseDTO
from database import get_session
from core.security import verify_jwt, get_gateway_user
from Repositories.ChatWindowRepository import ChatWindowRepository
from services.chat_window_service import ChatWindowService
from services.chat_conversation_service import ChatConversationService

import os


router = APIRouter(
    prefix="/chat-window",
    tags=["ChatWindow"]
)

@router.post("/create-new-chat")
async def CreateChatWindow(chat_window: ChatWindowCreateRequestDTO, 
                       session: Session = Depends(get_session),
                    #    current_user = Depends(verify_jwt),
                       gateway_user = Depends(get_gateway_user)
                       ):
    chat_window_repository = ChatWindowRepository(session)
    chat_window_service = ChatWindowService(chat_window_repository)
    new_chat_window = await chat_window_service.create_chat_window(int(gateway_user['id']), chat_window)
    return new_chat_window

@router.get("/chat-windows", response_model=ChatWindowListResponseDTO)
async def get_chat_list( page_limit:int= Query(default=10, description="Number of chat windows to retrieve per page"),
                    page_number:int= Query(default=1, description="Page number to retrieve"),
                    session: Session = Depends(get_session),
                    # current_user = Depends(verify_jwt),
                    gateway_user = Depends(get_gateway_user)
                ):
    chat_window_repository = ChatWindowRepository(session)
    chat_window_service = ChatWindowService(chat_window_repository)
    chat_windows = await chat_window_service.get_chat_windows(int(gateway_user['id']),page_limit,page_number)
    return chat_windows


@router.get("/chat-windows/{chat_window_id}", response_model=ChatConversationResponseDTO)
async def get_chat_window(
    chat_window_id: int,
    page_number: int = Query(default=1),
    page_limit: int = Query(default=10),
    session: Session = Depends(get_session),
    # current_user = Depends(verify_jwt),
    gateway_user = Depends(get_gateway_user)
):
    service = ChatConversationService(session)
    return await service.get_chat_history(
        chat_window_id=chat_window_id,
        page_size=page_limit,
        page_number=page_number,
    )



@router.post("/chat-windows/{chat_window_id}", response_model=ChatConversationDTO)
async def post_chat_question(chat_window_id:int, 
                       user_query: Annotated[str, Form(...)],
                       file: Annotated[UploadFile | None, File(description="Upload a file")] = None,
                       session:Session = Depends(get_session),
                       # current_user = Depends(verify_jwt),
                       gateway_user = Depends(get_gateway_user)
                       ):
    print("Received user query:", user_query)
    service = ChatConversationService(session)
    conversation = await service.handle_user_message(
        user_message=user_query,
        user_id=int(gateway_user['id']),
        chat_window_id=chat_window_id,
    )
    response = ChatConversationDTO(
        id=conversation.id,
        user_message=conversation.user_message,
        bot_response=conversation.bot_response,
        chat_window_id=conversation.chat_window_id,
        timestamp=conversation.timestamp
    )
    print("Response to be returned:", response)
    return response
