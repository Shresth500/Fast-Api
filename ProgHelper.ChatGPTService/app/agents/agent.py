from abc import ABC, abstractmethod

class Agent(ABC):

    @abstractmethod
    def agent_output(self, user_query: str, user_id: int, chat_window_id: int):
        pass