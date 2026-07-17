from Repositories.ChatWindowRepository import ChatWindowRepository
from schemas.ChatWindowDTO import ChatWindowCreateRequestDTO
class ChatWindowService:
    def __init__(self, chat_window_repository: ChatWindowRepository):
        self.chat_window_repository = chat_window_repository

    async def get_chat_windows(self, user_id: int, page_limit: int, page_number: int):
        chat_windows = await self.chat_window_repository.get_chat_windows(user_id, page_limit, page_number)
        return chat_windows
    
    async def create_chat_window(self, user_id: int, chat_window_data:ChatWindowCreateRequestDTO):
        new_chat_window = await self.chat_window_repository.create_chat_window(user_id, chat_window_data)
        return new_chat_window