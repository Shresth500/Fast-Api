import asyncio
import logging

from sqlmodel import Session
from agents.orchestrator_agent import OrchestratorAgent
from Repositories.ChatConversationRepository import ChatConversationRepository
from models.ChatConversation import ChatConversation

logger = logging.getLogger(__name__)

# Instantiate once at app startup (ideally via FastAPI lifespan/DI, not import-time)
_orchestrator = OrchestratorAgent()


class ChatConversationService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = ChatConversationRepository(session)

    async def handle_user_message(
        self, user_message: str, user_id: int, chat_window_id: int
    ) -> ChatConversation:
        # agent_output is sync (LLM/RAG calls) — run off the event loop
        bot_response = await asyncio.to_thread(
            _orchestrator.agent_output,
            user_query=user_message,
            user_id=user_id,
            chat_window_id=chat_window_id,
        )

        conversation = self.repository.create_conversation(
            user_message=user_message,
            bot_response=bot_response,
            chat_window_id=chat_window_id,
        )
        return conversation
    
    async def get_chat_history(self, chat_window_id: int, page_size: int = 10, page_number: int = 1):
        chat_history_response = await asyncio.to_thread(
            self.repository.get_chat_history,
            chat_window_id,
            page_size,
            page_number
        )
        return chat_history_response