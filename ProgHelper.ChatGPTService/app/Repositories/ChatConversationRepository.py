from sqlmodel import Session, select
from sqlmodel import Session
from models.ChatConversation import ChatConversation
from schemas.ChatConversationDTO import ChatConversationDTO, ChatConversationResponseDTO


class ChatConversationRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_conversation(
        self, user_message: str, bot_response: str, chat_window_id: int
    ) -> ChatConversation:
        conversation = ChatConversation(
            user_message=user_message,
            bot_response=bot_response,
            chat_window_id=chat_window_id,
        )
        try:
            self.session.add(conversation)
            self.session.commit()
            self.session.refresh(conversation)
        except Exception:
            self.session.rollback()
            raise
        return conversation
    
    def get_chat_history(self, chat_window_id: int, page_size: int = 10, page_number: int = 1):
        statement = select(ChatConversation).where(ChatConversation.chat_window_id == chat_window_id).order_by(ChatConversation.timestamp.desc()).offset((page_number - 1) * page_size).limit(page_size)
        response = self.session.exec(statement).all()
        print(f"Retrieved {len(response)} chat history records for chat_window_id {chat_window_id}, page {page_number}, page_size {page_size}")
        print(f"Chat history records: {response}")
        chat_history_list = [ChatConversationDTO(id=resp.id, user_message=resp.user_message, bot_response=resp.bot_response, chat_window_id=resp.chat_window_id, timestamp=resp.timestamp) for resp in response]
        chat_history_response = ChatConversationResponseDTO(chat_list=chat_history_list, status="success", page_number=page_number, page_size=page_size)
        print(f"Chat history response: {chat_history_response}")
        return chat_history_response