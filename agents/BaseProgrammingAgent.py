import logging
import os
from agent import Agent
from BaseAgent import BaseAgent
from load_vector_embedding import load_vector_store

class BaseProgrammingAgent(Agent):
    logger = logging.getLogger(__name__)

    def __init__(self, document_env_key: str):
        self.base_agent = BaseAgent()
        self.document_name = os.getenv(document_env_key)
        self.vector_db = load_vector_store(self.document_name)

    def agent_output(self, user_query: str, user_id: int, chat_window_id: int):
        return self.base_agent.output(
            user_query=user_query,
            user_id=user_id,
            chat_window_id=chat_window_id,
            vector_db=self.vector_db
        )
