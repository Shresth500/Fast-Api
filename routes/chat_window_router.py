import os
from typing import Annotated, Optional

from fastapi import APIRouter, File, Form, Query, UploadFile
from sqlmodel import Session
from fastapi.params import Depends

from DbConnections import get_session
from models.ChatBot import ChatBotRequest, ChatBotResponse
from models.ChatWindow import ChatWindowCreateRequest, ChatWindowListResponse
from routes.extractor_context import extractor_context
from services.access_token_service import get_current_user
from services.chat_bot_service import chat_app
from services.chat_window_service import create_chat_window, get_chat_windows
from agents.orchestrator_agent import OrchestratorAgent

router = APIRouter(
    prefix="/chat-window",
    tags=["ChatWindow"]
)


_orchestrator = OrchestratorAgent()
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
async def post_chat_question(chat_window_id:int, 
                       user_query: Annotated[str, Form(...)],
                       file: Annotated[UploadFile | None, File(description="Upload a file")] = None,
                       session:Session = Depends(get_session),
                       current_user = Depends(get_current_user),
                       ):
    # response = chat_app(user_query=user_input.user_query,user_id=current_user.id,chat_window_id=chat_window_id)
    # return response
    content=""
    if file is not None:
        filename = file.filename
        _, extension = os.path.splitext(filename)
        extension = extension.lower().lstrip(".")
        content_extractor = extractor_context.get(extension)()
        file_path = content_extractor.save_content_from_pdf(
            user_id=current_user.id,
            chat_window_id=chat_window_id,
            file=file
        )
        content = content_extractor.extract_content_from_pdf(
            file_path=file_path
        )
    if content != "":
        user_query = content + "\n " + user_query

    response=_orchestrator.agent_output(
        user_query=user_query,
        chat_window_id=chat_window_id,
        user_id=current_user.id
    )
    return ChatBotResponse(
        status="success",
        resposne=response.content
    )


